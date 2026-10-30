-- hover_scan_all: read-only. For every placed model larger than 8 studs in any Phase1Map folder (except foam, farsea, elf trees/bridges): gap between model bottom and the lowest of 5 footprint ground samples.
local T = workspace.Terrain
local rp = RaycastParams.new(); rp.FilterType = Enum.RaycastFilterType.Include; rp.FilterDescendantsInstances = { T }; rp.IgnoreWater = true
local function ground(x, z) local r = workspace:Raycast(Vector3.new(x, 900, z), Vector3.new(0, -1300, 0), rp); return r and r.Position.Y or nil end
local skip = { v4_foam = true, v4_farsea = true, Enterable = true, v3_interiors = true }
local res, checked = {}, 0
local pm = workspace.Phase1Map
for _, f in ipairs(pm:GetChildren()) do
  if f:IsA('Folder') and not skip[f.Name] then
    for _, m in ipairs(f:GetDescendants()) do
      if m:IsA('Model') and (m:GetAttribute('PlanKey') or m.Parent == f or m.Parent.Parent == f) and not m:FindFirstAncestorOfClass('Model') then
        local ok, cf, size = pcall(function() return m:GetBoundingBox() end)
        if ok and math.max(size.X, size.Z) >= 8 then
          checked += 1
          local hx, hz = size.X * 0.35, size.Z * 0.35
          local lo = 1e9
          for _, o in ipairs({ { 0, 0 }, { hx, 0 }, { -hx, 0 }, { 0, hz }, { 0, -hz } }) do
            local g = ground(cf.X + o[1], cf.Z + o[2])
            if g and g < lo then lo = g end
          end
          local bottom = cf.Position.Y - size.Y / 2
          if lo < 1e8 then
            local gap = bottom - lo
            if gap > 4 and not string.find(m.Name, 'bridge', 1, true) and not string.find(m.Name, 'canopy', 1, true) and not string.find(m.Name, 'treehouse', 1, true) and not string.find(m.Name, 'pier', 1, true) and not string.find(m.Name, 'dock', 1, true) then
              res[#res + 1] = { gap = gap, s = string.format('%s/%s (%.0f,%.0f,%.0f) size %.0fx%.0fx%.0f gap %.1f', f.Name, m.Name, cf.X, cf.Y, cf.Z, size.X, size.Y, size.Z, gap) }
            end
          end
          if checked % 250 == 0 then task.wait() end
        end
      end
    end
  end
end
table.sort(res, function(a, b) return a.gap > b.gap end)
local out = { 'models checked ' .. checked .. ', suspects ' .. #res }
for i = 1, math.min(#res, 18) do out[#out + 1] = '   ' .. res[i].s end
return table.concat(out, '\n')

