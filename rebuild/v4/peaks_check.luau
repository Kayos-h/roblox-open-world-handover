-- peaks_check: read-only. For each snow peak / mesa: model height, bottom, ground under centre, top elevation. Flags peaks whose top is lower than ground + 30.
local f = workspace.Phase1Map:FindFirstChild('v4_pieces2')
local T = workspace.Terrain
local rp = RaycastParams.new(); rp.FilterType = Enum.RaycastFilterType.Include; rp.FilterDescendantsInstances = { T }; rp.IgnoreWater = true
local out, low = {}, 0
for _, g in ipairs(f:GetChildren()) do
  for _, m in ipairs(g:GetChildren()) do
    local cf, size = m:GetBoundingBox()
    local r = workspace:Raycast(Vector3.new(cf.Position.X, 900, cf.Position.Z), Vector3.new(0, -1300, 0), rp)
    local gy = r and r.Position.Y or -99
    local top = cf.Position.Y + size.Y / 2
    local bottom = cf.Position.Y - size.Y / 2
    local protrude = top - gy
    if protrude < 25 then low += 1 end
    if #out < 12 then out[#out + 1] = string.format('%s/%s at (%.0f,%.0f) size %.0fx%.0fx%.0f ground=%.0f bottom=%.0f top=%.0f protrude=%.0f', g.Name, m.Name, cf.Position.X, cf.Position.Z, size.X, size.Y, size.Z, gy, bottom, top, protrude) end
  end
end
return 'pieces whose top is < 25 studs above the ground: ' .. low .. '\n' .. table.concat(out, '\n')
