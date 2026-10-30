-- wf_probe: read-only. Parts of the elf waterfall with positions in world space and relative to the model's bounding box.
local pm = workspace.Phase1Map
local out = {}
local target
for _, m in ipairs(pm.v4_elf:GetDescendants()) do
  if m:IsA('Model') and m.Name == 'R05_01_waterfall_cliff_large_01' then target = m end
end
if not target then return 'waterfall model not found' end
local cf, size = target:GetBoundingBox()
out[#out + 1] = string.format('model bbox centre (%.1f,%.1f,%.1f) size %.1fx%.1fx%.1f  scale %.2f  look=(%.2f,%.2f,%.2f) parent=%s', cf.X, cf.Y, cf.Z, size.X, size.Y, size.Z, target:GetScale(), cf.LookVector.X, cf.LookVector.Y, cf.LookVector.Z, target.Parent and target.Parent.Name or '?')
local T = workspace.Terrain
local rp = RaycastParams.new(); rp.FilterType = Enum.RaycastFilterType.Include; rp.FilterDescendantsInstances = { T }; rp.IgnoreWater = true
for _, p in ipairs(target:GetChildren()) do
  if p:IsA('BasePart') then
    local rel = cf:PointToObjectSpace(p.Position)
    out[#out + 1] = string.format('  %-18s %-12s pos(%.0f,%.0f,%.0f) rel(%.0f,%.0f,%.0f) size %.0fx%.0fx%.0f tr=%.2f', p.Name, p.Material.Name, p.Position.X, p.Position.Y, p.Position.Z, rel.X, rel.Y, rel.Z, p.Size.X, p.Size.Y, p.Size.Z, p.Transparency)
  end
end
-- terrain heights in front of the model (south, +z) and at the model
for _, dz in ipairs({ -40, -25, -10, 0, 10, 25, 40, 60, 90 }) do
  local r = workspace:Raycast(Vector3.new(cf.X, 500, cf.Z + dz), Vector3.new(0, -800, 0), rp)
  out[#out + 1] = string.format('  terrain at z=%.0f: %s', cf.Z + dz, r and string.format('%.1f %s', r.Position.Y, r.Material.Name) or 'none')
end
return table.concat(out, '\n')
