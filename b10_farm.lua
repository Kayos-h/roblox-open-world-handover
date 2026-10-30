local L = _G.L
local V, CF, A, rad = L.V, L.CF, L.A, math.rad
local P = L.part
local C = L.C
local town = workspace:FindFirstChild('SpawnTown')
local f = L.folder(town, 'Farm')
local T = workspace.Terrain
local WOOD = Color3.fromRGB(128,90,56)
local DARK = Color3.fromRGB(80,56,38)
local function road(p1, p2, w, mat)
	local cf = CF((p1+p2)/2, p2)
	T:FillBlock(cf*CF(0,-2,0), V(w, 4, (p2-p1).Magnitude + w*0.5), mat)
end
road(V(250,0,312), V(287,0,312), 14, Enum.Material.Ground)      -- barn yard
T:FillBlock(CF(272, -2, 312), V(30, 4, 34), Enum.Material.Ground)
road(V(180,0,318), V(180,0,330), 8, Enum.Material.Ground)       -- farmhouse path
road(V(250,0,345), V(362,0,345), 8, Enum.Material.Ground)       -- windmill path
T:FillBlock(CF(250, -2, 384), V(166, 4, 58), Enum.Material.Ground)
for r = 0, 4 do T:FillBlock(CF(250, -2, 360 + r*12), V(162, 4, 4), Enum.Material.Mud) end

-- ===================== BARN =====================
do
	local m = L.model(f, 'Barn')
	local cf = L.at(300, 312, rad(-90))   -- front faces -X
	local w, d, h = 36, 26, 16
	local RED = Color3.fromRGB(150,52,44)
	local TRIM = Color3.fromRGB(236,230,214)
	P(m, V(w + 2, 1.4, d + 2), cf*CF(0, 0.3, 0), C.stone, L.M.cobble, nil, 'Foundation')
	P(m, V(w - 2, 0.3, d - 2), cf*CF(0, 1.1, 0), Color3.fromRGB(150,120,80), L.M.wood, nil, 'Floor')
	T:FillBlock(cf*CF(0, 6, 0), V(w + 2, 9, d + 2), Enum.Material.Air)
	T:FillBlock(cf*CF(0, -1.6, 0), V(w + 4, 4, d + 4), Enum.Material.Ground)
	local y0 = 1
	local dw, dh = 14, 13
	local function wall(size, at) return P(m, size, cf*CF(at), RED, L.M.planks, nil, 'Wall') end
	wall(V(1.2, h, d), V(-w/2 + 0.6, y0 + h/2, 0))
	wall(V(1.2, h, d), V(w/2 - 0.6, y0 + h/2, 0))
	wall(V(w, h, 1.2), V(0, y0 + h/2, -d/2 + 0.6))
	local seg = (w - dw)/2
	wall(V(seg, h, 1.2), V(-(dw/2 + seg/2), y0 + h/2, d/2 - 0.6))
	wall(V(seg, h, 1.2), V((dw/2 + seg/2), y0 + h/2, d/2 - 0.6))
	wall(V(dw, h - dh, 1.2), V(0, y0 + dh + (h - dh)/2, d/2 - 0.6))
	-- white corner + door trim
	for _, sx in ipairs({-1, 1}) do for _, sz in ipairs({-1, 1}) do
		P(m, V(1.4, h, 1.4), cf*CF(sx*(w/2 - 0.5), y0 + h/2, sz*(d/2 - 0.5)), TRIM, L.M.wood)
	end end
	P(m, V(dw + 2, 1, 1.4), cf*CF(0, y0 + dh + 0.5, d/2), TRIM, L.M.wood)
	for _, sx in ipairs({-1, 1}) do P(m, V(1, dh, 1.4), cf*CF(sx*(dw/2 + 0.5), y0 + dh/2, d/2), TRIM, L.M.wood) end
	-- open barn doors (swung outward) with white X bracing
	for _, sx in ipairs({-1, 1}) do
		local hinge = cf*CF(sx*(dw/2), y0, d/2 + 0.4)*A(0, sx*rad(110), 0)
		local leaf = hinge*CF(-sx*dw/4, dh/2, 0)
		P(m, V(dw/2, dh - 0.4, 0.6), leaf, RED, L.M.planks, nil, 'BarnDoor')
		for _, q in ipairs({{-1, 1}, {1, -1}}) do
			L.beam(m, (leaf*CF(-dw/4 + 0.5, -dh/2 + 0.8, 0.4)).Position, (leaf*CF(dw/4 - 0.5, dh/2 - 0.8, 0.4)).Position, 0.6, TRIM, L.M.wood, 0.3)
			L.beam(m, (leaf*CF(-dw/4 + 0.5, dh/2 - 0.8, 0.4)).Position, (leaf*CF(dw/4 - 0.5, -dh/2 + 0.8, 0.4)).Position, 0.6, TRIM, L.M.wood, 0.3)
			break
		end
		P(m, V(dw/2, 0.6, 0.8), leaf*CF(0, dh/2 - 0.5, 0.2), TRIM, L.M.wood)
		P(m, V(dw/2, 0.6, 0.8), leaf*CF(0, -dh/2 + 0.5, 0.2), TRIM, L.M.wood)
	end
	-- side windows
	for _, sx in ipairs({-1, 1}) do for _, z in ipairs({-6, 6}) do
		L.window(m, cf*CF(sx*(w/2), y0 + 9, z)*A(0, sx*rad(90), 0), 3.4, 3.4, {shutter = C.shutterGreen})
	end end
	-- steep roof (ridge along local X) + hay loft door in front gable
	L.gableRoof(m, cf*CF(0, y0 + h, 0)*A(0, rad(90), 0), d, w, 15, {roof = Color3.fromRGB(86,72,64), wall = RED, wallMat = L.M.planks, timber = false, overhang = 2.4, barge = TRIM})
	local lo = cf*CF(0, y0 + h + 3.5, d/2 + 0.1)
	P(m, V(6, 6, 0.4), lo, Color3.fromRGB(40,30,24), L.M.wood)
	P(m, V(7, 0.8, 0.8), lo*CF(0, 3.3, 0.3), TRIM, L.M.wood)
	P(m, V(0.6, 0.6, 5), lo*CF(0, 5, 2.4), DARK, L.M.wood)             -- hoist beam
	L.beam(m, (lo*CF(0, 5, 4.6)).Position, (lo*CF(0, -2, 4.6)).Position, 0.15, Color3.fromRGB(190,170,120), L.M.fabric)
	L.haybale(m, lo*CF(0, -3, 0.2), false)
	-- weathervane cupola
	local cu = cf*CF(0, y0 + h + 15.6, 0)
	P(m, V(5, 4, 5), cu*CF(0, 2, 0), TRIM, L.M.wood)
	P(m, V(5.6, 0.6, 5.6), cu*CF(0, 4.3, 0), DARK, L.M.wood)
	for i = 0, 4 do local s = 6 - i*1.2; P(m, V(s, 1, s), cu*CF(0, 5 + i, 0), Color3.fromRGB(86,72,64), L.M.slate) end
	L.cyl(m, 4, 0.3, cu*CF(0, 11, 0), C.iron, L.M.metal)
	P(m, V(3, 1.2, 0.2), cu*CF(0.6, 12, 0), C.iron, L.M.metal)
	L.wedge(m, V(0.2, 1, 1.4), cu*CF(-1.6, 12, 0)*A(0, rad(90), 0), C.iron, L.M.metal)
	-- interior: hay stacks, stalls, loft
	for k = 0, 3 do L.haybale(m, cf*CF(-12 + (k % 2)*6.4, y0 + 0.3 + math.floor(k/2)*3.4, -9), false) end
	L.haybale(m, cf*CF(12, y0 + 0.3, -8), true)
	for _, x in ipairs({6, 12}) do
		P(m, V(0.6, 5, 10), cf*CF(x - 3, y0 + 2.8, 4), WOOD, L.M.planks)
	end
	P(m, V(w - 2.6, 0.6, 9), cf*CF(0, y0 + 10, -d/2 + 5.8), WOOD, L.M.planks, nil, 'Loft')
	for k = 0, 2 do L.haybale(m, cf*CF(-10 + k*8, y0 + 10.3, -d/2 + 5), false) end
	local lan = P(m, V(1, 1.4, 1), cf*CF(0, y0 + 9, 2), Color3.fromRGB(255,206,130), L.M.neon); L.light(lan, Color3.fromRGB(255,196,128), 1.2, 22, false)
	-- yard props
	L.cart(m, cf*CF(-14, 0, d/2 + 10)*A(0, rad(20), 0), 'hay')
	L.haybale(m, cf*CF(14, 0, d/2 + 6), true); L.haybale(m, cf*CF(19, 0, d/2 + 4), true)
	L.barrel(m, cf*CF(w/2 + 2, 0.4, d/2 - 2)); L.barrel(m, cf*CF(w/2 + 2, 0.4, d/2 - 5))
	-- water trough
	local tq = cf*CF(-w/2 - 4, 0, 4)
	P(m, V(3, 2.4, 8), tq*CF(0, 1.2, 0), WOOD, L.M.planks)
	local wq = P(m, V(2.4, 0.2, 7.4), tq*CF(0, 2.3, 0), Color3.fromRGB(60,110,130), L.M.glass); wq.Transparency = 0.3
end

-- ===================== FARMHOUSE =====================
do
	local m = L.model(f, 'Farmhouse')
	local cf = L.at(180, 304, 0)    -- front faces +Z (toward the track)
	L.house(m, cf, {w=24, d=16, floors=2, fh=10, stoneGround=true, flowers=true, lit=true, roof=Color3.fromRGB(176,132,70), wall=C.plasterA, shutter=C.shutterGreen, chimney=true, name='FarmhouseMain'})
	-- porch
	local pc = cf*CF(0, 0, 10)
	P(m, V(16, 0.8, 4), pc*CF(0, 1.2, 0), WOOD, L.M.planks)
	for _, x in ipairs({-7.4, 7.4}) do P(m, V(0.8, 8, 0.8), pc*CF(x, 5, 1.6), DARK, L.M.wood) end
	P(m, V(17, 0.6, 5.4), pc*CF(0, 9.2, 0.4)*A(rad(10), 0, 0), Color3.fromRGB(160,118,64), L.M.shingles)
	L.bench(m, pc*CF(-4, 1, -0.6)*A(0, 0, 0))
	-- kitchen garden + fence
	local g = cf*CF(-22, 0, 2)
	L.fence(m, (g*CF(-8, 0, -9)).Position, (g*CF(8, 0, -9)).Position)
	L.fence(m, (g*CF(-8, 0, -9)).Position, (g*CF(-8, 0, 9)).Position)
	L.fence(m, (g*CF(-8, 0, 9)).Position, (g*CF(2, 0, 9)).Position)
	for r = 0, 3 do
		for k = 0, 4 do
			local p = (g*CF(-5.5 + k*2.8, 0, -6 + r*4)).Position
			L.ball(m, 1.6, CF(p + V(0, 0.6, 0)), (r % 2 == 0) and Color3.fromRGB(96,160,70) or Color3.fromRGB(70,130,60), L.M.grass)
		end
	end
	-- stone well
	local wl = cf*CF(18, 0, 14)
	L.cyl(m, 3.2, 6, wl*CF(0, 1.6, 0), C.stone, L.M.cobble)
	L.cyl(m, 0.3, 4.8, wl*CF(0, 3.1, 0), Color3.fromRGB(40,70,90), L.M.glass)
	for _, x in ipairs({-2.6, 2.6}) do P(m, V(0.6, 6, 0.6), wl*CF(x, 5, 0), DARK, L.M.wood) end
	L.gableRoof(m, wl*CF(0, 8, 0), 6.4, 5, 2, {roof = Color3.fromRGB(176,132,70), wall = DARK, wallMat = L.M.wood, timber = false, overhang = 0.6})
	P(m, V(5.2, 0.5, 0.5), wl*CF(0, 6.6, 0), DARK, L.M.wood)
	L.cyl(m, 1, 1.2, wl*CF(0, 4.6, 0), WOOD, L.M.wood)
	-- clothesline + trees
	L.tree(m, (cf*CF(-14, 0, -16)).Position, 1.0); L.tree(m, (cf*CF(16, 0, -14)).Position, 0.9)
	-- chicken coop + chickens
	local co = cf*CF(30, 0, -2)
	P(m, V(8, 5, 6), co*CF(0, 3.6, 0), WOOD, L.M.planks)
	for _, x in ipairs({-3.4, 3.4}) do for _, z in ipairs({-2.4, 2.4}) do P(m, V(0.6, 1.4, 0.6), co*CF(x, 0.7, z), DARK, L.M.wood) end end
	L.gableRoof(m, co*CF(0, 6.1, 0), 8, 6, 2.4, {roof = Color3.fromRGB(150,52,44), wall = WOOD, wallMat = L.M.planks, timber = false, overhang = 0.6})
	P(m, V(2, 2, 0.3), co*CF(0, 3.2, 3.05), Color3.fromRGB(30,24,20), L.M.wood)
	L.beam(m, (co*CF(0, 2.2, 3.1)).Position, (co*CF(0, 0, 6)).Position, 1.6, DARK, L.M.planks, 0.3)
	L.fence(m, (co*CF(-8, 0, 4)).Position, (co*CF(8, 0, 4)).Position)
	L.fence(m, (co*CF(-8, 0, 4)).Position, (co*CF(-8, 0, 16)).Position)
	L.fence(m, (co*CF(8, 0, 4)).Position, (co*CF(8, 0, 16)).Position)
	L.fence(m, (co*CF(-8, 0, 16)).Position, (co*CF(8, 0, 16)).Position)
	local rng = Random.new(7)
	for k = 1, 6 do
		local hc = CF((co*CF(rng:NextNumber(-6, 6), 0, rng:NextNumber(6, 14))).Position)*A(0, rng:NextNumber(0, 6.28), 0)
		local ch = L.model(m, 'Chicken')
		local body = (k % 3 == 0) and Color3.fromRGB(150,96,60) or Color3.fromRGB(245,242,236)
		L.ball(ch, 1.4, hc*CF(0, 1.1, 0), body, L.M.fabric)
		L.ball(ch, 0.9, hc*CF(0, 1.9, 0.6), body, L.M.fabric)
		P(ch, V(0.3, 0.3, 0.4), hc*CF(0, 1.9, 1.15), Color3.fromRGB(240,170,40), L.M.plastic)
		P(ch, V(0.2, 0.4, 0.5), hc*CF(0, 2.45, 0.6), Color3.fromRGB(210,40,40), L.M.plastic)
		P(ch, V(0.3, 0.8, 0.8), hc*CF(0, 1.4, -0.7)*A(rad(30), 0, 0), body, L.M.fabric)
	end
end

-- ===================== CROPS =====================
do
	local m = L.model(f, 'Crops')
	local rng = Random.new(11)
	local kinds = {'wheat', 'cabbage', 'pumpkin', 'carrot', 'wheat'}
	for r = 0, 4 do
		local z = 360 + r*12
		local kind = kinds[r + 1]
		local x = 173
		while x < 328 do
			if math.abs(x - 250) > 8 then
				local y = L.ground(x, z)
				local p = V(x, y, z)
				if kind == 'wheat' then
					for s = 1, 2 do
						local hgt = rng:NextNumber(2.6, 3.8)
						local q = p + V(rng:NextNumber(-0.9, 0.9), 0, rng:NextNumber(-0.9, 0.9))
						local tilt = A(rng:NextNumber(-0.12, 0.12), rng:NextNumber(0, 3), rng:NextNumber(-0.12, 0.12))
						P(m, V(0.5, hgt, 0.5), CF(q + V(0, hgt/2, 0))*tilt, Color3.fromRGB(186,160,80), L.M.grass)
						P(m, V(0.8, 1.2, 0.8), CF(q + V(0, hgt + 0.3, 0))*tilt, Color3.fromRGB(230,198,96), L.M.sand)
					end
				elseif kind == 'cabbage' then
					L.ball(m, 1.8, CF(p + V(0, 0.7, 0)), Color3.fromRGB(110,170,80), L.M.grass)
					L.ball(m, 1.2, CF(p + V(0, 1.3, 0)), Color3.fromRGB(150,200,110), L.M.grass)
				elseif kind == 'pumpkin' then
					if rng:NextNumber() < 0.6 then
						L.ball(m, rng:NextNumber(1.6, 2.4), CF(p + V(0, 0.8, 0)), Color3.fromRGB(226,128,40), L.M.plastic)
						P(m, V(0.3, 0.6, 0.3), CF(p + V(0, 1.9, 0)), Color3.fromRGB(80,110,50), L.M.wood)
					else
						P(m, V(2.2, 0.6, 1.6), CF(p + V(0, 0.4, 0))*A(0, rng:NextNumber(0, 3), 0), Color3.fromRGB(80,140,60), L.M.grass)
					end
				else
					P(m, V(1.2, 1.6, 1.2), CF(p + V(0, 0.9, 0))*A(0, rng:NextNumber(0, 3), 0), Color3.fromRGB(90,160,60), L.M.grass)
					P(m, V(0.5, 0.4, 0.5), CF(p + V(0, 0.15, 0)), Color3.fromRGB(230,120,40), L.M.plastic)
				end
			end
			x = x + 3
		end
	end
	-- field fence (north side + ends) with a gap for the track
	L.fence(m, V(166, L.ground(166, 353), 353), V(242, L.ground(242, 353), 353))
	L.fence(m, V(258, L.ground(258, 353), 353), V(334, L.ground(334, 353), 353))
	L.fence(m, V(166, L.ground(166, 353), 353), V(166, L.ground(166, 404), 404))
	L.fence(m, V(334, L.ground(334, 353), 353), V(334, L.ground(334, 404), 404))
	-- scarecrows
	for _, q in ipairs({{205, 378}, {296, 390}}) do
		local p = V(q[1], L.ground(q[1], q[2]), q[2])
		local s = L.model(m, 'Scarecrow')
		P(s, V(0.6, 9, 0.6), CF(p + V(0, 4.5, 0)), DARK, L.M.wood)
		P(s, V(7, 0.5, 0.5), CF(p + V(0, 7, 0)), DARK, L.M.wood)
		P(s, V(3, 3.4, 1.4), CF(p + V(0, 6.4, 0)), Color3.fromRGB(70,100,150), L.M.fabric)
		P(s, V(6.4, 1, 1.2), CF(p + V(0, 7.4, 0)), Color3.fromRGB(70,100,150), L.M.fabric)
		L.ball(s, 2.2, CF(p + V(0, 9.4, 0)), Color3.fromRGB(214,184,98), L.M.sand)
		L.cyl(s, 0.3, 4, CF(p + V(0, 10.3, 0)), Color3.fromRGB(176,140,70), L.M.fabric)
		L.cyl(s, 1.2, 2.2, CF(p + V(0, 11, 0)), Color3.fromRGB(176,140,70), L.M.fabric)
		P(s, V(1.4, 2.2, 0.3), CF(p + V(0.4, 5.6, 0.75)), Color3.fromRGB(150,60,50), L.M.fabric)
	end
end

-- ===================== WINDMILL =====================
do
	local m = L.model(f, 'Windmill')
	local base = V(372, L.ground(372, 345), 345)
	local cf = CF(base)*A(0, rad(-90), 0)     -- sails face -X (toward the farm)
	local TH = 38
	local n = 12
	for i = 0, n - 1 do
		local t = i/n
		local dia = 19 - t*7
		L.cyl(m, TH/n + 0.05, dia, cf*CF(0, 0.5 + (i + 0.5)*TH/n, 0), Color3.fromRGB(226,218,200), L.M.plaster)
	end
	L.cyl(m, 1.4, 20.4, cf*CF(0, 0.7, 0), C.stone, L.M.cobble)
	L.cyl(m, 1, 13, cf*CF(0, TH + 0.4, 0), DARK, L.M.wood)
	-- balcony ring
	L.cyl(m, 0.6, 18.6, cf*CF(0, 14, 0), DARK, L.M.planks)
	for k = 0, 15 do local a = k/16*math.pi*2; P(m, V(0.4, 2.4, 0.4), cf*CF(math.cos(a)*9, 15.4, math.sin(a)*9), DARK, L.M.wood) end
	L.cyl(m, 0.4, 18.4, cf*CF(0, 16.6, 0), DARK, L.M.wood).Transparency = 0
	-- door + windows
	L.door(m, cf*CF(0, 1.4, 9.3), 4.6, 8)
	for _, y in ipairs({20, 28}) do L.window(m, cf*CF(0, y, 8.4 - (y - 20)*0.18), 2.6, 3.4, {}) end
	-- cap (stepped dome)
	for i = 0, 6 do local s = 14 - i*1.9; L.cyl(m, 1.2, s, cf*CF(0, TH + 1.4 + i*1.1, 0), Color3.fromRGB(110,70,52), L.M.shingles) end
	L.ball(m, 1.6, cf*CF(0, TH + 9.6, 0), C.gold, L.M.metal)
	-- hub + sails (rotate via script)
	local hubCF = cf*CF(0, TH - 2, 8.6)
	P(m, V(1.6, 1.6, 4), hubCF*CF(0, 0, -1.6), DARK, L.M.wood)
	local sails = L.model(m, 'Sails')
	local hub = L.cyl(sails, 1.6, 3, hubCF*A(rad(90), 0, 0), DARK, L.M.wood); hub.Name = 'Hub'
	for k = 0, 3 do
		local arm = hubCF*A(0, 0, k*math.pi/2)
		P(sails, V(1, 24, 0.8), arm*CF(0, 12.5, 0), DARK, L.M.wood, nil, 'Arm')
		local cloth = P(sails, V(5, 19, 0.2), arm*CF(3.2, 14.5, -0.2), Color3.fromRGB(236,228,206), L.M.fabric, nil, 'Cloth')
		for j = 0, 5 do P(sails, V(5.6, 0.3, 0.4), arm*CF(3, 5.5 + j*3.6, 0.15), DARK, L.M.wood) end
		P(sails, V(0.4, 19, 0.4), arm*CF(5.7, 14.5, 0.15), DARK, L.M.wood)
	end
	sails.PrimaryPart = hub
	for _, p in ipairs(sails:GetDescendants()) do if p:IsA('BasePart') then p.CanCollide = false end end
	local sc = Instance.new('Script')
	sc.Name = 'SpinSails'
	sc.Source = [[
local sails = script.Parent:WaitForChild('Sails')
local hub = sails:WaitForChild('Hub')
local axis = hub.CFrame
local rel = {}
for _, p in ipairs(sails:GetDescendants()) do if p:IsA('BasePart') then rel[p] = axis:ToObjectSpace(p.CFrame) end end
local ang = 0
game:GetService('RunService').Heartbeat:Connect(function(dt)
	ang = (ang + dt*0.6) % (math.pi*2)
	local c = axis * CFrame.Angles(ang, 0, 0)
	for p, r in pairs(rel) do p.CFrame = c * r end
end)
]]
	sc.Parent = m
	-- sacks of flour by the door
	for k = 0, 2 do L.ball(m, 2.2, cf*CF(-3 + k*1.6, 1.8, 11)*A(0, 0, 0), Color3.fromRGB(226,214,180), L.M.fabric) end
	L.cart(m, cf*CF(8, 0.4, 14)*A(0, rad(70), 0), 'goods')
end

local cnt = 0; for _, d in ipairs(f:GetDescendants()) do if d:IsA('BasePart') then cnt = cnt + 1 end end
return 'farm ok parts=' .. cnt
