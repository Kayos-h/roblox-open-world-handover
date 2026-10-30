-- slab_scan: read-only. All placed models within 160 studs of (1600,205,-1020) taller than 15 studs or wider than 25, with the ground gap under their footprint.
local pm = workspace.Phase1Map
local T = workspace.Terrain
local rp = RaycastParams.new(); rp.FilterType = Enum.RaycastFilterType.Include; rp.FilterDescendantsInstances = { T }; rp.IgnoreWater = true
local function ground(x, z) local r = workspace:Raycast(Vector3.new(x, 900, z), Vector3.new(0, -1300, 0), rp); return r and r.Position.Y or nil end
local out = {}
for _, m in ipairs(pm:GetDescendants()) do
  if m:IsA('Model') and (m:GetAttribute('PlanKey') or m.Parent.Parent == pm) and not m:FindFirstAncestorOfClass('Model') then
    local ok, cf, size = pcall(function() return m:GetBoundingBox() end)
    if ok and (Vector3.new(cf.X, 0, cf.Z) - Vector3.new(1600, 0, -1020)).Magnitude < 160 and (size.Y > 15 or math.max(size.X, size.Z) > 25) then
      local lo, hi = 1e9, -1e9
      for _, o in ipairs({ { 0, 0 }, { 0.4, 0 }, { -0.4, 0 }, { 0, 0.4 }, { 0, -0.4 } }) do
        local g = ground(cf.X + o[1] * size.X, cf.Z + o[2] * size.Z)
        if g then if g < lo then lo = g end; if g > hi then hi = g end end
      end
      local bottom = cf.Position.Y - size.Y / 2
      out[#out + 1] = string.format('%s/%s at (%.0f,%.0f,%.0f) size %.0fx%.0fx%.0f bottom %.0f ground %.0f..%.0f gap-to-low %.1f', m.Parent.Name, m.Name, cf.X, cf.Y, cf.Z, size.X, size.Y, size.Z, bottom, lo, hi, bottom - lo)
    end
  end
end
table.sort(out)
return #out .. ' models\n' .. table.concat(out, '\n')
