-- Phase 1 terrain generator (v4: relief, west cliffs, robust rivers, default biome). Data: world.json + run options, injected as __DATA__.
-- Runs in a background thread; progress in _G.TG.
local HS = game:GetService('HttpService')
local D = HS:JSONDecode([==[__DATA__]==])
local W = D.world
local OPT = D.opt
local T = workspace.Terrain
local RES = 4
local CH = 128

local M = Enum.Material
local MAT = {}
for _, n in ipairs({ 'Grass', 'LeafyGrass', 'Ground', 'Mud', 'Sand', 'Sandstone', 'Rock', 'Slate', 'Basalt', 'Cobblestone', 'Pavement', 'Snow', 'Glacier', 'Ice', 'Limestone', 'Salt', 'Water', 'Air', 'Brick', 'Concrete', 'Asphalt', 'WoodPlanks' }) do MAT[n] = M[n] end

local floor, max, min, abs, sqrt, exp, noise = math.floor, math.max, math.min, math.abs, math.sqrt, math.exp, math.noise
local function ss(a, b, x)
  if b == a then return x >= b and 1 or 0 end
  local t = (x - a) / (b - a)
  if t < 0 then t = 0 elseif t > 1 then t = 1 end
  return t * t * (3 - 2 * t)
end
local function lerp(a, b, t) return a + (b - a) * t end

local FEAT = W.features
local RL = W.relief or {}
local CO = W.coast
local function coastD(x, z)
  local az = z < 0 and CO.az_n or CO.az_s
  local a, b = abs(x) / CO.ax, abs(z) / az
  local p = CO.p or 4
  return (a ^ p + b ^ p) ^ (1 / p) + 0.055 * noise(x / 900, z / 900, 3.3) + 0.03 * noise(x / 420, z / 420, 5.5) + 0.018 * noise(x / 180, z / 180, 7.7)
end
local function coastStart(x, z)
  local ws = CO.west_start
  if not ws then return CO.start end
  return lerp(CO.start, ws, ss(900, 1700, -x))
end
local POST = W.post or {}
local function postH(h, x, z)
  for _, f in ipairs(POST) do
    local d = sqrt((x - f[1]) ^ 2 + (z - f[2]) ^ 2)
    local r = f[3] * (1 + 0.15 * noise(x / 45, z / 45, f[1] * 0.002))
    if d < r then
      local top = f[4] + 2.5 * noise(x / 30, z / 30, 1.9)
      local v = lerp(top, h, ss(r * 0.55, r, d))
      if v > h then h = v end
    end
  end
  return h
end
local function ridged(x, z)
  local v, a, f = 0, 0.6, 1 / 260
  for o = 1, 4 do
    local n = 1 - abs(noise(x * f, z * f, 11.3 + o * 7.1) * 2)
    v += a * n * n
    a *= 0.5; f *= 2.1
  end
  return v / 1.125
end
local function featH(x, z)
  local h = 6
  for _, f in ipairs(FEAT) do
    local dx, dz = x - f[2], z - f[3]
    local r = f[4]
    if abs(dx) < r * 3 and abs(dz) < r * 3 then
      local d = sqrt(dx * dx + dz * dz)
      if f[1] == 'g' then h += f[5] * exp(-(d / r) ^ 2)
      elseif f[1] == 'M' then
        local g = exp(-(d / r) ^ 2)
        if g > 0.004 then h += f[5] * g * (0.55 + 0.6 * ridged(x, z)) end
      else
        -- mesa: flat top with eroded steep rim
        local rr = r * (1 + 0.12 * noise(x / 60, z / 60, f[2] * 0.001))
        h += f[5] * (1 - ss(rr * 0.72, rr, d))
      end
    end
  end
  return h
end
local function fbm(x, z)
  return noise(x / 650, z / 650, 1.7) + 0.5 * noise(x / 260, z / 260, 5.1) + 0.25 * noise(x / 110, z / 110, 9.3) + 0.1 * noise(x / 43, z / 43, 2.2)
end
local function padMask(p, x, z)
  local out
  if p.shape == 'rect' then
    local dx, dz = abs(x - p.cx) - p.hx, abs(z - p.cz) - p.hz
    if dx <= 0 and dz <= 0 then out = 0 else out = sqrt(max(dx, 0) ^ 2 + max(dz, 0) ^ 2) end
  else
    local nx, nz = (x - p.cx) / p.rx, (z - p.cz) / p.rz
    out = max(0, (sqrt(nx * nx + nz * nz) - 1) * min(p.rx, p.rz))
  end
  if p.cliff then out = out + 6 * noise(x / 40, z / 40, 4.4) end
  return 1 - ss(0, p.e, out)
end
local function padGround(p, x, z)
  local g = p.ground
  if g.type == 'flat' then return g.y end
  local t = (x - g.p0[1]) * g.dir[1] + (z - g.p0[2]) * g.dir[2]
  return min(g.hi, max(g.lo, g.y0 + g.slope * t))
end

-- segment list for roads / rivers / streets: {x0,z0,y0,x1,z1,y1,w,mat,kind,bank,level,depth}
local SEGS = {}
local function addPoly(pts, w, mat, kind, extra)
  for i = 1, #pts - 1 do
    local a, b = pts[i], pts[i + 1]
    local s = { a[1], a[2], a[3] or 0, b[1], b[2], b[3] or 0, w, mat, kind }
    if extra then for k, v in pairs(extra) do s[k] = v end end
    local pad = w + (kind == 'road' and 80 or 30)
    s.bx0 = min(a[1], b[1]) - pad; s.bx1 = max(a[1], b[1]) + pad
    s.bz0 = min(a[2], b[2]) - pad; s.bz1 = max(a[2], b[2]) + pad
    table.insert(SEGS, s)
  end
end
for _, r in ipairs(W.roads) do addPoly(r.pts, r.w, r.mat, 'road') end
for _, r in ipairs(W.streets or {}) do addPoly(r.pts, r.w, r.mat, 'road', { street = true, bankMax = r.bank or 20 }) end
for _, r in ipairs(W.rivers) do
  local pts = {}
  for _, p in ipairs(r.pts) do table.insert(pts, { p[1], p[2], p[3] or r.level }) end
  addPoly(pts, r.w, 'Mud', 'river', { depth = r.depth })
end
local LAKES = W.lakes
local BIO = W.biomes
local KT = W.keep and W.keep.town1
local KM = W.keep and W.keep.mountain
local T1 = W.t1
local SNAP = _G.T1SNAP

local function segDist(s, x, z)
  local ax, az, bx, bz = s[1], s[2], s[4], s[5]
  local vx, vz = bx - ax, bz - az
  local L2 = vx * vx + vz * vz
  local t = 0
  if L2 > 0 then t = ((x - ax) * vx + (z - az) * vz) / L2; if t < 0 then t = 0 elseif t > 1 then t = 1 end end
  local px, pz = ax + vx * t, az + vz * t
  return sqrt((x - px) ^ 2 + (z - pz) ^ 2), t
end

local function biomeAt(x, z)
  local best, bw = (W.default_biome or 'plains'), 0.3
  for _, b in ipairs(BIO) do
    local d = sqrt((x - b[2]) ^ 2 + (z - b[3]) ^ 2)
    local wgt = 1 - ss(0.5 * b[4], b[4], d + 60 * noise(x / 300, z / 300, 8.1))
    if wgt > bw then best, bw = b[1], wgt end
  end
  return best
end

-- returns h, roadMat, waterLevel, coastal, streetCore, padWeight, snapMaterial
local function snapAt(x, z)
  local S = SNAP
  local ox, oz = x / 0.7, z / 0.7
  local fi, fk = (ox - S.X0) / 4 + 0.5, (oz - S.Z0) / 4 + 0.5
  local i0, k0 = floor(fi), floor(fk)
  local ti, tk = fi - i0, fk - k0
  local function H(i, k)
    i = max(1, min(S.nx, i)); k = max(1, min(S.nz, k))
    return S.H[i .. ',' .. k] or 2
  end
  local h = lerp(lerp(H(i0, k0), H(i0 + 1, k0), ti), lerp(H(i0, k0 + 1), H(i0 + 1, k0 + 1), ti), tk)
  local ni, nk = max(1, min(S.nx, floor(fi + 0.5))), max(1, min(S.nz, floor(fk + 0.5)))
  local key = ni .. ',' .. nk
  return h, S.M[key] or 'Grass', S.W[key]
end
local function column(x, z, segs)
  if SNAP and T1 and abs(x) <= T1.x and z >= T1.z0 and z <= T1.z1 then
    local h, m, wl = snapAt(x, z)
    return h, nil, wl, 0, false, 1, m
  end
  local h = featH(x, z)
  local cd = coastD(x, z)
  local c = ss(coastStart(x, z), CO['end'], cd)
  local amp = ((RL.base or 8) + (RL.slope or 0.10) * max(0, h - 6)) * (1 - c)
  h = h + fbm(x, z) * amp
  h = lerp(h, (CO.floor - (CO.deep or 0) * ss(1.0, 1.15, cd)) + 4 * noise(x / 300, z / 300, 6.6), c)
  h = postH(h, x, z)
  local pm = 0
  for _, p in ipairs(W.pads) do
    local m = padMask(p, x, z)
    if m > 0 then
      local tg = padGround(p, x, z)
      if p.noise and p.noise > 0 then tg += p.noise * (noise(x / 90, z / 90, 2.9) + 0.4 * noise(x / 33, z / 33, 1.1)) end
      h = lerp(h, tg, m)
      if m > pm then pm = m end
    end
  end
  local roadMat, bestD, water, street = nil, 1e9, nil, false
  for _, s in ipairs(segs) do
    if s[9] == 'road' then
      local d, t = segDist(s, x, z)
      local w = s[7]
      local ry = lerp(s[3], s[6], t)
      local bank = min(s.bankMax or 70, 10 + 1.6 * abs(h - ry))
      if d < w + bank then
        local m = 1 - ss(w, w + bank, d)
        h = lerp(h, ry, m)
        if d < w and d < bestD then bestD = d; roadMat = s[8]; street = s.street or false end
      end
    end
  end
  local h0 = h
  for _, s in ipairs(segs) do
    if s[9] == 'river' then
      local d = segDist(s, x, z)
      local w = s[7]
      if d < w + 24 then
        local lv = s[3]
        if h0 >= lv - 8 then
          local tgt
          if d < w then tgt = lv - s.depth * (1 - (d / w) ^ 2) - 0.6
          else tgt = lv + 1.0 + (d - w) * 0.35 end
          if tgt < h then h = tgt end
          if d < w + 2 and (not water or lv < water) then water = lv end
        end
      end
    end
  end
  local frozen = false
  for _, L in ipairs(LAKES) do
    local nx, nz = (x - L.cx) / L.rx, (z - L.cz) / L.rz
    local r = sqrt(nx * nx + nz * nz) + (min(L.rx, L.rz) > 90 and 0.05 or 0.02) * noise(x / 60, z / 60, 5.5)
    if r < 1.45 then
      local tgt
      if L.frozen then
        if r < 1 then h = L.level - 1.2 * (1 - r * r); frozen = true
        else
          tgt = L.level + 0.4 + (r - 1) * min(L.rx, L.rz) * 0.18
          if tgt < h then h = tgt end
        end
      else
        if r < 1 then tgt = L.level - L.depth * (1 - r * r) - 0.6
        else tgt = L.level + 1.0 + (r - 1) * min(L.rx, L.rz) * 0.32 end
        if tgt < h then h = tgt end
        if r < 1.04 then water = L.level end
      end
    end
  end
  if not water and c > 0.15 and h < 0 then water = 0 end
  if frozen then roadMat = 'Ice' end
  return h, roadMat, water, c, street, pm
end

local function surfMat(x, z, h, slope, roadMat, coastal, street, inPad)
  if roadMat then return MAT[roadMat] end
  local wx = x + 90 * noise(x / 200, z / 200, 1.1)
  local wz = z + 90 * noise(x / 200, z / 200, 2.2)
  local b = biomeAt(wx, wz)
  local n1 = noise(x / 140, z / 140, 3.7)
  local n2 = noise(x / 47, z / 47, 8.2)
  local n3 = noise(x / 71, z / 71, 12.3)
  local n4 = noise(x / 260, z / 260, 15.1)
  if h > 262 + 20 * n1 and slope < 0.6 then return M.Snow end
  if h < 3.4 and coastal > 0.05 then return (h < -6 and n1 > 0.1) and M.Mud or M.Sand end
  if h < 7 and coastal > 0.02 and n3 > 0.1 then return M.Sand end
  if b == 'dry' then
    if slope > 0.8 then return n2 > 0.2 and M.Rock or M.Sandstone end
    if slope > 0.45 then return M.Sandstone end
    if n3 > 0.38 then return M.Sandstone end
    if n4 > 0.35 then return M.Salt end
    return M.Ground
  end
  if b == 'alpine' then
    local sn = 165 + 25 * n1
    if slope > 0.75 then return n2 > 0.25 and M.Rock or M.Slate end
    if slope > 0.5 then return M.Rock end
    if h > sn then return M.Snow end
    if h > 130 and n2 > 0.3 then return M.Snow end
    if h > 100 and n3 > 0.45 then return M.Snow end
    if h > 90 and n2 > 0.55 then return M.Rock end
    return (n1 > 0.3 and not inPad) and M.LeafyGrass or M.Grass
  end
  if slope > 0.9 then return n2 > 0.1 and M.Rock or M.Slate end
  if slope > 0.62 then return n2 > 0.1 and M.Rock or M.LeafyGrass end
  if inPad and inPad > 0.5 then return (b == 'jungle' and n2 > -0.15) and M.LeafyGrass or M.Grass end
  if b == 'jungle' then return n2 > 0.36 and M.Grass or M.LeafyGrass end
  if b == 'plains' then
    if n3 > 0.62 and slope < 0.3 then return M.Ground end
    return (n1 + 0.5 * n4 > 0.5) and M.LeafyGrass or M.Grass
  end
  if n3 > 0.6 and slope < 0.3 then return M.Ground end
  if slope > 0.45 and n2 > 0.0 then return M.Rock end
  return (n1 * 0.6 + n4 * 0.4 > 0.25) and M.Grass or M.LeafyGrass
end

local function inRect(r, x, z) return x >= r[1] and x <= r[2] and z >= r[3] and z <= r[4] end
local function rectHit(r, x0, z0, x1, z1) return x1 > r[1] and x0 < r[2] and z1 > r[3] and z0 < r[4] end

local function doChunk(cx0, cz0)
  local cx1, cz1 = cx0 + CH, cz0 + CH
  local N = CH / RES
  local segs = {}
  for _, s in ipairs(SEGS) do if s.bx1 > cx0 and s.bx0 < cx1 and s.bz1 > cz0 and s.bz0 < cz1 then table.insert(segs, s) end end
  local hitTown = KT and rectHit(KT, cx0, cz0, cx1, cz1) or false
  local hitMtn = KM and rectHit(KM, cx0 - 0, cz0 - 0, cx1, cz1) or false
  -- heights on an (N+2)^2 grid with a 1-cell border for slopes
  local H, RM, WL, CO2, ST, PM, SM = {}, {}, {}, {}, {}, {}, {}
  for i = 0, N + 1 do
    H[i], RM[i], WL[i], CO2[i], ST[i], PM[i], SM[i] = {}, {}, {}, {}, {}, {}, {}
    for k = 0, N + 1 do
      local x, z = cx0 + (i - 1) * RES + 2, cz0 + (k - 1) * RES + 2
      local h, rm, wl, c, st, pm, sm = column(x, z, segs)
      H[i][k], RM[i][k], WL[i][k], CO2[i][k], ST[i][k], PM[i][k], SM[i][k] = h, rm, wl, c, st, pm, sm
    end
  end
  local yLo, yHi
  local readM, readO, keepCol, modM
  if hitMtn or hitTown then
    yLo = -48; yHi = hitMtn and 524 or 124
    local reg = Region3.new(Vector3.new(cx0, yLo, cz0), Vector3.new(cx1, yHi, cz1)):ExpandToGrid(RES)
    readM, readO = T:ReadVoxels(reg, RES)
    keepCol, modM = {}, {}
    local ny = #readM[1]
    for i = 1, N do
      keepCol[i], modM[i] = {}, {}
      for k = 1, N do
        local x, z = cx0 + (i - 1) * RES + 2, cz0 + (k - 1) * RES + 2
        if hitTown and inRect(KT, x, z) then keepCol[i][k] = true
        elseif hitMtn and inRect(KM, x, z) then
          -- existing surface height
          local hx = yLo
          for j = ny, 1, -1 do
            local mt = readM[i][j][k]
            if mt ~= M.Air and mt ~= M.Water and readO[i][j][k] > 0 then hx = yLo + (j - 1) * RES + readO[i][j][k] * RES; break end
          end
          local edge = min(x - KM[1], KM[2] - x, z - KM[3], KM[4] - z)
          local m = max(1 - ss(55, 115, hx), 1 - ss(0, 140, edge))
          for _, p in ipairs(W.pads) do if p.name == 'alpine_shelf' then m = max(m, padMask(p, x, z)) end end
          if RM[i][k] then m = 1 end
          for _, s in ipairs(segs) do
            if s[9] == 'road' then
              local d = segDist(s, x, z)
              m = max(m, 1 - ss(s[7] + 6, s[7] + 60, d))
            end
          end
          if m <= 0.001 then keepCol[i][k] = true
          else H[i][k] = lerp(hx, H[i][k], m); modM[i][k] = m end
        end
      end
    end
  else
    local lo, hi = 1e9, -1e9
    for i = 1, N do for k = 1, N do
      local h = H[i][k]; if h < lo then lo = h end; if h > hi then hi = h end
      if WL[i][k] and WL[i][k] > hi then hi = WL[i][k] end
    end end
    yLo = -64
    yHi = floor((hi + 12) / RES) * RES + RES
  end
  local ny = (yHi - yLo) / RES
  local mats, occ = table.create(N), table.create(N)
  for i = 1, N do
    local mi, oi = table.create(ny), table.create(ny)
    for j = 1, ny do mi[j] = table.create(N, M.Air); oi[j] = table.create(N, 0) end
    mats[i], occ[i] = mi, oi
    for k = 1, N do
      if keepCol and keepCol[i][k] then
        for j = 1, ny do mi[j][k] = readM[i][j][k]; oi[j][k] = readO[i][j][k] end
      else
        local x, z = cx0 + (i - 1) * RES + 2, cz0 + (k - 1) * RES + 2
        local h = H[i][k]
        local sx = (H[i + 1][k] - H[i - 1][k]) / (2 * RES)
        local sz = (H[i][k + 1] - H[i][k - 1]) / (2 * RES)
        local slope = sqrt(sx * sx + sz * sz)
        local sm = SM[i][k] and (M[SM[i][k]] or M.Grass) or surfMat(x, z, h, slope, RM[i][k], CO2[i][k], ST[i][k], PM[i][k])
        local deep = (sm == M.Sand) and M.Sandstone or ((sm == M.Ground or sm == M.Salt) and M.Sandstone or M.Rock)
        local wl = WL[i][k]
        if wl and h < wl - 1 and sm ~= M.Ice then
          local dp = wl - h
          if dp < 5 then sm = M.Sand elseif dp < 30 then sm = M.Mud else sm = M.Basalt end
        end
        for j = 1, ny do
          local yb = yLo + (j - 1) * RES
          local o = (h - yb) / RES
          if o >= 1 then
            mi[j][k] = (h - yb > 14) and deep or sm; oi[j][k] = 1
          elseif o > 0 then
            if wl and yb < wl and o < 0.5 then mi[j][k] = M.Water; oi[j][k] = 1
            else mi[j][k] = sm; oi[j][k] = o end
          elseif wl and yb < wl then
            mi[j][k] = M.Water; oi[j][k] = min(1, (wl - yb) / RES)
          end
        end
      end
    end
  end
  local reg = Region3.new(Vector3.new(cx0, yLo, cz0), Vector3.new(cx1, yHi, cz1)):ExpandToGrid(RES)
  T:WriteVoxels(reg, RES, mats, occ)
  if not (hitMtn or hitTown) and yHi < 360 then
    T:FillBlock(CFrame.new(cx0 + CH / 2, (yHi + 380) / 2, cz0 + CH / 2), Vector3.new(CH, 380 - yHi, CH), M.Air)
  end
end


local PTS = D.opt.pts
local out = {}
local function segsFor(x, z)
  local segs = {}
  for _, s in ipairs(SEGS) do if s.bx1 > x - 140 and s.bx0 < x + 140 and s.bz1 > z - 140 and s.bz0 < z + 140 then table.insert(segs, s) end end
  return segs
end
for _, p in ipairs(PTS) do
  local x, z = p[1], p[2]
  local h, rm, wl, c, st, pm = column(x, z, segsFor(x, z))
  local line = string.format('(%d,%d) h=%.2f water=%s coast=%.3f roadMat=%s', x, z, h, tostring(wl), c, tostring(rm))
  local cells = {}
  local sm = M.Grass
  if wl and h < wl - 1 then
    local dp = wl - h
    sm = (dp < 5) and M.Sand or ((dp < 30) and M.Mud or M.Basalt)
  end
  for j = 1, 24 do
    local yb = -64 + (j - 1) * RES
    local o = (h - yb) / RES
    local tag = '.'
    if o >= 1 then tag = ((h - yb > 14) and 'R' or string.sub(sm.Name, 1, 1))
    elseif o > 0 then
      if wl and yb < wl and o < 0.5 then tag = 'w' else tag = string.sub(sm.Name, 1, 1):lower() .. string.format('%.1f', o) end
    elseif wl and yb < wl then tag = '~' end
    cells[#cells + 1] = yb .. tag
  end
  out[#out + 1] = line
  out[#out + 1] = '   ' .. table.concat(cells, ' ')
end
return table.concat(out, '\n')
