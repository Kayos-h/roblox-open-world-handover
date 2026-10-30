-- desert_patches: breaks up the flat tan floor around the rusty town with Sandstone / Salt / Rock patches and dune-like Limestone streaks (material only).
local T = workspace.Terrain
local rp = RaycastParams.new(); rp.FilterType = Enum.RaycastFilterType.Include; rp.FilterDescendantsInstances = { T }; rp.IgnoreWater = true
local rng = Random.new(2024)
local n, miss = 0, 0
local choices = { Enum.Material.Sandstone, Enum.Material.Sandstone, Enum.Material.Salt, Enum.Material.Rock, Enum.Material.Limestone, Enum.Material.Mud }
for i = 1, 140 do
  local x = 1000 + rng:NextNumber() * 540
  local z = 880 + rng:NextNumber() * 460
  local r = workspace:Raycast(Vector3.new(x, 900, z), Vector3.new(0, -1300, 0), rp)
  if r and r.Material == Enum.Material.Ground and r.Position.Y > 4 then
    local sx, sz = 14 + rng:NextNumber() * 60, 10 + rng:NextNumber() * 30
    if rng:NextNumber() < 0.4 then sx, sz = sz, sx end
    local sy = r.Position.Y
    local mat = choices[rng:NextInteger(1, #choices)]
    local ok = pcall(function() T:ReplaceMaterial(Region3.new(Vector3.new(x - sx / 2, sy - 4, z - sz / 2), Vector3.new(x + sx / 2, sy + 2, z + sz / 2)):ExpandToGrid(4), 4, Enum.Material.Ground, mat) end)
    if ok then n += 1 else miss += 1 end
  else miss += 1 end
end
return string.format('desert patches painted %d (skipped %d)', n, miss)
