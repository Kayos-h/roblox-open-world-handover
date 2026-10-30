local HS = game:GetService('HttpService')
local D = HS:JSONDecode([==[__DATA__]==])
local root = workspace.Phase1Map
local F0 = root:FindFirstChild('PartBuilt') or Instance.new('Folder'); F0.Name = 'PartBuilt'; F0.Parent = root
local function folder(name) local f = F0:FindFirstChild(name); if f then f:Destroy() end; f = Instance.new('Folder'); f.Name = name; f.Parent = F0; return f end
local rng = Random.new(D.seed or 7)
local n = 0
local function P(parent, cls, size, cf, color, mat, opt)
  local p = Instance.new(cls)
  p.Anchored = true; p.Size = size; p.CFrame = cf; p.Color = color; p.Material = mat
  p.TopSurface = Enum.SurfaceType.Smooth; p.BottomSurface = Enum.SurfaceType.Smooth; p.CanTouch = false
  if opt then if opt.t then p.Transparency = opt.t end if opt.nc then p.CanCollide = false end if opt.shape then p.Shape = opt.shape end if opt.ns then p.CastShadow = false end end
  p.Parent = parent; n += 1; return p
end
local rgb = Color3.fromRGB
local function jitter(c, a) local k = 1 + rng:NextNumber(-a, a) return Color3.new(math.clamp(c.R * k, 0, 1), math.clamp(c.G * k, 0, 1), math.clamp(c.B * k, 0, 1)) end

-------------------------------------------------- rusty huts
local function hut(f, it, idx)
  local m = Instance.new('Model'); m.Name = 'Hut_' .. idx; m.Parent = f
  local B = CFrame.new(it.x, it.y, it.z) * CFrame.Angles(0, math.rad(it.rot), 0)
  local w, d = it.w, it.d
  local h = 8 + rng:NextNumber(0, 2)
  local woodC = jitter(rgb(118, 92, 66), 0.12)
  local wallMat = Enum.Material.WoodPlanks
  if it.v == 2 then woodC = jitter(rgb(170, 138, 100), 0.08); wallMat = Enum.Material.Sandstone end
  local roofC = jitter(rgb(136, 70, 40), 0.15)
  local T = 0.8
  P(m, 'Part', Vector3.new(w + 1, 1.4, d + 1), B * CFrame.new(0, -0.3, 0), rgb(110, 96, 80), Enum.Material.Cobblestone)
  -- back + sides
  P(m, 'Part', Vector3.new(w, h, T), B * CFrame.new(0, h / 2 + 0.4, -d / 2), woodC, wallMat)
  for s = -1, 1, 2 do
    P(m, 'Part', Vector3.new(T, h, d), B * CFrame.new(s * w / 2, h / 2 + 0.4, 0), woodC, wallMat)
  end
  -- front with door and window
  local dw = 3.6
  P(m, 'Part', Vector3.new((w - dw) / 2, h, T), B * CFrame.new(-(w + dw) / 4, h / 2 + 0.4, d / 2), woodC, wallMat)
  P(m, 'Part', Vector3.new((w - dw) / 2, h, T), B * CFrame.new((w + dw) / 4, h / 2 + 0.4, d / 2), woodC, wallMat)
  P(m, 'Part', Vector3.new(dw, h - 7, T), B * CFrame.new(0, 7 + (h - 7) / 2 + 0.4, d / 2), woodC, wallMat)
  P(m, 'Part', Vector3.new(dw - 0.4, 6.8, 0.2), B * CFrame.new(0, 3.8, d / 2 - 0.3), rgb(28, 22, 18), Enum.Material.Slate, { nc = true })
  -- window with boards
  -- v3 detail pass: skirting, corner posts, door frame, step, front windows, shutters
  do
    local trim = jitter(rgb(72, 54, 38), 0.1)
    P(m, 'Part', Vector3.new(w + 0.5, 1.1, d + 0.5), B * CFrame.new(0, 0.95, 0), trim, Enum.Material.WoodPlanks)
    for sx = -1, 1, 2 do for sz = -1, 1, 2 do
      P(m, 'Part', Vector3.new(0.9, h + 0.4, 0.9), B * CFrame.new(sx * (w / 2), h / 2 + 0.4, sz * (d / 2)), trim, Enum.Material.Wood)
    end end
    P(m, 'Part', Vector3.new(0.55, 7.4, 1.0), B * CFrame.new(-(dw / 2 + 0.3), 3.9, d / 2 + 0.1), trim, Enum.Material.Wood)
    P(m, 'Part', Vector3.new(0.55, 7.4, 1.0), B * CFrame.new((dw / 2 + 0.3), 3.9, d / 2 + 0.1), trim, Enum.Material.Wood)
    P(m, 'Part', Vector3.new(dw + 1.4, 0.7, 1.0), B * CFrame.new(0, 7.6, d / 2 + 0.1), trim, Enum.Material.Wood)
    P(m, 'Part', Vector3.new(dw + 2.2, 0.7, 2.0), B * CFrame.new(0, 0.2, d / 2 + 1.4), rgb(120, 108, 92), Enum.Material.Cobblestone)
    if w >= 9 then
      for sx = -1, 1, 2 do
        local wx = sx * (w / 2 - 2.0)
        P(m, 'Part', Vector3.new(2.4, 2.4, 0.3), B * CFrame.new(wx, 5.2, d / 2 + 0.15), rgb(26, 30, 36), Enum.Material.Glass, { nc = true })
        P(m, 'Part', Vector3.new(3.0, 0.4, 0.5), B * CFrame.new(wx, 6.55, d / 2 + 0.25), trim, Enum.Material.Wood)
        P(m, 'Part', Vector3.new(3.0, 0.4, 0.5), B * CFrame.new(wx, 3.85, d / 2 + 0.25), trim, Enum.Material.Wood)
        P(m, 'Part', Vector3.new(1.0, 2.9, 0.3), B * CFrame.new(wx - sx * 1.6, 5.2, d / 2 + 0.3), jitter(rgb(88, 70, 52), 0.2), Enum.Material.WoodPlanks)
        P(m, 'Part', Vector3.new(1.0, 2.9, 0.3), B * CFrame.new(wx + sx * 1.6, 5.2, d / 2 + 0.3), jitter(rgb(88, 70, 52), 0.2), Enum.Material.WoodPlanks)
      end
    end
  end
  -- window with boards
  P(m, 'Part', Vector3.new(0.2, 2.2, 2.6), B * CFrame.new(w / 2 + 0.45, 5.5, 0), rgb(30, 26, 22), Enum.Material.Slate)
  for k = 0, 1 do P(m, 'Part', Vector3.new(0.3, 0.5, 3.2), B * CFrame.new(w / 2 + 0.6, 5 + k, 0) * CFrame.Angles(math.rad(rng:NextNumber(-15, 15)), 0, 0), rgb(96, 72, 50), Enum.Material.WoodPlanks) end
  -- roof
  if it.v == 1 then
    local ang = math.rad(12)
    P(m, 'Part', Vector3.new(w + 2.4, 0.4, d / math.cos(ang) + 2), B * CFrame.new(0, h + 0.4 + math.tan(ang) * 0 + 0.6, 0) * CFrame.Angles(ang, 0, 0), roofC, Enum.Material.CorrodedMetal)
  elseif it.v == 2 then
    local rise = 3.2
    local half = w / 2 + 1
    local sl = math.sqrt(half * half + rise * rise)
    local ang = math.atan2(rise, half)
    for s = -1, 1, 2 do
      P(m, 'Part', Vector3.new(sl, 0.35, d + 1.6), B * CFrame.new(s * half / 2, h + 0.4 + rise / 2, 0) * CFrame.Angles(0, 0, -s * ang), roofC, Enum.Material.CorrodedMetal)
    end
    for s = -1, 1, 2 do
      P(m, 'WedgePart', Vector3.new(T, rise, w / 2), B * CFrame.new(s * w / 4, h + 0.4 + rise / 2, d / 2 * (1)) * CFrame.Angles(0, math.rad(-90 * s), 0), woodC, wallMat)
      P(m, 'WedgePart', Vector3.new(T, rise, w / 2), B * CFrame.new(s * w / 4, h + 0.4 + rise / 2, -d / 2) * CFrame.Angles(0, math.rad(-90 * s), 0), woodC, wallMat)
    end
  else
    P(m, 'Part', Vector3.new(w + 2, 0.4, d + 2), B * CFrame.new(0, h + 0.6, 0) * CFrame.Angles(0, 0, math.rad(4)), roofC, Enum.Material.CorrodedMetal)
    for k = 1, 3 do P(m, 'Part', Vector3.new(1.4, 1, 1.2), B * CFrame.new(rng:NextNumber(-w / 3, w / 3), h + 1.3, rng:NextNumber(-d / 3, d / 3)), rgb(110, 105, 100), Enum.Material.Slate) end
  end
  -- awning + stovepipe
  if rng:NextNumber() < 0.6 then
    P(m, 'Part', Vector3.new(dw + 3, 0.25, 3), B * CFrame.new(0, 7.6, d / 2 + 1.4) * CFrame.Angles(math.rad(-14), 0, 0), jitter(rgb(150, 120, 80), 0.2), Enum.Material.Fabric)
  end
  if rng:NextNumber() < 0.55 then
    local pipe = P(m, 'Part', Vector3.new(5, 0.9, 0.9), B * CFrame.new(-w / 4, h + 2.5, -d / 4) * CFrame.Angles(0, 0, math.rad(90)), rgb(70, 64, 60), Enum.Material.CorrodedMetal, { shape = Enum.PartType.Cylinder })
    if rng:NextNumber() < 0.5 then local s = Instance.new('Smoke'); s.Size = 1.2; s.Opacity = 0.08; s.RiseVelocity = 3; s.Color = rgb(120, 115, 110); s.Parent = pipe end
  end
  -- interior glow (some huts)
  if rng:NextNumber() < 0.5 then
    local a = P(m, 'Part', Vector3.new(0.3, 0.3, 0.3), B * CFrame.new(0, 4.5, 0), rgb(255, 160, 80), Enum.Material.Neon, { t = 1, nc = true, ns = true })
    local l = Instance.new('PointLight'); l.Color = rgb(255, 170, 90); l.Range = 12; l.Brightness = 1; l.Parent = a
  end
end

-------------------------------------------------- igloos
local function igloo(f, it, idx)
  local m = Instance.new('Model'); m.Name = 'Igloo_' .. idx; m.Parent = f
  local d = it.d
  local B = CFrame.new(it.x, it.y, it.z) * CFrame.Angles(0, math.rad(it.rot), 0)
  local snow = rgb(238, 246, 252)
  P(m, 'Part', Vector3.new(d, d, d), B * CFrame.new(0, -d * 0.12, 0), snow, Enum.Material.Snow, { shape = Enum.PartType.Ball })
  -- block seams: thin darker rings faked with flattened discs
  for k = 1, 3 do
    local yy = d * (0.08 + k * 0.1)
    local rr = math.sqrt(math.max(0, (d / 2) ^ 2 - (yy + d * 0.12) ^ 2)) * 2 + 0.2
    P(m, 'Part', Vector3.new(0.25, rr, rr), B * CFrame.new(0, yy, 0) * CFrame.Angles(0, 0, math.rad(90)), rgb(214, 228, 238), Enum.Material.Glacier, { shape = Enum.PartType.Cylinder, nc = true, ns = true })
  end
  local tl, td = d * 0.36, d * 0.46
  P(m, 'Part', Vector3.new(tl, td, td), B * CFrame.new(0, 0, d * 0.42) * CFrame.Angles(0, math.rad(90), 0), snow, Enum.Material.Snow, { shape = Enum.PartType.Cylinder })
  P(m, 'Part', Vector3.new(0.3, td * 0.62, td * 0.62), B * CFrame.new(0, td * 0.12, d * 0.42 + tl / 2 + 0.05) * CFrame.Angles(0, math.rad(90), 0), rgb(22, 28, 38), Enum.Material.Slate, { shape = Enum.PartType.Cylinder, nc = true })
  P(m, 'Part', Vector3.new(d * 1.3, 0.6, d * 1.3), B * CFrame.new(0, -0.2, 0.06 * d) * CFrame.Angles(0, 0, math.rad(90)), rgb(232, 240, 248), Enum.Material.Snow, { shape = Enum.PartType.Cylinder, nc = true })
  local a = P(m, 'Part', Vector3.new(0.3, 0.3, 0.3), B * CFrame.new(0, 1.2, d * 0.62), rgb(255, 170, 90), Enum.Material.Neon, { t = 1, nc = true, ns = true })
  local l = Instance.new('PointLight'); l.Color = rgb(255, 170, 100); l.Range = 10; l.Brightness = 1.4; l.Parent = a
  for k = 1, 4 do
    local ang = rng:NextNumber(0, math.pi * 2)
    P(m, 'Part', Vector3.new(2.6, 1.6, 2.2), B * CFrame.new(math.cos(ang) * d * 0.62, 0.4, math.sin(ang) * d * 0.62) * CFrame.Angles(0, ang, 0), snow, Enum.Material.Snow)
  end
end

-------------------------------------------------- ice fishing shanties + holes
local function shanty(f, it, idx)
  local m = Instance.new('Model'); m.Name = 'IceShanty_' .. idx; m.Parent = f
  local B = CFrame.new(it.x, it.y, it.z) * CFrame.Angles(0, math.rad(it.rot), 0)
  local cols = { rgb(150, 50, 45), rgb(60, 90, 140), rgb(70, 110, 70), rgb(160, 120, 60) }
  local c = cols[(idx % #cols) + 1]
  local w, d, h = 8, 9, 7
  P(m, 'Part', Vector3.new(w + 0.6, 0.6, d + 0.6), B * CFrame.new(0, 0.3, 0), rgb(110, 80, 55), Enum.Material.WoodPlanks)
  P(m, 'Part', Vector3.new(w, h, 0.5), B * CFrame.new(0, h / 2 + 0.6, -d / 2), c, Enum.Material.WoodPlanks)
  for s = -1, 1, 2 do P(m, 'Part', Vector3.new(0.5, h, d), B * CFrame.new(s * w / 2, h / 2 + 0.6, 0), c, Enum.Material.WoodPlanks) end
  P(m, 'Part', Vector3.new((w - 3) / 2, h, 0.5), B * CFrame.new(-(w + 3) / 4, h / 2 + 0.6, d / 2), c, Enum.Material.WoodPlanks)
  P(m, 'Part', Vector3.new((w - 3) / 2, h, 0.5), B * CFrame.new((w + 3) / 4, h / 2 + 0.6, d / 2), c, Enum.Material.WoodPlanks)
  P(m, 'Part', Vector3.new(3, 1.5, 0.5), B * CFrame.new(0, h - 0.15, d / 2), c, Enum.Material.WoodPlanks)
  local half, rise = w / 2 + 0.8, 2.6
  local sl, ang = math.sqrt(half * half + rise * rise), math.atan2(rise, half)
  for s = -1, 1, 2 do
    P(m, 'Part', Vector3.new(sl, 0.3, d + 1.2), B * CFrame.new(s * half / 2, h + 0.6 + rise / 2, 0) * CFrame.Angles(0, 0, -s * ang), rgb(235, 242, 248), Enum.Material.Snow)
    P(m, 'WedgePart', Vector3.new(0.5, rise, w / 2), B * CFrame.new(s * w / 4, h + 0.6 + rise / 2, d / 2) * CFrame.Angles(0, math.rad(-90 * s), 0), c, Enum.Material.WoodPlanks)
    P(m, 'WedgePart', Vector3.new(0.5, rise, w / 2), B * CFrame.new(s * w / 4, h + 0.6 + rise / 2, -d / 2) * CFrame.Angles(0, math.rad(-90 * s), 0), c, Enum.Material.WoodPlanks)
  end
  local pipe = P(m, 'Part', Vector3.new(4, 0.7, 0.7), B * CFrame.new(w / 4, h + 3.2, -d / 4) * CFrame.Angles(0, 0, math.rad(90)), rgb(50, 48, 46), Enum.Material.Metal, { shape = Enum.PartType.Cylinder })
  local s = Instance.new('Smoke'); s.Size = 1; s.Opacity = 0.1; s.RiseVelocity = 3; s.Color = rgb(200, 200, 205); s.Parent = pipe
  local a = P(m, 'Part', Vector3.new(0.3, 0.3, 0.3), B * CFrame.new(0, 4, 0), rgb(255, 170, 90), Enum.Material.Neon, { t = 1, nc = true, ns = true })
  local l = Instance.new('PointLight'); l.Color = rgb(255, 170, 100); l.Range = 9; l.Brightness = 1.2; l.Parent = a
end
local function hole(f, it, idx)
  local m = Instance.new('Model'); m.Name = 'FishingHole_' .. idx; m.Parent = f
  local B = CFrame.new(it.x, it.y + 0.05, it.z)
  P(m, 'Part', Vector3.new(0.2, 4.2, 4.2), B * CFrame.Angles(0, 0, math.rad(90)), rgb(18, 52, 70), Enum.Material.Glass, { shape = Enum.PartType.Cylinder, t = 0.05, nc = true })
  for k = 0, 5 do
    local a = k * math.pi / 3 + rng:NextNumber(-0.2, 0.2)
    P(m, 'Part', Vector3.new(1.4, 0.6, 1.1), B * CFrame.new(math.cos(a) * 2.8, 0.2, math.sin(a) * 2.8) * CFrame.Angles(0, a, 0), rgb(240, 247, 252), Enum.Material.Snow)
  end
end

local out = {}
local rp = RaycastParams.new(); rp.FilterType = Enum.RaycastFilterType.Include; rp.FilterDescendantsInstances = { workspace.Terrain }; rp.IgnoreWater = false
for _, key in ipairs({ 'huts', 'igloos', 'shanties', 'fishing_holes' }) do
  for _, it in ipairs(D[key] or {}) do
    local hit = workspace:Raycast(Vector3.new(it.x, 600, it.z), Vector3.new(0, -800, 0), rp)
    if hit then it.y = hit.Position.Y end
  end
end
if D.huts then local f = folder('RustyHuts'); for i, it in ipairs(D.huts) do hut(f, it, i) end; table.insert(out, 'huts ' .. #D.huts) end
if D.igloos then local f = folder('Igloos'); for i, it in ipairs(D.igloos) do igloo(f, it, i) end; table.insert(out, 'igloos ' .. #D.igloos) end
if D.shanties then local f = folder('IceShanties'); for i, it in ipairs(D.shanties) do shanty(f, it, i) end; table.insert(out, 'shanties ' .. #D.shanties) end
if D.fishing_holes then local f = folder('FishingHoles'); for i, it in ipairs(D.fishing_holes) do hole(f, it, i) end; table.insert(out, 'holes ' .. #D.fishing_holes) end
return table.concat(out, ', ') .. ' parts ' .. n
