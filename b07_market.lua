local L = _G.L
local V, CF, A, rad = L.V, L.CF, L.A, math.rad
local P = L.part
local C = L.C
local town = workspace:FindFirstChild('SpawnTown')
local f = L.folder(town, 'Market')
local ts = workspace:FindFirstChild('TEST_Show'); if ts then ts:Destroy() end
local T = workspace.Terrain
local rng = Random.new(77)

-- market squares (paved): material-only swap so heights stay flush with the roads
for _, zc in ipairs({0}) do
	local r = Region3.new(V(222 - 56, -8, zc - 102), V(222 + 56, 4, zc + 102)):ExpandToGrid(4)
	for _, m in ipairs({Enum.Material.Grass, Enum.Material.LeafyGrass, Enum.Material.Ground, Enum.Material.Mud}) do
		T:ReplaceMaterial(r, 4, m, Enum.Material.Cobblestone)
	end
end

local function sign(parent, cf, color, icon)
	-- iron bracket + hanging board with a simple painted icon. cf = attach point on wall face (+Z outward)
	P(parent, V(0.4, 0.4, 5), cf*CF(0, 0, 2.5), C.iron, L.M.metal)
	L.beam(parent, cf*V(0, -2, 0.2), cf*V(0, 0, 3.4), 0.3, C.iron, L.M.metal)
	for _, z in ipairs({1.2, 4.2}) do P(parent, V(0.15, 1, 0.15), cf*CF(0, -0.5, z), C.iron, L.M.metal) end
	local b = P(parent, V(0.5, 3.4, 4), cf*CF(0, -2.7, 2.7), color, L.M.planks, nil, 'Sign')
	P(parent, V(0.6, 3.8, 0.4), cf*CF(0, -2.7, 0.6), C.beamDark, L.M.wood); P(parent, V(0.6, 3.8, 0.4), cf*CF(0, -2.7, 4.8), C.beamDark, L.M.wood)
	if icon == 'bread' then
		for _, sx in ipairs({-1, 1}) do L.ball(parent, 1.6, cf*CF(sx*0.3, -2.7, 2.7), Color3.fromRGB(214,160,80), L.M.smooth) end
	elseif icon == 'potion' then
		for _, sx in ipairs({-1, 1}) do
			L.ball(parent, 1.6, cf*CF(sx*0.3, -3.1, 2.7), Color3.fromRGB(120,80,220), L.M.neon)
			P(parent, V(0.7, 0.9, 0.5), cf*CF(sx*0.3, -2, 2.7), Color3.fromRGB(200,200,210), L.M.glass)
		end
	elseif icon == 'cloth' then
		for _, sx in ipairs({-1, 1}) do P(parent, V(0.2, 2, 2.6), cf*CF(sx*0.3, -2.7, 2.7)*A(rad(15), 0, 0), Color3.fromRGB(200,60,70), L.M.fabric) end
	else
		for _, sx in ipairs({-1, 1}) do P(parent, V(0.2, 0.6, 2.6), cf*CF(sx*0.3, -2.7, 2.7), C.gold, L.M.metal) end
	end
	return b
end

local function awning(parent, cf, w, color)
	-- canvas door awning, cf = top-centre on wall face
	local st = 6
	for i = 1, st do
		local x = -w/2 + (i - 0.5)*(w/st)
		P(parent, V(w/st, 0.25, 4.6), cf*CF(x, -1, 2.1)*A(rad(24), 0, 0), (i % 2 == 0) and Color3.fromRGB(245,238,225) or color, L.M.fabric)
	end
	for _, sx in ipairs({-1, 1}) do L.beam(parent, cf*V(sx*w/2, -4.6, 0), cf*V(sx*w/2, -2, 4.2), 0.3, C.iron, L.M.metal) end
end

local walls = {C.plasterA, C.plasterB, C.plasterC, Color3.fromRGB(232,214,190)}
local roofs = {C.roofRed, C.roofOrange, C.roofBrown, C.roofBlue, C.roofGreen}
local aw = {Color3.fromRGB(180,50,50), Color3.fromRGB(50,110,170), Color3.fromRGB(60,140,80), Color3.fromRGB(200,150,40), Color3.fromRGB(130,60,150)}
local icons = {'bread', 'potion', 'cloth', 'coin'}
local function shop(x, z, yaw, o, i)
	local cf = L.at(x, z, rad(yaw))
	o.wall = o.wall or walls[(i % #walls) + 1]
	o.roof = o.roof or roofs[(i % #roofs) + 1]
	o.stoneGround = true
	o.lit = true
	local h = L.house(f, cf, o)
	local d = o.d or 18
	local w = o.w or 24
	sign(h, cf*CF(w/2 - 2, (o.fh or 11) + 0.5, d/2)*A(0, rad(90), 0)*A(0, rad(-90), 0), Color3.fromRGB(110,76,48), icons[(i % #icons) + 1])
	awning(h, cf*CF(0, 1.6 + 11, d/2 + 0.6), 12, aw[(i % #aw) + 1])
	-- goods outside
	L.barrel(h, cf*CF(-w/2 + 2, 1.3, d/2 + 3))
	L.crate(h, cf*CF(-w/2 + 5.5, 1.3, d/2 + 3), 3)
	return h
end

local i = 0
local function S(x, z, yaw, o) i = i + 1; return shop(x, z, yaw, o, i) end
-- spine west side, facing the spine (+X)
S(124, -62, 90, {w=24, d=18, floors=2, jetty=true, name='Shop_Bakery'})
S(124, 62, 90, {w=24, d=18, floors=2, name='Shop_Tailor'})
-- lane x=290 east side, facing -X
S(316, -72, -90, {w=22, d=18, floors=2, flowers=true, name='Shop_Apothecary'})
S(316, -32, -90, {w=20, d=16, floors=2, fh=10, name='Shop_Jeweller'})
S(316, 36, -90, {w=24, d=18, floors=3, fh=10, jetty=true, name='Shop_General'})
S(316, 78, -90, {w=20, d=16, floors=2, name='Shop_Candles'})
-- street z=-110 north side (faces +Z) and z=110 south side (faces -Z)
S(200, -136, 0, {w=26, d=18, floors=2, jetty=true, name='Shop_Cartographer'})
S(262, -136, 0, {w=22, d=18, floors=2, flowers=true, name='Shop_Herbalist'})
S(200, 136, 180, {w=24, d=18, floors=2, name='Shop_Cobbler'})
S(262, 136, 180, {w=26, d=20, floors=3, fh=10, jetty=true, ridgeZ=true, name='Shop_Bookbinder'})

-- ===== MARKET HALL (open timber hall on stone columns) =====
do
	local m = L.model(f, 'MarketHall')
	local cf = L.at(222, -60, 0)
	local w, d, h = 48, 28, 12
	P(m, V(w + 4, 1.2, d + 4), cf*CF(0, 0.6, 0), Color3.fromRGB(150,144,134), L.M.limestone, nil, 'Floor')
	for ix = -3, 3 do for _, sz in ipairs({-1, 1}) do
		local p = cf*CF(ix*(w/6), 0, sz*d/2)
		L.cyl(m, h, 2.6, p*CF(0, h/2 + 1.2, 0), Color3.fromRGB(170,164,154), L.M.limestone)
		P(m, V(3.4, 1.2, 3.4), p*CF(0, 1.8, 0), Color3.fromRGB(140,134,126), L.M.limestone)
		P(m, V(3.4, 1, 3.4), p*CF(0, h + 0.8, 0), Color3.fromRGB(140,134,126), L.M.limestone)
	end end
	-- timber beam ring
	for _, sz in ipairs({-1, 1}) do P(m, V(w + 2, 1.6, 1.6), cf*CF(0, h + 2, sz*d/2), C.beam, L.M.wood) end
	for _, sx in ipairs({-1, 1}) do P(m, V(1.6, 1.6, d + 2), cf*CF(sx*w/2, h + 2, 0), C.beam, L.M.wood) end
	for ix = -2, 2 do P(m, V(1, 1, d), cf*CF(ix*(w/6), h + 2.4, 0), C.beam, L.M.wood) end
	L.gableRoof(m, cf*CF(0, h + 2.8, 0), w + 2, d + 2, 9, {roof = Color3.fromRGB(150,62,48), wall = C.plasterA, finials = true, overhang = 3})
	-- cupola with bell lantern
	P(m, V(6, 5, 6), cf*CF(0, h + 13.6, 0), C.plasterA, L.M.plaster)
	L.gableRoof(m, cf*CF(0, h + 16.1, 0), 6, 6, 3, {roof = Color3.fromRGB(62,84,124), wall = C.plasterA, overhang = 1, timber = false})
	-- hall tables with goods
	for ix = -1, 1 do
		local tc = cf*CF(ix*14, 1.2, 0)
		P(m, V(10, 0.6, 5), tc*CF(0, 3, 0), Color3.fromRGB(140,98,62), L.M.planks)
		for _, q in ipairs({{-4.4,-2},{4.4,-2},{-4.4,2},{4.4,2}}) do P(m, V(0.6, 3, 0.6), tc*CF(q[1], 1.5, q[2]), C.beamDark, L.M.wood) end
		local kinds = {{'apples', 'bread'}, {'cheese', 'veg'}, {'potions', 'pottery'}}
		for k = 0, 1 do
			L.goods(m, tc*CF(-2.5 + k*5, 3.3, 0), kinds[ix + 2][k + 1])
		end
		L.crate(m, tc*CF(0, 0, 4.4), 2.6)
	end
	-- lanterns hanging from the beams
	for _, x in ipairs({-16, 0, 16}) do
		local g = P(m, V(1.2, 1.6, 1.2), cf*CF(x, h - 0.6, 0), Color3.fromRGB(255,206,130), L.M.neon, nil, 'Glow')
		P(m, V(0.2, 3, 0.2), cf*CF(x, h + 1, 0), C.iron, L.M.metal)
		L.light(g, Color3.fromRGB(255,196,128), 1.2, 22, false)
	end
end

-- ===== stalls around the market hall (north square only) =====
local stalls = L.model(f, 'Stalls')
for _, x in ipairs({180, 264}) do
	L.stall(stalls, L.at(x, -88, 0), aw[(x % 5) + 1])
	L.stall(stalls, L.at(x, -32, math.pi), aw[((x + 2) % 5) + 1])
end

-- ===== GRAND EMPORIUM (south square): big 3-storey shop with an arcaded, goods-filled front =====
do
	local cf = L.at(222, 66, math.pi)          -- front faces -Z (toward the east road and market hall)
	local w, d = 60, 34
	local em = L.house(f, cf, {w = w, d = d, floors = 3, fh = 11, jetty = true, stoneGround = true, lit = true,
		roof = C.roofBlue, wall = C.plasterC, shutter = C.shutterRed, chimney = true, finials = true, name = 'GrandEmporium'})
	-- corner turrets with cone roofs
	for _, sx in ipairs({-1, 1}) do
		local tp = cf*CF(sx*(w/2 + 4.6), 0, d/2 - 2)
		L.cyl(em, 40, 9, tp*CF(0, 20, 0), C.stoneLight, L.M.limestone)
		L.cyl(em, 1.2, 10.4, tp*CF(0, 40.6, 0), C.stone, L.M.limestone)
		for t = 0, 9 do L.cyl(em, 1.6, 11 - t*1.1, tp*CF(0, 42 + t*1.5, 0), C.roofBlue, L.M.slate) end
		L.cyl(em, 6, 0.4, tp*CF(0, 59, 0), C.iron, L.M.metal)
		L.ball(em, 1.2, tp*CF(0, 62, 0), C.gold, L.M.metal)
		for _, y in ipairs({14, 25}) do L.window(em, tp*CF(0, y, 4.6), 2.6, 4.4, {shutters = false, lit = true}) end
	end
	-- arcade: stone columns + slate lean-to roof in front of the ground floor
	local ar = cf*CF(0, 0, d/2 + 7)
	P(em, V(w + 4, 1, 14), ar*CF(0, 0.5, 0), Color3.fromRGB(150,144,134), L.M.limestone, nil, 'ArcadeFloor')
	for k = -3, 3 do
		local c = ar*CF(k*(w/6), 0, 5.6)
		P(em, V(2.4, 1, 2.4), c*CF(0, 1.5, 0), C.stone, L.M.limestone)
		L.cyl(em, 9, 1.6, c*CF(0, 6.5, 0), C.stoneLight, L.M.limestone)
		P(em, V(2.4, 1, 2.4), c*CF(0, 11.5, 0), C.stone, L.M.limestone)
	end
	P(em, V(w + 2, 1.4, 1.4), ar*CF(0, 12.1, 5.6), C.beam, L.M.wood)
	P(em, V(w + 4, 0.6, 15), ar*CF(0, 13.9, 0)*A(rad(8), 0, 0), C.roofSlate, L.M.slate, nil, 'ArcadeRoof')
	-- display tables full of goods under the arcade
	local kinds = {'apples', 'bread', 'cheese', 'potions', 'cloth', 'pottery', 'veg', 'fish', 'oranges', 'potions', 'cloth', 'bread'}
	local q = 0
	for k = -3, 2 do
		local tc = ar*CF((k + 0.5)*(w/6), 1, 0.5)
		P(em, V(8, 0.5, 4), tc*CF(0, 3, 0), Color3.fromRGB(140,98,62), L.M.planks, nil, 'Table')
		for _, qx in ipairs({-3.5, 3.5}) do P(em, V(0.6, 3, 3.4), tc*CF(qx, 1.5, 0), C.beamDark, L.M.wood) end
		for s = 0, 1 do q = q + 1; L.goods(em, tc*CF(-2 + s*4, 3.25, 0), kinds[q]) end
	end
	-- big gilded shop sign over the arcade + hanging lanterns
	local sg = ar*CF(0, 15.6, 7.6)
	for _, sx in ipairs({-9, 9}) do P(em, V(0.5, 2.6, 0.5), sg*CF(sx, -2.6, -0.2), C.iron, L.M.metal) end
	P(em, V(22, 4.4, 0.6), sg, Color3.fromRGB(70,40,30), L.M.planks, nil, 'EmporiumSign')
	P(em, V(22.8, 0.5, 0.8), sg*CF(0, 2.3, 0), C.gold, L.M.metal); P(em, V(22.8, 0.5, 0.8), sg*CF(0, -2.3, 0), C.gold, L.M.metal)
	-- (no ornament dots: they covered the lettering)
	-- painted lettering on the sign board
	local sgp = em:FindFirstChild('EmporiumSign')
	local gui = Instance.new('SurfaceGui'); gui.Face = Enum.NormalId.Back; gui.SizingMode = Enum.SurfaceGuiSizingMode.PixelsPerStud; gui.PixelsPerStud = 40
	gui.LightInfluence = 1; gui.Parent = sgp
	local tl = Instance.new('TextLabel'); tl.Size = UDim2.fromScale(1, 1); tl.BackgroundTransparency = 1
	tl.Text = 'GRAND EMPORIUM'; tl.Font = Enum.Font.Fantasy; tl.TextScaled = true; tl.TextColor3 = C.gold
	tl.TextStrokeTransparency = 0.4; tl.TextStrokeColor3 = Color3.fromRGB(40,20,10); tl.Parent = gui
	local pad = Instance.new('UIPadding'); pad.PaddingLeft = UDim.new(0.06, 0); pad.PaddingRight = UDim.new(0.06, 0); pad.PaddingTop = UDim.new(0.2, 0); pad.PaddingBottom = UDim.new(0.2, 0); pad.Parent = tl
	for k = -2, 2 do
		local lp = ar*CF(k*(w/5), 11.2, 5.6)
		P(em, V(0.2, 1.4, 0.2), lp*CF(0, -0.7, 0), C.iron, L.M.metal)
		P(em, V(1.1, 0.3, 1.1), lp*CF(0, -1.45, 0), C.iron, L.M.metal)
		local g = P(em, V(0.7, 1, 0.7), lp*CF(0, -2.1, 0), Color3.fromRGB(255,160,80), L.M.neon, nil, 'Glow')
		g.CanCollide = false
		P(em, V(1, 0.3, 1), lp*CF(0, -2.75, 0), C.iron, L.M.metal)
		L.light(g, Color3.fromRGB(255,180,110), 0.8, 18, false)
	end
	-- stacked stock beside the building
	for n2 = 0, 3 do L.crate(f, cf*CF(w/2 + 9, 1.3 + (n2 % 2)*3.4, -6 + math.floor(n2/2)*4), 3.4) end
	L.barrel(f, cf*CF(-w/2 - 9, 1.3, -4)); L.barrel(f, cf*CF(-w/2 - 9, 1.3, 0)); L.barrel(f, cf*CF(-w/2 - 9, 6.3, -2))
end
-- festival tents (store models) flanking the emporium plaza
do
	local afk = _G.loadAsset(121230482146932):GetChildren()[1]
	_G.place(afk:FindFirstChild('Tent_01'), f, L.at(176, 27, rad(20)), 11).Name = 'TentL'
	_G.place(afk:FindFirstChild('Tent_02'), f, L.at(268, 27, rad(-20)), 11).Name = 'TentR'
end
-- clutter: carts, crates, barrels, sacks
local cl = L.model(f, 'Clutter')
local function sack(cf)
	local s = L.ball(cl, 2.6, cf*CF(0, 1.1, 0), Color3.fromRGB(196,170,120), L.M.fabric)
	P(cl, V(1, 0.6, 1), cf*CF(0, 2.4, 0), Color3.fromRGB(160,130,90), L.M.fabric)
end
L.cart(cl, L.at(172, 8, rad(-70)), 'goods')
L.cart(cl, L.at(278, -12, rad(110)), 'hay')
L.cart(cl, L.at(240, 104, rad(15)), 'goods')
for n = 1, 22 do
	local x = rng:NextNumber(170, 276); local z = rng:NextNumber(-98, -20)
	if math.abs(x - 222) > 30 or math.abs(z + 60) > 20 then
		local r = rng:NextNumber()
		local cf = L.at(x, z, rng:NextNumber(0, 6))
		if r < 0.35 then L.barrel(cl, cf) elseif r < 0.7 then L.crate(cl, cf, rng:NextNumber(2.6, 4)) else sack(cf) end
	end
end
-- lamps around the squares
for _, p in ipairs({{168,-98},{276,-98},{168,-22},{276,-22},{168,22},{276,22},{168,98},{276,98}}) do
	L.lamp(cl, V(p[1], L.ground(p[1], p[2]), p[2]))
end
-- (south-square bunting removed: the Grand Emporium now stands there)
for _, z in ipairs({}) do
	local a, b = V(166, 0, z), V(278, 0, z)
	local ya, yb = L.ground(a.X, a.Z) + 14, L.ground(b.X, b.Z) + 14
	P(cl, V(0.8, 14, 0.8), CF(a.X, ya - 7, a.Z), C.beam, L.M.wood); P(cl, V(0.8, 14, 0.8), CF(b.X, yb - 7, b.Z), C.beam, L.M.wood)
	local N = 24
	for q = 0, N - 1 do
		local t = (q + 0.5)/N
		local sag = 3*math.sin(t*math.pi)
		local p = V(a.X + (b.X - a.X)*t, ya - sag - 0.6, z)
		local flag = L.wedge(cl, V(0.1, 1.6, 1.6), CF(p)*A(0, rad(90), 0)*A(math.pi, 0, 0), aw[(q % #aw) + 1], L.M.fabric)
		flag.CanCollide = false
	end
	L.beam(cl, V(a.X, ya, z), V(222, ya - 3, z), 0.1, C.iron, L.M.metal)
	L.beam(cl, V(222, ya - 3, z), V(b.X, yb, z), 0.1, C.iron, L.M.metal)
end

-- ===== WAREHOUSE (big stone + timber, facing the lane) =====
do
	local cf = L.at(372, -40, rad(-90))
	local wh = L.house(f, cf, {w=46, d=28, floors=2, fh=12, stoneGround=true, roof=C.roofSlate, wall=C.plasterD, shutter=C.shutterRed, chimney=false, name='Warehouse'})
	-- big double cargo doors + hoist beam
	P(wh, V(12, 12, 0.8), cf*CF(0, 7.4, 14.4), Color3.fromRGB(96,62,38), L.M.planks, nil, 'CargoDoor')
	for _, y in ipairs({4, 10}) do P(wh, V(12.4, 0.8, 1), cf*CF(0, y, 14.8), C.iron, L.M.metal) end
	P(wh, V(1.2, 1.2, 8), cf*CF(0, 25.5, 17), C.beamDark, L.M.wood)
	L.beam(wh, cf*V(0, 25, 20.6), cf*V(0, 16, 20.6), 0.15, Color3.fromRGB(200,190,160), L.M.fabric)
	L.crate(wh, cf*CF(0, 13.6, 20.6), 2.8)
	for n = 0, 4 do L.crate(f, cf*CF(-18 + n*4.5, 1.3, 18), 3.6) end
	L.barrel(f, cf*CF(14, 1.3, 18)); L.barrel(f, cf*CF(18, 1.3, 18)); L.barrel(f, cf*CF(16, 6.3, 18))
	L.cart(f, cf*CF(-8, 1.3, 30)*A(0, rad(80), 0), 'goods')
end

local n = 0; for _, d in ipairs(f:GetDescendants()) do if d:IsA('BasePart') then n = n + 1 end end
return 'market ok parts=' .. n
