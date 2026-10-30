-- qa_probe: read-only. (1) shelf profiles, (2) terrain materials near the red patch, (3) scan placed models for underwater / floating, (4) R04 slabs
local T = workspace.Terrain
local rp = RaycastParams.new(); rp.FilterType = Enum.RaycastFilterType.Include; rp.FilterDescendantsInstances = { T }; rp.IgnoreWater = true
local function ray(x, z)
  local r = workspace:Raycast(Vector3.new(x, 700, z), Vector3.new(0, -900, 0), rp)
  if r then return r.Position.Y, r.Material.Name end
  return nil, nil
end
local out = {}
local function P(s) out[#out + 1] = s end

-- 1. shelf profiles (surface height ignoring water) along four axes
local function profile(name, f, a, b, step)
  local s = {}
  for t = a, b, step do
    local x, z = f(t)
    local h = ray(x, z)
    s[#s + 1] = string.format('%d:%s', t, h and string.format('%.0f', h) or 'nil')
  end
  P('PROFILE ' .. name .. '  ' .. table.concat(s, ' '))
end
profile('south x300 z', function(t) return 300, t end, 1500, 3300, 100)
profile('west z-300 x', function(t) return t, -300 end, -3600, -2000, 100)
profile('east z900 x', function(t) return t, 900 end, 2400, 4000, 100)
profile('north x0 z', function(t) return 0, t end, -4300, -2800, 100)

-- 2. red patch near the castle back
local mats = {}
for z = -2600, -2300, 50 do
  local row = {}
  for x = -100, 300, 100 do
    local h, m = ray(x, z)
    row[#row + 1] = string.format('(%d,%d)%s@%s', x, z, m or '?', h and string.format('%.0f', h) or '?')
  end
  P('MAT ' .. table.concat(row, ' '))
end

-- 3. scan placed models
local pm = workspace:FindFirstChild('Phase1Map')
local function scan(folderName)
  local f = pm and pm:FindFirstChild(folderName)
  if not f then P('SCAN ' .. folderName .. ' missing'); return end
  local n, uw, fl, ex = 0, 0, 0, {}
  local cnt = 0
  for _, m in ipairs(f:GetDescendants()) do
    if m:IsA('Model') and m:GetAttribute('PlanKey') then
      n += 1
      local cf, size = m:GetBoundingBox()
      local px, pz = cf.Position.X, cf.Position.Z
      local g = ray(px, pz)
      local bottom = cf.Position.Y - size.Y / 2
      if g == nil then
        fl += 1
        if #ex < 12 then ex[#ex + 1] = string.format('NOGROUND %s (%.0f,%.0f,%.0f)', m.Name, px, bottom, pz) end
      elseif g < 0.6 then
        uw += 1
        if #ex < 12 then ex[#ex + 1] = string.format('UW %s (%.0f,%.0f,%.0f) g=%.1f', m.Name, px, bottom, pz, g) end
      elseif bottom - g > 3.5 then
        fl += 1
        if #ex < 12 then ex[#ex + 1] = string.format('FLOAT %s (%.0f,%.0f,%.0f) gap=%.1f', m.Name, px, bottom, pz, bottom - g) end
      end
      cnt += 1
      if cnt % 300 == 0 then task.wait() end
    end
  end
  P(string.format('SCAN %s models=%d underwater=%d floating/noground=%d', folderName, n, uw, fl))
  for _, e in ipairs(ex) do P('   ' .. e) end
end
for _, fn in ipairs({ 'v4_pieces', 'v4_shore', 'v4_rocks', 'v4_elf' }) do scan(fn) end

-- 4. R04 slabs
local r04 = {}
if pm then
  for _, d in ipairs(pm:GetDescendants()) do
    if d:IsA('Model') and d:GetAttribute('PlanKey') and string.sub(d.Name, 1, 4) == 'R04_' then
      local cf = d:GetPivot()
      r04[#r04 + 1] = string.format('%s/%s (%.0f,%.0f,%.0f)', d.Parent.Parent.Name, d.Name, cf.X, cf.Y, cf.Z)
    end
  end
end
P('R04 models: ' .. #r04)
for i = 1, math.min(#r04, 20) do P('   ' .. r04[i]) end
return table.concat(out, '\n')
