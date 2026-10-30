-- one-cell experiment 2: Air first, then Water, on the orphan cell (3000,-8,-1700)
local T = workspace.Terrain
local function look(tag)
  local m, o = T:ReadVoxels(Region3.new(Vector3.new(3000, -16, -1700), Vector3.new(3004, 4, -1696)), 4)
  local s = {}
  for j = 1, #m[1] do s[#s + 1] = string.format('%d:%s/%.2f', -16 + (j - 1) * 4, string.sub(m[1][j][1].Name, 1, 4), o[1][j][1]) end
  return tag .. ' ' .. table.concat(s, ' ')
end
local out = { look('before') }
local reg = Region3.new(Vector3.new(3000, -8, -1700), Vector3.new(3004, -4, -1696)):ExpandToGrid(4)
T:WriteVoxels(reg, 4, { { { Enum.Material.Air } } }, { { { 0 } } })
out[#out + 1] = look('after Air write')
T:WriteVoxels(reg, 4, { { { Enum.Material.Water } } }, { { { 1 } } })
out[#out + 1] = look('after Water write')
return table.concat(out, '\n')
