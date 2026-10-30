-- elf_ground: dappled ground in the elf valley (terrain material paint only, idempotent in effect) + path edge wear
local T = workspace.Terrain
local rp = RaycastParams.new(); rp.FilterType = Enum.RaycastFilterType.Include; rp.FilterDescendantsInstances = { T }; rp.IgnoreWater = true
local rng = Random.new(1313)
local function repl(x0, x1, z0, z1, y0, y1, from, to)
  return pcall(function() T:ReplaceMaterial(Region3.new(Vector3.new(x0, y0, z0), Vector3.new(x1, y1, z1)):ExpandToGrid(4), 4, from, to) end)
end
local n1, n2 = 0, 0
-- dapple: 120 irregular patches of LeafyGrass (darker) and Grass (lighter) inside the valley floor (heights 10..20)
for i = 1, 120 do
  local x = -1900 + rng:NextNumber() * 700
  local z = -820 + rng:NextNumber() * 700
  local r = workspace:Raycast(Vector3.new(x, 600, z), Vector3.new(0, -900, 0), rp)
  if r and r.Position.Y > 8 and r.Position.Y < 26 and (r.Material == Enum.Material.Grass or r.Material == Enum.Material.LeafyGrass) then
    local sx, sz = 18 + rng:NextNumber() * 46, 14 + rng:NextNumber() * 34
    local to = (rng:NextNumber() < 0.55) and Enum.Material.LeafyGrass or Enum.Material.Grass
    local from = (to == Enum.Material.LeafyGrass) and Enum.Material.Grass or Enum.Material.LeafyGrass
    if repl(r.Position.X - sx / 2, r.Position.X + sx / 2, r.Position.Z - sz / 2, r.Position.Z + sz / 2, r.Position.Y - 4, r.Position.Y + 2, from, to) then n1 += 1 end
  end
end
-- path edge wear: Mud patches near the ring road crossings (just a few, small)
for k = 1, 28 do
  local a = rng:NextNumber() * math.pi * 2
  local x, z = -1560 + math.cos(a) * 125, -430 + math.sin(a) * 115
  local r = workspace:Raycast(Vector3.new(x, 600, z), Vector3.new(0, -900, 0), rp)
  if r and r.Material == Enum.Material.Ground then
    if repl(x - 7, x + 7, z - 7, z + 7, r.Position.Y - 4, r.Position.Y + 2, Enum.Material.Ground, Enum.Material.Mud) then n2 += 1 end
  end
end
return string.format('dapple patches %d, path wear patches %d', n1, n2)
