-- floater_fine: read-only. Detached solid terrain: any column where solid terrain sits above an air/water gap of >= 8 studs, step 8, in given rects. y range -64..520
local D = game:GetService('HttpService'):JSONDecode([==[__DATA__]==])
local T = workspace.Terrain
local EMPTY = { [Enum.Material.Air] = true, [Enum.Material.Water] = true }
local out = {}
for ri, r in ipairs(D.rects) do
  local found, cols = {}, 0
  for x = r[1], r[2], 8 do
    for z = r[3], r[4], 8 do
      local ok, m = pcall(function() return T:ReadVoxels(Region3.new(Vector3.new(x, -64, z), Vector3.new(x + 4, 520, z + 4)), 4) end)
      if ok and m then
        local col = m[1]
        local runs, s = {}, nil
        for i = 1, #col do
          local solid = not EMPTY[col[i][1]]
          if solid and not s then s = i end
          if (not solid) and s then runs[#runs + 1] = { s, i - 1 }; s = nil end
        end
        if s then runs[#runs + 1] = { s, #col } end
        for k = 2, #runs do
          local gap = (runs[k][1] - runs[k - 1][2] - 1) * 4
          if gap >= 8 then found[#found + 1] = string.format('(%d,%d) floater y %d..%d gap %d', x, z, -64 + (runs[k][1] - 1) * 4, -64 + runs[k][2] * 4, gap) end
        end
      end
      cols += 1
      if cols % 300 == 0 then task.wait() end
    end
  end
  out[#out + 1] = string.format('rect %d [%d..%d, %d..%d] cols=%d floaters=%d', ri, r[1], r[2], r[3], r[4], cols, #found)
  for i = 1, math.min(#found, 5) do out[#out + 1] = '   ' .. found[i] end
end
return table.concat(out, '\n')
