local L = _G.L
local V, CF, A = L.V, L.CF, L.A
local T = workspace.Terrain
local E = Enum.Material
local t0 = os.clock()
local tb = workspace:FindFirstChild('TEST_Builds'); if tb then tb:Destroy() end
local old = workspace:FindFirstChild('SpawnTown'); if old then old:Destroy() end
T:Clear()
T:SetMaterialColor(E.Grass, Color3.fromRGB(106,150,64))
T:SetMaterialColor(E.LeafyGrass, Color3.fromRGB(94,140,58))
T:SetMaterialColor(E.Cobblestone, Color3.fromRGB(150,144,134))
T:SetMaterialColor(E.Ground, Color3.fromRGB(134,110,78))
T:SetMaterialColor(E.Mud, Color3.fromRGB(96,82,64))
T:SetMaterialColor(E.Sand, Color3.fromRGB(206,190,150))
T:SetMaterialColor(E.Rock, Color3.fromRGB(122,118,110))
T:SetMaterialColor(E.Pavement, Color3.fromRGB(160,154,144))
pcall(function() T.Decoration = true end)
T.WaterColor = Color3.fromRGB(44,110,130); T.WaterTransparency = 0.6; T.WaterWaveSize = 0.08; T.WaterWaveSpeed = 8; T.WaterReflectance = 0.5

-- base ground: -24..0
T:FillBlock(CF(0,-12,0), V(1400,24,1400), E.Grass)
-- leafy grass variation patches
local rng = Random.new(7)
for i = 1, 60 do
	local x, z = rng:NextNumber(-460,460), rng:NextNumber(-460,460)
	T:FillBlock(CF(x,-2,z)*A(0,rng:NextNumber(0,3),0), V(rng:NextNumber(20,60),4,rng:NextNumber(20,60)), E.LeafyGrass)
end

-- RIVER: z = 250 + 22*sin(x/90), from x=-700 to 700, width 34
local function riverZ(x) return 250 + 22*math.sin(x/90) end
_G.TOWN_riverZ = riverZ
for x = -700, 700, 8 do
	local z = riverZ(x)
	local z2 = riverZ(x+8)
	local ang = math.atan2(z2 - z, 8)
	local cf = CF(x+4, 0, (z+z2)/2)*A(0, -ang, 0)
	T:FillBlock(cf*CF(0,-1,0), V(10, 6, 52), E.Sand)       -- banks
	T:FillBlock(cf*CF(0,-6,0), V(10, 16, 36), E.Air)       -- channel
	T:FillBlock(cf*CF(0,-13,0), V(10, 4, 36), E.Mud)       -- bed
	T:FillBlock(cf*CF(0,-7.5,0), V(10, 9, 36), E.Water)    -- water (top at ~-3)
end

-- HQ PLATEAU (north): raised mound top at y=16 around (0,-320)
T:FillCylinder(CF(0,-8,-320), 48, 92, E.Grass)
T:FillCylinder(CF(0,4,-320), 24, 86, E.Grass)
T:FillCylinder(CF(0,10,-322), 12, 80, E.Grass)
-- rocky rim of plateau
for i = 0, 40 do
	local a = i/40*math.pi*2
	if not (a > math.pi*0.40 and a < math.pi*0.60) then
		local x, z = math.cos(a)*86, -320 + math.sin(a)*86
		T:FillBall(V(x, 8, z), rng:NextNumber(8,12), E.Rock)
	end
end
-- ramp from avenue up to plateau (south side, z=-150 -> -245, y 0 -> 16)
for k = 0, 19 do
	local top = k * 16/19
	T:FillBlock(CF(0, top - 6, -150 - k*5), V(64, 12, 6), E.Grass)
	T:FillBlock(CF(0, top - 2, -150 - k*5), V(30, 4, 6), E.Cobblestone)
end

-- OUTER HILLS (beyond walls)
local hills = {{-560,-560,170},{0,-640,190},{560,-560,170},{-640,0,160},{640,-80,170},{-600,520,150},{620,560,160},{-200,-680,140},{240,-660,140},{680,300,130},{-680,300,130}}
for _, h in ipairs(hills) do
	T:FillBall(V(h[1], -h[3]*0.45, h[2]), h[3], E.Grass)
	T:FillBall(V(h[1]*1.02, -h[3]*0.2, h[2]*1.02), h[3]*0.55, E.LeafyGrass)
end
for i = 1, 26 do
	local a = rng:NextNumber()*math.pi*2; local r = rng:NextNumber(500,620)
	T:FillBall(V(math.cos(a)*r, rng:NextNumber(0,20), math.sin(a)*r), rng:NextNumber(10,22), E.Rock)
end
-- rock outcrops inside town (natural accents)
for _, p in ipairs({{-390,-150},{-360,120},{380,-260},{300,-380},{-120,-420},{120,-420}}) do
	T:FillBall(V(p[1], -2, p[2]), 9, E.Rock); T:FillBall(V(p[1]+7, -4, p[2]+5), 6, E.Rock)
end

-- POND (west residential) at (-300, -40)
do
	local c = V(-300, 0, -40)
	T:FillBall(c + V(0,-14,0), 32, E.Sand)
	T:FillBlock(CF(c + V(0,21.5,0)), V(140,43,140), E.Air)
	T:FillBall(c + V(0,-12,0), 28, E.Air)
	T:FillBall(c + V(0,-12,0), 26.5, E.Water)
	T:FillBlock(CF(c + V(0,21.5,0)), V(140,43,140), E.Air)
	T:FillBlock(CF(c + V(0,-1.5,0)), V(56,3,56), E.Air)
	for i = 0, 11 do
		local a = i/12*math.pi*2 + 0.2
		T:FillBall(c + V(math.cos(a)*30, -1, math.sin(a)*30), 3 + (i % 3), E.Rock)
	end
end

-- ROADS (painted): helper paints a 4-deep layer from p1 to p2
local function road(p1, p2, w, mat)
	local d = p2 - p1
	local len = d.Magnitude
	local cf = CF((p1+p2)/2, p2)
	T:FillBlock(cf*CF(0,-2,0), V(w, 4, len + w*0.5), mat)
end
_G.TOWN_road = road
local C_ = E.Cobblestone
-- plaza disc
T:FillCylinder(CF(0,-2,0), 4, 78, E.Pavement)
T:FillCylinder(CF(0,-2,0), 4, 70, C_)
-- main avenue: gate (south) -> plaza ; bridge gap at river handled by bridge part
road(V(0,0,450), V(0,0,276), 30, C_)
road(V(0,0,224), V(0,0,60), 30, C_)
-- north avenue plaza -> HQ ramp
road(V(0,0,-60), V(0,0,-150), 30, C_)
-- plateau courtyard
T:FillCylinder(CF(0,14,-300), 4, 62, E.Pavement)
T:FillCylinder(CF(0,14,-300), 4, 56, C_)
road(V(0,16,-240), V(0,16,-250), 30, C_)
-- east road to market + east gate
road(V(60,0,0), V(450,0,0), 24, C_)
-- west road to residential + west gate
road(V(-60,0,0), V(-450,0,0), 24, C_)
-- residential streets (west)
road(V(-150,0,-200), V(-150,0,190), 18, C_)
road(V(-330,0,-180), V(-150,0,-180), 16, C_)
road(V(-380,0,140), V(-150,0,140), 16, C_)
road(V(-260,0,-160), V(-260,0,20), 12, E.Ground)
-- market streets (east)
road(V(150,0,-170), V(150,0,180), 18, C_)
road(V(150,0,110), V(330,0,110), 16, C_)
road(V(150,0,-110), V(330,0,-110), 16, C_)
road(V(290,0,-110), V(290,0,110), 14, C_)
-- diagonal lanes plaza -> districts
road(V(52,0,52), V(150,0,150), 14, C_)
road(V(-52,0,52), V(-150,0,150), 14, C_)
road(V(52,0,-52), V(150,0,-150), 14, C_)
road(V(-52,0,-52), V(-150,0,-150), 14, C_)
-- farm dirt tracks (south-east, beyond river)
road(V(0,0,330), V(250,0,330), 14, E.Ground)
road(V(250,0,300), V(250,0,410), 12, E.Ground)
-- mage tower path (south-west)
road(V(0,0,360), V(-260,0,360), 14, E.Ground)
-- wall-side ring track
for _, s in ipairs({{V(-410,0,-410),V(410,0,-410)},{V(410,0,-410),V(410,0,410)},{V(410,0,410),V(-410,0,410)},{V(-410,0,410),V(-410,0,-410)}}) do road(s[1], s[2], 10, E.Ground) end

-- FARM FIELDS: tilled mud rows with leafy rows
for row = 0, 9 do
	road(V(170, 0, 360 + row*6), V(330, 0, 360 + row*6), 3, (row % 2 == 0) and E.Mud or E.LeafyGrass)
end
local function h(x,z) local r = workspace:Raycast(V(x,200,z), V(0,-400,0)); return r and string.format('%.2f %s', r.Position.Y, r.Material.Name) or 'nil' end
return string.format('terrain ok %.1fs', os.clock()-t0)..' grass:'..h(-80,-250)..' road:'..h(0,120)..' dirt:'..h(-260,-90)..' court:'..h(20,-300)..' ramp:'..h(0,-200)
