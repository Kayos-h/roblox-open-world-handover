local f = workspace.Phase1Map.town1.Church
local ch = f:FindFirstChild('D01_church')
if not ch then return 'no church' end
if not ch:GetAttribute('V3Done') then
  local cf0, sz0 = ch:GetBoundingBox()
  ch:PivotTo(CFrame.new(cf0.Position) * CFrame.Angles(0, math.pi, 0) * (CFrame.new(cf0.Position):Inverse() * ch:GetPivot()))
  ch:ScaleTo(ch:GetScale() * 1.3)
  local cf1, sz1 = ch:GetBoundingBox()
  local bottom1 = cf1.Y - sz1.Y / 2
  local target = Vector3.new(-140, 2.0 - 0.3, 245)
  ch:PivotTo(ch:GetPivot() + Vector3.new(target.X - cf1.X, target.Y - bottom1, target.Z - cf1.Z))
  ch:SetAttribute('V3Done', true)
end
local st = f:FindFirstChild('A08_stairs_3')
if st then st:Destroy() end
-- terrain: church square paving in front (east), graveyard ground behind (west)
local T = workspace.Terrain
local function rep(x0, x1, z0, z1, from, to)
  local reg = Region3.new(Vector3.new(x0, -12, z0), Vector3.new(x1, 24, z1)):ExpandToGrid(4)
  for _, m in ipairs(from) do T:ReplaceMaterial(reg, 4, m, to) end
end
rep(-296, -184, 200, 292, { Enum.Material.Pavement, Enum.Material.Cobblestone, Enum.Material.Ground, Enum.Material.Mud }, Enum.Material.LeafyGrass)
rep(-100, -30, 222, 270, { Enum.Material.Grass, Enum.Material.LeafyGrass, Enum.Material.Ground }, Enum.Material.Cobblestone)
local sp = workspace:FindFirstChildWhichIsA('SpawnLocation', true)
if sp then sp.CFrame = CFrame.new(-66, sp.Position.Y, 245) end
local cf, sz = ch:GetBoundingBox()
return string.format('church at (%.0f,%.0f,%.0f) size (%.0f,%.0f,%.0f); spawn %s', cf.X, cf.Y, cf.Z, sz.X, sz.Y, sz.Z, tostring(sp and sp.Position))
