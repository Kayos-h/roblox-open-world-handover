-- remove underwater items from town1_dress
local f = workspace.Phase1Map.town1_dress
local T = workspace.Terrain
local rp = RaycastParams.new(); rp.FilterType = Enum.RaycastFilterType.Include; rp.FilterDescendantsInstances = { T }; rp.IgnoreWater = true
local n = 0
for _, m in ipairs(f:GetDescendants()) do
  if m:IsA('Model') and m:GetAttribute('PlanKey') then
    local cf = m:GetBoundingBox()
    local r = workspace:Raycast(Vector3.new(cf.Position.X, 900, cf.Position.Z), Vector3.new(0, -1300, 0), rp)
    if r and r.Position.Y < -0.5 then m:Destroy(); n += 1 end
  end
end
return 'removed underwater: ' .. n
