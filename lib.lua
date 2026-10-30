--!nocheck
-- ===================== TOWN BUILDER LIBRARY =====================
local L = {}
local V, CF, A = Vector3.new, CFrame.new, CFrame.Angles
local rad = math.rad
L.V, L.CF, L.A = V, CF, A

local function M(name, fb)
	local ok, m = pcall(function() return Enum.Material[name] end)
	if ok and m then return m end
	return Enum.Material[fb]
end
L.M = {
	plaster = M('Plaster','SmoothPlastic'), brick = M('Brick','Brick'), cobble = M('Cobblestone','Cobblestone'),
	wood = M('Wood','Wood'), planks = M('WoodPlanks','WoodPlanks'), shingles = M('RoofShingles','Slate'),
	clay = M('ClayRoofTiles','Slate'), slate = M('Slate','Slate'), rock = M('Rock','Slate'), limestone = M('Limestone','Sandstone'),
	sandstone = M('Sandstone','Sandstone'), marble = M('Marble','Marble'), metal = M('Metal','Metal'), iron = M('CorrodedMetal','Metal'),
	glass = M('Glass','Glass'), neon = M('Neon','Neon'), fabric = M('Fabric','Fabric'), grass = M('Grass','Grass'),
	leafy = M('LeafyGrass','Grass'), smooth = M('SmoothPlastic','SmoothPlastic'), pavement = M('Pavement','Concrete'),
	basalt = M('Basalt','Slate'), granite = M('Granite','Granite'), ground = M('Ground','Ground'), sand = M('Sand','Sand'),
	gold = M('Foil','Metal'), concrete = M('Concrete','Concrete'), leather = M('Leather','Fabric'),
}
local MAT = L.M
L.C = {
	beam = Color3.fromRGB(74,50,34), beamDark = Color3.fromRGB(52,36,26), stone = Color3.fromRGB(128,124,118),
	stoneLight = Color3.fromRGB(168,162,152), plasterA = Color3.fromRGB(236,226,204), plasterB = Color3.fromRGB(226,212,186),
	plasterC = Color3.fromRGB(240,234,222), plasterD = Color3.fromRGB(214,200,176), glass = Color3.fromRGB(70,96,120),
	roofRed = Color3.fromRGB(150,62,48), roofBlue = Color3.fromRGB(62,84,124), roofBrown = Color3.fromRGB(104,72,54),
	roofGreen = Color3.fromRGB(62,104,82), roofSlate = Color3.fromRGB(78,82,92), roofOrange = Color3.fromRGB(176,96,52),
	shutterGreen = Color3.fromRGB(58,96,70), shutterBlue = Color3.fromRGB(56,86,130), shutterRed = Color3.fromRGB(130,48,44),
	gold = Color3.fromRGB(212,170,72), iron = Color3.fromRGB(46,44,44), bone = Color3.fromRGB(228,220,198),
}
local C = L.C

function L.folder(parent, name)
	local f = parent:FindFirstChild(name)
	if f then f:Destroy() end
	f = Instance.new('Folder'); f.Name = name; f.Parent = parent
	return f
end
function L.model(parent, name)
	local m = Instance.new('Model'); m.Name = name; m.Parent = parent; return m
end
-- generic part
function L.part(parent, size, cf, color, material, shape, name)
	local p = Instance.new('Part')
	p.Anchored = true
	if shape then p.Shape = shape end
	p.Size = size; p.CFrame = cf
	p.Color = color or C.stone; p.Material = material or MAT.smooth
	p.TopSurface = Enum.SurfaceType.Smooth; p.BottomSurface = Enum.SurfaceType.Smooth
	p.Name = name or 'Part'
	p.Parent = parent
	return p
end
local P = L.part
function L.ball(parent, d, cf, color, material) return P(parent, V(d,d,d), cf, color, material, Enum.PartType.Ball, 'Ball') end
-- vertical cylinder (axis = Y): height h, diameter d
function L.cyl(parent, h, d, cf, color, material)
	return P(parent, V(h,d,d), cf * A(0,0,rad(90)), color, material, Enum.PartType.Cylinder, 'Cyl')
end
function L.wedge(parent, size, cf, color, material)
	local w = Instance.new('WedgePart'); w.Anchored = true; w.Size = size; w.CFrame = cf
	w.Color = color; w.Material = material; w.TopSurface = Enum.SurfaceType.Smooth; w.BottomSurface = Enum.SurfaceType.Smooth
	w.Parent = parent; return w
end
-- part spanning from point a to point b (thickness t x t)
function L.beam(parent, a, b, t, color, material, t2)
	local mid = (a + b) / 2
	local len = (b - a).Magnitude
	return P(parent, V(t, t2 or t, len), CF(mid, b), color, material)
end
function L.light(part, color, brightness, range, shadows)
	local l = Instance.new('PointLight'); l.Color = color; l.Brightness = brightness; l.Range = range
	l.Shadows = shadows or false; l.Parent = part; return l
end

-- ---------- WINDOW (cf = centre on wall exterior face, +Z outward) ----------
function L.window(parent, cf, ww, wh, o)
	o = o or {}
	local frameC = o.frame or C.beam
	local g = P(parent, V(ww, wh, 0.3), cf * CF(0,0,0.05), o.glassColor or C.glass, MAT.glass, nil, 'Glass')
	g.Reflectance = 0.15; g.Transparency = 0.15
	local t = 0.7
	P(parent, V(ww+t*2, t, 0.8), cf*CF(0, wh/2+t/2, 0.35), frameC, MAT.wood)
	P(parent, V(ww+t*2, t, 0.8), cf*CF(0, -wh/2-t/2, 0.35), frameC, MAT.wood)
	P(parent, V(t, wh, 0.8), cf*CF(-ww/2-t/2, 0, 0.35), frameC, MAT.wood)
	P(parent, V(t, wh, 0.8), cf*CF(ww/2+t/2, 0, 0.35), frameC, MAT.wood)
	P(parent, V(0.3, wh, 0.4), cf*CF(0,0,0.25), frameC, MAT.wood)
	P(parent, V(ww, 0.3, 0.4), cf*CF(0,wh*0.1,0.25), frameC, MAT.wood)
	-- sill
	P(parent, V(ww+2, 0.5, 1.4), cf*CF(0, -wh/2-t-0.25, 0.6), o.sill or C.stoneLight, MAT.limestone)
	-- shutters (opened)
	if o.shutters ~= false then
		local sc = o.shutterColor or C.shutterGreen
		local sw = ww*0.36
		P(parent, V(sw, wh+0.4, 0.3), cf*CF(-ww/2-t-sw/2-0.05, 0, 0.5), sc, MAT.planks, nil, 'Shutter')
		P(parent, V(sw, wh+0.4, 0.3), cf*CF(ww/2+t+sw/2+0.05, 0, 0.5), sc, MAT.planks, nil, 'Shutter')
	end
	-- flower box
	if o.flowers then
		local fy = -wh/2 - t - 1.3
		P(parent, V(ww+1.6, 1.4, 1.4), cf*CF(0, fy, 1.1), C.beam, MAT.planks, nil, 'FlowerBox')
		local cols = {Color3.fromRGB(230,70,90), Color3.fromRGB(250,210,70), Color3.fromRGB(240,240,250), Color3.fromRGB(180,90,220)}
		local n = math.max(3, math.floor(ww/1.4))
		for i = 1, n do
			local x = -ww/2 - 0.2 + (i-0.5)*((ww+0.4)/n)
			L.ball(parent, 1.0, cf*CF(x, fy+0.6, 1.1), Color3.fromRGB(70,130,60), MAT.leafy)
			L.ball(parent, 0.75, cf*CF(x, fy+1.15, 1.2), cols[(i % #cols)+1], MAT.smooth)
		end
	end
	if o.lit then
		g.Material = MAT.neon; g.Color = Color3.fromRGB(255,200,120); g.Transparency = 0.2
		L.light(g, Color3.fromRGB(255,200,130), 1, 14)
	end
end

-- ---------- DOOR (cf = bottom centre on wall exterior face, +Z outward) ----------
function L.door(parent, cf, dw, dh, o)
	o = o or {}
	local fc = o.frame or C.beamDark
	local d = P(parent, V(dw, dh, 0.6), cf*CF(0, dh/2, 0.1), o.color or Color3.fromRGB(96,62,38), MAT.planks, nil, 'Door')
	for i = -1, 1 do P(parent, V(0.25, dh, 0.2), cf*CF(i*dw/3, dh/2, 0.45), Color3.fromRGB(70,46,30), MAT.wood) end
	P(parent, V(dw*0.7, 0.4, 0.2), cf*CF(0, dh*0.25, 0.5), C.iron, MAT.metal)
	P(parent, V(dw*0.7, 0.4, 0.2), cf*CF(0, dh*0.75, 0.5), C.iron, MAT.metal)
	L.ball(parent, 0.6, cf*CF(dw*0.32, dh*0.48, 0.6), C.gold, MAT.metal)
	P(parent, V(dw+2, 1, 1), cf*CF(0, dh+0.5, 0.4), fc, MAT.wood)
	P(parent, V(1, dh, 1), cf*CF(-dw/2-0.5, dh/2, 0.4), fc, MAT.wood)
	P(parent, V(1, dh, 1), cf*CF(dw/2+0.5, dh/2, 0.4), fc, MAT.wood)
	if o.step ~= false then P(parent, V(dw+3, 0.8, 3), cf*CF(0, -0.4, 1.5), C.stoneLight, MAT.limestone, nil, 'Step') end
	if o.lantern then
		local lp = cf*CF(dw/2+2, dh*0.8, 0.8)
		P(parent, V(0.3, 0.3, 1.2), lp*CF(0,0,-0.2), C.iron, MAT.metal)
		local lb = P(parent, V(1, 1.4, 1), lp*CF(0,-0.6,0.5), Color3.fromRGB(255,200,120), MAT.neon, nil, 'Lantern')
		L.light(lb, Color3.fromRGB(255,190,110), 1.2, 16)
	end
	return d
end

-- ---------- TIMBER-FRAME WALL ----------
-- cf: bottom-centre of exterior face, +Z outward, +X along wall. bays: list of 'win','door','brace','x','plain'
function L.timberWall(parent, cf, len, h, bays, o)
	o = o or {}
	local wallC = o.wall or C.plasterA
	local bc = o.beamColor or C.beam
	P(parent, V(len, h, 1), cf*CF(0, h/2, -0.5), wallC, o.wallMat or MAT.plaster, nil, 'Wall')
	local bt = 0.9
	if o.timber ~= false then
		P(parent, V(len, bt, 0.6), cf*CF(0, bt/2, 0.3), bc, MAT.wood)
		P(parent, V(len, bt, 0.6), cf*CF(0, h-bt/2, 0.3), bc, MAT.wood)
	end
	local n = #bays
	local bw = len / n
	for i = 1, n do
		local x0 = -len/2 + (i-1)*bw
		local cx = x0 + bw/2
		if o.timber ~= false and i > 1 then P(parent, V(bt, h, 0.6), cf*CF(x0, h/2, 0.3), bc, MAT.wood) end
		local kind = bays[i]
		if kind == 'win' or kind == 'winF' then
			local ww = math.min(bw - 3.2, o.winW or 4.2)
			local wh = math.min(h - 4.5, o.winH or 5.2)
			L.window(parent, cf*CF(cx, h*0.56, 0), ww, wh, {flowers = (kind=='winF') or o.flowers, shutterColor = o.shutter, lit = o.lit, shutters = o.shutters})
			if o.timber ~= false then P(parent, V(bw, bt*0.8, 0.5), cf*CF(cx, h*0.56 - wh/2 - 1.6, 0.25), bc, MAT.wood) end
		elseif kind == 'door' then
			local dh = math.min(h - 2.5, o.doorH or 9)
			L.door(parent, cf, math.min(bw - 2.5, o.doorW or 5.5), dh, {lantern = true})
		elseif kind == 'brace' and o.timber ~= false then
			L.beam(parent, cf*V(x0+bt/2, bt, 0.3), cf*V(x0+bw-bt/2, h-bt, 0.3), 0.7, bc, MAT.wood, 0.5)
		elseif kind == 'x' and o.timber ~= false then
			L.beam(parent, cf*V(x0+bt/2, bt, 0.3), cf*V(x0+bw-bt/2, h-bt, 0.3), 0.7, bc, MAT.wood, 0.5)
			L.beam(parent, cf*V(x0+bw-bt/2, bt, 0.32), cf*V(x0+bt/2, h-bt, 0.32), 0.7, bc, MAT.wood, 0.5)
		end
	end
end

-- ---------- GABLE ROOF ----------
-- cf: centre of the roof base (top of walls), ridge along local X. lenR = gable-to-gable length, span = width across ridge
function L.gableRoof(parent, cf, lenR, span, pH, o)
	o = o or {}
	local rc = o.roof or C.roofRed
	local rm = o.roofMat or MAT.shingles
	local wallC = o.wall or C.plasterA
	local ov = o.overhang or 2.2
	local t = 1.3
	local half = span/2
	local a = math.atan2(pH, half)
	-- gable triangles (two wedges per end), flush with gable walls
	for _, sx in ipairs({-1, 1}) do
		local gx = sx * (lenR/2 - 0.5)
		L.wedge(parent, V(1, pH, half), cf*CF(gx, pH/2, -half/2), wallC, o.wallMat or MAT.plaster)
		L.wedge(parent, V(1, pH, half), cf*CF(gx, pH/2, half/2)*A(0, math.pi, 0), wallC, o.wallMat or MAT.plaster)
		if o.timber ~= false then
			local fx = sx * (lenR/2 + 0.15)
			P(parent, V(0.6, 0.9, span), cf*CF(fx, 0.45, 0), C.beam, MAT.wood)
			P(parent, V(0.6, pH*0.85, 0.9), cf*CF(fx, pH*0.425, 0), C.beam, MAT.wood)
			L.beam(parent, cf*V(fx, 0.9, -half*0.5), cf*V(fx, pH*0.55, 0), 0.6, C.beam, MAT.wood, 0.5)
			L.beam(parent, cf*V(fx, 0.9, half*0.5), cf*V(fx, pH*0.55, 0), 0.6, C.beam, MAT.wood, 0.5)
		end
		-- barge boards following the slope
		local bx = sx * (lenR/2 + ov - 0.3)
		for _, sz in ipairs({-1, 1}) do
			local top = cf*V(bx, pH + 0.6, 0)
			local eave = cf*V(bx, pH - (half+ov)*math.tan(a) + 0.6, sz*(half+ov))
			L.beam(parent, top, eave, 0.8, o.barge or C.beamDark, MAT.wood, 1.6)
		end
	end
	-- roof slabs
	local run = half + ov
	local L2 = run / math.cos(a) + 0.4
	for _, sz in ipairs({-1, 1}) do
		local dir = V(0, -math.sin(a), sz*math.cos(a))
		local nrm = V(0, math.cos(a), sz*math.sin(a))
		local ridge = V(0, pH, 0)
		local c = ridge + dir*(L2/2 - 0.4) + nrm*(t/2)
		local rot = (sz > 0) and A(a, 0, 0) or A(-a, 0, 0)
		P(parent, V(lenR + ov*2, t, L2), cf*CF(c)*rot, rc, rm, nil, 'Roof')
		-- eave fascia
		local e = ridge + dir*(L2 - 0.4) + nrm*(t/2)
		P(parent, V(lenR + ov*2, 1.4, 0.6), cf*CF(e)*rot, o.barge or C.beamDark, MAT.wood)
	end
	-- ridge cap
	P(parent, V(lenR + ov*2 + 0.6, 1.5, 1.5), cf*CF(0, pH + t*0.9, 0)*A(rad(45),0,0), o.ridge or Color3.new(rc.R*0.7, rc.G*0.7, rc.B*0.7), rm, nil, 'Ridge')
	if o.finials then
		for _, sx in ipairs({-1,1}) do
			L.ball(parent, 1.6, cf*CF(sx*(lenR/2+ov), pH+t*0.9+1, 0), C.gold, MAT.metal)
		end
	end
end

-- ---------- CHIMNEY ----------
function L.chimney(parent, baseCF, height, smoke)
	P(parent, V(3.6, height, 3.6), baseCF*CF(0, height/2, 0), Color3.fromRGB(140,96,80), MAT.brick, nil, 'Chimney')
	P(parent, V(4.4, 0.8, 4.4), baseCF*CF(0, height + 0.4, 0), C.stone, MAT.cobble)
	P(parent, V(2.4, 0.6, 2.4), baseCF*CF(0, height + 1.1, 0), Color3.fromRGB(40,36,34), MAT.slate)
	if smoke then
		local emitPart = P(parent, V(1,1,1), baseCF*CF(0, height + 1.5, 0), Color3.new(), MAT.smooth, nil, 'SmokeSrc')
		emitPart.Transparency = 1; emitPart.CanCollide = false
		local s = Instance.new('Smoke'); s.Color = Color3.fromRGB(200,200,205); s.Opacity = 0.12; s.RiseVelocity = 4; s.Size = 2.5; s.Parent = emitPart
	end
end

-- ---------- HOUSE ----------
-- cf: ground centre, front faces local +Z.  o: w,d,floors,fh,wall,roof,shutter,jetty,ridgeZ,pitch,chimney,flowers,stoneGround
function L.house(parent, cf, o)
	local m = L.model(parent, o.name or 'House')
	local w, d = o.w or 24, o.d or 18
	local floors = o.floors or 2
	local fh = o.fh or 11
	local found = 1.6
	P(m, V(w+2, found, d+2), cf*CF(0, found/2 - 0.3, 0), C.stone, MAT.cobble, nil, 'Foundation')
	local y = found - 0.3
	local fw, fd = w, d
	local function bayList(len, isFront, ground)
		local n = math.max(2, math.floor(len / 7.5 + 0.5))
		local t = {}
		for i = 1, n do
			if isFront then t[i] = ((i % 2 == 1) == (n % 2 == 1)) and 'win' or 'brace'
			else t[i] = (i % 2 == 0) and 'win' or 'brace' end
		end
		if isFront then
			for i = 1, n do if t[i] == 'win' then t[i] = o.flowers and 'winF' or 'win' end end
			if ground then t[math.floor((n+1)/2)] = 'door' end
		end
		return t, n
	end
	for f = 1, floors do
		local j = (o.jetty and f > 1) and 1.4 or 0
		fw, fd = w + j*2, d + j*2
		local stone = (o.stoneGround and f == 1)
		local wo = {wall = stone and C.stoneLight or (o.wall or C.plasterA), wallMat = stone and MAT.cobble or MAT.plaster,
			timber = not stone, shutter = o.shutter, flowers = false, lit = o.lit}
		local bf = cf*CF(0, y, 0)
		local fb = bayList(fw, true, f == 1)
		L.timberWall(m, bf*CF(0,0,fd/2), fw, fh, fb, wo)
		local bb = bayList(fw, false)
		L.timberWall(m, bf*CF(0,0,-fd/2)*A(0,math.pi,0), fw, fh, bb, wo)
		local sb = bayList(fd - 2, false)
		L.timberWall(m, bf*CF(fw/2,0,0)*A(0,rad(90),0), fd - 2, fh, sb, wo)
		L.timberWall(m, bf*CF(-fw/2,0,0)*A(0,rad(-90),0), fd - 2, fh, sb, wo)
		-- windows w/ flower boxes on front upper floors
		if o.flowers and f > 1 then
			-- add flower boxes under existing front windows: re-run front with flowers
		end
		-- corner posts
		for _, sx in ipairs({-1,1}) do for _, sz in ipairs({-1,1}) do
			P(m, V(1.4, fh, 1.4), bf*CF(sx*(fw/2-0.3), fh/2, sz*(fd/2-0.3)), stone and C.stone or C.beam, stone and MAT.cobble or MAT.wood, nil, 'Post')
		end end
		-- floor band / jetty corbels
		if f > 1 then
			P(m, V(fw+0.6, 1.2, fd+0.6), bf*CF(0, 0.2, 0), C.beamDark, MAT.wood, nil, 'FloorBand')
			if j > 0 then
				for k = -2, 2 do
					local x = k * (fw/5)
					L.wedge(m, V(0.9, 1.6, 1.6), bf*CF(x, -0.8, fd/2 - 0.8)*A(0, math.pi, 0)*A(0,0,0), C.beamDark, MAT.wood)
				end
			end
		end
		y = y + fh
	end
	-- roof
	local pitch = o.pitch or 0.62
	local topCF = cf*CF(0, y, 0)
	local lenR, span = fw, fd
	if o.ridgeZ then topCF = topCF*A(0, rad(90), 0); lenR, span = fd, fw end
	local pH = span/2 * pitch * 2 * 0.6
	L.gableRoof(m, topCF, lenR, span, pH, {roof = o.roof, wall = o.wall or C.plasterA, finials = o.finials})
	if o.chimney ~= false then
		L.chimney(m, topCF*CF(lenR/2 - 3.5, 0, -span/4), pH + 3, true)
	end
	m.PrimaryPart = m:FindFirstChild('Foundation')
	return m
end

-- ---------- NATURE ----------
local rng = Random.new(1337)
L.rng = rng
function L.tree(parent, pos, s, kind)
	s = s or 1
	local m = L.model(parent, 'Tree')
	local trunkC = Color3.fromRGB(96,70,50)
	if kind == 'pine' then
		L.cyl(m, 10*s, 2.2*s, CF(pos + V(0, 5*s, 0)), trunkC, MAT.wood)
		local tiers = 5
		for i = 1, tiers do
			local r = (13 - i*2)*s
			local hh = 6*s
			local yy = (6 + i*4.6)*s
			local cone = L.cyl(m, hh, r*2, CF(pos + V(0, yy, 0))*A(0, rng:NextNumber()*6, 0), Color3.fromRGB(38 + i*4, 92 + i*6, 58), MAT.leafy)
		end
		L.ball(m, 3*s, CF(pos + V(0, 33*s, 0)), Color3.fromRGB(58,124,72), MAT.leafy)
	else
		local lean = A(rad(rng:NextNumber(-6,6)), 0, rad(rng:NextNumber(-6,6)))
		local base = CF(pos)*lean
		L.cyl(m, 9*s, 3*s, base*CF(0, 4.5*s, 0), trunkC, MAT.wood)
		L.cyl(m, 8*s, 2.2*s, base*CF(0, 12*s, 0), trunkC, MAT.wood)
		-- roots
		for i = 1, 4 do
			local ang = i*math.pi/2 + rng:NextNumber()
			P(m, V(1.2*s, 1.2*s, 4*s), base*CF(math.cos(ang)*1.6*s, 0.4*s, math.sin(ang)*1.6*s)*A(0, -ang + math.pi/2, 0)*A(rad(-20),0,0), trunkC, MAT.wood)
		end
		-- branches
		for i = 1, 3 do
			local ang = i*2.1 + rng:NextNumber()
			local from = base*V(0, 11*s, 0)
			local to = base*V(math.cos(ang)*6*s, 17*s, math.sin(ang)*6*s)
			L.beam(m, from, to, 1.1*s, trunkC, MAT.wood)
		end
		local greens = {Color3.fromRGB(76,140,62), Color3.fromRGB(92,156,70), Color3.fromRGB(64,124,58), Color3.fromRGB(110,168,76)}
		local blobs = {{0,20,0,15},{5,18,2,11},{-5,18,-2,11},{2,17,-5,10},{-2,18,5,10},{0,25,0,10},{4,23,-3,8},{-4,23,3,8}}
		for i, b in ipairs(blobs) do
			L.ball(m, b[4]*s*rng:NextNumber(0.9,1.1), base*CF(b[1]*s, b[2]*s, b[3]*s), greens[(i % #greens)+1], MAT.leafy)
		end
	end
	return m
end
function L.bush(parent, pos, s)
	s = s or 1
	local m = L.model(parent, 'Bush')
	local g = {Color3.fromRGB(70,130,58), Color3.fromRGB(86,146,64)}
	L.ball(m, 5*s, CF(pos + V(0,1.8*s,0)), g[1], MAT.leafy)
	L.ball(m, 4*s, CF(pos + V(2*s,1.4*s,0.8*s)), g[2], MAT.leafy)
	L.ball(m, 3.6*s, CF(pos + V(-1.8*s,1.3*s,-0.6*s)), g[2], MAT.leafy)
	if rng:NextNumber() < 0.5 then
		for i = 1, 4 do L.ball(m, 0.8*s, CF(pos + V(rng:NextNumber(-2,2)*s, 3.4*s, rng:NextNumber(-1.5,1.5)*s)), Color3.fromRGB(240,120,150), MAT.smooth) end
	end
	return m
end
function L.rock(parent, pos, s)
	local m = L.model(parent, 'Rock')
	local cols = {Color3.fromRGB(120,118,112), Color3.fromRGB(104,102,98), Color3.fromRGB(136,132,124)}
	for i = 1, 3 do
		local sz = V(rng:NextNumber(4,7)*s, rng:NextNumber(3,5)*s, rng:NextNumber(4,7)*s)
		P(m, sz, CF(pos + V(rng:NextNumber(-2,2)*s, sz.Y*0.35, rng:NextNumber(-2,2)*s))*A(rng:NextNumber(-0.4,0.4), rng:NextNumber(0,6), rng:NextNumber(-0.4,0.4)), cols[i], MAT.rock)
	end
	return m
end
function L.flowers(parent, center, radius, count)
	local m = L.model(parent, 'Flowers')
	local cols = {Color3.fromRGB(235,80,100), Color3.fromRGB(250,215,80), Color3.fromRGB(245,245,255), Color3.fromRGB(170,110,235), Color3.fromRGB(255,150,70)}
	for i = 1, count do
		local a = rng:NextNumber()*math.pi*2; local r = math.sqrt(rng:NextNumber())*radius
		local p = center + V(math.cos(a)*r, 0, math.sin(a)*r)
		local stem = P(m, V(0.2, 1.4, 0.2), CF(p + V(0,0.7,0)), Color3.fromRGB(70,130,60), MAT.smooth)
		stem.CanCollide = false
		local h = L.ball(m, 0.8, CF(p + V(0,1.5,0)), cols[rng:NextInteger(1,#cols)], MAT.smooth); h.CanCollide = false
	end
	return m
end

-- ---------- PROPS ----------
function L.barrel(parent, cf)
	local m = L.model(parent, 'Barrel')
	L.cyl(m, 5, 4, cf*CF(0,2.5,0), Color3.fromRGB(122,82,50), MAT.planks)
	L.cyl(m, 4, 4.4, cf*CF(0,2.5,0), Color3.fromRGB(116,78,48), MAT.planks)
	for _, yy in ipairs({0.7, 4.3}) do L.cyl(m, 0.4, 4.3, cf*CF(0,yy,0), C.iron, MAT.metal) end
	L.cyl(m, 0.2, 3.8, cf*CF(0,5.05,0), Color3.fromRGB(96,64,40), MAT.wood)
	return m
end
function L.crate(parent, cf, s)
	s = s or 4
	local m = L.model(parent, 'Crate')
	P(m, V(s,s,s), cf*CF(0,s/2,0), Color3.fromRGB(150,110,70), MAT.planks)
	local t = 0.45
	for _, a in ipairs({{1,1},{1,-1},{-1,1},{-1,-1}}) do
		P(m, V(t+0.05, s+0.1, t+0.05), cf*CF(a[1]*(s/2-t/2), s/2, a[2]*(s/2-t/2)), Color3.fromRGB(96,66,42), MAT.wood)
	end
	for _, yy in ipairs({t/2, s-t/2}) do
		P(m, V(s+0.1, t, t+0.05), cf*CF(0,yy,s/2-t/2), Color3.fromRGB(96,66,42), MAT.wood)
		P(m, V(s+0.1, t, t+0.05), cf*CF(0,yy,-s/2+t/2), Color3.fromRGB(96,66,42), MAT.wood)
		P(m, V(t+0.05, t, s+0.1), cf*CF(s/2-t/2,yy,0), Color3.fromRGB(96,66,42), MAT.wood)
		P(m, V(t+0.05, t, s+0.1), cf*CF(-s/2+t/2,yy,0), Color3.fromRGB(96,66,42), MAT.wood)
	end
	return m
end
function L.haybale(parent, cf, round)
	local m = L.model(parent, 'Haybale')
	local hc = Color3.fromRGB(214,184,98)
	if round then
		P(m, V(5, 6, 6), cf*CF(0,3,0), hc, MAT.sand, Enum.PartType.Cylinder)
		P(m, V(4.6, 6.1, 6.1), cf*CF(0,3,0), Color3.fromRGB(196,166,86), MAT.sand, Enum.PartType.Cylinder).Transparency = 0.5
	else
		P(m, V(6, 3.4, 3.6), cf*CF(0,1.7,0), hc, MAT.sand)
		for _, x in ipairs({-1.6, 1.6}) do P(m, V(0.25, 3.5, 3.7), cf*CF(x,1.7,0), Color3.fromRGB(150,120,70), MAT.fabric) end
	end
	return m
end
function L.lamp(parent, pos)
	local m = L.model(parent, 'LampPost')
	local ic = Color3.fromRGB(36,34,34)
	P(m, V(2.4, 1.2, 2.4), CF(pos + V(0,0.6,0)), C.stone, MAT.cobble)
	L.cyl(m, 14, 0.8, CF(pos + V(0,8,0)), ic, MAT.metal)
	L.cyl(m, 1, 1.4, CF(pos + V(0,1.6,0)), ic, MAT.metal)
	P(m, V(5, 0.4, 0.4), CF(pos + V(1.8,14.6,0)), ic, MAT.metal)
	L.beam(m, pos + V(0,12.6,0), pos + V(2.2,14.4,0), 0.3, ic, MAT.metal)
	local lp = pos + V(3.8,12.6,0)
	P(m, V(0.2,1.2,0.2), CF(lp + V(0,1.6,0)), ic, MAT.metal)
	P(m, V(1.9,0.3,1.9), CF(lp + V(0,1.0,0)), ic, MAT.metal)
	for _, q in ipairs({{1,1},{1,-1},{-1,1},{-1,-1}}) do
		P(m, V(0.22,2,0.22), CF(lp + V(q[1]*0.8,0,q[2]*0.8)), ic, MAT.metal)
	end
	L.wedge(m, V(1.9,0.9,0.95), CF(lp + V(0,1.6,0.475))*A(0,math.pi,0), ic, MAT.metal)
	L.wedge(m, V(1.9,0.9,0.95), CF(lp + V(0,1.6,-0.475)), ic, MAT.metal)
	local g = P(m, V(1.2,1.6,1.2), CF(lp), Color3.fromRGB(255,206,130), MAT.neon, nil, 'Glow')
	g.Transparency = 0.15
	L.light(g, Color3.fromRGB(255,196,128), 1.6, 26, true)
	P(m, V(1.9,0.3,1.9), CF(lp - V(0,1.1,0)), ic, MAT.metal)
	return m
end
function L.bench(parent, cf)
	local m = L.model(parent, 'Bench')
	P(m, V(8, 0.6, 2.4), cf*CF(0,2.2,0), Color3.fromRGB(140,98,62), MAT.planks)
	P(m, V(8, 2, 0.5), cf*CF(0,3.6,-1.1)*A(rad(-10),0,0), Color3.fromRGB(140,98,62), MAT.planks)
	for _, x in ipairs({-3.4, 3.4}) do P(m, V(0.6, 2.2, 2.4), cf*CF(x,1.1,0), C.iron, MAT.metal) end
	return m
end
function L.fence(parent, a, b, o)
	o = o or {}
	local m = L.model(parent, 'Fence')
	local len = (b - a).Magnitude
	local n = math.max(1, math.floor(len / 7))
	local fc = o.color or Color3.fromRGB(120,86,56)
	for i = 0, n do
		local p = a:Lerp(b, i/n)
		P(m, V(0.9, 5, 0.9), CF(p + V(0,2.5,0)), fc, MAT.wood)
		L.wedge(m, V(0.9,0.6,0.45), CF(p + V(0,5.3,0.225))*A(0,math.pi,0), fc, MAT.wood)
		L.wedge(m, V(0.9,0.6,0.45), CF(p + V(0,5.3,-0.225)), fc, MAT.wood)
	end
	L.beam(m, a + V(0,3.8,0), b + V(0,3.8,0), 0.5, fc, MAT.wood, 0.9)
	L.beam(m, a + V(0,1.9,0), b + V(0,1.9,0), 0.5, fc, MAT.wood, 0.9)
	return m
end
function L.cart(parent, cf, load)
	local m = L.model(parent, 'Cart')
	local wc = Color3.fromRGB(128,90,56)
	P(m, V(7, 0.6, 11), cf*CF(0,3.4,0), wc, MAT.planks)
	P(m, V(0.5, 2, 11), cf*CF(3.3,4.6,0), wc, MAT.planks)
	P(m, V(0.5, 2, 11), cf*CF(-3.3,4.6,0), wc, MAT.planks)
	P(m, V(7, 2, 0.5), cf*CF(0,4.6,-5.3), wc, MAT.planks)
	for _, x in ipairs({-4, 4}) do
		local wheel = L.part(m, V(0.8, 6, 6), cf*CF(x, 3, 1), Color3.fromRGB(90,62,40), MAT.wood, Enum.PartType.Cylinder)
		L.part(m, V(1.0, 1.5, 1.5), cf*CF(x, 3, 1), C.iron, MAT.metal, Enum.PartType.Cylinder)
	end
	L.beam(m, cf*V(-1.5, 3.2, 5.5), cf*V(-1.5, 2.4, 12), 0.6, wc, MAT.wood)
	L.beam(m, cf*V(1.5, 3.2, 5.5), cf*V(1.5, 2.4, 12), 0.6, wc, MAT.wood)
	if load == 'hay' then
		P(m, V(6, 3, 9), cf*CF(0,5.2,-0.5), Color3.fromRGB(214,184,98), MAT.sand)
	elseif load == 'goods' then
		L.crate(m, cf*CF(-1.5,3.7,-2.5), 3); L.crate(m, cf*CF(1.4,3.7,-2.6), 3); L.barrel(m, cf*CF(0,3.7,2.2))
	end
	return m
end
function L.stall(parent, cf, awning, goods)
	local m = L.model(parent, 'Stall')
	local wc = Color3.fromRGB(132,92,58)
	P(m, V(14, 4, 5), cf*CF(0,2,1.5), wc, MAT.planks)
	P(m, V(14.6, 0.5, 5.6), cf*CF(0,4.25,1.5), Color3.fromRGB(110,76,48), MAT.wood)
	for _, x in ipairs({-6.6, 6.6}) do
		P(m, V(0.8, 12, 0.8), cf*CF(x, 6, 3.8), wc, MAT.wood)
		P(m, V(0.8, 14, 0.8), cf*CF(x, 7, -2.6), wc, MAT.wood)
	end
	-- striped awning
	local stripes = 6
	local aw = 15/stripes
	local c2 = Color3.fromRGB(245,238,225)
	for i = 1, stripes do
		local x = -7.5 + (i-0.5)*aw
		P(m, V(aw, 0.35, 8.4), cf*CF(x, 13.3, 0.8)*A(rad(14),0,0), (i % 2 == 0) and c2 or awning, MAT.fabric)
		L.wedge(m, V(aw, 1.4, 0.3), cf*CF(x, 11.9, 4.9)*A(0,math.pi,0)*A(rad(180),0,0), (i % 2 == 0) and c2 or awning, MAT.fabric)
	end
	-- goods: detailed displays rotate through kinds
	L._stallN = (L._stallN or 0) + 1
	local kinds = {'apples', 'veg', 'bread', 'cheese', 'oranges', 'potions', 'cloth', 'pottery', 'fish'}
	for i = 1, 4 do
		local x = -5.25 + (i-1)*3.5
		P(m, V(3.2, 0.6, 3), cf*CF(x, 4.8, 1.6), Color3.fromRGB(150,110,70), MAT.planks)
		L.goods(m, cf*CF(x, 5.1, 1.6), kinds[((L._stallN*3 + i) % #kinds) + 1])
	end
	L.crate(m, cf*CF(-8.5, 0, 3), 3); L.barrel(m, cf*CF(8.6, 0, 3))
	return m
end

-- ===== detailed market goods: cf = centre of the display surface (top face), ~3x3 footprint =====
local function goodsBall(m, d, cf, col, mat) local b = L.ball(m, d, cf, col, mat or MAT.smooth); b.CanCollide = false; return b end
local function goodsPart(m, s, cf, col, mat, shape) local p = P(m, s, cf, col, mat or MAT.smooth, shape); p.CanCollide = false; return p end
local function basket(m, cf, d)
	goodsPart(m, V(0.9, d, d), cf*CF(0, 0.45, 0)*A(0, 0, rad(90)), Color3.fromRGB(150,108,62), MAT.fabric, Enum.PartType.Cylinder)
	goodsPart(m, V(0.25, d + 0.25, d + 0.25), cf*CF(0, 0.95, 0)*A(0, 0, rad(90)), Color3.fromRGB(112,78,44), MAT.wood, Enum.PartType.Cylinder)
	for k = 0, 5 do
		local a = k/6*math.pi*2
		goodsPart(m, V(0.12, 0.9, 0.18), cf*CF(math.cos(a)*d/2, 0.45, math.sin(a)*d/2)*A(0, -a, 0), Color3.fromRGB(96,66,38), MAT.wood)
	end
end
local function mound(m, cf, d, ballD, cols, stem)
	local r0 = d/2 - ballD/2 - 0.05
	local layers = {{r0, 7, 0}, {r0*0.5, 4, ballD*0.75}, {0, 1, ballD*1.45}}
	local n = 0
	for _, ly in ipairs(layers) do
		for k = 0, ly[2] - 1 do
			n = n + 1
			local a = k/ly[2]*math.pi*2 + ly[3]
			local p = cf*CF(math.cos(a)*ly[1], ly[3] + ballD/2, math.sin(a)*ly[1])
			goodsBall(m, ballD, p, cols[(n % #cols) + 1])
			if stem and n % 2 == 0 then goodsPart(m, V(0.08, 0.25, 0.08), p*CF(0, ballD/2 + 0.08, 0), Color3.fromRGB(70,50,30), MAT.wood) end
		end
	end
end
function L.goods(parent, cf, kind)
	local m = L.model(parent, 'Goods')
	if kind == 'apples' or kind == 'oranges' then
		basket(m, cf, 2.4)
		local cols = (kind == 'apples') and {Color3.fromRGB(196,36,34), Color3.fromRGB(170,28,30), Color3.fromRGB(214,70,40), Color3.fromRGB(150,186,60)}
			or {Color3.fromRGB(242,140,30), Color3.fromRGB(230,120,24), Color3.fromRGB(250,170,50)}
		mound(m, cf*CF(0, 0.95, 0), 2.4, 0.68, cols, kind == 'apples')
		if kind == 'apples' then goodsPart(m, V(0.05, 0.3, 0.5), cf*CF(0.2, 2.5, 0.1)*A(rad(30), 0, 0), Color3.fromRGB(60,120,50), MAT.grass) end
	elseif kind == 'veg' then
		basket(m, cf*CF(-0.6, 0, 0), 1.8)
		for k = 0, 2 do
			local p = cf*CF(-0.6 + (k - 1)*0.5, 1.35, (k % 2)*0.4 - 0.2)
			goodsBall(m, 0.95, p, Color3.fromRGB(120,170,70), MAT.leafy)
			goodsBall(m, 0.7, p*CF(0, 0.12, 0), Color3.fromRGB(160,200,100), MAT.smooth)
		end
		for k = 0, 5 do
			local p = cf*CF(0.9, 0.18, -1 + k*0.4)*A(0, rad(k*7), 0)
			goodsPart(m, V(1.5, 0.28, 0.28), p*A(0, 0, 0), Color3.fromRGB(236,118,30), MAT.smooth, Enum.PartType.Cylinder)
			goodsPart(m, V(0.5, 0.1, 0.35), p*CF(-0.95, 0.05, 0), Color3.fromRGB(80,150,60), MAT.grass)
		end
	elseif kind == 'bread' then
		goodsPart(m, V(2.8, 0.12, 2.4), cf*CF(0, 0.06, 0), Color3.fromRGB(230,220,196), MAT.fabric)
		for k = 0, 2 do
			local p = cf*CF(0, 0.45, -0.8 + k*0.8)*A(0, rad(-8 + k*8), 0)
			goodsPart(m, V(1.8, 0.75, 0.75), p, Color3.fromRGB(196,132,62), MAT.smooth, Enum.PartType.Cylinder)
			for s = -1, 1 do goodsPart(m, V(0.08, 0.1, 0.55), p*CF(s*0.45, 0.36, 0)*A(0, rad(35), 0), Color3.fromRGB(236,196,130), MAT.smooth) end
		end
		local b = cf*CF(0.9, 1.05, 0.2)
		goodsPart(m, V(0.5, 1.1, 1.1), b*A(0, 0, rad(90)), Color3.fromRGB(176,112,52), MAT.smooth, Enum.PartType.Cylinder)
		goodsBall(m, 1.05, b*CF(0, 0.2, 0), Color3.fromRGB(186,122,58))
	elseif kind == 'potions' then
		local cols = {Color3.fromRGB(150,60,230), Color3.fromRGB(60,200,120), Color3.fromRGB(230,60,80), Color3.fromRGB(60,140,240), Color3.fromRGB(250,190,40)}
		for k = 0, 5 do
			local p = cf*CF(-0.9 + (k % 3)*0.9, 0, (k < 3) and -0.5 or 0.5)
			local d = (k % 2 == 0) and 0.8 or 0.65
			local g = goodsBall(m, d, p*CF(0, d/2, 0), Color3.fromRGB(220,235,245), MAT.glass); g.Transparency = 0.45
			goodsBall(m, d*0.72, p*CF(0, d/2 - 0.04, 0), cols[(k % #cols) + 1], MAT.neon)
			goodsPart(m, V(0.45, 0.24, 0.24), p*CF(0, d + 0.18, 0)*A(0, 0, rad(90)), Color3.fromRGB(220,235,245), MAT.glass, Enum.PartType.Cylinder).Transparency = 0.3
			goodsPart(m, V(0.18, 0.3, 0.3), p*CF(0, d + 0.46, 0)*A(0, 0, rad(90)), Color3.fromRGB(150,110,70), MAT.wood, Enum.PartType.Cylinder)
		end
	elseif kind == 'cloth' then
		local cols = {Color3.fromRGB(150,40,48), Color3.fromRGB(56,86,130), Color3.fromRGB(70,40,120), Color3.fromRGB(212,170,72), Color3.fromRGB(58,96,70)}
		for k = 0, 2 do goodsPart(m, V(2.4, 0.7, 0.7), cf*CF(0, 0.35, -0.8 + k*0.8), cols[k + 1], MAT.fabric, Enum.PartType.Cylinder) end
		for k = 0, 1 do goodsPart(m, V(2.4, 0.7, 0.7), cf*CF(0, 0.95, -0.4 + k*0.8), cols[k + 4], MAT.fabric, Enum.PartType.Cylinder) end
	elseif kind == 'pottery' then
		local cols = {Color3.fromRGB(176,96,58), Color3.fromRGB(150,78,48), Color3.fromRGB(196,170,130)}
		for k = 0, 2 do
			local p = cf*CF(-0.85 + k*0.85, 0, (k == 1) and 0.4 or -0.3)
			local c = cols[k + 1]
			goodsPart(m, V(1, 0.85, 0.85), p*CF(0, 0.5, 0)*A(0, 0, rad(90)), c, MAT.slate, Enum.PartType.Cylinder)
			goodsBall(m, 0.95, p*CF(0, 1.05, 0), c, MAT.slate)
			goodsPart(m, V(0.5, 0.42, 0.42), p*CF(0, 1.6, 0)*A(0, 0, rad(90)), c, MAT.slate, Enum.PartType.Cylinder)
			goodsPart(m, V(0.1, 0.5, 0.5), p*CF(0, 1.85, 0)*A(0, 0, rad(90)), c:Lerp(Color3.new(0,0,0), 0.2), MAT.slate, Enum.PartType.Cylinder)
			L.beam(m, p*V(0.2, 1.7, 0), p*V(0.55, 1.1, 0), 0.12, c, MAT.slate)
		end
	elseif kind == 'cheese' then
		for k = 0, 2 do
			goodsPart(m, V(0.55, 1.5, 1.5), cf*CF(-0.5 + (k % 2)*0.7, 0.28 + math.floor(k/2)*0.56, (k % 2)*0.3)*A(0, 0, rad(90)), Color3.fromRGB(238,196,80), MAT.smooth, Enum.PartType.Cylinder)
		end
		goodsPart(m, V(0.55, 1.5, 1.5), cf*CF(0.9, 0.28, -0.6)*A(0, 0, rad(90)), Color3.fromRGB(220,120,50), MAT.smooth, Enum.PartType.Cylinder)
		L.wedge(m, V(0.5, 0.5, 0.7), cf*CF(1, 0.25, 0.8), Color3.fromRGB(250,220,120), MAT.smooth).CanCollide = false
	elseif kind == 'fish' then
		goodsPart(m, V(2.8, 0.3, 2.4), cf*CF(0, 0.15, 0), Color3.fromRGB(110,80,52), MAT.planks)
		goodsPart(m, V(2.5, 0.2, 2.1), cf*CF(0, 0.38, 0), Color3.fromRGB(220,236,245), MAT.sand)
		for k = 0, 3 do
			local p = cf*CF(-0.2, 0.6, -0.75 + k*0.5)*A(0, rad(k*10 - 15), 0)
			goodsPart(m, V(1.6, 0.36, 0.42), p, Color3.fromRGB(160,170,180), MAT.metal, Enum.PartType.Cylinder)
			goodsPart(m, V(0.5, 0.36, 0.42), p*CF(0.85, 0, 0), Color3.fromRGB(130,140,150), MAT.metal, Enum.PartType.Ball)
			L.wedge(m, V(0.08, 0.5, 0.5), p*CF(-0.95, 0, 0)*A(0, rad(90), 0), Color3.fromRGB(120,130,140), MAT.metal).CanCollide = false
		end
	end
	return m
end
function L.banner(parent, cf, color, h, emblemColor)
	-- v2: folded cloth (zig-zag panels), pointed tail + tassel, gold trim, rod with finials, cord, clover crest
	local m = L.model(parent, 'Banner')
	h = h or 12
	local W, n, th = 5.6, 5, rad(13)
	local sw = W/n
	local tail = math.min(3.2, h*0.26)
	local dark = color:Lerp(Color3.new(0,0,0), 0.18)
	local GOLD = C.gold
	local function drop(x) return tail*(1 - math.abs(x)/(W/2)) end
	for i = 0, n-1 do
		local xl, xr = -W/2 + sw*i, -W/2 + sw*(i+1)
		local xc = (xl + xr)/2
		local yaw = ((i % 2 == 0) and 1 or -1)*th
		local dl, dr = drop(xl), drop(xr)
		local mn, df = math.min(dl, dr), math.abs(dl - dr)
		local scf = cf*CF(xc, 0, 0)*A(0, yaw, 0)
		local col = (i % 2 == 0) and color or dark
		local pw = sw/math.cos(th) + 0.04
		P(m, V(pw, h + mn, 0.2), scf*CF(0, -mn/2, 0), col, MAT.fabric, nil, 'Cloth')
		if df > 0.05 then
			local s = (dr > dl) and 1 or -1
			local base = scf*CF(0, -h/2 - mn - df/2, 0)
			local ex, ey, ez = base.RightVector, base.UpVector, base.LookVector*-1
			local w = Instance.new('WedgePart'); w.Anchored = true; w.Size = V(0.2, df, pw)
			w.CFrame = CFrame.fromMatrix(base.Position, ez*s, -ey)
			w.Color = col; w.Material = MAT.fabric; w.TopSurface = Enum.SurfaceType.Smooth; w.BottomSurface = Enum.SurfaceType.Smooth
			w.Name = 'Tail'; w.Parent = m
		end
		-- gold piping along the top hem of each panel
		P(m, V(pw, 0.45, 0.28), scf*CF(0, h/2 - 0.35, 0), GOLD, MAT.fabric, nil, 'Hem')
		P(m, V(pw, 0.9, 0.24), scf*CF(0, h/2 - 1.1, 0), dark:Lerp(Color3.new(0,0,0), 0.3), MAT.fabric, nil, 'Band')
	end
	-- gold edging down both outer edges (panels at the ends sit slightly forward/back because of the folds)
	local ez0 = math.sin(th)*(sw/math.cos(th))/2
	for _, sx in ipairs({-1, 1}) do P(m, V(0.3, h - 0.4, 0.3), cf*CF(sx*(W/2 - 0.1), -0.2, -sx*ez0), GOLD, MAT.fabric, nil, 'Edge') end
	-- tassel at the tail point
	local tp = cf*CF(0, -h/2 - tail + 0.15, 0)
	L.ball(m, 0.6, tp, GOLD, MAT.metal)
	P(m, V(0.35, 1.2, 0.35), tp, GOLD, MAT.fabric, Enum.PartType.Cylinder).CFrame = tp*CF(0, -0.75, 0)*A(0, 0, rad(90))
	-- rod, finials, rings, hanging cord
	local rod = cf*CF(0, h/2 + 0.35, 0)
	P(m, V(W + 1.6, 0.5, 0.5), rod, Color3.fromRGB(70,46,30), MAT.wood, Enum.PartType.Cylinder, 'Rod')
	for _, sx in ipairs({-1, 1}) do
		L.ball(m, 0.85, rod*CF(sx*(W/2 + 0.95), 0, 0), GOLD, MAT.metal)
		P(m, V(0.35, 0.75, 0.75), rod*CF(sx*(W/2 - 0.6), 0, 0), GOLD, MAT.metal, Enum.PartType.Cylinder)
		L.beam(m, (rod*CF(sx*(W/2 + 0.4), 0, 0)).Position, (rod*CF(0, 2.2, 0)).Position, 0.14, GOLD, MAT.fabric)
	end
	L.ball(m, 0.5, rod*CF(0, 2.25, 0), C.iron, MAT.metal)
	if emblemColor then
		-- crest: gold ring, dark disc, four heart leaves, curled stem
		local c0 = cf*CF(0, h*0.08, 0.48)
		local function disc(d, at, col, t) local p = P(m, V(t or 0.1, d, d), at*A(0, rad(90), 0), col, MAT.smooth, Enum.PartType.Cylinder, 'Crest') return p end
		disc(4.2, c0, GOLD, 0.12)
		disc(3.7, c0*CF(0, 0, 0.04), dark:Lerp(Color3.new(0,0,0), 0.35), 0.12)
		for k = 0, 3 do
			local a = rad(45 + k*90)
			local d = V(math.cos(a), math.sin(a), 0)
			local pp = V(-d.Y, d.X, 0)
			for _, s in ipairs({-1, 1}) do
				local q = d*0.82 + pp*0.33*s
				disc(0.95, c0*CF(q.X, q.Y, 0.1), emblemColor, 0.1)
			end
			local q = d*0.42
			P(m, V(0.62, 0.62, 0.1), c0*CF(q.X, q.Y, 0.1)*A(0, 0, a + rad(45)), emblemColor, MAT.smooth, nil, 'Crest')
		end
		disc(0.5, c0*CF(0, 0, 0.14), GOLD, 0.1)
		P(m, V(0.22, 1.3, 0.1), c0*CF(0.25, -1.15, 0.1)*A(0, 0, rad(-18)), emblemColor, MAT.smooth, nil, 'Crest')
		P(m, V(0.22, 0.6, 0.1), c0*CF(0.6, -1.85, 0.1)*A(0, 0, rad(-60)), emblemColor, MAT.smooth, nil, 'Crest')
		-- small gold chevron below the crest
		for _, s in ipairs({-1, 1}) do P(m, V(1.8, 0.3, 0.1), cf*CF(s*0.75, -h*0.28, 0.48)*A(0, 0, rad(-s*22)), GOLD, MAT.smooth, nil, 'Chevron') end
	end
	for _, d in ipairs(m:GetDescendants()) do if d:IsA('BasePart') then d.CanCollide = false end end
	return m
end

_G.L = L
local gp = RaycastParams.new(); gp.FilterType = Enum.RaycastFilterType.Include; gp.FilterDescendantsInstances = {workspace.Terrain}
gp.IgnoreWater = true
function L.ground(x, z)
	local r = workspace:Raycast(V(x, 400, z), V(0, -800, 0), gp)
	return r and r.Position.Y or 2
end
function L.at(x, z, yaw) return CF(x, L.ground(x, z), z) * A(0, yaw or 0, 0) end
