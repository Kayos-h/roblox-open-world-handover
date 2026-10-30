-- one-cell experiment on an orphan voxel at (3000,-8,-1700): can WriteVoxels replace it with Water?
local T = workspace.Terrain
local function look(tag)
  local m, o = T:ReadVoxels(Region3.new(Vector3.new(3000, -16, -1700), Vector3.new(3004, 4, -1696)), 4)
  local s = {}
  for j = 1, #m[1] do s[#s + 1] = string.format('%d:%s/%.2f', -16 + (j - 1) * 4, string.sub(m[1][j][1].Name, 1, 4), o[1][j][1]) end
  return tag .. ' ' .. table.concat(s, ' ')
end
local out = { look('before') }
-- write Water 1.0 into the y=-8 cell only
local reg = Region3.new(Vector3.new(3000, -8, -1700), Vector3.new(3004, -4, -1696)):ExpandToGrid(4)
T:WriteVoxels(reg, 4, { { { Enum.Material.Water } } }, { { { 1 } } })
out[#out + 1] = look('after 1-cell water write')
return table.concat(out, '\n')
