-- qa_perch: read-only. Finds placed models whose footprint is largely over open water or far above the terrain under their edges (hovering look).
local T = workspace.Terrain
local rp = RaycastParams.new(); rp.FilterType = Enum.RaycastFilterType.Include; rp.FilterDescendantsInstances = { T }; rp.IgnoreWater = true
local function ground(x, z)
  local r = workspace:Raycast(Vector3.new(x, 700, z), Vector3.new(0, -900, 0), rp)
  return r and r.Position.Y or -80
end
local pm = workspace:FindFirstChild('Phase1Map')
local out = {}
local function P(s) out[#out + 1] = s end
local offenders = {}
local checked = 0
for _, folderName in ipairs({ 'v4_pieces', 'v4_rocks', 'v4_shore' }) do
  local f = pm:FindFirstChild(folderName)
  if f then
    for _, m in ipairs(f:GetDescendants()) do
      if m:IsA('Model') and m:GetAttribute('PlanKey') then
        local cf, size = m:GetBoundingBox()
        local bottom = cf.Position.Y - size.Y / 2
        local px, pz = cf.Position.X, cf.Position.Z
        local hx, hz = size.X * 0.4, size.Z * 0.4
        local pts = { { 0, 0 }, { hx, 0 }, { -hx, 0 }, { 0, hz }, { 0, -hz }, { hx * 0.8, hz * 0.8 }, { -hx * 0.8, hz * 0.8 }, { hx * 0.8, -hz * 0.8 }, { -hx * 0.8, -hz * 0.8 } }
        local over, maxgap, mingap = 0, -1e9, 1e9
        for _, o in ipairs(pts) do
          local g = ground(px + o[1], pz + o[2])
          local gap = bottom - g
          if g < -2 then over += 1 end
          if gap > maxgap then maxgap = gap end
          if gap < mingap then mingap = gap end
        end
        checked += 1
        if (maxgap > 8 and over >= 2) or (bottom > 3 and over >= 4) then
          offenders[#offenders + 1] = { name = m.Name, folder = folderName, x = px, y = bottom, z = pz, sx = size.X, sy = size.Y, sz = size.Z, over = over, maxgap = maxgap }
        end
        if checked % 400 == 0 then task.wait() end
      end
    end
  end
end
table.sort(offenders, function(a, b) return a.maxgap > b.maxgap end)
P(string.format('checked %d models, perched/hovering suspects %d', checked, #offenders))
for i = 1, math.min(#offenders, 40) do
  local o = offenders[i]
  P(string.format('%s/%s at (%.0f, bottom %.1f, %.0f) size %.0fx%.0fx%.0f overWater=%d/9 maxGap=%.1f', o.folder, o.name, o.x, o.y, o.z, o.sx, o.sy, o.sz, o.over, o.maxgap))
end
-- red-ish large parts near the castle back (x -100..300, z -2650..-2300)
local reds = {}
for _, d in ipairs(workspace:GetDescendants()) do
  if d:IsA('BasePart') and d.Parent ~= nil then
    local p = d.Position
    if p.X > -150 and p.X < 350 and p.Z > -2700 and p.Z < -2300 then
      local c = d.Color
      if c.R > 0.45 and c.R > c.G * 1.5 and c.R > c.B * 1.5 and (d.Size.X + d.Size.Z) > 12 then
        reds[#reds + 1] = string.format('%s/%s (%.0f,%.0f,%.0f) size %.0fx%.0fx%.0f rgb %.0f,%.0f,%.0f', d.Parent.Name, d.Name, p.X, p.Y, p.Z, d.Size.X, d.Size.Y, d.Size.Z, c.R * 255, c.G * 255, c.B * 255)
      end
    end
  end
end
P('red-ish large parts near castle back: ' .. #reds)
for i = 1, math.min(#reds, 12) do P('   ' .. reds[i]) end
return table.concat(out, '\n')
