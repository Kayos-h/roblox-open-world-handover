-- slice probe: read-only. (1) ASCII map of one horizontal layer, (2) sampled count of "orphan solid" voxels (solid cell with water or air on both sides vertically) in open ocean.
local T = workspace.Terrain
local out = {}
local function slice(x0, z0, w, d, y)
  local m, o = T:ReadVoxels(Region3.new(Vector3.new(x0, y, z0), Vector3.new(x0 + w, y + 4, z0 + d)), 4)
  local rows = {}
  for k = 1, #m[1][1] do
    local s = {}
    for i = 1, #m do
      local mat = m[i][1][k]
      local occ = o[i][1][k]
      local c = '.'
      if mat == Enum.Material.Air then c = ' ' elseif mat == Enum.Material.Water then c = '.' else c = string.sub(mat.Name, 1, 1) end
      s[#s + 1] = c
    end
    rows[#rows + 1] = table.concat(s)
  end
  return rows
end
out[#out + 1] = 'SLICE y=-8 x 2900..3100 z -1800..-1600 (rows = z, cols = x, 4 studs per char)'
for _, r in ipairs(slice(2900, -1800, 200, 200, -8)) do out[#out + 1] = r end

-- orphan voxels in open-ocean samples
local EMPTY = { [Enum.Material.Air] = true, [Enum.Material.Water] = true }
local function orphans(x0, x1, z0, z1, step)
  local n, cols, ylist = 0, 0, {}
  for x = x0, x1, step do
    for z = z0, z1, step do
      local ok, m = pcall(function() return T:ReadVoxels(Region3.new(Vector3.new(x, -64, z), Vector3.new(x + 4, 24, z + 4)), 4) end)
      if ok and m then
        cols += 1
        local col = m[1]
        for j = 2, #col - 1 do
          local c = col[j][1]
          if not EMPTY[c] and EMPTY[col[j - 1][1]] and EMPTY[col[j + 1][1]] then
            n += 1
            local y = -64 + (j - 1) * 4
            ylist[y] = (ylist[y] or 0) + 1
          end
        end
      end
    end
  end
  local ys = {}
  for y, c in pairs(ylist) do ys[#ys + 1] = y .. ':' .. c end
  table.sort(ys)
  return string.format('cols=%d orphans=%d  by y: %s', cols, n, table.concat(ys, ' '))
end
out[#out + 1] = 'ORPHANS east coast band  ' .. orphans(2850, 3150, -1500, -1100, 20)
out[#out + 1] = 'ORPHANS south sea         ' .. orphans(-400, 600, 2300, 2700, 24)
out[#out + 1] = 'ORPHANS far west sea      ' .. orphans(-3900, -3400, -800, -200, 24)
out[#out + 1] = 'ORPHANS north sea         ' .. orphans(-300, 300, -4000, -3500, 24)
out[#out + 1] = 'ORPHANS island interior   ' .. orphans(300, 700, 600, 1000, 24)
return table.concat(out, '\n')
