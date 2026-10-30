local L = _G.L
local V, CF, A, rad = L.V, L.CF, L.A, math.rad
local P = L.part
local town = workspace:FindFirstChild('SpawnTown')
local f = L.folder(town, 'Plaza')
local bp = workspace:FindFirstChild('Baseplate'); if bp then bp:Destroy() end
local G = L.ground(0, 0)
local MARBLE = Color3.fromRGB(232,228,218)
local STONE = Color3.fromRGB(160,154,144)
local WATER = Color3.fromRGB(70,150,200)

-- ===== FOUNTAIN =====
local fm = L.model(f, 'Fountain')
local R = 22
local K = 16
-- low stepped platform
L.cyl(fm, 1.2, R*2 + 12, CF(0, G + 0.6, 0), Color3.fromRGB(140,134,126), L.M.cobble)
L.cyl(fm, 1.2, R*2 + 6, CF(0, G + 1.8, 0), STONE, L.M.limestone)
-- basin wall made of K segments with caps
for k = 0, K-1 do
	local a = (k + 0.5)/K*math.pi*2
	local segL = 2*math.pi*R/K + 0.6
	local cf = CF(math.cos(a)*R, G + 4.4, math.sin(a)*R)*A(0, -a + math.pi/2, 0)
	P(fm, V(segL, 4, 2.4), cf, MARBLE, L.M.marble, nil, 'Basin')
	P(fm, V(segL + 0.4, 0.8, 3.4), cf*CF(0, 2.4, 0), Color3.fromRGB(205,198,184), L.M.marble, nil, 'Rim')
end
local w1 = L.cyl(fm, 0.6, R*2 - 1, CF(0, G + 5.2, 0), WATER, L.M.glass); w1.Transparency = 0.35; w1.Name = 'Water'; w1.CanCollide = false
L.cyl(fm, 2.6, R*2 - 1, CF(0, G + 3.6, 0), Color3.fromRGB(60,100,120), L.M.slate)
-- central column with tiered bowls
L.cyl(fm, 10, 6, CF(0, G + 9, 0), MARBLE, L.M.marble)
L.cyl(fm, 1.4, 20, CF(0, G + 12.8, 0), MARBLE, L.M.marble)
L.cyl(fm, 1.6, 22, CF(0, G + 14, 0), Color3.fromRGB(205,198,184), L.M.marble)
local w2 = L.cyl(fm, 0.4, 20, CF(0, G + 14.9, 0), WATER, L.M.glass); w2.Transparency = 0.3; w2.CanCollide = false
L.cyl(fm, 6, 4, CF(0, G + 18, 0), MARBLE, L.M.marble)
L.cyl(fm, 1.2, 11, CF(0, G + 21.2, 0), Color3.fromRGB(205,198,184), L.M.marble)
local w3 = L.cyl(fm, 0.3, 9.6, CF(0, G + 21.9, 0), WATER, L.M.glass); w3.Transparency = 0.3; w3.CanCollide = false
-- cascading water curtains (particles) from each bowl
local function spray(pos, rate, speed, spread, size)
	local e = P(fm, V(1,1,1), CF(pos), Color3.new(), L.M.smooth, nil, 'Spray'); e.Transparency = 1; e.CanCollide = false
	local pe = Instance.new('ParticleEmitter')
	pe.Color = ColorSequence.new(Color3.fromRGB(200,235,255)); pe.LightEmission = 0.3
	pe.Rate = rate; pe.Lifetime = NumberRange.new(1, 1.6); pe.Speed = NumberRange.new(speed, speed*1.3)
	pe.SpreadAngle = Vector2.new(spread, spread); pe.Acceleration = V(0, -30, 0)
	pe.Size = NumberSequence.new({NumberSequenceKeypoint.new(0, size), NumberSequenceKeypoint.new(1, size*1.8)})
	pe.Transparency = NumberSequence.new({NumberSequenceKeypoint.new(0, 0.35), NumberSequenceKeypoint.new(1, 1)})
	pe.EmissionDirection = Enum.NormalId.Top; pe.Parent = e
end
spray(V(0, G + 15.2, 0), 60, 6, 80, 0.7)
spray(V(0, G + 22.2, 0), 40, 5, 70, 0.6)
-- four lion-less spouts: stone fish heads around the basin pouring inward
for k = 0, 3 do
	local a = k*math.pi/2 + math.pi/4
	local p = V(math.cos(a)*(R - 3), G + 5.6, math.sin(a)*(R - 3))
	P(fm, V(3, 3, 3), CF(p)*A(0, -a, 0), STONE, L.M.limestone, nil, 'Spout')
	spray(p - V(math.cos(a), 0, math.sin(a))*1.6, 25, 8, 6, 0.5)
end
-- ===== STATUE: robed mage knight raising a grimoire (original design) =====
local sm = L.model(fm, 'Statue')
local sb = G + 24.4
local SC = Color3.fromRGB(214,208,196)
L.cyl(sm, 2, 7, CF(0, sb - 1, 0), Color3.fromRGB(190,184,172), L.M.marble)
-- robe (tapered stack)
for i = 0, 5 do L.cyl(sm, 1.6, 5.4 - i*0.45, CF(0, sb + 0.8 + i*1.5, 0), SC, L.M.marble) end
-- torso + cape
P(sm, V(3.6, 4, 2.4), CF(0, sb + 11, 0), SC, L.M.marble, nil, 'Torso')
P(sm, V(4, 9, 0.6), CF(0, sb + 7.6, -1.5)*A(rad(8), 0, 0), Color3.fromRGB(200,194,182), L.M.marble, nil, 'Cape')
-- shoulder pauldrons
L.ball(sm, 2.2, CF(-2.2, sb + 12.6, 0), SC, L.M.marble); L.ball(sm, 2.2, CF(2.2, sb + 12.6, 0), SC, L.M.marble)
-- head + hood
L.ball(sm, 2.4, CF(0, sb + 14.4, 0), SC, L.M.marble)
-- raised right arm with open book
L.beam(sm, V(2.4, sb + 12.4, 0), V(3.4, sb + 16.4, 0.6), 1.1, SC, L.M.marble)
local book = CF(3.6, sb + 17.4, 0.8)*A(rad(-20), 0, rad(-10))
P(sm, V(1.4, 0.3, 2), book*CF(-0.7, 0, 0)*A(0, 0, rad(12)), SC, L.M.marble)
P(sm, V(1.4, 0.3, 2), book*CF(0.7, 0, 0)*A(0, 0, rad(-12)), SC, L.M.marble)
-- left arm holds a sword point-down
L.beam(sm, V(-2.4, sb + 12.4, 0), V(-2.6, sb + 9, 1.2), 1.1, SC, L.M.marble)
P(sm, V(0.5, 7, 0.2), CF(-2.6, sb + 5.6, 1.4), SC, L.M.marble, nil, 'Blade')
P(sm, V(2.4, 0.4, 0.4), CF(-2.6, sb + 9.2, 1.4), SC, L.M.marble)
-- floating glowing grimoire glyph above the book
local glyph = P(sm, V(0.2, 2.6, 2.6), CF(3.8, sb + 21, 1)*A(0, rad(90), 0), Color3.fromRGB(120,255,170), L.M.neon, Enum.PartType.Cylinder, 'Glyph')
glyph.Transparency = 0.2; glyph.CanCollide = false
L.light(glyph, Color3.fromRGB(140,255,180), 1.2, 18, false)
local gpe = Instance.new('ParticleEmitter'); gpe.Color = ColorSequence.new(Color3.fromRGB(160,255,190)); gpe.LightEmission = 1
gpe.Rate = 8; gpe.Lifetime = NumberRange.new(1.5, 2.5); gpe.Speed = NumberRange.new(0.5, 1.5); gpe.Size = NumberSequence.new(0.5, 0)
gpe.SpreadAngle = Vector2.new(180, 180); gpe.Parent = glyph
-- scale the whole fountain + statue up 1.5x about its ground centre (user: "make the fountain bigger")
local FS = 1.5
fm.WorldPivot = CF(0, G, 0)
fm:ScaleTo(FS)
local RF = R*FS

-- ===== PAVING DETAIL: radial inlay ring + compass star =====
local inlay = L.model(f, 'Inlay')
for k = 0, 47 do
	local a = k/48*math.pi*2
	P(inlay, V(6.6, 0.2, 2.4), CF(math.cos(a)*47, G + 0.1, math.sin(a)*47)*A(0, -a + math.pi/2, 0), (k % 2 == 0) and Color3.fromRGB(196,186,166) or Color3.fromRGB(120,110,100), L.M.limestone)
end
for k = 0, 7 do
	local a = k*math.pi/4
	local len = (k % 2 == 0) and 12 or 7
	P(inlay, V(2.2, 0.2, len), CF(math.cos(a)*(RF + 16 + len/2), G + 0.1, math.sin(a)*(RF + 16 + len/2))*A(0, -a + math.pi/2, 0)*A(0, rad(90), 0), Color3.fromRGB(176,150,96), L.M.limestone)
end

-- ===== BENCHES, PLANTERS, LAMPS =====
local furn = L.model(f, 'Furniture')
for k = 0, 7 do
	local a = (k + 0.5)/8*math.pi*2
	local p = V(math.cos(a)*54, G, math.sin(a)*54)
	-- bench faces the fountain; 1.5x bigger to match the larger fountain
	local b = L.bench(furn, CF(p, V(0, G, 0))*A(0, math.pi, 0))
	b.WorldPivot = CF(p)
	b:ScaleTo(1.5)
end
local function planter(pos, r)
	local m = L.model(f, 'Planter')
	local KK = 10
	for k = 0, KK-1 do
		local a = (k + 0.5)/KK*math.pi*2
		P(m, V(2*math.pi*r/KK + 0.5, 2.2, 1.4), CF(pos + V(math.cos(a)*r, 1.1, math.sin(a)*r))*A(0, -a + math.pi/2, 0), STONE, L.M.limestone)
	end
	L.cyl(m, 1.8, r*2 - 1, CF(pos + V(0, 1, 0)), Color3.fromRGB(80,58,40), L.M.ground)
	L.tree(m, pos + V(0, 1.6, 0), 0.75)
	L.flowers(m, pos + V(0, 1.8, 0), r - 2, 22)
	return m
end
for k = 0, 3 do
	local a = k*math.pi/2 + math.pi/4
	planter(V(math.cos(a)*61, G, math.sin(a)*61), 7)
end
for k = 0, 11 do
	local a = (k + 0.5)/12*math.pi*2
	if math.abs(math.sin(a*2)) > 0.2 then
		L.lamp(furn, V(math.cos(a)*70, G, math.sin(a)*70))
	end
end
-- ===== BANNER POLES at each road mouth =====
local function pole(pos, color)
	local m = L.model(f, 'BannerPole')
	P(m, V(3, 1.6, 3), CF(pos + V(0, 0.8, 0)), STONE, L.M.limestone)
	L.cyl(m, 30, 1, CF(pos + V(0, 16, 0)), L.C.iron, L.M.metal)
	L.ball(m, 1.8, CF(pos + V(0, 31.4, 0)), L.C.gold, L.M.metal)
	L.banner(m, CF(pos + V(0, 22, 0.5)), color, 12, L.C.gold)
	return m
end
for _, d in ipairs({{0,1},{0,-1},{1,0},{-1,0}}) do
	for _, s in ipairs({-1, 1}) do
		local side = V(d[2], 0, d[1])*s*20
		local p = V(d[1]*80, G, d[2]*80) + side
		pole(p, (s > 0) and Color3.fromRGB(70,40,120) or Color3.fromRGB(150,40,48))
	end
end

-- ===== SPAWN =====
local sp = Instance.new('SpawnLocation')
sp.Name = 'TownSpawn'; sp.Anchored = true; sp.Size = V(12, 1, 12); sp.CFrame = CF(0, G + 0.4, 63)
sp.Material = L.M.marble; sp.Color = Color3.fromRGB(206,196,176); sp.Neutral = true; sp.Duration = 0
sp.TopSurface = Enum.SurfaceType.Smooth
for _, c in ipairs(sp:GetChildren()) do if c:IsA('Decal') then c:Destroy() end end
sp.Parent = f
for _, o in ipairs(workspace:GetChildren()) do
	if o:IsA('SpawnLocation') and o ~= sp then o:Destroy() end
end

local n = 0; for _, d in ipairs(f:GetDescendants()) do if d:IsA('BasePart') then n = n + 1 end end
return string.format('plaza ok parts=%d G=%.2f', n, G)
