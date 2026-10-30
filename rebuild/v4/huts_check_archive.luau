-- huts_check_and_archive: counts the V4 replacements, verifies each stands on the ground, then archives the part-built placeholders (PartBuilt) into ServerStorage.Phase1Archive_v4.
local f = workspace.Phase1Map:FindFirstChild('v4_huts')
local T = workspace.Terrain
local rp = RaycastParams.new(); rp.FilterType = Enum.RaycastFilterType.Include; rp.FilterDescendantsInstances = { T }; rp.IgnoreWater = true
local by, keys, dup, bad = {}, {}, 0, {}
for _, d in ipairs(f:GetDescendants()) do
  if d:IsA('Model') and d:GetAttribute('PlanKey') then
    local k = d:GetAttribute('PlanKey')
    if keys[k] then dup += 1 else keys[k] = true end
    by[d.Parent.Name] = (by[d.Parent.Name] or 0) + 1
    local cf, size = d:GetBoundingBox()
    local r = workspace:Raycast(Vector3.new(cf.Position.X, 900, cf.Position.Z), Vector3.new(0, -1300, 0), rp)
    local gap = r and (cf.Position.Y - size.Y / 2 - r.Position.Y) or 99
    if math.abs(gap) > 3 and #bad < 6 then bad[#bad + 1] = string.format('%s (%.0f,%.0f) gap=%.1f', d.Name, cf.Position.X, cf.Position.Z, gap) end
  end
end
local s = {}
for k, v in pairs(by) do s[#s + 1] = k .. '=' .. v end
local out = { 'v4_huts groups: ' .. table.concat(s, ' ') .. ' duplicates=' .. dup .. ' off-ground(>3)=' .. #bad }
for _, b in ipairs(bad) do out[#out + 1] = '   ' .. b end
local total = 0
for _, g in ipairs(by) do total += g end
local n = 0
for _, _ in pairs(by) do n += 1 end
if dup == 0 and (by.Huts or 0) >= 44 and (by.Igloos or 0) >= 15 and (by.IceShanties or 0) >= 12 then
  local SS = game:GetService('ServerStorage')
  local arch = SS:FindFirstChild('Phase1Archive_v4') or Instance.new('Folder')
  arch.Name = 'Phase1Archive_v4'; arch.Parent = SS
  local pb = workspace.Phase1Map:FindFirstChild('PartBuilt')
  if pb then pb.Name = 'PartBuilt_v3_placeholders'; pb.Parent = arch; out[#out + 1] = 'PartBuilt archived (' .. #pb:GetDescendants() .. ' instances)' end
else
  out[#out + 1] = 'counts too low or duplicates: PartBuilt NOT archived'
end
return table.concat(out, '\n')
