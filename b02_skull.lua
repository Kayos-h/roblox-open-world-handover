local L = _G.L
local V, CF, A, rad = L.V, L.CF, L.A, math.rad
local t0 = os.clock()
local town = workspace:FindFirstChild('SpawnTown') or Instance.new('Folder')
town.Name = 'SpawnTown'; town.Parent = workspace
local hq = town:FindFirstChild('SkullHQ'); if hq then hq:Destroy() end
hq = L.model(town, 'SkullHQ')
local oldtmp = workspace:FindFirstChild('_csg'); if oldtmp then oldtmp:Destroy() end
local tmp = Instance.new('Folder'); tmp.Name = '_csg'; tmp.Parent = workspace

local Z0 = -575
local S = 1.8   -- whole HQ is built at base scale, then scaled up 1.8x about its ground centre
local G = 18   -- plateau top (fixed so reruns are idempotent)
-- dark anime-style stone: charcoal skull, ashen teeth
local BONE = Color3.fromRGB(66,58,60)
-- undo any earlier raise, then swap grass->ground under the hall (material only, no height change)
do
	local T = workspace.Terrain
	T:FillBlock(CF(0, G + 6, Z0 - 14*S), V(100*S, 12, 100*S), Enum.Material.Air)
	local half = V(50*S, 0, 50*S)
	local c = V(0, 0, Z0 - 14*S)
	local r = Region3.new(c - half + V(0, G - 8, 0), c + half + V(0, G + 4, 0)):ExpandToGrid(4)
	T:ReplaceMaterial(r, 4, Enum.Material.Grass, Enum.Material.Ground)
	T:ReplaceMaterial(r, 4, Enum.Material.LeafyGrass, Enum.Material.Ground)
end
local function O(x,y,z) return V(x, G + y, Z0 + z) end
local function pos(list, size, cf, shape)
	local p = Instance.new('Part'); p.Anchored = true; p.Size = size; p.CFrame = cf
	if shape then p.Shape = shape end
	p.Parent = tmp; table.insert(list, p); return p
end
local function ball(list, d, at) return pos(list, V(d,d,d), CF(at), Enum.PartType.Ball) end

-- ===== positive volumes =====
local plus = {}
ball(plus, 132, O(0, 84, -10))                -- cranium
ball(plus, 112, O(0, 66, 18))                 -- face mass
ball(plus, 62, O(-34, 48, 30)); ball(plus, 62, O(34, 48, 30))   -- cheekbones (embedded, smooth)
ball(plus, 90, O(0, 32, 26))                  -- upper jaw / maxilla (rounded)
ball(plus, 124, O(0, 42, -14))                -- rounded base (gives hall walls)
pos(plus, V(33, 104, 104), CF(O(0, 13.5, -14))*A(0,0,rad(90)), Enum.PartType.Cylinder)
-- heavy brow ridge: rounded horizontal cylinders in a menacing V
pos(plus, V(34, 15, 15), CF(O(-20, 82, 58))*A(0, rad(-14), rad(-16)), Enum.PartType.Cylinder)
pos(plus, V(34, 15, 15), CF(O(20, 82, 58))*A(0, rad(14), rad(16)), Enum.PartType.Cylinder)
ball(plus, 18, O(0, 78, 60))

local first = table.remove(plus, 1)
local shell = first:UnionAsync(plus)
shell.Parent = tmp

-- ===== negative volumes =====
local minus = {}
-- sockets are shallow bowls (no inner ball) so they never break through into the hall -> no light leaks
ball(minus, 36, O(-25, 66, 62))
ball(minus, 36, O(25, 66, 62))
-- nose: inverted-heart triangle from two rotated blocks
pos(minus, V(9, 26, 40), CF(O(-4, 45, 66))*A(0,0,rad(-18)))
pos(minus, V(9, 26, 40), CF(O(4, 45, 66))*A(0,0,rad(18)))
-- mouth doorway: rectangle + round arch, tunnelling into the hall
pos(minus, V(34, 24, 90), CF(O(0, 12, 50)))
pos(minus, V(90, 34, 34), CF(O(0, 24, 50))*A(0, rad(90), 0)*A(0,0,rad(90)), Enum.PartType.Cylinder)
-- great hall interior: round hall (r=46) stays inside the base shell everywhere -> walls fully closed
ball(minus, 110, O(0, 84, -10))
pos(minus, V(52, 92, 92), CF(O(0, 26, -14))*A(0,0,rad(90)), Enum.PartType.Cylinder)
pos(minus, V(40, 24, 36), CF(O(0, 12, 22)))
-- flatten bottom (sits on plateau)
-- flatten bottom: shell sinks 3 studs into the plateau so no daylight gap at the base
pos(minus, V(400, 40, 400), CF(O(0, -23, 0)))
local carved = shell:SubtractAsync(minus)
carved.Name = 'SkullShell'
carved.UsePartColor = true
carved.Color = BONE
carved.Material = L.M.slate
carved.Anchored = true
carved.CollisionFidelity = Enum.CollisionFidelity.PreciseConvexDecomposition
carved.RenderFidelity = Enum.RenderFidelity.Precise
carved.Parent = hq
tmp:Destroy()

-- ===== eyes: dark recess + glowing cores + wisps =====
local function eye(sx)
	local back = L.ball(hq, 26, CF(O(sx*25, 66, 54)), Color3.fromRGB(10,8,12), L.M.slate)
	back.CanCollide = false
	local core = L.ball(hq, 8, CF(O(sx*25, 65, 56)), Color3.fromRGB(176,70,255), L.M.neon)
	core.Name = 'EyeCore'; core.CanCollide = false
	local halo = L.ball(hq, 13, CF(O(sx*25, 65, 56)), Color3.fromRGB(140,60,230), L.M.neon)
	halo.Transparency = 0.86; halo.CanCollide = false
	L.light(core, Color3.fromRGB(170,80,255), 1.6, 26, false)
	local pe = Instance.new('ParticleEmitter')
	pe.Color = ColorSequence.new(Color3.fromRGB(200,120,255), Color3.fromRGB(90,30,200))
	pe.LightEmission = 1; pe.Rate = 18; pe.Lifetime = NumberRange.new(1.5, 2.6)
	pe.Speed = NumberRange.new(2, 5); pe.SpreadAngle = Vector2.new(25, 25)
	pe.Size = NumberSequence.new({NumberSequenceKeypoint.new(0, 2.2), NumberSequenceKeypoint.new(1, 0)})
	pe.Transparency = NumberSequence.new({NumberSequenceKeypoint.new(0, 0.3), NumberSequenceKeypoint.new(1, 1)})
	pe.Acceleration = V(0, 3, 0); pe.EmissionDirection = Enum.NormalId.Front
	pe.Parent = core
end
eye(-1); eye(1)
-- nose cavity backing
local nb = L.part(hq, V(14, 20, 2), CF(O(0, 44, 52)), Color3.fromRGB(26,22,22), L.M.slate)

-- ===== teeth (upper row hangs over the door, lower row flanks it) =====
local toothC = Color3.fromRGB(150,140,128)
local function tooth(x, yTop, z, w, h, down, yaw)
	local m = L.model(hq, 'Tooth')
	local cf = CF(O(x, yTop, z))*A(0, yaw or 0, 0)
	if down then
		L.part(m, V(w, h*0.65, 5), cf*CF(0, -h*0.325, 0), toothC, L.M.marble)
		L.wedge(m, V(w, h*0.35, 2.5), cf*CF(0, -h*0.65 - h*0.175, 1.25)*A(math.pi, 0, 0), toothC, L.M.marble)
		L.wedge(m, V(w, h*0.35, 2.5), cf*CF(0, -h*0.65 - h*0.175, -1.25)*A(math.pi, math.pi, 0), toothC, L.M.marble)
	else
		L.part(m, V(w, h*0.65, 5), cf*CF(0, h*0.325, 0), toothC, L.M.marble)
		L.wedge(m, V(w, h*0.35, 2.5), cf*CF(0, h*0.65 + h*0.175, -1.25), toothC, L.M.marble)
		L.wedge(m, V(w, h*0.35, 2.5), cf*CF(0, h*0.65 + h*0.175, 1.25)*A(0, math.pi, 0), toothC, L.M.marble)
	end
end
-- upper row along mouth top (door top y=24..41 arch); teeth hang from y=34 at z~64
for i, x in ipairs({-30, -22.5, -15, 15, 22.5, 30}) do
	local h = (math.abs(x) < 20) and 14 or 11
	tooth(x, 36, 62 - math.abs(x)*0.25, 6.6, h, true, rad(-x*0.6))
end
for i, x in ipairs({-7.5, 0, 7.5}) do tooth(x, 41, 64, 6.6, 8, true) end
-- lower row: standing teeth either side of the door
for i, x in ipairs({-38, -30.5, -23, 23, 30.5, 38}) do
	tooth(x, 0, 60 - math.abs(x)*0.3, 6.4, 10 + (40 - math.abs(x))*0.15, false, rad(-x*0.6))
end
-- gum line ridge across the mouth top
-- (gum plank removed: read as a flat board)

-- ===== cracks (dark seams) =====
local crackC = Color3.fromRGB(70,62,56)
local function crack(a, b) local p = L.beam(hq, O(a.X,a.Y,a.Z), O(b.X,b.Y,b.Z), 0.9, crackC, L.M.slate, 0.9); p.CanCollide = false end
-- (surface cracks omitted: straight beams float off the curved shell)

-- ===== horns: curved, tapering, attached at the temples =====
local function bez(p0, p1, p2, p3, t)
	local u = 1 - t
	return p0*(u*u*u) + p1*(3*u*u*t) + p2*(3*u*t*t) + p3*(t*t*t)
end
local function horn(sx)
	local m = L.model(hq, sx < 0 and 'HornL' or 'HornR')
	local p0 = O(sx*50, 112, -6)
	local p1 = O(sx*82, 120, 0)
	local p2 = O(sx*104, 160, 12)
	local p3 = O(sx*92, 212, 36)
	local N = 22
	local prev = p0
	local r0, r1 = 15, 1.6
	for i = 1, N do
		local t = i/N
		local p = bez(p0, p1, p2, p3, t)
		local r = r0 + (r1 - r0)*t
		local dark = Color3.fromRGB(26 - t*10, 22 - t*8, 28 - t*8)
		local seg = L.part(m, V(r*2, r*2, (p - prev).Magnitude + r*0.4), CF((p + prev)/2, p), dark, L.M.basalt)
		seg.Shape = Enum.PartType.Cylinder
		seg.Size = V((p - prev).Magnitude + r*0.4, r*2, r*2)
		seg.CFrame = CF((p + prev)/2, p) * A(0, rad(90), 0)
		L.ball(m, r*2, CF(p), dark, L.M.basalt)
		-- ridged bands
		if i % 3 == 0 and t < 0.85 then
			local band = L.part(m, V(1.2, r*2.25, r*2.25), CF(p, p + (p - prev)) * A(0, rad(90), 0), Color3.fromRGB(70,60,66), L.M.basalt, Enum.PartType.Cylinder)
		end
		prev = p
	end
	L.ball(m, 30, CF(p0), BONE, L.M.slate)  -- socket boss blending into skull
	local tip = L.ball(m, 4.4, CF(p3), Color3.fromRGB(190,90,255), L.M.neon)
	L.light(tip, Color3.fromRGB(180,90,255), 3, 30)
	local pe = Instance.new('ParticleEmitter'); pe.Color = ColorSequence.new(Color3.fromRGB(210,140,255))
	pe.LightEmission = 1; pe.Rate = 10; pe.Lifetime = NumberRange.new(1, 2); pe.Speed = NumberRange.new(1, 3)
	pe.Size = NumberSequence.new(1.4, 0); pe.Transparency = NumberSequence.new(0.2, 1); pe.Parent = tip
end
horn(-1); horn(1)

-- ===== approach: stone stairs + door threshold =====
local stairC = Color3.fromRGB(150,144,134)
for k = 0, 3 do
	L.part(hq, V(56 - k*4, 1.2, 10), CF(O(0, 0.6 + k*1.2 - 1.2, 84 - k*8)), stairC, L.M.limestone, nil, 'Stair')
end
L.part(hq, V(44, 1, 60), CF(O(0, 0.2, 40)), Color3.fromRGB(120,40,50), L.M.fabric, nil, 'Carpet')
-- braziers flanking the entrance
for _, sx in ipairs({-1, 1}) do
	local b = L.model(hq, 'Brazier')
	local bp = O(sx*48, 0, 82)
	L.part(b, V(5, 2, 5), CF(bp + V(0,1,0)), L.C.stone, L.M.cobble)
	L.cyl(b, 10, 2, CF(bp + V(0,7,0)), L.C.iron, L.M.metal)
	L.cyl(b, 3, 7, CF(bp + V(0,13,0)), L.C.iron, L.M.metal)
	local fsrc = L.part(b, V(4,1,4), CF(bp + V(0,15,0)), Color3.fromRGB(255,120,40), L.M.neon)
	local f = Instance.new('Fire'); f.Size = 7; f.Heat = 9; f.Color = Color3.fromRGB(180,90,255); f.SecondaryColor = Color3.fromRGB(255,160,255); f.Parent = fsrc
	L.light(fsrc, Color3.fromRGB(190,110,255), 1.2, 22, false)
end

-- ===== GREAT HALL INTERIOR (built at base scale, scaled with the rest) =====
local inn = L.model(hq, 'Interior')
local FLOOR = Color3.fromRGB(40,36,42)
L.cyl(inn, 0.6, 90, CF(O(0, 0.3, -14)), FLOOR, L.M.slate)
-- inlaid floor ring + star (gold) under the dome
for k = 0, 35 do
	local a = k/36*math.pi*2
	L.part(inn, V(5.6, 0.12, 1), CF(O(math.cos(a)*30, 0.65, -14 + math.sin(a)*30))*A(0, -a + math.pi/2, 0), L.C.gold, L.M.metal)
end
-- two colonnades of stone pillars with bases and capitals
local PIL = Color3.fromRGB(70,64,72)
for _, sx in ipairs({-1, 1}) do
	for _, z in ipairs({-42, -26, -10, 6}) do
		local p = O(sx*30, 0, z)
		L.cyl(inn, 2, 8, CF(p + V(0, 1, 0)), PIL, L.M.slate)
		L.cyl(inn, 44, 5, CF(p + V(0, 24, 0)), PIL, L.M.slate)
		L.cyl(inn, 2.4, 8, CF(p + V(0, 46.6, 0)), PIL, L.M.slate)
		-- iron wall sconce (bracket + cup) with a small purple flame, facing the aisle
		local sp = p + V(-sx*3.4, 16, 0)
		L.part(inn, V(2.2, 0.5, 0.5), CF(sp + V(sx*1, -0.8, 0)), L.C.iron, L.M.metal)
		L.cyl(inn, 1, 1.6, CF(sp + V(0, -0.3, 0)), L.C.iron, L.M.metal)
		local s = L.part(inn, V(0.6, 0.4, 0.6), CF(sp + V(0, 0.3, 0)), Color3.fromRGB(190,110,255), L.M.neon, nil, 'Sconce')
		s.CanCollide = false
		local fi = Instance.new('Fire'); fi.Size = 2.5; fi.Heat = 5; fi.Color = Color3.fromRGB(170,80,255); fi.SecondaryColor = Color3.fromRGB(240,170,255); fi.Parent = s
		L.light(s, Color3.fromRGB(180,100,255), 0.9, 20, false)
		-- hanging banner on the aisle face of each pillar
		L.banner(inn, CF(p + V(-sx*2.9, 34, 0))*A(0, -sx*rad(90), 0), Color3.fromRGB(28,22,36), 16, Color3.fromRGB(170,110,255))
	end
end
-- red carpet aisle from the door to the dais
L.part(inn, V(10, 0.2, 44), CF(O(0, 0.7, -9)), Color3.fromRGB(120,30,44), L.M.fabric, nil, 'Aisle')
-- dais + throne at the back of the hall
local D = O(0, 0, -44)
for k = 0, 2 do L.cyl(inn, 1.2, 26 - k*5, CF(D + V(0, 0.6 + k*1.2, 0)), Color3.fromRGB(56,50,58), L.M.slate) end
local tb = D + V(0, 3.6, 0)
L.part(inn, V(8, 2.4, 7), CF(tb + V(0, 1.2, 0)), Color3.fromRGB(30,26,32), L.M.basalt, nil, 'ThroneSeat')
L.part(inn, V(8, 1, 6), CF(tb + V(0, 2.9, 0.3)), Color3.fromRGB(90,30,40), L.M.fabric)
L.part(inn, V(9, 18, 1.6), CF(tb + V(0, 10, -3.2)), Color3.fromRGB(30,26,32), L.M.basalt, nil, 'ThroneBack')
for _, sx in ipairs({-1, 1}) do
	L.part(inn, V(1.2, 3, 6), CF(tb + V(sx*4.4, 3.4, 0)), Color3.fromRGB(30,26,32), L.M.basalt)
	-- swept horn spikes on the throne back
	L.beam(inn, tb + V(sx*4, 18, -3.2), tb + V(sx*7.5, 25, -2), 1.2, Color3.fromRGB(24,20,26), L.M.basalt, 0.2)
end
local gem = L.ball(inn, 2.6, CF(tb + V(0, 16, -2.2)), Color3.fromRGB(176,70,255), L.M.neon)
L.light(gem, Color3.fromRGB(170,80,255), 1.4, 28, false)
-- grand chandelier under the dome
local ch = O(0, 64, -14)
L.cyl(inn, 20, 0.6, CF(ch + V(0, 10, 0)), L.C.iron, L.M.metal)
L.cyl(inn, 0.8, 22, CF(ch), L.C.iron, L.M.metal)
L.cyl(inn, 0.6, 14, CF(ch + V(0, -3, 0)), L.C.iron, L.M.metal)
for k = 0, 11 do
	local a = k/12*math.pi*2
	local c = L.part(inn, V(0.7, 1.6, 0.7), CF(ch + V(math.cos(a)*10.6, 1.2, math.sin(a)*10.6)), Color3.fromRGB(255,220,170), L.M.neon)
	c.CanCollide = false
end
L.light(L.part(inn, V(1, 1, 1), CF(ch + V(0, -1, 0)), L.C.iron, L.M.metal), Color3.fromRGB(255,200,150), 1.6, 60, true)
-- long tables for knights along the aisle
for _, sx in ipairs({-1, 1}) do
	local tcf = CF(O(sx*17, 0, -18))
	L.part(inn, V(5, 0.6, 34), tcf*CF(0, 3.4, 0), Color3.fromRGB(96,62,38), L.M.planks, nil, 'Table')
	for _, z in ipairs({-15, 0, 15}) do L.part(inn, V(4, 3.1, 0.8), tcf*CF(0, 1.55, z), Color3.fromRGB(70,46,30), L.M.wood) end
	for _, bx in ipairs({-4.2, 4.2}) do L.part(inn, V(1.6, 2, 32), tcf*CF(bx, 1, 0), Color3.fromRGB(84,56,34), L.M.planks, nil, 'Bench') end
end

-- ===== scale the whole HQ up about its ground centre =====
hq.WorldPivot = CF(O(0, 0, 0))
hq:ScaleTo(S)

local n = 0; for _, d in ipairs(hq:GetDescendants()) do if d:IsA('BasePart') then n = n + 1 end end
return string.format('skull ok parts=%d G=%.1f %.1fs', n, G, os.clock()-t0)
