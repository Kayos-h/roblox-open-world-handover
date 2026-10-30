local L = _G.L
local V, CF, A, rad = L.V, L.CF, L.A, math.rad
local P = L.part
local C = L.C
local town = workspace:FindFirstChild('SpawnTown')
local f = L.folder(town, 'Crafts')
local T = workspace.Terrain
local STONE = Color3.fromRGB(150,144,134)
local function road(p1, p2, w, mat)
	local cf = CF((p1+p2)/2, p2)
	T:FillBlock(cf*CF(0,-2,0), V(w, 4, (p2-p1).Magnitude + w*0.5), mat)
end
-- paths
road(V(-150,0,-200), V(-150,0,-300), 12, Enum.Material.Cobblestone)
road(V(-150,0,-300), V(-180,0,-300), 14, Enum.Material.Cobblestone)
road(V(150,0,-170), V(150,0,-250), 12, Enum.Material.Ground)
road(V(150,0,-250), V(215,0,-250), 12, Enum.Material.Ground)
road(V(297,0,58), V(366,0,58), 10, Enum.Material.Cobblestone)
T:FillBlock(CF(220, -2, -290), V(110, 4, 80), Enum.Material.Ground)   -- training yard (packed dirt)
T:FillBlock(CF(372, 0, 64), V(44, 4, 40), Enum.Material.Ground)       -- forge floor

-- ===================== BLACKSMITH =====================
do
	local m = L.model(f, 'Blacksmith')
	local cf = L.at(380, 64, rad(-90))   -- front faces -X (toward the lane)
	L.house(m, cf*CF(0, 0, -8), {w=24, d=16, floors=1, fh=13, stoneGround=true, roof=C.roofSlate, wall=C.plasterD, chimney=false, name='SmithHouse'})
	-- open lean-to workshop in front
	local ws = cf*CF(0, 0, 8)
	P(m, V(26, 0.8, 14), ws*CF(0, 0.4, 0), Color3.fromRGB(110,104,98), L.M.cobble, nil, 'Floor')
	for _, x in ipairs({-12, 0, 12}) do P(m, V(1.4, 11, 1.4), ws*CF(x, 5.5, 6.4), C.beam, L.M.wood, nil, 'Post') end
	P(m, V(27, 1.2, 1.4), ws*CF(0, 11.2, 6.4), C.beam, L.M.wood)
	P(m, V(28, 0.8, 16), ws*CF(0, 13.4, 0)*A(rad(12), 0, 0), Color3.fromRGB(104,72,54), L.M.shingles, nil, 'LeanTo')
	-- forge: brick hearth + hood + chimney
	local fc = ws*CF(-6, 0, -2)
	P(m, V(8, 4, 6), fc*CF(0, 2, 0), Color3.fromRGB(140,90,74), L.M.brick, nil, 'Forge')
	local coals = P(m, V(5, 0.6, 3.6), fc*CF(0, 4.2, 0), Color3.fromRGB(255,110,40), L.M.neon, nil, 'Coals')
	local fi = Instance.new('Fire'); fi.Size = 4; fi.Heat = 7; fi.Color = Color3.fromRGB(255,120,40); fi.SecondaryColor = Color3.fromRGB(255,220,120); fi.Parent = coals
	L.light(coals, Color3.fromRGB(255,140,70), 2, 28, true)
	local sp = Instance.new('ParticleEmitter'); sp.Color = ColorSequence.new(Color3.fromRGB(255,200,100)); sp.LightEmission = 1
	sp.Rate = 12; sp.Lifetime = NumberRange.new(0.5, 1.2); sp.Speed = NumberRange.new(4, 9); sp.SpreadAngle = Vector2.new(30, 30)
	sp.Size = NumberSequence.new(0.25, 0); sp.Acceleration = V(0, -12, 0); sp.Parent = coals
	L.wedge(m, V(8, 4, 6), fc*CF(0, 8.4, 0), Color3.fromRGB(120,80,66), L.M.brick)
	L.chimney(m, fc*CF(0, 6.4, -1.5), 12, true)
	-- anvil on a stump
	local an = ws*CF(3, 0, 0)
	L.cyl(m, 2.6, 3, an*CF(0, 2.1, 0), Color3.fromRGB(110,78,50), L.M.wood)
	P(m, V(3.4, 0.8, 1.4), an*CF(0, 3.8, 0), C.iron, L.M.metal, nil, 'Anvil')
	P(m, V(2, 1, 1), an*CF(0, 4.6, 0), C.iron, L.M.metal)
	L.wedge(m, V(1, 1, 1.4), an*CF(1.9, 4.6, 0)*A(0, rad(-90), 0), C.iron, L.M.metal)
	P(m, V(0.3, 0.3, 2.4), an*CF(-0.8, 5.25, 0)*A(0, rad(30), 0), C.beam, L.M.wood)
	P(m, V(0.8, 0.6, 0.6), an*CF(-0.2, 5.25, 0.9), C.iron, L.M.metal)
	-- quench trough
	local tq = ws*CF(9, 0, -2)
	P(m, V(6, 2.6, 3), tq*CF(0, 2.1, 0), Color3.fromRGB(110,78,50), L.M.planks)
	local wq = P(m, V(5.4, 0.2, 2.4), tq*CF(0, 3.3, 0), Color3.fromRGB(60,110,130), L.M.glass); wq.Transparency = 0.3
	-- grindstone
	local gs = ws*CF(9, 0, 4)
	P(m, V(0.8, 2.6, 0.8), gs*CF(-1.2, 1.3, 0), C.beam, L.M.wood); P(m, V(0.8, 2.6, 0.8), gs*CF(1.2, 1.3, 0), C.beam, L.M.wood)
	P(m, V(1, 4, 4), gs*CF(0, 3.2, 0), Color3.fromRGB(150,140,124), L.M.sandstone, Enum.PartType.Cylinder)
	-- weapon + shield rack
	local wr = ws*CF(-11, 0, 4)
	P(m, V(0.6, 6, 0.6), wr*CF(-2.5, 3, 0), C.beam, L.M.wood); P(m, V(0.6, 6, 0.6), wr*CF(2.5, 3, 0), C.beam, L.M.wood)
	P(m, V(6, 0.5, 0.6), wr*CF(0, 5.4, 0), C.beam, L.M.wood)
	for k = -1, 1 do
		P(m, V(0.4, 5, 0.15), wr*CF(k*1.5, 3, 0.4), Color3.fromRGB(200,200,210), L.M.metal)
		P(m, V(1.5, 0.3, 0.3), wr*CF(k*1.5, 4.6, 0.4), C.gold, L.M.metal)
	end
	for _, x in ipairs({-3.6, 3.6}) do
		P(m, V(0.3, 3, 3), wr*CF(x, 3.6, 0.8)*A(0, rad(90), 0), Color3.fromRGB(140,40,44), L.M.planks, Enum.PartType.Cylinder)
		P(m, V(0.4, 1, 1), wr*CF(x, 3.6, 1)*A(0, rad(90), 0), C.iron, L.M.metal, Enum.PartType.Cylinder)
	end
	-- coal + ore crates, barrels
	L.crate(m, ws*CF(-11, 0.8, -4), 3); L.barrel(m, ws*CF(12, 0.8, -5))
	for k = 0, 5 do L.ball(m, 1, ws*CF(-11 + (k % 3)*0.8, 4.3, -4 + math.floor(k/3)*0.8), Color3.fromRGB(30,28,28), L.M.slate) end
	-- sign: crossed hammer
	local sc = ws*CF(12.6, 10, 7)
	P(m, V(0.4, 0.4, 4), sc*CF(0, 0, 2), C.iron, L.M.metal)
	P(m, V(0.5, 3.4, 3.8), sc*CF(0, -2.4, 2.4), Color3.fromRGB(110,76,48), L.M.planks)
	P(m, V(0.6, 2.6, 0.4), sc*CF(0, -2.4, 2.4)*A(rad(40), 0, 0), C.iron, L.M.metal)
	P(m, V(0.6, 2.6, 0.4), sc*CF(0, -2.4, 2.4)*A(rad(-40), 0, 0), C.iron, L.M.metal)
end

-- ===================== CHAPEL + BELL TOWER =====================
do
	local m = L.model(f, 'Chapel')
	local cf = L.at(-205, -300, rad(90))   -- front faces +X (local +Z)
	local w, d, h = 26, 52, 20
	local WALLC = Color3.fromRGB(196,190,178)
	P(m, V(w + 4, 1.6, d + 4), cf*CF(0, 0.5, 0), STONE, L.M.cobble, nil, 'Foundation')
	-- side walls with buttresses + lancet windows
	for _, sx in ipairs({-1, 1}) do
		P(m, V(2, h, d), cf*CF(sx*(w/2 - 1), 1.3 + h/2, 0), WALLC, L.M.limestone, nil, 'Wall')
		for k = -2, 2 do
			local z = k*10
			P(m, V(3, h*0.75, 3), cf*CF(sx*(w/2 + 0.8), 1.3 + h*0.375, z + 5), STONE, L.M.limestone, nil, 'Buttress')
			L.wedge(m, V(3, 3, 3), cf*CF(sx*(w/2 + 0.8), 1.3 + h*0.75 + 1.5, z + 5)*A(0, sx*rad(-90), 0), STONE, L.M.limestone)
			if k < 2 then
				local wc = cf*CF(sx*(w/2 + 0.12), 1.3 + h*0.45, z)*A(0, sx*rad(90), 0)
				P(m, V(4.4, 10.6, 0.3), wc*CF(0, 0.4, -0.05), STONE, L.M.limestone)
				P(m, V(0.3, 4.4, 4.4), wc*CF(0, 4.6, -0.05)*A(0, rad(90), 0), STONE, L.M.limestone, Enum.PartType.Cylinder)
				local g = P(m, V(3.4, 9, 0.3), wc*CF(0, 0, 0.1), Color3.fromRGB(90,130,200), L.M.glass, nil, 'StainedGlass'); g.Transparency = 0.1
				P(m, V(0.3, 3.4, 3.4), wc*CF(0, 4.5, 0.1)*A(0, rad(90), 0), Color3.fromRGB(200,80,110), L.M.glass, Enum.PartType.Cylinder).Transparency = 0.1
				P(m, V(0.25, 9, 0.35), wc*CF(0, 0, 0.15), STONE, L.M.limestone)
				P(m, V(4.4, 0.8, 1), wc*CF(0, -4.8, 0.3), STONE, L.M.limestone)
			end
		end
	end
	P(m, V(w, h, 2), cf*CF(0, 1.3 + h/2, -d/2 + 1), WALLC, L.M.limestone)
	-- front facade with pointed door and rose window
	P(m, V(w, h, 2), cf*CF(0, 1.3 + h/2, d/2 - 1), WALLC, L.M.limestone, nil, 'Facade')
	L.door(m, cf*CF(0, 1.3, d/2), 7, 12, {lantern = true})
	L.wedge(m, V(9, 3, 1), cf*CF(0, 1.3 + 14.5, d/2 + 0.3), STONE, L.M.limestone)
	local rose = P(m, V(0.4, 8, 8), cf*CF(0, 1.3 + h - 3, d/2 + 0.1)*A(0, rad(90), 0), Color3.fromRGB(150,90,200), L.M.glass, Enum.PartType.Cylinder, 'RoseWindow')
	P(m, V(0.3, 9, 9), cf*CF(0, 1.3 + h - 3, d/2 + 0.05)*A(0, rad(90), 0), STONE, L.M.limestone, Enum.PartType.Cylinder)
	for k = 0, 3 do P(m, V(0.5, 8, 0.4), cf*CF(0, 1.3 + h - 3, d/2 + 0.35)*A(0, 0, rad(k*45)), STONE, L.M.limestone) end
	-- steep slate roof (ridge along local Z)
	L.gableRoof(m, cf*CF(0, 1.3 + h, 0)*A(0, rad(90), 0), d, w, 16, {roof = Color3.fromRGB(78,82,92), wall = WALLC, timber = false, finials = true, overhang = 2})
	-- bell tower at the back-left corner
	local tc = cf*CF(-w/2 - 7, 0, -d/2 + 9)
	local tw, th = 14, 54
	P(m, V(tw, th, tw), tc*CF(0, th/2 + 1, 0), WALLC, L.M.limestone, nil, 'BellTower')
	for _, y in ipairs({18, 36, th}) do P(m, V(tw + 1.4, 1.4, tw + 1.4), tc*CF(0, y, 0), STONE, L.M.limestone) end
	-- belfry openings with a bell
	for _, a in ipairs({0, 90, 180, 270}) do
		local oc = tc*A(0, rad(a), 0)*CF(0, th - 7, tw/2 + 0.05)
		P(m, V(5, 8, 0.4), oc, Color3.fromRGB(26,24,24), L.M.slate)
		L.wedge(m, V(5, 2.4, 0.4), oc*CF(0, 5.2, 0), Color3.fromRGB(26,24,24), L.M.slate)
		local ck = tc*A(0, rad(a), 0)*CF(0, th - 22, tw/2)
		P(m, V(0.4, 6.4, 6.4), ck*CF(0, 0, 0.1)*A(0, rad(90), 0), C.gold, L.M.metal, Enum.PartType.Cylinder)
		P(m, V(0.4, 5.6, 5.6), ck*CF(0, 0, 0.25)*A(0, rad(90), 0), Color3.fromRGB(240,236,226), L.M.marble, Enum.PartType.Cylinder, 'ClockFace')
		P(m, V(0.3, 2.4, 0.2), ck*CF(0, 1, 0.5), Color3.fromRGB(30,30,34), L.M.metal)
		P(m, V(1.8, 0.3, 0.2), ck*CF(0.8, 0, 0.5), Color3.fromRGB(30,30,34), L.M.metal)
	end
	local bell = L.ball(m, 4.6, tc*CF(0, th - 7.5, 0), C.gold, L.M.metal); bell.Name = 'Bell'
	-- spire
	for i = 0, 17 do
		local s = (tw + 1)*(1 - i/18) + 0.4
		P(m, V(s, 1.5, s), tc*CF(0, th + 1.4 + i*1.5, 0), Color3.fromRGB(62,78,118), L.M.slate, nil, 'Spire')
	end
	L.cyl(m, 5, 0.5, tc*CF(0, th + 30, 0), C.iron, L.M.metal)
	L.ball(m, 1.6, tc*CF(0, th + 33, 0), C.gold, L.M.metal)
	-- yard: low wall, yew trees, benches, flowers
	for _, q in ipairs({{-24, 30}, {24, 30}, {-20, -30}, {22, -24}}) do L.tree(m, cf*V(q[1], 0, q[2]), 0.85, 'pine') end
	L.flowers(m, cf*V(-10, 1.3, d/2 + 6), 5, 20); L.flowers(m, cf*V(10, 1.3, d/2 + 6), 5, 20)
	L.bench(m, cf*CF(-22, 0, 12)*A(0, rad(90), 0)); L.bench(m, cf*CF(22, 0, 12)*A(0, rad(-90), 0))
	for _, x in ipairs({-8, 8}) do L.lamp(m, cf*V(x, 0, d/2 + 12)) end
end

-- ===================== KNIGHTS' TRAINING YARD =====================
do
	local m = L.model(f, 'TrainingYard')
	local c = V(220, L.ground(220, -290), -290)
	-- perimeter fence with a gap facing the path
	L.fence(m, c + V(-52, 0, -36), c + V(52, 0, -36))
	L.fence(m, c + V(52, 0, -36), c + V(52, 0, 36))
	L.fence(m, c + V(-52, 0, -36), c + V(-52, 0, 36))
	L.fence(m, c + V(-52, 0, 36), c + V(-78 + 64, 0, 36))
	L.fence(m, c + V(-60 + 64, 0, 36), c + V(52, 0, 36))
	-- training dummies (store models, alternating two styles)
	local DUM = {_G.tpl(92960550414449, 'Training Dummy'), _G.tpl(10140126732, 'Target')}
	for k = 0, 4 do
		local p = c + V(-36 + k*12, 0, -18)
		_G.place(DUM[k % 2 + 1], m, CF(p)*A(0, math.pi, 0), 7.5)
		P(m, V(4, 0.3, 4), CF(p + V(0, 0.15, 0)), Color3.fromRGB(176,150,104), L.M.sand)
	end
	-- archery range: A-frame targets on stands + a shooting line
	local TGT = _G.tpl(11900295788, 'Target')
	-- painted face is the model's Left side; pi/2 turns it toward the shooting line (+Z)
	for k = 0, 2 do _G.place(TGT, m, CF(c + V(-30 + k*14, 0, -31))*A(0, math.pi/2, 0), 7.5) end
	-- store dummies carry Humanoids: hide their floating name tags
	for _, d in ipairs(m:GetDescendants()) do
		if d:IsA('Humanoid') then
			d.DisplayDistanceType = Enum.HumanoidDisplayDistanceType.None
			d.HealthDisplayType = Enum.HumanoidHealthDisplayType.AlwaysOff
		end
	end
	for k = 0, 9 do P(m, V(2.4, 0.2, 0.6), CF(c + V(-34 + k*4, 0.1, -6)), Color3.fromRGB(236,226,196), L.M.smooth) end
	for _, x in ipairs({-36, -8}) do
		local q = c + V(x, 0, -4)
		P(m, V(1, 3, 1), CF(q + V(0, 1.5, 0)), C.beam, L.M.wood)
		L.cyl(m, 2.6, 1.4, CF(q + V(1.6, 1.3, 0)), Color3.fromRGB(120,84,52), L.M.leather)   -- quiver barrel
		for a = 0, 4 do P(m, V(0.12, 3.2, 0.12), CF(q + V(1.6 + (a - 2)*0.22, 3.4, (a % 2)*0.3 - 0.15))*A(0, 0, rad((a - 2)*5)), Color3.fromRGB(200,170,120), L.M.wood) end
	end
	-- sparring ring: raised plank stage with rope posts
	local sr = c + V(-22, 0, 16)
	P(m, V(26, 1.6, 26), CF(sr + V(0, 0.8, 0)), Color3.fromRGB(128,90,56), L.M.planks, nil, 'SparringRing')
	P(m, V(27, 0.6, 27), CF(sr + V(0, 0.3, 0)), STONE, L.M.cobble)
	L.cyl(m, 0.1, 14, CF(sr + V(0, 1.65, 0)), Color3.fromRGB(150,40,48), L.M.fabric)
	L.cyl(m, 0.12, 12.4, CF(sr + V(0, 1.68, 0)), Color3.fromRGB(128,90,56), L.M.planks)
	local cornersR = {}
	for _, sx in ipairs({-1, 1}) do for _, sz in ipairs({-1, 1}) do
		local pp = sr + V(sx*12, 1.6, sz*12)
		P(m, V(1.2, 6, 1.2), CF(pp + V(0, 3, 0)), C.beamDark, L.M.wood)
		L.ball(m, 1.4, CF(pp + V(0, 6.3, 0)), C.gold, L.M.metal)
		table.insert(cornersR, pp)
	end end
	local ord = {1, 2, 4, 3, 1}
	for i = 1, 4 do
		for _, hy in ipairs({2.4, 4.6}) do L.beam(m, cornersR[ord[i]] + V(0, hy, 0), cornersR[ord[i+1]] + V(0, hy, 0), 0.25, Color3.fromRGB(214,190,140), L.M.fabric) end
	end
	for _, sz in ipairs({-1, 1}) do for s = 0, 1 do P(m, V(4, 0.8, 1.4 + s*1.4), CF(sr + V(0, 0.4 + s*0.0, sz*(13.6 + s*0.6))), Color3.fromRGB(110,76,48), L.M.planks) end end
	-- magic practice circle (glowing runes, stone rim, standing runestones)
	local mc = c + V(26, 0.15, 6)
	L.cyl(m, 0.6, 25, CF(mc + V(0, -0.1, 0)), STONE, L.M.cobble)
	L.cyl(m, 0.2, 22, CF(mc + V(0, 0.2, 0)), Color3.fromRGB(46,34,70), L.M.slate)
	local ring = L.cyl(m, 0.25, 20, CF(mc + V(0, 0.25, 0)), Color3.fromRGB(150,90,255), L.M.neon); ring.Transparency = 0.4
	L.cyl(m, 0.3, 17, CF(mc + V(0, 0.3, 0)), Color3.fromRGB(46,34,70), L.M.slate)
	local in2 = L.cyl(m, 0.32, 8, CF(mc + V(0, 0.32, 0)), Color3.fromRGB(150,90,255), L.M.neon); in2.Transparency = 0.5
	L.cyl(m, 0.34, 6.6, CF(mc + V(0, 0.34, 0)), Color3.fromRGB(46,34,70), L.M.slate)
	for k = 0, 7 do
		local a = k/8*math.pi*2
		P(m, V(1.6, 0.35, 0.5), CF(mc + V(math.cos(a)*9.2, 0.32, math.sin(a)*9.2))*A(0, -a, 0), Color3.fromRGB(190,140,255), L.M.neon)
		local sp = mc + V(math.cos(a + 0.39)*13.6, 0, math.sin(a + 0.39)*13.6)
		local st = P(m, V(1.8, 4.4 + (k % 2)*1.6, 1.2), CF(sp + V(0, 2.2 + (k % 2)*0.8, 0))*A(0, -a, rad(4)), Color3.fromRGB(110,104,112), L.M.slate, nil, 'Runestone')
		P(m, V(0.5, 1.8, 0.2), st.CFrame*CF(0, 0.4, -0.62)*A(0, a, 0)*A(0, -a, 0), Color3.fromRGB(190,140,255), L.M.neon)
	end
	local crystal = P(m, V(2, 4, 2), CF(mc + V(0, 4, 0))*A(rad(45), 0, rad(45)), Color3.fromRGB(170,110,255), L.M.neon, nil, 'Crystal')
	crystal.CanCollide = false
	L.light(crystal, Color3.fromRGB(170,110,255), 1.4, 22, false)
	local pe = Instance.new('ParticleEmitter'); pe.Color = ColorSequence.new(Color3.fromRGB(200,150,255)); pe.LightEmission = 1
	pe.Rate = 10; pe.Lifetime = NumberRange.new(2, 3); pe.Speed = NumberRange.new(0.5, 1.5); pe.Size = NumberSequence.new(0.4, 0)
	pe.SpreadAngle = Vector2.new(180, 180); pe.Parent = crystal
	-- viewing stand (bleachers) with a striped canopy on the east side
	for r = 0, 2 do
		P(m, V(4, 1, 30), CF(c + V(44 - r*0, 1 + r*2, 10) + V(r*4, 0, 0)), Color3.fromRGB(128,90,56), L.M.planks, nil, 'Bleacher')
		P(m, V(4, 1 + r*2, 30), CF(c + V(44 + r*4, 0.5 + r, 10)), Color3.fromRGB(96,66,42), L.M.wood)
	end
	for _, z in ipairs({-4, 10, 24}) do
		P(m, V(0.8, 14, 0.8), CF(c + V(42, 7, z)), C.beamDark, L.M.wood)
		P(m, V(0.8, 16, 0.8), CF(c + V(55, 8, z)), C.beamDark, L.M.wood)
	end
	for k = 0, 5 do
		P(m, V(15, 0.4, 5), CF(c + V(48.5, 15, -2.5 + k*5))*A(0, 0, rad(-8)), (k % 2 == 0) and Color3.fromRGB(70,40,120) or Color3.fromRGB(236,226,196), L.M.fabric, nil, 'Canopy')
	end
	-- weapon racks (store models)
	local RK = {_G.tpl(131782675995926, 'Filled weapon rack'), _G.tpl(698770549, 'Weapon Rack')}
	for i, z in ipairs({-6, 4, 18, 28}) do _G.place(RK[i % 2 + 1], m, CF(c + V(-47, 0, z))*A(0, rad(90), 0), 6.6) end
	-- banners on poles, AFK tents/torches/flags
	for _, x in ipairs({-52, 52}) do
		local pp = c + V(x, 0, 36)
		L.cyl(m, 20, 0.8, CF(pp + V(0, 10, 0)), L.C.iron, L.M.metal)
		L.banner(m, CF(pp + V(0, 13, 0.5)), Color3.fromRGB(70,40,120), 9, C.gold)
	end
	local AFK = 121230482146932
	_G.place(_G.tpl(AFK, 'Tent_03'), m, CF(c + V(-30, 0, 48))*A(0, rad(180), 0), 12)
	_G.place(_G.tpl(AFK, 'Tent_01'), m, CF(c + V(30, 0, 48))*A(0, rad(180), 0), 11)
	for _, q in ipairs({{-52, -36}, {52, -36}, {-52, 0}, {52, -16}, {-16, 37}, {6, 37}}) do
		local tm = _G.place(_G.tpl(AFK, 'Torch_01'), m, CF(c + V(q[1], 0, q[2])), 7)
		local _, bb = tm:GetBoundingBox()
		local lp = P(m, V(0.2, 0.2, 0.2), CF(c + V(q[1], 6.6, q[2])), Color3.new(1,1,1), L.M.smooth); lp.Transparency = 1
		L.light(lp, Color3.fromRGB(255,160,80), 1.2, 18)
		local fi = Instance.new('Fire'); fi.Size = 2; fi.Heat = 4; fi.Parent = lp
	end
	for _, q in ipairs({{-52, -18}, {52, 20}, {0, -36}}) do _G.place(_G.tpl(AFK, 'Flag_01'), m, CF(c + V(q[1], 0, q[2])), 14) end
	_G.place(_G.tpl(AFK, 'Crate_01'), m, CF(c + V(-42, 0, 32)), 3.4)
	L.haybale(m, CF(c + V(-46, 0, 40))); L.haybale(m, CF(c + V(-40, 0, 41))); L.haybale(m, CF(c + V(-43, 3.4, 40.5)))
end

local n = 0; for _, d in ipairs(f:GetDescendants()) do if d:IsA('BasePart') then n = n + 1 end end
return 'crafts ok parts=' .. n
