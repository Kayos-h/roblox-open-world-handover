-- Enterable part-built buildings. Data: {kind, name, cx, cz, y, rot, style, ...}
local HS = game:GetService('HttpService')
local D = HS:JSONDecode([==[__DATA__]==])
local root = workspace:FindFirstChild('Phase1Map')
local parentF = root:FindFirstChild('Enterable') or Instance.new('Folder')
parentF.Name = 'Enterable'; parentF.Parent = root
local old = parentF:FindFirstChild(D.name)
if old then old:Destroy() end
local model = Instance.new('Model'); model.Name = D.name; model.Parent = parentF
local folders = {}
local function F(name)
  if not folders[name] then local f = Instance.new('Folder'); f.Name = name; f.Parent = model; folders[name] = f end
  return folders[name]
end
local BASE = CFrame.new(D.cx, D.y, D.cz) * CFrame.Angles(0, math.rad(D.rot), 0)
local C3 = function(t) return Color3.fromRGB(t[1], t[2], t[3]) end
local ST = D.style
local function mat(n) return Enum.Material[n] end
local nparts = 0
local function part(fold, size, lcf, color, material, opt)
  local p = Instance.new((opt and opt.class) or 'Part')
  p.Anchored = true
  p.Size = size
  p.CFrame = BASE * lcf
  p.Color = typeof(color) == 'Color3' and color or C3(color)
  p.Material = mat(material)
  p.TopSurface = Enum.SurfaceType.Smooth; p.BottomSurface = Enum.SurfaceType.Smooth
  p.CanTouch = false
  if opt then
    if opt.t then p.Transparency = opt.t end
    if opt.nc then p.CanCollide = false end
    if opt.ns then p.CastShadow = false end
    if opt.shape then p.Shape = opt.shape end
  end
  p.Parent = F(fold)
  nparts += 1
  return p
end
local function L(x, y, z) return CFrame.new(x, y, z) end
-- triangle between three LOCAL points (Vector3), built from two wedges
local function tri(fold, a, b, c, thick, color, material)
  local ab, ac, bc = b - a, c - a, c - b
  local abd, acd, bcd = ab:Dot(ab), ac:Dot(ac), bc:Dot(bc)
  if abd > acd and abd > bcd then c, a = a, c
  elseif acd > bcd and acd > abd then a, b = b, a end
  ab, ac, bc = b - a, c - a, c - b
  local right = ac:Cross(ab)
  if right.Magnitude < 1e-6 then return end
  right = right.Unit
  local up = bc:Cross(right).Unit
  local back = bc.Unit
  local height = math.abs(ab:Dot(up))
  local w1 = Instance.new('WedgePart')
  w1.Size = Vector3.new(thick, height, math.abs(ab:Dot(back)))
  w1.CFrame = BASE * CFrame.fromMatrix((a + b) / 2, right, up, back)
  local w2 = Instance.new('WedgePart')
  w2.Size = Vector3.new(thick, height, math.abs(ac:Dot(back)))
  w2.CFrame = BASE * CFrame.fromMatrix((a + c) / 2, -right, up, -back)
  for _, w in ipairs({ w1, w2 }) do
    w.Anchored = true; w.Color = typeof(color) == 'Color3' and color or C3(color); w.Material = mat(material)
    w.CanTouch = false; w.TopSurface = Enum.SurfaceType.Smooth; w.BottomSurface = Enum.SurfaceType.Smooth
    w.Parent = F(fold); nparts += 1
  end
end
local function light(fold, pos, color, range, bright)
  local a = part(fold, Vector3.new(0.4, 0.4, 0.4), pos, color, 'Neon', { t = 1, nc = true, ns = true })
  local l = Instance.new('PointLight'); l.Color = C3(color); l.Range = range; l.Brightness = bright; l.Shadows = true; l.Parent = a
end

-- pointed-arch window: glass pane (w x h) with gable top, stone frame, in the plane z=0 of frame cf (facing +Z)
local function window(fold, cf, w, h, glassColor, frameColor, frameMat, broken)
  local gh = w * 0.55
  if not broken then
    part(fold, Vector3.new(w, h, 0.4), cf * L(0, h / 2, 0), glassColor, 'Glass', { t = 0.25, ns = true })
    for s = -1, 1, 2 do
      part(fold, Vector3.new(0.4, gh, w / 2), cf * L(s * w / 4, h + gh / 2, 0) * CFrame.Angles(0, math.rad(-90 * s), 0), glassColor, 'Glass', { class = 'WedgePart', t = 0.25, ns = true })
    end
  end
  part(fold, Vector3.new(0.6, h + 1, 1.4), cf * L(-w / 2 - 0.3, h / 2, 0), frameColor, frameMat)
  part(fold, Vector3.new(0.6, h + 1, 1.4), cf * L(w / 2 + 0.3, h / 2, 0), frameColor, frameMat)
  part(fold, Vector3.new(w + 1.8, 0.8, 2.0), cf * L(0, -0.4, 0.3), frameColor, frameMat)
  part(fold, Vector3.new(0.6, h * 0.95, 0.5), cf * L(0, h * 0.5, 0), frameColor, frameMat)
end

-- wall along local X from x0..x1 at local z, thickness t, height h, with openings {{xc, w, y0, y1}}
local function wall(fold, z, x0, x1, t, h, openings, color, material, rotY)
  table.sort(openings, function(a, b) return a[1] < b[1] end)
  local R = CFrame.Angles(0, math.rad(rotY or 0), 0)
  local cur = x0
  local function seg(a, b, ya, yb)
    if b - a > 0.05 and yb - ya > 0.05 then
      part(fold, Vector3.new(b - a, yb - ya, t), R * L((a + b) / 2, (ya + yb) / 2, z), color, material)
    end
  end
  for _, o in ipairs(openings) do
    local a, b = o[1] - o[2] / 2, o[1] + o[2] / 2
    seg(cur, a, 0, h)
    seg(a, b, 0, o[3])
    seg(a, b, o[4], h)
    cur = b
  end
  seg(cur, x1, 0, h)
end

local function gableRoof(fold, cfC, len, span, rise, thick, color, material, over)
  -- two sloped slabs meeting at a ridge, roof runs along local Z
  local half = span / 2 + over
  local slope = math.sqrt(half * half + rise * rise)
  local ang = math.atan2(rise, half)
  for s = -1, 1, 2 do
    part(fold, Vector3.new(slope, thick, len), cfC * L(s * half / 2, rise / 2, 0) * CFrame.Angles(0, 0, -s * ang), color, material)
  end
  part(fold, Vector3.new(1.6, 1.6, len + 0.6), cfC * L(0, rise + 0.3, 0), D.style.ridge or color, material)
end

local function gableEnd(fold, cfC, span, rise, thick, color, material)
  -- triangular wall closing a gable (two wedges)
  for s = -1, 1, 2 do
    part(fold, Vector3.new(thick, rise, span / 2), cfC * L(s * span / 4, rise / 2, 0) * CFrame.Angles(0, math.rad(-90 * s), 0), color, material, { class = 'WedgePart' })
  end
end

local function spire(fold, cf, size, h, color, material)
  -- square pyramid from 4 corner wedges
  local hs = size / 2
  for k = 0, 3 do
    local a = math.rad(90 * k)
    local off = CFrame.Angles(0, a, 0) * L(hs / 2, h / 2, hs / 2)
    part(fold, Vector3.new(hs, h, hs), cf * off * CFrame.Angles(0, math.rad(90), 0), color, material, { class = 'CornerWedgePart' })
  end
end

-------------------------------------------------------------------- church / cathedral
local function church()
  local W2, Lh, H = D.half_w, D.half_l, D.wall_h   -- nave half width, half length, wall height
  local wallC, wallM = ST.wall, ST.wall_mat
  local trimC, trimM = ST.trim, ST.trim_mat
  local roofC, roofM = ST.roof, ST.roof_mat
  local T = 3
  local zF, zB = Lh, -Lh                 -- front (door end) and back
  -- plinth / floor (covers apse behind and tower in front)
  local below = D.plinth or 4
  local TWp = D.tower_w or 24
  local AR0 = W2 * 0.85
  local pz0, pz1 = zB - AR0 - 5, zF + TWp + 5
  part('Base', Vector3.new(W2 * 2 + 14, below + 1.4, pz1 - pz0), L(0, (1.4 - below) / 2 - 0.2, (pz0 + pz1) / 2), trimC, trimM)
  part('Base', Vector3.new(W2 * 2 - 2, 0.4, Lh * 2 - 2), L(0, 1.4, 0), ST.floor, ST.floor_mat)
  part('Base', Vector3.new(TWp - 2, 0.4, TWp - 2), L(0, 1.4, zF + TWp / 2 + 1.5), ST.floor, ST.floor_mat)
  local fy = 1.6
  -- steps in front of the tower door
  for k = 0, 3 do
    local hk = 0.4 * (k + 1)
    part('Base', Vector3.new(20 - k, hk, 2.4), L(0, hk / 2 - 0.2, pz1 + 1.2 + (3 - k) * 2.2), trimC, trimM)
  end
  -- side walls with tall windows between buttresses
  local bays = math.floor((Lh * 2 - 20) / 20)
  local bayLen = (Lh * 2 - 20) / bays
  for s = -1, 1, 2 do
    local ops = {}
    for b = 0, bays - 1 do
      local zc = zB + 10 + bayLen * (b + 0.5)
      table.insert(ops, { zc, 8, 12, 12 + 26 + 5 })
    end
    -- wall runs along local Z: build as wall in rotated frame (rot 90 -> local X becomes Z)
    local fold = 'Walls'
    local R = CFrame.Angles(0, math.rad(90), 0)
    table.sort(ops, function(a, b) return a[1] < b[1] end)
    local cur = zB
    local function seg(a, b, ya, yb)
      if b - a > 0.05 and yb - ya > 0.05 then
        part(fold, Vector3.new(T, yb - ya, b - a), L(s * W2, fy + (ya + yb) / 2, (a + b) / 2), wallC, wallM)
      end
    end
    for _, o in ipairs(ops) do
      local a, b = o[1] - o[2] / 2, o[1] + o[2] / 2
      seg(cur, a, 0, H); seg(a, b, 0, o[3]); seg(a, b, o[4], H); cur = b
      local wcf = L(s * W2, fy + o[3], o[1]) * CFrame.Angles(0, math.rad(90 * s), 0)
      local broken = ST.broken and (math.random() < ST.broken)
      window('Windows', wcf, 7.4, 26, ST.glass[(math.random(1, #ST.glass))], trimC, trimM, broken)
      if broken and ST.boards then
        for k = 0, 3 do
          part('Windows', Vector3.new(8.6, 1.2, 0.5), wcf * L(0, 4 + k * 6.5, 0.3) * CFrame.Angles(0, 0, math.rad(math.random(-12, 12))), ST.boards, 'WoodPlanks')
        end
      end
    end
    seg(cur, zF, 0, H)
    -- buttresses
    for b = 0, bays do
      local zc = zB + 10 + bayLen * b
      part('Buttress', Vector3.new(5, H - 6, 6), L(s * (W2 + 3.5), fy + (H - 6) / 2, zc), wallC, wallM)
      part('Buttress', Vector3.new(5, 8, 6), L(s * (W2 + 2.6), fy + H - 6, zc) * CFrame.Angles(0, 0, math.rad(s * 18)), trimC, trimM)
      part('Buttress', Vector3.new(2.2, 7, 2.2), L(s * (W2 + 3.5), fy + H - 1, zc), trimC, trimM)
      spire('Buttress', L(s * (W2 + 3.5), fy + H + 2.5, zc), 2.6, 6, roofC, roofM)
    end
    -- cornice
    part('Walls', Vector3.new(4, 2, Lh * 2 + 4), L(s * (W2 + 0.5), fy + H + 0.6, 0), trimC, trimM)
  end
  -- back wall + apse (sanctuary behind a tall arch)
  local AR = W2 * 0.85
  wall('Walls', zB, -W2 - 1.5, W2 + 1.5, T, H, { { 0, AR * 1.5, 0, H - 9 } }, wallC, wallM)
  part('Walls', Vector3.new(AR * 1.5 + 2, 1.6, T + 1), L(0, fy + H - 9.8, zB), trimC, trimM)
  local apexY = fy + H - 6 + 16
  for k = 0, 4 do
    local a1, a2 = math.rad(180 + k * 36), math.rad(180 + (k + 1) * 36)
    local p1 = Vector3.new(math.cos(a1) * AR, 0, zB + math.sin(a1) * AR)
    local p2 = Vector3.new(math.cos(a2) * AR, 0, zB + math.sin(a2) * AR)
    local mid = (p1 + p2) / 2
    local len = (p2 - p1).Magnitude
    local ang = math.atan2(p2.X - p1.X, p2.Z - p1.Z)
    part('Apse', Vector3.new(T, H - 6, len + 0.8), L(mid.X, fy + (H - 6) / 2, mid.Z) * CFrame.Angles(0, ang, 0), wallC, wallM)
    window('Windows', L(mid.X, fy + 12, mid.Z) * CFrame.Angles(0, ang + math.rad(90), 0), 5, 20, ST.glass[(k % #ST.glass) + 1], trimC, trimM)
    local q1 = Vector3.new(p1.X * 1.08, fy + H - 6, zB + (p1.Z - zB) * 1.08)
    local q2 = Vector3.new(p2.X * 1.08, fy + H - 6, zB + (p2.Z - zB) * 1.08)
    tri('Apse', q1, q2, Vector3.new(0, apexY, zB), 1.0, roofC, roofM)
    part('Apse', Vector3.new(2, 1.6, len + 1.4), L(mid.X * 1.02, fy + H - 6.2, zB + (mid.Z - zB) * 1.02) * CFrame.Angles(0, ang, 0), trimC, trimM)
  end
  part('Apse', Vector3.new(W2 * 2, 0.4, AR), L(0, fy + 0.2 - 0.2, zB - AR / 2), ST.floor, ST.floor_mat)
  part('Apse', Vector3.new(W2 * 2, 3, AR + 8), L(0, fy + 1.5, zB - AR / 2 + 4), ST.chancel, ST.floor_mat)
  -- front wall with portal into the nave (behind the tower)
  wall('Walls', zF, -W2 - 1.5, W2 + 1.5, T, H, { { 0, 14, 0, 22 } }, wallC, wallM)
  local TWf = D.tower_w or 24
  local zT = zF + TWf + 1.5 + T / 2
  for s = -1, 1, 2 do
    for k = 0, 2 do
      part('Portal', Vector3.new(1.4, 20 + k * 2, 1.6), L(s * (6.8 + k * 1.6), fy + (20 + k * 2) / 2, zT + 0.8 + k * 0.7), trimC, trimM)
    end
    part('Portal', Vector3.new(6, 0.8, 3), L(s * 8.8, fy + 22.5 + 0.8, zT + 1.4) * CFrame.Angles(0, 0, math.rad(-s * 32)), trimC, trimM)
    -- tower corner pilasters + blind lancets
    part('Tower', Vector3.new(3, D.tower_h or 100, 3), L(s * (TWf / 2 + 0.6), fy + (D.tower_h or 100) / 2, zT + 0.2), trimC, trimM)
    for k = 0, 1 do
      window('Tower', L(s * 6, fy + 52 + k * 0, zT + 0.3), 4, 14, ST.glass[3], trimC, trimM, false)
    end
  end
  part('Portal', Vector3.new(12, 1.0, 1.0), L(0, fy + 22.5, zT + 0.5), trimC, trimM)
  part('Portal', Vector3.new(11, 20.5, 0.6), L(0, fy + 10.2, zT - T - 0.2), ST.beam, 'Wood', { t = 1, nc = true })
  -- rose window on the tower front above the door
  local ry = fy + 36
  part('Windows', Vector3.new(0.4, 16, 16), L(0, ry, zT + 0.25) * CFrame.Angles(0, math.rad(90), 0), ST.glass[2], 'Glass', { shape = Enum.PartType.Cylinder, t = 0.1, ns = true })
  for k = 0, 11 do
    local a = math.rad(k * 30)
    part('Windows', Vector3.new(4.8, 1.3, 1.2), L(math.cos(a) * 8.4, ry + math.sin(a) * 8.4, zT + 0.6) * CFrame.Angles(0, 0, a + math.rad(90)), trimC, trimM)
    part('Windows', Vector3.new(0.45, 8, 0.6), L(math.cos(a) * 4, ry + math.sin(a) * 4, zT + 0.5) * CFrame.Angles(0, 0, a + math.rad(90)), trimC, trimM)
  end
  -- roof (steep) + gable ends
  local rise = D.roof_rise or 30
  gableRoof('Roof', L(0, fy + H + 1, 0), Lh * 2 + 6, W2 * 2 + 4, rise, 1.6, roofC, roofM, 3)
  gableEnd('Roof', L(0, fy + H + 1, zF), W2 * 2 + 2, rise, T, wallC, wallM)
  gableEnd('Roof', L(0, fy + H + 1, zB), W2 * 2 + 2, rise, T, wallC, wallM)
  -- ceiling beams inside
  for b = 0, bays do
    local zc = zB + 10 + bayLen * b
    part('Interior', Vector3.new(W2 * 2 - 2, 1.6, 1.6), L(0, fy + H - 1, zc), ST.beam, 'Wood')
  end
  -- bell tower over the front, with a spire
  local TW, TH = D.tower_w or 24, D.tower_h or 100
  local tz = zF + TW / 2 + 1.5
  wall('Tower', tz + TW / 2, -TW / 2 - 1.5, TW / 2 + 1.5, T, TH, { { 0, 12, 0, 21 } }, wallC, wallM)
  for s = -1, 1, 2 do
    part('Tower', Vector3.new(T, TH, TW), L(s * TW / 2, fy + TH / 2, tz), wallC, wallM)
  end
  part('Tower', Vector3.new(TW, 1.2, TW), L(0, fy + 26, tz), ST.beam, 'Wood')
  light('Tower', L(0, fy + 20, tz), { 255, 200, 150 }, 22, 1.2)
  -- belfry openings
  for k = 0, 3 do
    local a = math.rad(90 * k)
    local cf = L(0, fy + TH - 24, tz) * CFrame.Angles(0, a, 0) * L(0, 0, TW / 2 + 0.2)
    part('Tower', Vector3.new(7, 14, 1), cf * L(0, 7, 0), Color3.fromRGB(25, 22, 20), 'Slate', { ns = true })
    window('Tower', cf * L(0, 0, 0.6), 6, 12, ST.glass[3], trimC, trimM, true)
  end
  for _, yy in ipairs({ 24, TH * 0.55, TH - 28, TH }) do
    part('Tower', Vector3.new(TW + 2, 1.6, TW + 2), L(0, fy + yy, tz), trimC, trimM)
  end
  for sx = -1, 1, 2 do for sz = -1, 1, 2 do
    part('Tower', Vector3.new(3, 9, 3), L(sx * (TW / 2 - 0.5), fy + TH + 4.5, tz + sz * (TW / 2 - 0.5)), trimC, trimM)
    spire('Tower', L(sx * (TW / 2 - 0.5), fy + TH + 9, tz + sz * (TW / 2 - 0.5)), 3.4, 8, roofC, roofM)
  end end
  spire('Tower', L(0, fy + TH + 0.8, tz), TW - 2, D.spire_h or 46, roofC, roofM)
  part('Tower', Vector3.new(0.6, 6, 0.6), L(0, fy + TH + (D.spire_h or 46) + 3, tz), ST.gold, 'Metal')
  part('Tower', Vector3.new(3.4, 0.6, 0.6), L(0, fy + TH + (D.spire_h or 46) + 4, tz), ST.gold, 'Metal')
  -- interior lights
  for b = 0, bays - 1, 2 do
    local zc = zB + 10 + bayLen * (b + 0.5)
    light('Interior', L(0, fy + H - 8, zc), { 255, 205, 150 }, 40, 1.6)
  end
  light('Interior', L(0, fy + 14, zB - 6), { 255, 210, 160 }, 30, 1.8)
  return { fy = fy, bays = bays, bayLen = bayLen, zF = zF, zB = zB }
end

-------------------------------------------------------------------- hall (tavern, lodge)
local function hall()
  local W2, Lh, H = D.half_w, D.half_l, D.wall_h
  local T = 1.6
  local lowC, lowM = ST.low, ST.low_mat
  local upC, upM = ST.up, ST.up_mat
  local below = D.plinth or 3
  part('Base', Vector3.new(W2 * 2 + 4, below + 1.2, Lh * 2 + 4), L(0, (1.2 - below) / 2, 0), ST.base, ST.base_mat)
  part('Base', Vector3.new(W2 * 2 - 1, 0.3, Lh * 2 - 1), L(0, 1.25, 0), ST.floor, ST.floor_mat)
  local fy = 1.4
  local split = H * 0.45
  -- front (+Z) with door, back, sides with windows; lower stone, upper timber
  local function band(fold, z, x0, x1, ops, rotY, isSide)
    local R = CFrame.Angles(0, math.rad(rotY), 0)
    local function seg(a, b, ya, yb, c, m)
      if b - a > 0.05 and yb - ya > 0.05 then part(fold, Vector3.new(b - a, yb - ya, T), R * L((a + b) / 2, fy + (ya + yb) / 2, z), c, m) end
    end
    table.sort(ops, function(a, b) return a[1] < b[1] end)
    for _, layer in ipairs({ { 0, split, lowC, lowM }, { split, H, upC, upM } }) do
      local cur = x0
      for _, o in ipairs(ops) do
        local a, b = o[1] - o[2] / 2, o[1] + o[2] / 2
        local oy0, oy1 = math.max(o[3], layer[1]), math.min(o[4], layer[2])
        seg(cur, a, layer[1], layer[2], layer[3], layer[4])
        if oy1 > oy0 then
          seg(a, b, layer[1], oy0, layer[3], layer[4]); seg(a, b, oy1, layer[2], layer[3], layer[4])
        else seg(a, b, layer[1], layer[2], layer[3], layer[4]) end
        cur = b
      end
      seg(cur, x1, layer[1], layer[2], layer[3], layer[4])
    end
    for _, o in ipairs(ops) do
      if o[5] then
        local cf = R * L(o[1], fy + o[3], z) 
        part('Windows', Vector3.new(o[2], o[4] - o[3], 0.3), cf * L(0, (o[4] - o[3]) / 2, 0), ST.glass, 'Glass', { t = 0.35, ns = true })
        part('Windows', Vector3.new(o[2] + 1.2, 0.6, T + 0.8), cf * L(0, -0.3, 0), ST.trim, 'Wood')
        part('Windows', Vector3.new(o[2] + 1.2, 0.6, T + 0.6), cf * L(0, o[4] - o[3] + 0.3, 0), ST.trim, 'Wood')
        part('Windows', Vector3.new(0.4, o[4] - o[3], 0.5), cf * L(0, (o[4] - o[3]) / 2, 0), ST.trim, 'Wood')
      end
    end
  end
  local winS = {}
  for k = -1, 1 do table.insert(winS, { k * Lh * 0.55, 5, 5, 11, true }) end
  band('Walls', Lh, -W2, W2, { { 0, 6, 0, 9.5 }, { -W2 * 0.55, 4.5, 5, 10.5, true }, { W2 * 0.55, 4.5, 5, 10.5, true } }, 0)
  band('Walls', -Lh, -W2, W2, { { -W2 * 0.5, 4.5, 5, 10.5, true }, { W2 * 0.5, 4.5, 5, 10.5, true } }, 0)
  band('Walls', W2, -Lh, Lh, winS, 90)
  band('Walls', W2, -Lh, Lh, {}, 270)
  for _, c in ipairs(folders.Walls:GetChildren()) do end
  -- timber frame posts on the corners
  for sx = -1, 1, 2 do for sz = -1, 1, 2 do part('Frame', Vector3.new(1.4, H, 1.4), L(sx * W2, fy + H / 2, sz * Lh), ST.trim, 'Wood') end end
  part('Frame', Vector3.new(W2 * 2 + 1, 1, 1.2), L(0, fy + split, Lh + 0.3), ST.trim, 'Wood')
  part('Frame', Vector3.new(W2 * 2 + 1, 1, 1.2), L(0, fy + split, -Lh - 0.3), ST.trim, 'Wood')
  -- roof along Z
  local rise = D.roof_rise or 12
  gableRoof('Roof', L(0, fy + H, 0), Lh * 2 + 5, W2 * 2, rise, 1.0, ST.roof, ST.roof_mat, 2.2)
  gableEnd('Roof', L(0, fy + H, Lh), W2 * 2, rise, T, upC, upM)
  gableEnd('Roof', L(0, fy + H, -Lh), W2 * 2, rise, T, upC, upM)
  if ST.snow then
    local half = W2 + 2.2
    local ang = math.atan2(rise, half)
    for s = -1, 1, 2 do
      part('Roof', Vector3.new(math.sqrt(half * half + rise * rise), 0.6, Lh * 2 + 5.2), L(s * half / 2, fy + H + rise / 2 + 0.75, 0) * CFrame.Angles(0, 0, -s * ang), { 245, 248, 252 }, 'Snow')
    end
  end
  -- chimney + fireplace on the back wall
  part('Interior', Vector3.new(9, 9, 3), L(0, fy + 4.5, -Lh + 2.2), ST.stone, 'Cobblestone')
  part('Interior', Vector3.new(5, 4, 1.2), L(0, fy + 2, -Lh + 3.4), { 30, 20, 15 }, 'Slate')
  local fire = part('Interior', Vector3.new(2.5, 1.5, 0.8), L(0, fy + 0.9, -Lh + 3.6), { 255, 120, 30 }, 'Neon', { nc = true, ns = true })
  local fl = Instance.new('PointLight'); fl.Color = Color3.fromRGB(255, 150, 70); fl.Range = 22; fl.Brightness = 2; fl.Parent = fire
  local fx = Instance.new('Fire'); fx.Size = 3; fx.Heat = 6; fx.Parent = fire
  part('Roof', Vector3.new(4, rise + 8, 4), L(W2 * 0.4, fy + H + rise / 2, -Lh * 0.6), ST.stone, 'Cobblestone')
  -- counter (bar)
  if D.bar then
    part('Interior', Vector3.new(W2 * 1.1, 4, 2.4), L(-W2 * 0.2, fy + 2, -Lh * 0.45), ST.trim, 'Wood')
    part('Interior', Vector3.new(W2 * 1.1 + 0.6, 0.4, 3), L(-W2 * 0.2, fy + 4.2, -Lh * 0.45), { 120, 80, 50 }, 'WoodPlanks')
  end
  for k = -1, 1 do light('Interior', L(0, fy + H - 2, k * Lh * 0.55), { 255, 196, 130 }, 24, 1.3) end
  -- door frame + sign post
  part('Frame', Vector3.new(7.4, 1, 2), L(0, fy + 9.9, Lh + 0.4), ST.trim, 'Wood')
  return { fy = fy }
end

-------------------------------------------------------------------- elf moon shrine
local function shrine()
  local R0 = D.radius
  part('Base', Vector3.new(4 + (D.plinth or 3), R0 * 2 + 8, R0 * 2 + 8), L(0, (1 - (D.plinth or 3)) / 2, 0) * CFrame.Angles(0, 0, math.rad(90)), ST.base, ST.base_mat, { shape = Enum.PartType.Cylinder })
  part('Base', Vector3.new(0.6, R0 * 2, R0 * 2), L(0, 1.3, 0) * CFrame.Angles(0, 0, math.rad(90)), ST.floor, ST.floor_mat, { shape = Enum.PartType.Cylinder })
  local fy = 1.6
  local N = 10
  for k = 0, N - 1 do
    local a = math.rad(k * 360 / N)
    local x, z = math.cos(a) * R0, math.sin(a) * R0
    part('Columns', Vector3.new(D.col_h, 2.6, 2.6), L(x, fy + D.col_h / 2, z) * CFrame.Angles(0, 0, math.rad(90)), ST.col, ST.col_mat, { shape = Enum.PartType.Cylinder })
    part('Columns', Vector3.new(4, 1.2, 4), L(x, fy + 0.6, z), ST.trim, ST.col_mat)
    part('Columns', Vector3.new(4, 1.4, 4), L(x, fy + D.col_h - 0.2, z), ST.trim, ST.col_mat)
    local g = part('Columns', Vector3.new(1.4, 1.4, 1.4), L(x, fy + D.col_h + 1.6, z), ST.glow, 'Neon', { shape = Enum.PartType.Ball, nc = true, ns = true })
    local l = Instance.new('PointLight'); l.Color = C3(ST.glow); l.Range = 14; l.Brightness = 1.2; l.Parent = g
    -- ring beam segment
    local a2 = math.rad((k + 1) * 360 / N)
    local p1, p2 = Vector3.new(x, 0, z), Vector3.new(math.cos(a2) * R0, 0, math.sin(a2) * R0)
    local mid, len = (p1 + p2) / 2, (p2 - p1).Magnitude
    part('Ring', Vector3.new(len + 1.2, 2, 3), L(mid.X, fy + D.col_h + 0.6, mid.Z) * CFrame.Angles(0, math.atan2(-(p2.Z - p1.Z), p2.X - p1.X), 0), ST.trim, ST.col_mat)
    -- arch petals rising to the crown
    local top = Vector3.new(0, fy + D.col_h + D.crown, 0)
    local base = Vector3.new(x, fy + D.col_h + 1.2, z)
    local v = top - base
    part('Crown', Vector3.new(1.2, 1.2, v.Magnitude), CFrame.lookAt(base + v / 2, top) * CFrame.new(0, 0, 0), ST.col, ST.col_mat).CFrame = BASE * CFrame.lookAt(base + v / 2, top)
  end
  local crown = part('Crown', Vector3.new(4, 4, 4), L(0, fy + D.col_h + D.crown, 0), ST.glow, 'Neon', { shape = Enum.PartType.Ball, nc = true, ns = true })
  local l = Instance.new('PointLight'); l.Color = C3(ST.glow); l.Range = 40; l.Brightness = 1.6; l.Parent = crown
  -- inner pool
  part('Interior', Vector3.new(1, R0 * 0.9, R0 * 0.9), L(0, fy + 0.3, 0) * CFrame.Angles(0, 0, math.rad(90)), ST.trim, ST.col_mat, { shape = Enum.PartType.Cylinder })
  part('Interior', Vector3.new(0.4, R0 * 0.8, R0 * 0.8), L(0, fy + 0.85, 0) * CFrame.Angles(0, 0, math.rad(90)), { 90, 200, 230 }, 'Glass', { shape = Enum.PartType.Cylinder, t = 0.3, nc = true })
  return { fy = fy }
end

-------------------------------------------------------------------- elf round house (enterable)
local function elfhouse()
  local R0, H = D.radius or 14, D.wall_h or 12
  local below = D.plinth or 3
  part('Base', Vector3.new(below + 1.4, R0 * 2 + 5, R0 * 2 + 5), L(0, (1.4 - below) / 2 - 0.2, 0) * CFrame.Angles(0, 0, math.rad(90)), ST.base, ST.base_mat, { shape = Enum.PartType.Cylinder })
  part('Base', Vector3.new(0.4, R0 * 2, R0 * 2), L(0, 1.4, 0) * CFrame.Angles(0, 0, math.rad(90)), ST.floor, ST.floor_mat, { shape = Enum.PartType.Cylinder })
  local fy = 1.6
  local N = 16
  local seg = 2 * R0 * math.sin(math.pi / N) + 0.6
  for k = 0, N - 1 do
    local a = (k + 0.5) * 2 * math.pi / N
    local x, z = math.cos(a) * R0, math.sin(a) * R0
    local cf = L(x, fy, z) * CFrame.Angles(0, -a + math.rad(90), 0)
    local isDoor = math.abs(math.cos(a)) < 0.2 and math.sin(a) > 0
    if isDoor then
      part('Walls', Vector3.new(seg, H - 9, 1.4), cf * L(0, 9 + (H - 9) / 2, 0), ST.wall, ST.wall_mat)
      part('Frame', Vector3.new(1.2, 9.6, 1.8), cf * L(-seg / 2, 4.8, 0), ST.trim, ST.trim_mat)
      part('Frame', Vector3.new(1.2, 9.6, 1.8), cf * L(seg / 2, 4.8, 0), ST.trim, ST.trim_mat)
    elseif k % 2 == 0 then
      part('Walls', Vector3.new(seg, 4, 1.4), cf * L(0, 2, 0), ST.wall, ST.wall_mat)
      part('Walls', Vector3.new(seg, H - 9, 1.4), cf * L(0, 9 + (H - 9) / 2, 0), ST.wall, ST.wall_mat)
      part('Windows', Vector3.new(seg - 0.8, 5, 0.3), cf * L(0, 6.5, 0), ST.glass, 'Glass', { t = 0.3, ns = true })
      part('Windows', Vector3.new(seg, 0.6, 1.8), cf * L(0, 4.1, 0), ST.trim, ST.trim_mat)
    else
      part('Walls', Vector3.new(seg, H, 1.4), cf * L(0, H / 2, 0), ST.wall, ST.wall_mat)
      part('Frame', Vector3.new(0.8, H, 1.9), cf * L(seg / 2, H / 2, 0), ST.trim, ST.trim_mat)
    end
    -- conical leaf roof (two tiers)
    local a1, a2 = k * 2 * math.pi / N, (k + 1) * 2 * math.pi / N
    local Rr = R0 + 3
    local p1 = Vector3.new(math.cos(a1) * Rr, fy + H + 0.4, math.sin(a1) * Rr)
    local p2 = Vector3.new(math.cos(a2) * Rr, fy + H + 0.4, math.sin(a2) * Rr)
    tri('Roof', p1, p2, Vector3.new(0, fy + H + 15, 0), 0.8, ST.roof, ST.roof_mat)
    local q1 = Vector3.new(math.cos(a1) * (Rr * 0.55), fy + H + 7.2, math.sin(a1) * (Rr * 0.55))
    local q2 = Vector3.new(math.cos(a2) * (Rr * 0.55), fy + H + 7.2, math.sin(a2) * (Rr * 0.55))
    tri('Roof', Vector3.new(q1.X * 1.35, q1.Y - 1.6, q1.Z * 1.35), Vector3.new(q2.X * 1.35, q2.Y - 1.6, q2.Z * 1.35), Vector3.new(0, fy + H + 13, 0), 0.6, ST.roof2, ST.roof_mat)
    local mid = (p1 + p2) / 2
    part('Frame', Vector3.new((p2 - p1).Magnitude + 0.4, 0.9, 0.9), L(mid.X * 0.93, fy + H + 0.2, mid.Z * 0.93) * CFrame.Angles(0, -math.atan2(p2.Z - p1.Z, p2.X - p1.X), 0), ST.trim, ST.trim_mat)
  end
  local g = part('Roof', Vector3.new(2.6, 2.6, 2.6), L(0, fy + H + 16, 0), ST.glow, 'Neon', { shape = Enum.PartType.Ball, nc = true, ns = true })
  local gl = Instance.new('PointLight'); gl.Color = C3(ST.glow); gl.Range = 26; gl.Brightness = 1.4; gl.Parent = g
  light('Interior', L(0, fy + H - 2, 0), { 160, 255, 210 }, 22, 1.4)
  light('Interior', L(0, fy + 4, -R0 * 0.5), { 255, 220, 170 }, 14, 1)
  return { fy = fy }
end

local info
if D.kind == 'church' then info = church() elseif D.kind == 'hall' then info = hall() elseif D.kind == 'elfhouse' then info = elfhouse() else info = shrine() end
model:SetAttribute('FloorY', D.y + (info.fy or 0))
return HS:JSONEncode({ name = D.name, parts = nparts, fy = info.fy, bays = info.bays, bayLen = info.bayLen })
