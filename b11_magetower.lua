local L = _G.L
local V, CF, A, rad = L.V, L.CF, L.A, math.rad
local P = L.part
local C = L.C
local town = workspace:FindFirstChild('SpawnTown')
local f = L.folder(town, 'MageTower')
local T = workspace.Terrain
local STONE = Color3.fromRGB(120,118,132)
local STONE2 = Color3.fromRGB(98,96,112)
local TRIM = Color3.fromRGB(196,190,206)
local PURP = Color3.fromRGB(150,90,255)
local ROOF = Color3.fromRGB(74,46,120)

local cx, cz = -260, 360
T:FillBlock(CF(cx, -2, cz), V(64, 4, 64), Enum.Material.Cobblestone)
T:FillBlock(CF(cx + 40, -2, cz), V(30, 4, 14), Enum.Material.Cobblestone)
local g = L.ground(cx, cz)
local base = CF(cx, g, cz)*A(0, rad(90), 0)   -- local +Z faces +X (toward the path)
local m = L.model(f, 'Tower')

-- plinth: stepped round platform
for i = 0, 2 do L.cyl(m, 1, 40 - i*5, base*CF(0, 0.5 + i, 0), (i % 2 == 0) and TRIM or STONE, L.M.limestone) end
local y0 = 3
-- tower shaft: tapered rings with alternating courses
local H = 64
local n = 16
for i = 0, n - 1 do
	local t = i/n
	local dia = 24 - t*6
	L.cyl(m, H/n + 0.05, dia, base*CF(0, y0 + (i + 0.5)*H/n, 0), (i % 3 == 0) and STONE2 or STONE, L.M.slate)
end
-- string courses + buttress ribs
for _, y in ipairs({14, 30, 46}) do
	local dia = 24 - (y/H)*6 + 1.6
	L.cyl(m, 1.2, dia, base*CF(0, y0 + y, 0), TRIM, L.M.limestone)
end
for k = 0, 5 do
	local a = k/6*math.pi*2 + math.pi/6
	local rib = base*A(0, a, 0)
	for s = 0, 7 do
		local y = s*8
		local r = (24 - (y/H)*6)/2
		P(m, V(2, 8.2, 2.2), rib*CF(0, y0 + y + 4, r + 0.2)*A(rad(5), 0, 0), STONE2, L.M.slate)
	end
end
-- door (arched) facing the path
local dcf = base*CF(0, y0, 11.6)
L.door(m, dcf, 6, 10, {lantern = true})
P(m, V(8, 1.2, 1.6), dcf*CF(0, 10.6, 0.2), TRIM, L.M.limestone)
L.wedge(m, V(8, 2.2, 1.6), dcf*CF(0, 12.3, 0.2), TRIM, L.M.limestone)
-- stairs to the door
for s = 0, 2 do P(m, V(10, 1, 2), base*CF(0, 0.5 + s, 21 - s*2), TRIM, L.M.limestone) end
-- glowing slit windows spiralling up
for k = 0, 9 do
	local a = k*0.95
	local y = 12 + k*5
	local r = (24 - (y/H)*6)/2
	local wc = base*A(0, a, 0)*CF(0, y0 + y, r + 0.05)
	P(m, V(2.4, 5, 0.4), wc, Color3.fromRGB(120,70,220), L.M.neon, nil, 'Window')
	P(m, V(3.2, 0.6, 1), wc*CF(0, -2.8, 0.2), TRIM, L.M.limestone)
	L.wedge(m, V(3.2, 1.4, 0.8), wc*CF(0, 3.2, 0.1), TRIM, L.M.limestone)
end
-- observatory crown: overhanging ring with corbels, balcony, glowing band
local top = y0 + H
for k = 0, 15 do
	local a = k/16*math.pi*2
	P(m, V(1.6, 3, 3), base*A(0, a, 0)*CF(0, top - 1.5, 9.5), TRIM, L.M.limestone)
end
L.cyl(m, 1.4, 28, base*CF(0, top + 0.7, 0), STONE2, L.M.slate)
for k = 0, 23 do
	local a = k/24*math.pi*2
	P(m, V(1, 2.4, 1), base*A(0, a, 0)*CF(0, top + 2.6, 13.4), TRIM, L.M.limestone)
end
L.cyl(m, 0.6, 28, base*CF(0, top + 4, 0), TRIM, L.M.limestone).Transparency = 0
-- the 0.6 ring above is a solid cap; carve a walkable ring by making the upper room narrower
L.cyl(m, 12, 20, base*CF(0, top + 10, 0), STONE, L.M.slate)
local band = L.cyl(m, 1.2, 20.4, base*CF(0, top + 12, 0), PURP, L.M.neon); band.Transparency = 0.2
for k = 0, 5 do
	local a = k/6*math.pi*2
	local wc = base*A(0, a, 0)*CF(0, top + 9, 10.05)
	P(m, V(3, 6, 0.4), wc, Color3.fromRGB(120,70,220), L.M.neon)
	P(m, V(4, 7, 0.3), wc*CF(0, 0, -0.1), TRIM, L.M.limestone)
end
-- tall conical roof (fine tiers) + spire
local rt = top + 16
for i = 0, 23 do
	local s = 26*(1 - i/24) + 0.6
	L.cyl(m, 1.25, s, base*CF(0, rt + i*1.2, 0), ROOF, L.M.slate)
end
L.cyl(m, 1, 27, base*CF(0, rt - 0.4, 0), TRIM, L.M.limestone)
L.cyl(m, 8, 0.6, base*CF(0, rt + 31, 0), C.gold, L.M.metal)
local orb = L.ball(m, 2.4, base*CF(0, rt + 36, 0), Color3.fromRGB(200,160,255), L.M.neon); orb.Name = 'SpireOrb'
L.light(orb, PURP, 3, 40, false)
-- moon-and-star finial
P(m, V(0.4, 3, 0.4), base*CF(0, rt + 38.6, 0), C.gold, L.M.metal)

-- ===================== FLOATING CRYSTALS (animated) =====================
local fl = L.model(m, 'Floaters')
local function crystal(par, pos, s, col)
	local c = P(par, V(s, s*2.2, s), CF(pos)*A(0, 0, 0), col, L.M.neon, nil, 'Crystal')
	c.CanCollide = false; c.Transparency = 0.1
	local tip = L.wedge(par, V(s, s*0.8, s*0.5), CF(pos + V(0, s*1.5, -s*0.25)), col, L.M.neon); tip.CanCollide = false
	local tip2 = L.wedge(par, V(s, s*0.8, s*0.5), CF(pos + V(0, s*1.5, s*0.25))*A(0, math.pi, 0), col, L.M.neon); tip2.CanCollide = false
	return c
end
for k = 0, 5 do
	local a = k/6*math.pi*2
	local p = (base*CF(math.cos(a)*19, top - 6 + (k % 2)*5, math.sin(a)*19)).Position
	local c = crystal(fl, p, 2, (k % 2 == 0) and Color3.fromRGB(170,110,255) or Color3.fromRGB(120,200,255))
	if k % 2 == 0 then L.light(c, PURP, 1, 16, false) end
end
-- floating rock chunks around the lower shaft
for k = 0, 3 do
	local a = k/4*math.pi*2 + 0.4
	local p = (base*CF(math.cos(a)*17, y0 + 22 + k*3, math.sin(a)*17)).Position
	local r = P(fl, V(3.6, 2.2, 3), CF(p)*A(0.3, a, 0.2), STONE, L.M.slate, nil, 'FloatRock'); r.CanCollide = false
	local cr = crystal(fl, p + V(0, 1.4, 0), 0.9, Color3.fromRGB(170,110,255))
end
local sc = Instance.new('Script')
sc.Name = 'Orbit'
sc.Source = [[
local fl = script.Parent:WaitForChild('Floaters')
local center = script.Parent:GetAttribute('Center')
local parts, rel = {}, {}
for _, p in ipairs(fl:GetDescendants()) do if p:IsA('BasePart') then table.insert(parts, p); rel[p] = CFrame.new(center):ToObjectSpace(p.CFrame) end end
local t = 0
game:GetService('RunService').Heartbeat:Connect(function(dt)
	t = t + dt
	local spin = CFrame.new(center) * CFrame.Angles(0, t*0.15, 0)
	for i, p in ipairs(parts) do
		p.CFrame = spin * CFrame.new(0, math.sin(t*1.2 + i*0.7)*0.8, 0) * rel[p]
	end
end)
]]
m:SetAttribute('Center', base.Position)
sc.Parent = m

-- ===================== RUNE CIRCLE + GARDEN =====================
do
	local yard = L.model(f, 'ArcaneYard')
	local rc = base*CF(0, 0, 30)
	local rp = rc.Position + V(0, 0.15, 0)
	L.cyl(yard, 0.2, 16, CF(rp), Color3.fromRGB(60,46,90), L.M.slate)
	local r1 = L.cyl(yard, 0.25, 14.4, CF(rp + V(0, 0.05, 0)), PURP, L.M.neon); r1.Transparency = 0.35
	L.cyl(yard, 0.3, 12.4, CF(rp + V(0, 0.1, 0)), Color3.fromRGB(60,46,90), L.M.slate)
	for k = 0, 5 do
		local a = k/6*math.pi*2
		P(yard, V(7, 0.36, 0.35), CF(rp + V(0, 0.12, 0))*A(0, a, 0), Color3.fromRGB(190,140,255), L.M.neon)
	end
	-- standing stones (obelisks) with glowing glyphs
	for k = 0, 5 do
		local a = k/6*math.pi*2 + math.pi/6
		local p = rc*CF(math.cos(a)*13, 0, math.sin(a)*13)
		P(yard, V(2.4, 8, 2.4), p*CF(0, 4, 0)*A(0, a, 0), STONE2, L.M.slate, nil, 'Obelisk')
		L.wedge(yard, V(2.4, 1.6, 1.2), p*CF(0, 8.8, 0.6)*A(0, a + math.pi, 0), STONE2, L.M.slate)
		L.wedge(yard, V(2.4, 1.6, 1.2), p*CF(0, 8.8, -0.6)*A(0, a, 0), STONE2, L.M.slate)
		local gly = P(yard, V(2.5, 1.4, 2.5), p*CF(0, 5.5, 0)*A(0, a, 0), Color3.fromRGB(180,130,255), L.M.neon); gly.Transparency = 0.3
	end
	local pe = Instance.new('ParticleEmitter'); pe.Color = ColorSequence.new(Color3.fromRGB(200,160,255), Color3.fromRGB(120,200,255))
	pe.LightEmission = 1; pe.Rate = 14; pe.Lifetime = NumberRange.new(2, 4); pe.Speed = NumberRange.new(1, 3)
	pe.Size = NumberSequence.new(0.5, 0); pe.SpreadAngle = Vector2.new(20, 20); pe.Parent = r1
	-- blue-flame braziers along the approach
	for _, q in ipairs({{-7, 16}, {7, 16}, {-7, 40}, {7, 40}}) do
		local bp = base*CF(q[1], 0, q[2])
		L.cyl(yard, 4, 1.6, bp*CF(0, 2, 0), STONE2, L.M.slate)
		L.cyl(yard, 1.2, 3, bp*CF(0, 4.6, 0), C.iron, L.M.metal)
		local fp = P(yard, V(1.6, 0.4, 1.6), bp*CF(0, 5.3, 0), Color3.fromRGB(120,180,255), L.M.neon)
		local fi = Instance.new('Fire'); fi.Color = Color3.fromRGB(110,150,255); fi.SecondaryColor = Color3.fromRGB(200,160,255); fi.Size = 3; fi.Heat = 6; fi.Parent = fp
		L.light(fp, Color3.fromRGB(130,160,255), 1.6, 20, false)
	end
	-- garden: hedges, glowing mushrooms, trees, bench
	for _, q in ipairs({{-22, -14}, {22, -14}, {-24, 12}, {24, 12}, {-18, -26}, {18, -26}}) do L.tree(yard, (base*CF(q[1], 0, q[2])).Position, 1.0, (q[2] < 0) and 'pine' or nil) end
	local rng = Random.new(3)
	for k = 1, 18 do
		local a = rng:NextNumber(0, 6.28); local r = rng:NextNumber(15, 26)
		local p = (base*CF(math.cos(a)*r, 0, math.sin(a)*r)).Position
		if (p - rc.Position).Magnitude > 10 then
			local s = rng:NextNumber(0.6, 1.2)
			L.cyl(yard, 1.2*s, 0.4*s, CF(p + V(0, 0.6*s, 0)), Color3.fromRGB(230,226,210), L.M.plastic)
			local cap = L.ball(yard, 1.4*s, CF(p + V(0, 1.2*s, 0)), (k % 2 == 0) and Color3.fromRGB(120,200,255) or Color3.fromRGB(190,130,255), L.M.neon)
			cap.Size = V(1.6*s, 0.8*s, 1.6*s); cap.Shape = Enum.PartType.Ball
		end
	end
	L.flowers(yard, (base*CF(-12, 0, 24)).Position + V(0, 0, 0), 4, 14)
	L.flowers(yard, (base*CF(12, 0, 24)).Position, 4, 14)
	L.bench(yard, base*CF(-14, 0, 30)*A(0, rad(90), 0))
	L.bench(yard, base*CF(14, 0, 30)*A(0, rad(-90), 0))
	-- archway gate at the path entrance with floating glyph
	local ga = base*CF(0, 0, 46)
	for _, x in ipairs({-7, 7}) do
		P(yard, V(2.6, 14, 2.6), ga*CF(x, 7, 0), STONE2, L.M.slate)
		L.ball(yard, 2.4, ga*CF(x, 15, 0), Color3.fromRGB(180,130,255), L.M.neon)
	end
	for k = 0, 8 do
		local t = k/8*math.pi
		P(yard, V(2.4, 1.6, 2.6), ga*CF(-math.cos(t)*7, 13 + math.sin(t)*4, 0)*A(0, 0, t - math.pi/2), STONE, L.M.slate)
	end
end

local cnt = 0; for _, d in ipairs(f:GetDescendants()) do if d:IsA('BasePart') then cnt = cnt + 1 end end
return 'mage ok parts=' .. cnt
