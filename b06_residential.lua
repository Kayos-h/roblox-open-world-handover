local L = _G.L
local V, CF, A, rad = L.V, L.CF, L.A, math.rad
local P = L.part
local C = L.C
local town = workspace:FindFirstChild('SpawnTown')
local f = L.folder(town, 'Residential')
local T = workspace.Terrain
local rng = Random.new(42)

-- footbridge connector paths (dirt), painted flush
local function road(p1, p2, w, mat)
	local cf = CF((p1+p2)/2, p2)
	T:FillBlock(cf*CF(0,-2,0), V(w, 4, (p2-p1).Magnitude + w*0.5), mat)
end
road(V(-260,0,148), V(-260,0,226), 10, Enum.Material.Ground)
road(V(-260,0,266), V(-260,0,356), 10, Enum.Material.Ground)
road(V(250,0,118), V(250,0,238), 10, Enum.Material.Ground)
road(V(250,0,280), V(250,0,326), 10, Enum.Material.Ground)

local walls = {C.plasterA, C.plasterB, C.plasterC, C.plasterD, Color3.fromRGB(232,214,190), Color3.fromRGB(222,206,214)}
local roofs = {C.roofRed, C.roofBlue, C.roofBrown, C.roofGreen, C.roofSlate, C.roofOrange}
local shutters = {C.shutterGreen, C.shutterBlue, C.shutterRed, Color3.fromRGB(150,110,60)}

local function garden(cf, w, d)
	local g = L.model(f, 'Garden')
	local gd = 18
	local back = cf*CF(0, 0, -d/2 - 2)
	-- picket fence around the back garden
	local c1 = back*V(-w/2 - 2, 0, 0); local c2 = back*V(-w/2 - 2, 0, -gd)
	local c3 = back*V(w/2 + 2, 0, -gd); local c4 = back*V(w/2 + 2, 0, 0)
	L.fence(g, c1, c2); L.fence(g, c2, c3); L.fence(g, c3, c4)
	-- vegetable rows or flower beds
	if rng:NextNumber() < 0.5 then
		for r = 0, 2 do
			local rc = back*CF(0, 0, -5 - r*4)
			P(g, V(w - 4, 0.8, 2.2), rc*CF(0, 0.4, 0), Color3.fromRGB(96,70,48), L.M.ground)
			for k = 0, math.floor((w - 6)/2.2) do
				L.ball(g, 1.4, rc*CF(-w/2 + 3 + k*2.2, 1.3, 0), Color3.fromRGB(70 + r*20, 140, 60), L.M.leafy)
			end
		end
	else
		L.flowers(g, back*V(0, 0, -8), math.min(w, 14)/2, 30)
	end
	-- tree in the garden corner
	L.tree(g, back*V(w/2 - 3, 0, -gd + 4), rng:NextNumber(0.7, 0.95))
	-- props
	if rng:NextNumber() < 0.6 then L.barrel(g, back*CF(-w/2 + 1, 0, -2)) end
	if rng:NextNumber() < 0.5 then L.crate(g, back*CF(-w/2 + 1, 0, -6), 3) end
	-- washing line
	if rng:NextNumber() < 0.5 then
		local a = back*V(-w/4, 0, -gd + 3); local b = back*V(w/6, 0, -gd + 3)
		P(g, V(0.5, 8, 0.5), CF(a + V(0,4,0)), C.beam, L.M.wood); P(g, V(0.5, 8, 0.5), CF(b + V(0,4,0)), C.beam, L.M.wood)
		L.beam(g, a + V(0,7.6,0), b + V(0,7.6,0), 0.15, Color3.fromRGB(220,220,210), L.M.fabric)
		local cols = {Color3.fromRGB(200,80,80), Color3.fromRGB(240,240,230), Color3.fromRGB(90,130,200)}
		for k = 1, 3 do
			local p = a:Lerp(b, k/4)
			local cl = P(g, V(2, 2.6, 0.15), CF(p + V(0, 6.2, 0), b + V(0,6.2,0))*A(0, rad(90), 0), cols[k], L.M.fabric); cl.CanCollide = false
		end
	end
	-- front: bushes beside the door path and a small flower strip
	L.bush(g, cf*V(-w/2 + 2, 0, d/2 + 3), 0.7)
	L.bush(g, cf*V(w/2 - 2, 0, d/2 + 3), 0.7)
end

local function plot(x, z, yawDeg, o)
	local cf = L.at(x, z, rad(yawDeg))
	o.wall = o.wall or walls[rng:NextInteger(1, #walls)]
	o.roof = o.roof or roofs[rng:NextInteger(1, #roofs)]
	o.shutter = o.shutter or shutters[rng:NextInteger(1, #shutters)]
	local h = L.house(f, cf, o)
	if o.garden ~= false then garden(cf, o.w or 24, o.d or 18) end
	return h
end

-- Spine x=-150, west side (front faces +X)
plot(-178, -120, 90, {w=26, d=20, floors=2, jetty=true, flowers=true, stoneGround=true, name='House_W1'})
plot(-178, -62, 90, {w=22, d=18, floors=2, fh=10, name='House_W2'})
plot(-178, 52, 90, {w=24, d=20, floors=3, fh=10, jetty=true, ridgeZ=true, name='House_W3', garden=false})
plot(-178, 100, 90, {w=20, d=16, floors=1, fh=12, flowers=true, name='Cottage_W4'})
-- Spine east side (front faces -X)
plot(-124, -58, -90, {w=22, d=18, floors=2, flowers=true, name='House_E1'})
plot(-124, 42, -90, {w=24, d=18, floors=2, jetty=true, stoneGround=true, name='House_E2'})
plot(-124, 84, -90, {w=18, d=16, floors=1, fh=12, name='Cottage_E3', garden=false})
-- Street z=-180: north side faces +Z, south side faces -Z
plot(-200, -206, 0, {w=24, d=18, floors=2, flowers=true, name='House_N1'})
plot(-300, -206, 0, {w=28, d=20, floors=3, fh=10, jetty=true, ridgeZ=true, stoneGround=true, name='House_N2'})
plot(-200, -152, 180, {w=22, d=18, floors=2, name='House_N3', garden=false})
plot(-305, -152, 180, {w=20, d=16, floors=1, fh=12, flowers=true, name='Cottage_N4', garden=false})
-- Lane x=-260 east side (faces -X)
plot(-238, -100, -90, {w=20, d=16, floors=2, fh=10, flowers=true, name='House_L1', garden=false})
-- West road z=0: north side faces +Z, south side faces -Z
plot(-200, -26, 0, {w=26, d=18, floors=2, jetty=true, flowers=true, name='House_R1', garden=false})
plot(-370, -26, 0, {w=22, d=18, floors=2, name='House_R2', garden=false})
plot(-212, 28, 180, {w=24, d=18, floors=2, stoneGround=true, name='House_R3'})
plot(-290, 28, 180, {w=26, d=20, floors=3, fh=10, jetty=true, name='House_R4'})
plot(-365, 28, 180, {w=20, d=16, floors=1, fh=12, flowers=true, name='Cottage_R5'})
-- Street z=140: north side faces +Z, south side faces -Z
plot(-228, 114, 0, {w=22, d=18, floors=2, flowers=true, name='House_S1', garden=false})
plot(-300, 114, 0, {w=26, d=18, floors=2, jetty=true, name='House_S2', garden=false})
plot(-205, 166, 180, {w=24, d=20, floors=2, stoneGround=true, flowers=true, name='House_S3', garden=false})
plot(-300, 166, 180, {w=20, d=16, floors=1, fh=12, name='Cottage_S4', garden=false})
plot(-355, 166, 180, {w=22, d=18, floors=2, name='House_S5', garden=false})

-- street lamps along the spine and cross streets
local lamps = L.model(f, 'Lamps')
for _, z in ipairs({-150, -90, -30, 30, 70, 120, 170}) do L.lamp(lamps, V(-161, L.ground(-161, z), z)) end
for _, x in ipairs({-230, -280, -330}) do L.lamp(lamps, V(x, L.ground(x, -170), -170)); L.lamp(lamps, V(x, L.ground(x, 150), 150)) end
for _, x in ipairs({-180, -240, -330, -400}) do L.lamp(lamps, V(x, L.ground(x, 14), 14)) end

-- pond dressing: reeds, rocks, a small dock and benches
local pd = L.model(f, 'PondSide')
for i = 1, 26 do
	local a = rng:NextNumber()*math.pi*2
	local r = rng:NextNumber(26, 31)
	local p = V(-300 + math.cos(a)*r, 0, -40 + math.sin(a)*r)
	local g = L.ground(p.X, p.Z)
	for k = 1, 3 do
		local reed = P(pd, V(0.3, rng:NextNumber(3, 5), 0.3), CF(p + V(k*0.5, g + 2, k*0.3))*A(rng:NextNumber(-0.2,0.2), 0, rng:NextNumber(-0.2,0.2)), Color3.fromRGB(96,130,60), L.M.leafy)
		reed.CanCollide = false
	end
end
local dk = L.at(-300, -8, 0)
for k = 0, 6 do P(pd, V(7, 0.5, 1.6), dk*CF(0, 0.6, -k*1.8), Color3.fromRGB(128,90,56), L.M.planks) end
for _, sx in ipairs({-1, 1}) do for _, kz in ipairs({0, -10}) do L.cyl(pd, 8, 0.9, dk*CF(sx*3.2, -2, kz), Color3.fromRGB(96,66,42), L.M.wood) end end
L.bench(pd, L.at(-300, 0, 0)*CF(-10, 0, 4)*A(0, math.pi, 0))
L.bench(pd, L.at(-268, -40, rad(-90))*CF(0, 0, 4))
for _, p in ipairs({{-335,-60},{-270,-75},{-260,-15},{-330,-5}}) do L.tree(pd, V(p[1], L.ground(p[1], p[2]), p[2]), rng:NextNumber(0.9, 1.15)) end

local n = 0; for _, d in ipairs(f:GetDescendants()) do if d:IsA('BasePart') then n = n + 1 end end
return 'residential ok parts=' .. n
