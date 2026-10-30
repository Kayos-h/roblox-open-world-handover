local L = _G.L
local V, CF, A, rad = L.V, L.CF, L.A, math.rad
local P = L.part
local C = L.C
local town = workspace:FindFirstChild('SpawnTown')
local f = L.folder(town, 'Landmarks')
local rng = Random.new(99)
local STONE = Color3.fromRGB(150,144,134)

-- ===================== TAVERN =====================
do
	local cf = L.at(110, -38, 0)
	local m = L.house(f, cf, {w=38, d=26, floors=3, fh=11, jetty=true, stoneGround=true, flowers=true, lit=true,
		roof=Color3.fromRGB(150,62,48), wall=C.plasterA, shutter=C.shutterGreen, finials=true, name='Tavern'})
	-- side wing (lower, perpendicular)
	L.house(m, cf*CF(-26, 0, -4)*A(0, rad(90), 0), {w=18, d=14, floors=2, fh=10, roof=Color3.fromRGB(104,72,54), wall=C.plasterB, shutter=C.shutterGreen, chimney=true, name='TavernWing'})
	-- big hanging sign: tankard
	local sc = cf*CF(10, 13.6, 13)
	P(m, V(0.5, 0.5, 7), sc*CF(0, 0, 3.5), C.iron, L.M.metal)
	L.beam(m, sc*V(0, -3, 0.2), sc*V(0, 0, 5), 0.35, C.iron, L.M.metal)
	local board = P(m, V(0.6, 5, 6), sc*CF(0, -3.4, 4), Color3.fromRGB(110,76,48), L.M.planks, nil, 'TavernSign')
	P(m, V(0.7, 5.4, 0.5), sc*CF(0, -3.4, 0.9), C.beamDark, L.M.wood); P(m, V(0.7, 5.4, 0.5), sc*CF(0, -3.4, 7.1), C.beamDark, L.M.wood)
	for _, sx in ipairs({-1, 1}) do
		L.cyl(m, 2.6, 2, sc*CF(sx*0.4, -3.6, 4), C.gold, L.M.metal)
		L.cyl(m, 0.6, 2.2, sc*CF(sx*0.4, -2.1, 4), Color3.fromRGB(245,240,230), L.M.smooth)
	end
	-- terrace: tables, stools, barrels, lanterns on posts, low fence
	local tr = L.model(m, 'Terrace')
	P(tr, V(40, 0.6, 10), cf*CF(0, 0.3, 19), Color3.fromRGB(128,90,56), L.M.planks, nil, 'Deck')
	for _, x in ipairs({-14, -5, 5, 14}) do
		local tc = cf*CF(x, 0.6, 19)
		L.cyl(tr, 0.5, 4.6, tc*CF(0, 3, 0), Color3.fromRGB(140,98,62), L.M.planks)
		L.cyl(tr, 3, 0.8, tc*CF(0, 1.5, 0), C.beamDark, L.M.wood)
		for k = 0, 3 do
			local a = k*math.pi/2 + 0.4
			L.cyl(tr, 2, 1.8, tc*CF(math.cos(a)*3.4, 1, math.sin(a)*3.4), Color3.fromRGB(120,84,52), L.M.planks)
		end
		L.cyl(tr, 1, 0.8, tc*CF(0.6, 3.7, 0.4), C.gold, L.M.metal)
		local cdl = P(tr, V(0.4, 0.8, 0.4), tc*CF(-0.8, 3.7, -0.5), Color3.fromRGB(255,220,150), L.M.neon); L.light(cdl, Color3.fromRGB(255,190,120), 0.8, 10)
	end
	L.fence(tr, cf*V(-20, 0, 24.5), cf*V(-4, 0, 24.5)); L.fence(tr, cf*V(4, 0, 24.5), cf*V(20, 0, 24.5))
	for _, x in ipairs({-22, 22}) do L.lamp(tr, cf*V(x, 0, 25)) end
	for k = 0, 2 do L.barrel(tr, cf*CF(21 + k*0.2, 0.6, 14 - k*4.6)) end
	L.barrel(tr, cf*CF(21, 5.6, 9.4))
end

-- ===================== GUILD HALL (enterable) =====================
workspace.Terrain:FillBlock(CF(112, 0, 42), V(46, 4, 36), Enum.Material.Ground)
workspace.Terrain:FillBlock(CF(112, 0, 22), V(20, 4, 8), Enum.Material.Cobblestone)
do
	local m = L.model(f, 'GuildHall')
	local cf = L.at(112, 42, math.pi)          -- front faces -Z (toward the east road)
	local w, d = 40, 30
	local h1 = 15
	local wt = 1.6
	local dw, dh = 9, 11.5
	-- foundation + interior floor
	P(m, V(w + 2, 1.6, d + 2), cf*CF(0, 0.5, 0), C.stone, L.M.cobble, nil, 'Foundation')
	P(m, V(w - 2*wt, 0.3, d - 2*wt), cf*CF(0, 1.45, 0), Color3.fromRGB(120,84,52), L.M.planks, nil, 'Floor')
	workspace.Terrain:FillBlock(cf*CF(0, 5.6, 0), V(w + 4, 8, d + 4), Enum.Material.Air)
	local y0 = 1.3
	local function wall(size, at) return P(m, size, cf*CF(at), Color3.fromRGB(168,162,152), L.M.limestone, nil, 'Wall') end
	-- front wall with door opening
	local segW = (w - dw)/2
	wall(V(segW, h1, wt), V(-(dw/2 + segW/2), y0 + h1/2, d/2 - wt/2))
	wall(V(segW, h1, wt), V((dw/2 + segW/2), y0 + h1/2, d/2 - wt/2))
	wall(V(dw, h1 - dh, wt), V(0, y0 + dh + (h1 - dh)/2, d/2 - wt/2))
	wall(V(w, h1, wt), V(0, y0 + h1/2, -d/2 + wt/2))
	wall(V(wt, h1, d - 2*wt), V(w/2 - wt/2, y0 + h1/2, 0))
	wall(V(wt, h1, d - 2*wt), V(-w/2 + wt/2, y0 + h1/2, 0))
	-- corner quoins
	for _, sx in ipairs({-1, 1}) do for _, sz in ipairs({-1, 1}) do
		for q = 0, 4 do P(m, V(2.4, 2.2, 2.4), cf*CF(sx*(w/2 - 0.9), y0 + 1.5 + q*3, sz*(d/2 - 0.9)), (q % 2 == 0) and Color3.fromRGB(190,184,172) or STONE, L.M.limestone) end
	end end
	-- door frame arch + open doors swung inward
	for k = 0, 8 do
		local a = math.pi*k/8
		P(m, V(2.2, 1.6, wt + 0.6), cf*CF(math.cos(a)*(dw/2 + 0.6), y0 + dh - 2 + math.sin(a)*2.6, d/2 - wt/2)*A(0, 0, a - math.pi/2), Color3.fromRGB(190,184,172), L.M.limestone)
	end
	for _, sx in ipairs({-1, 1}) do
		P(m, V(1.2, dh, wt + 0.8), cf*CF(sx*(dw/2 + 0.6), y0 + dh/2, d/2 - wt/2), Color3.fromRGB(190,184,172), L.M.limestone)
		local dr = P(m, V(0.6, dh - 2.6, dw/2), cf*CF(sx*(dw/2 - 0.4), y0 + (dh - 2.6)/2, d/2 - wt - dw/4), Color3.fromRGB(96,62,38), L.M.planks, nil, 'Door')
		for _, yy in ipairs({0.25, 0.75}) do P(m, V(0.8, 0.5, dw/2), cf*CF(sx*(dw/2 - 0.4), y0 + (dh - 2.6)*yy, d/2 - wt - dw/4), C.iron, L.M.metal) end
	end
	P(m, V(dw + 6, 0.8, 4), cf*CF(0, 0.6, d/2 + 2), Color3.fromRGB(190,184,172), L.M.limestone, nil, 'Step')
	-- exterior windows (on stone walls, front + sides)
	for _, x in ipairs({-13, 13}) do L.window(m, cf*CF(x, y0 + 8, d/2), 4.6, 6.4, {shutters = false, lit = true, frame = C.beamDark}) end
	for _, z in ipairs({-7, 7}) do
		L.window(m, cf*CF(w/2, y0 + 8, z)*A(0, rad(90), 0), 4.6, 6.4, {shutters = false, lit = true, frame = C.beamDark})
		L.window(m, cf*CF(-w/2, y0 + 8, z)*A(0, rad(-90), 0), 4.6, 6.4, {shutters = false, lit = true, frame = C.beamDark})
	end
	-- banners either side of the door and a crest over it
	for _, sx in ipairs({-1, 1}) do L.banner(m, cf*CF(sx*8.5, y0 + 8.5, d/2 + 0.5), Color3.fromRGB(70,40,120), 10, C.gold) end
	P(m, V(6, 6, 0.6), cf*CF(0, y0 + h1 - 1.6, d/2 + 0.3)*A(0, 0, rad(45)), Color3.fromRGB(60,36,104), L.M.slate)
	P(m, V(3.6, 3.6, 0.8), cf*CF(0, y0 + h1 - 1.6, d/2 + 0.35)*A(0, 0, rad(45)), C.gold, L.M.metal)
	-- ceiling / upper floor
	P(m, V(w + 1, 1.2, d + 1), cf*CF(0, y0 + h1 + 0.6, 0), C.beamDark, L.M.wood, nil, 'Ceiling')
	for x = -16, 16, 8 do P(m, V(1.2, 1.4, d - 2*wt), cf*CF(x, y0 + h1 - 0.7, 0), C.beam, L.M.wood, nil, 'Joist') end
	-- upper timber storey + roof
	local y1 = y0 + h1 + 1.2
	local wo = {wall = C.plasterA, shutter = C.shutterBlue, lit = true}
	L.timberWall(m, cf*CF(0, y1, d/2), w, 12, {'brace','win','x','win','x','win','brace'}, wo)
	L.timberWall(m, cf*CF(0, y1, -d/2)*A(0, math.pi, 0), w, 12, {'brace','win','x','win','brace'}, wo)
	L.timberWall(m, cf*CF(w/2, y1, 0)*A(0, rad(90), 0), d - 2, 12, {'brace','win','win','brace'}, wo)
	L.timberWall(m, cf*CF(-w/2, y1, 0)*A(0, rad(-90), 0), d - 2, 12, {'brace','win','win','brace'}, wo)
	L.gableRoof(m, cf*CF(0, y1 + 12, 0), w, d, 13, {roof = Color3.fromRGB(62,84,124), wall = C.plasterA, finials = true})
	L.chimney(m, cf*CF(-w/2 + 4, y1 + 12, -d/4), 16, true)
	-- bell-tower spire on the ridge
	local sp = cf*CF(6, y1 + 25, 0)
	P(m, V(6, 7, 6), sp*CF(0, 3.5, 0), C.plasterA, L.M.plaster)
	for _, a in ipairs({0, 90, 180, 270}) do P(m, V(2.4, 3.6, 0.3), sp*A(0, rad(a), 0)*CF(0, 4, 3.05), Color3.fromRGB(26,24,24), L.M.slate) end
	for i = 0, 9 do P(m, V(7 - i*0.68, 1.1, 7 - i*0.68), sp*CF(0, 7.5 + i*1.1, 0), Color3.fromRGB(62,84,124), L.M.slate) end
	L.ball(m, 1.2, sp*CF(0, 19.5, 0), C.gold, L.M.metal)

	-- ===== INTERIOR =====
	local inn = L.model(m, 'Interior')
	local fy = y0 + 0.45
	-- carpet runner from door to counter
	P(inn, V(6, 0.1, 16), cf*CF(0, fy + 0.05, 6), Color3.fromRGB(110,36,48), L.M.fabric)
	-- reception counter (back), with ledger, candles, quest bell
	local cc = cf*CF(0, fy, -8)
	P(inn, V(18, 4, 3), cc*CF(0, 2, 0), Color3.fromRGB(110,76,48), L.M.planks, nil, 'Counter')
	P(inn, V(18.6, 0.5, 3.6), cc*CF(0, 4.25, 0), Color3.fromRGB(80,54,36), L.M.wood)
	P(inn, V(2.4, 0.4, 1.8), cc*CF(-4, 4.7, 0), Color3.fromRGB(150,40,48), L.M.leather, nil, 'Ledger')
	L.cyl(inn, 0.8, 1, cc*CF(4, 4.9, 0), C.gold, L.M.metal)
	for _, x in ipairs({-7.5, 7.5}) do local cd = P(inn, V(0.4, 1.2, 0.4), cc*CF(x, 5.1, 0), Color3.fromRGB(255,230,170), L.M.neon); L.light(cd, Color3.fromRGB(255,200,130), 0.8, 12) end
	-- shelves with books/potions behind the counter
	for _, x in ipairs({-10, 0, 10}) do
		local sc = cf*CF(x, fy, -d/2 + wt + 1)
		P(inn, V(8, 10, 1.6), sc*CF(0, 5, 0), Color3.fromRGB(96,66,42), L.M.planks)
		for s = 0, 3 do
			P(inn, V(8, 0.3, 1.8), sc*CF(0, 1.5 + s*2.6, 0.2), Color3.fromRGB(80,54,36), L.M.wood)
			for b = 0, 6 do
				local col = ({Color3.fromRGB(150,40,48), Color3.fromRGB(50,80,140), Color3.fromRGB(60,110,70), Color3.fromRGB(170,130,60), Color3.fromRGB(110,60,140)})[(b + s + x) % 5 + 1]
				P(inn, V(0.8, 1.8 + (b % 3)*0.2, 1.2), sc*CF(-3.2 + b*1.05, 2.6 + s*2.6, 0.3), col, L.M.leather)
			end
		end
	end
	-- QUEST BOARD on the left wall with pinned notes
	local qb = cf*CF(-w/2 + wt + 0.4, fy + 6, 2)*A(0, rad(90), 0)
	P(inn, V(12, 7, 0.6), qb, Color3.fromRGB(150,110,70), L.M.planks, nil, 'QuestBoard')
	P(inn, V(13, 0.8, 0.9), qb*CF(0, 3.8, 0.1), C.beamDark, L.M.wood)
	for k = 0, 7 do
		local note = P(inn, V(2, 2.4, 0.1), qb*CF(-4.6 + (k % 4)*3.1, 1.5 - math.floor(k/4)*3.2, 0.35)*A(0, 0, rad(rng:NextNumber(-8, 8))), Color3.fromRGB(236,226,196), L.M.smooth, nil, 'QuestNote')
		P(inn, V(0.3, 0.3, 0.2), qb*CF(-4.6 + (k % 4)*3.1, 2.5 - math.floor(k/4)*3.2, 0.42), Color3.fromRGB(200,40,40), L.M.smooth)
	end
	-- fireplace on the right wall
	local fp = cf*CF(w/2 - wt - 1.4, fy, 0)*A(0, rad(-90), 0)
	P(inn, V(10, 9, 2.8), fp*CF(0, 4.5, -0.2), STONE, L.M.cobble)
	P(inn, V(5.4, 4.4, 2), fp*CF(0, 2.2, 0.6), Color3.fromRGB(30,26,24), L.M.slate)
	P(inn, V(11, 0.8, 3.4), fp*CF(0, 9.2, 0), Color3.fromRGB(110,76,48), L.M.wood)
	local fire = P(inn, V(3, 0.8, 1), fp*CF(0, 0.6, 0.8), Color3.fromRGB(255,140,60), L.M.neon, nil, 'Hearth')
	local fi = Instance.new('Fire'); fi.Size = 4; fi.Heat = 5; fi.Parent = fire
	L.light(fire, Color3.fromRGB(255,160,90), 1.6, 26, true)
	-- long feast tables (kit) along Z with wide benches, candle rows on top
	local R90 = A(0, rad(90), 0)
	for _, x in ipairs({-8, 8}) do
		local tc = cf*CF(x, fy, 3)
		_G.kit('Table', inn, tc*R90)
		for _, sx in ipairs({-4.3, 4.3}) do
			_G.kit('WIde Seat', inn, tc*CF(sx, 0, -3)*R90)
			_G.kit('WIde Seat', inn, tc*CF(sx, 0, 3.6)*R90)
		end
		local cdl = _G.kit('Candles', inn, tc*CF(0, 3.9, 0)*R90, 1)
		for _, d in ipairs(cdl:GetDescendants()) do if d:IsA('BasePart') and d.Size.Y < 0.5 and d.Size.X < 0.5 then d.Material = L.M.neon; d.Color = Color3.fromRGB(255,200,120) end end
		local lp = P(inn, V(0.2, 0.2, 0.2), tc*CF(0, 5, 0), Color3.new(1,1,1), L.M.smooth); lp.Transparency = 1
		L.light(lp, Color3.fromRGB(255,190,120), 0.45, 12)
		-- kit chandelier above each table (top flush with the ceiling)
		local chm = _G.kit('Chandelier', inn, cf*CF(x, y0 + h1 - 8.1, 3), 1.4)
		local cl = P(inn, V(0.2, 0.2, 0.2), cf*CF(x, y0 + h1 - 6.5, 3), Color3.new(1,1,1), L.M.smooth); cl.Transparency = 1
		L.light(cl, Color3.fromRGB(255,200,130), 0.7, 22, true)
	end
	-- corner furniture
	for _, sx in ipairs({-1, 1}) do _G.kit('Cabinet', inn, cf*CF(sx*16.2, fy, -10.6)) end
	_G.kit('Barrel Suport', inn, cf*CF(15.2, fy, 10.6)*A(0, rad(-90), 0))
	_G.kit('Chest', inn, cf*CF(-15.4, fy, 11.2)*R90)
	_G.kit('Round Chest', inn, cf*CF(-15.4, fy, 6.4)*R90)
	_G.kit('Vase', inn, cc*CF(-7, 4.5, 0.2), 1)
	_G.kit('Ornaments', inn, cc*CF(1.5, 4.5, 0), 1)
	for _, x in ipairs({-11, 11}) do _G.kit('Carpet', inn, cf*CF(x, fy + 0.02, 12), 2) end
	-- interior banners on the back wall
	for _, x in ipairs({-15, 15}) do L.banner(inn, cf*CF(x, y0 + 9, -d/2 + wt + 0.3), Color3.fromRGB(150,40,48), 8, C.gold) end
	-- weapon rack
	local wr = cf*CF(-w/2 + wt + 0.6, fy, -9)*A(0, rad(90), 0)
	P(inn, V(6, 0.6, 1), wr*CF(0, 4.5, 0.2), C.beamDark, L.M.wood)
	for k = -1, 1 do
		P(inn, V(0.4, 6, 0.2), wr*CF(k*2, 3.6, 0.6), Color3.fromRGB(200,200,210), L.M.metal)
		P(inn, V(1.6, 0.3, 0.3), wr*CF(k*2, 1.8, 0.6), C.gold, L.M.metal)
	end
end

local n = 0; for _, d in ipairs(f:GetDescendants()) do if d:IsA('BasePart') then n = n + 1 end end
return 'landmarks ok parts=' .. n
