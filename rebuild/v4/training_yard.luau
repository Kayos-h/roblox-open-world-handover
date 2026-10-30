-- training_yard: builds simple training equipment from parts inside the castle yard (x -141..-69, z -2222..-2172) on the ground. Replayable (rebuilds the model).
local T = workspace.Terrain
local rp = RaycastParams.new(); rp.FilterType = Enum.RaycastFilterType.Include; rp.FilterDescendantsInstances = { T }; rp.IgnoreWater = true
local function ground(x, z)
  local r = workspace:Raycast(Vector3.new(x, 400, z), Vector3.new(0, -600, 0), rp)
  return r and r.Position.Y or 92
end
local root = workspace.Phase1Map:FindFirstChild('v4_castle_yard')
if root then root:Destroy() end
root = Instance.new('Folder'); root.Name = 'v4_castle_yard'; root.Parent = workspace.Phase1Map
local function part(parent, name, size, cf, color, mat, shape)
  local p = Instance.new('Part'); p.Name = name; p.Anchored = true; p.CanTouch = false
  p.Size = size; p.CFrame = cf; p.Color = color; p.Material = mat
  if shape then p.Shape = shape end
  p.Parent = parent
  return p
end
local wood, darkWood = Color3.fromRGB(128, 92, 58), Color3.fromRGB(86, 60, 38)
local straw, cloth, iron = Color3.fromRGB(196, 168, 96), Color3.fromRGB(150, 36, 40), Color3.fromRGB(88, 90, 96)
local function dummy(x, z, yaw)
  local m = Instance.new('Model'); m.Name = 'TrainingDummy'; m.Parent = root
  local g = ground(x, z)
  local cf = CFrame.new(x, g, z) * CFrame.Angles(0, math.rad(yaw), 0)
  part(m, 'Base', Vector3.new(3.6, 0.6, 3.6), cf * CFrame.new(0, 0.3, 0), darkWood, Enum.Material.Wood)
  part(m, 'Post', Vector3.new(0.9, 6.2, 0.9), cf * CFrame.new(0, 3.7, 0), wood, Enum.Material.Wood)
  part(m, 'Arm', Vector3.new(4.6, 0.7, 0.7), cf * CFrame.new(0, 5.4, 0), wood, Enum.Material.Wood)
  part(m, 'Body', Vector3.new(2.4, 2.8, 1.6), cf * CFrame.new(0, 4.4, 0.1), straw, Enum.Material.Fabric)
  part(m, 'Head', Vector3.new(1.6, 1.6, 1.6), cf * CFrame.new(0, 6.6, 0.1), straw, Enum.Material.Fabric, Enum.PartType.Ball)
  part(m, 'Sash', Vector3.new(2.5, 0.5, 1.7), cf * CFrame.new(0, 4.0, 0.1), cloth, Enum.Material.Fabric)
  return m
end
local function target(x, z, yaw)
  local m = Instance.new('Model'); m.Name = 'ArcheryTarget'; m.Parent = root
  local g = ground(x, z)
  local cf = CFrame.new(x, g, z) * CFrame.Angles(0, math.rad(yaw), 0)
  part(m, 'LegA', Vector3.new(0.6, 5.2, 0.6), cf * CFrame.new(-1.6, 2.5, 0.9) * CFrame.Angles(math.rad(10), 0, 0), darkWood, Enum.Material.Wood)
  part(m, 'LegB', Vector3.new(0.6, 5.2, 0.6), cf * CFrame.new(1.6, 2.5, 0.9) * CFrame.Angles(math.rad(10), 0, 0), darkWood, Enum.Material.Wood)
  local face = cf * CFrame.new(0, 4.4, -0.2) * CFrame.Angles(0, 0, math.rad(90))
  part(m, 'Disc', Vector3.new(0.7, 5.6, 5.6), face, straw, Enum.Material.Fabric, Enum.PartType.Cylinder)
  part(m, 'RingR', Vector3.new(0.75, 3.8, 3.8), face * CFrame.new(0.02, 0, 0), cloth, Enum.Material.Fabric, Enum.PartType.Cylinder)
  part(m, 'RingW', Vector3.new(0.8, 2.2, 2.2), face * CFrame.new(0.04, 0, 0), Color3.fromRGB(236, 232, 220), Enum.Material.Fabric, Enum.PartType.Cylinder)
  part(m, 'Gold', Vector3.new(0.85, 0.9, 0.9), face * CFrame.new(0.06, 0, 0), Color3.fromRGB(214, 172, 72), Enum.Material.Metal, Enum.PartType.Cylinder)
  return m
end
local function rack(x, z, yaw)
  local m = Instance.new('Model'); m.Name = 'WeaponRack'; m.Parent = root
  local g = ground(x, z)
  local cf = CFrame.new(x, g, z) * CFrame.Angles(0, math.rad(yaw), 0)
  part(m, 'PostA', Vector3.new(0.8, 5.0, 0.8), cf * CFrame.new(-3.2, 2.5, 0), darkWood, Enum.Material.Wood)
  part(m, 'PostB', Vector3.new(0.8, 5.0, 0.8), cf * CFrame.new(3.2, 2.5, 0), darkWood, Enum.Material.Wood)
  part(m, 'BarLow', Vector3.new(7.2, 0.6, 0.7), cf * CFrame.new(0, 1.6, 0), wood, Enum.Material.Wood)
  part(m, 'BarHigh', Vector3.new(7.2, 0.6, 0.7), cf * CFrame.new(0, 3.6, 0), wood, Enum.Material.Wood)
  for i = -2, 2 do
    local len = 5.6 - math.abs(i) * 0.4
    part(m, 'Blade' .. i, Vector3.new(0.35, len, 0.2), cf * CFrame.new(i * 1.2, 3.4, -0.1) * CFrame.Angles(0, 0, math.rad(i * 4)), iron, Enum.Material.Metal)
    part(m, 'Hilt' .. i, Vector3.new(0.35, 0.9, 0.5), cf * CFrame.new(i * 1.2, 0.9 + len * 0.1, -0.1), darkWood, Enum.Material.Wood)
  end
  return m
end
-- yard layout: 4 dummies in two rows, 3 archery targets along the north fence, 2 weapon racks at the west fence
for i = 0, 3 do dummy(-124 + (i % 2) * 18, -2198 + math.floor(i / 2) * 14, 90 + (i % 2) * 20) end
for i = 0, 2 do target(-130 + i * 24, -2217, 0) end
rack(-136, -2186, 90); rack(-136, -2208, 90)
return 'training yard built: ' .. #root:GetChildren() .. ' props'
