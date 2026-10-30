-- column dump: read-only. Prints material + occupancy per 4-stud voxel from y=-64 to 12 at a few columns.
local T = workspace.Terrain
local cols = { { 3000, -1700 }, { 3012, -1652 }, { 2832, 1564 }, { 2868, 1480 }, { 2400, 900 } }
local out = {}
for _, c in ipairs(cols) do
  local m, o = T:ReadVoxels(Region3.new(Vector3.new(c[1], -64, c[2]), Vector3.new(c[1] + 4, 16, c[2] + 4)), 4)
  local s = {}
  for j = 1, #m[1] do
    local y = -64 + (j - 1) * 4
    s[#s + 1] = string.format('%d:%s/%.2f', y, string.sub(m[1][j][1].Name, 1, 5), o[1][j][1])
  end
  out[#out + 1] = string.format('(%d,%d) %s', c[1], c[2], table.concat(s, ' '))
end
return table.concat(out, '\n')
