-- roundtrip test on ONE chunk: (1) count orphans, (2) ReadVoxels+WriteVoxels the same region unchanged, (3) count orphans again. Region: x 2944..3072, z -1792..-1664 (a chunk that has orphans).
local T = workspace.Terrain
local EMPTY = { [Enum.Material.Air] = true, [Enum.Material.Water] = true }
local function count(x0, z0)
  local m = T:ReadVoxels(Region3.new(Vector3.new(x0, -64, z0), Vector3.new(x0 + 128, 24, z0 + 128)), 4)
  local n = 0
  for i = 1, #m do
    for k = 1, #m[1][1] do
      for j = 2, #m[1] - 1 do
        if not EMPTY[m[i][j][k]] and EMPTY[m[i][j - 1][k]] and EMPTY[m[i][j + 1][k]] then n += 1 end
      end
    end
  end
  return n
end
local x0, z0 = 2944, -1792
local before = count(x0, z0)
local reg = Region3.new(Vector3.new(x0, -64, z0), Vector3.new(x0 + 128, 24, z0 + 128)):ExpandToGrid(4)
local m, o = T:ReadVoxels(reg, 4)
-- list distinct occupancy values of non-solid water cells to see fractional water
local fracWater, fracSolid = 0, 0
for i = 1, #m do for j = 1, #m[1] do for k = 1, #m[1][1] do
  local oc = o[i][j][k]
  if m[i][j][k] == Enum.Material.Water and oc < 0.99 then fracWater += 1 end
  if (not EMPTY[m[i][j][k]]) and oc < 0.99 and oc > 0 then fracSolid += 1 end
end end end
T:WriteVoxels(reg, 4, m, o)
local after = count(x0, z0)
return string.format('orphans before=%d after roundtrip=%d  (fractional water cells %d, fractional solid cells %d)', before, after, fracWater, fracSolid)
