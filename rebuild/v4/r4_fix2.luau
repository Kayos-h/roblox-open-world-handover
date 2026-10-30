-- r4_fix2: (1) far sea colour = rendered near sea, slightly lighter far plane gradient, (2) shallow turquoise shelf paint, (3) foam rebuilt from main-coast chains only, (4) mesa variety, (5) rusty hut roof hues
local pm = workspace.Phase1Map
local T = workspace.Terrain
local HS = game:GetService('HttpService')
local out = {}
local function C(r, g, b) return Color3.fromRGB(r, g, b) end

-- 1. far sea: the near water renders around (3,57,134) at normal angles; use the same hue, with a faint lightening toward the outer ring so it blends into the haze
local n1 = 0
local fs = pm:FindFirstChild('v4_farsea')
if fs then
  for _, p in ipairs(fs:GetChildren()) do
    if p:IsA('BasePart') then
      local d = math.max(math.abs(p.Position.X), math.abs(p.Position.Z))
      local t = math.clamp((d - 5400) / 7600, 0, 1)
      p.Color = C(4, 58, 132):Lerp(C(70, 128, 176), t * 0.55)
      p.Material = Enum.Material.SmoothPlastic
      p.Reflectance = 0
      n1 += 1
    end
  end
end
out[#out + 1] = 'far sea slabs recoloured: ' .. n1

-- 2. shallow shelf paint: stronger turquoise: make the 4..12 stud deep band Concrete(teal) instead of Mud/Sand where depth is 6..14 studs (seabed ReplaceMaterial by depth is not possible; paint Sand->Concrete in the near-shore shelf ring)
-- Terrain colours: lighten the shelf steps
pcall(function() T:SetMaterialColor(Enum.Material.Sand, C(238, 224, 176)) end)
pcall(function() T:SetMaterialColor(Enum.Material.Concrete, C(96, 206, 200)) end)
pcall(function() T:SetMaterialColor(Enum.Material.Asphalt, C(38, 140, 190)) end)
out[#out + 1] = 'shelf colours lightened (Sand, Concrete teal, Asphalt blue)'
pcall(function() T.WaterTransparency = 0.82 end)
out[#out + 1] = 'water transparency 0.82'

-- 3. foam rebuilt from the main coast only
local segs = HS:JSONDecode([==[__DATA__]==]).segments
local rp = RaycastParams.new(); rp.FilterType = Enum.RaycastFilterType.Include; rp.FilterDescendantsInstances = { T }; rp.IgnoreWater = true
local function ground(x, z) local r = workspace:Raycast(Vector3.new(x, 600, z), Vector3.new(0, -900, 0), rp); return r and r.Position.Y or -60 end
local old = pm:FindFirstChild('v4_foam'); if old then old:Destroy() end
local folder = Instance.new('Folder'); folder.Name = 'v4_foam'; folder.Parent = pm
local rng = Random.new(31)
local made = 0
for idx, s in ipairs(segs) do
  local ax, az, bx, bz = s[1], s[2], s[3], s[4]
  local mx, mz = (ax + bx) / 2, (az + bz) / 2
  local dx, dz = bx - ax, bz - az
  local len = math.sqrt(dx * dx + dz * dz)
  if len > 0.5 then
    local ux, uz = dx / len, dz / len
    local nx, nz = -uz, ux
    if ground(mx + nx * 14, mz + nz * 14) > ground(mx - nx * 14, mz - nz * 14) then nx, nz = -nx, -nz end
    local lo, hi = -26, 26
    local gl, gh = ground(mx + nx * lo, mz + nz * lo), ground(mx + nx * hi, mz + nz * hi)
    if gl > -0.6 and gh < -0.6 then
      for _ = 1, 8 do
        local mid = (lo + hi) / 2
        if ground(mx + nx * mid, mz + nz * mid) > -0.6 then lo = mid else hi = mid end
      end
      local t = (lo + hi) / 2
      local cx, cz = mx + nx * (t + 3), mz + nz * (t + 3)
      local ang = math.atan2(-uz, ux)
      local p = Instance.new('Part'); p.Name = 'FoamA'; p.Anchored = true; p.CanCollide = false; p.CanTouch = false; p.CanQuery = false; p.CastShadow = false
      p.Material = Enum.Material.SmoothPlastic; p.Color = C(226, 242, 250); p.Transparency = 0.74 + rng:NextNumber() * 0.1
      p.Size = Vector3.new(len + 3.5, 0.1, 9 + rng:NextNumber() * 4)
      p.CFrame = CFrame.new(cx, 0.13, cz) * CFrame.Angles(0, ang, 0)
      p.Parent = folder
      made += 1
    end
  end
  if idx % 150 == 0 then task.wait() end
end
out[#out + 1] = 'foam rebuilt (main coast only): ' .. made

-- 4. mesa variety: stretch half of them in x or z (aspect 0.55..1.5), taller or lower
local nm = 0
local mesas = pm.v4_pieces2:FindFirstChild('Mesas')
if mesas then
  local k = 0
  for _, m in ipairs(mesas:GetChildren()) do
    k += 1
    if m:IsA('Model') and not m:GetAttribute('Stretched') then
      local sx, sy, sz
      local r = (k % 4)
      if r == 0 then sx, sy, sz = 1.45, 1.2, 0.7
      elseif r == 1 then sx, sy, sz = 0.65, 1.5, 0.65
      elseif r == 2 then sx, sy, sz = 1.2, 0.7, 1.7
      else sx, sy, sz = 0.85, 1.0, 1.3 end
      local piv = m:GetPivot()
      local ok = pcall(function()
        for _, p in ipairs(m:GetDescendants()) do
          if p:IsA('BasePart') then
            local rel = piv:PointToObjectSpace(p.Position)
            local newRel = Vector3.new(rel.X * sx, rel.Y * sy, rel.Z * sz)
            local cfRel = piv:ToObjectSpace(p.CFrame)
            p.Size = Vector3.new(p.Size.X * sx, p.Size.Y * sy, p.Size.Z * sz)
            p.CFrame = piv * CFrame.new(newRel) * (cfRel - cfRel.Position)
          end
        end
      end)
      if ok then m:SetAttribute('Stretched', true); nm += 1 end
    end
  end
end
out[#out + 1] = 'mesas stretched (parts scaled non-uniformly): ' .. nm

-- 5. rusty huts: 2 extra roof hues on a third of the huts (roof parts are the dark-metal or tile coloured ones)
local nh = 0
local huts = pm:FindFirstChild('v4_huts') and pm.v4_huts:FindFirstChild('Huts')
if huts then
  for i, m in ipairs(huts:GetChildren()) do
    if m:IsA('Model') and not m:GetAttribute('RoofHue') and i % 3 ~= 0 then
      local tint = (i % 3 == 1) and C(70, 128, 120) or C(150, 62, 44)
      for _, p in ipairs(m:GetChildren()) do
        if p:IsA('BasePart') and (p.Material == Enum.Material.CorrodedMetal or p.Material == Enum.Material.Metal or p.Material == Enum.Material.Slate) then
          p.Color = p.Color:Lerp(tint, 0.55)
        end
      end
      m:SetAttribute('RoofHue', true); nh += 1
    end
  end
end
out[#out + 1] = 'rusty huts roof hue varied: ' .. nh
return table.concat(out, '\n')
