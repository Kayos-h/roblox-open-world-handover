local L = _G.L
local V, CF, A, rad = L.V, L.CF, L.A, math.rad
local P = L.part
local town = workspace:FindFirstChild('SpawnTown')
local f = L.folder(town, 'Walls')
local W = 425          -- wall line (S, E, W sides)
local WN = 760         -- north wall line (map extended north for the giant skull HQ)
local H = 24           -- wall height above ground
local T = 8            -- thickness
local STONE = Color3.fromRGB(150,144,134)
local STONE2 = Color3.fromRGB(128,122,114)
local CAP = Color3.fromRGB(170,164,154)
local ROOF = Color3.fromRGB(62,78,118)
local PURPLE = Color3.fromRGB(70,40,120)
local function riverZ(x) return 250 + 22*math.sin(x/90) end

-- wall run along local X at frame cf (local +Z = outward), from x=a to x=b
local function wallRun(parent, cf, a, b)
	local seg = 16
	local n = math.max(1, math.floor((b - a)/seg + 0.5))
	local sl = (b - a)/n
	for i = 0, n-1 do
		local cx = a + (i + 0.5)*sl
		local wp = cf*V(cx, 0, 0)
		local g = L.ground(wp.X, wp.Z)
		local base = math.min(g, 2) - 8
		local top = 2 + H
		local c = cf*CF(cx, 0, 0)
		local wc = CF(wp.X, 0, wp.Z) * (c - c.Position)
		P(parent, V(sl + 0.05, top - base, T), wc*CF(0, (top + base)/2, 0), (i % 2 == 0) and STONE or STONE2, L.M.limestone, nil, 'Wall')
		-- plinth batter
		P(parent, V(sl + 0.05, 4, T + 3), wc*CF(0, g + 1, 0), STONE2, L.M.cobble, nil, 'Plinth')
		-- string course
		P(parent, V(sl + 0.05, 1, T + 1), wc*CF(0, top - 0.5, 0), CAP, L.M.limestone)
		-- walkway (inner)
		P(parent, V(sl + 0.05, 0.6, T - 2), wc*CF(0, top + 0.3, -0.6), Color3.fromRGB(110,104,98), L.M.cobble, nil, 'Walk')
		-- outer crenellations: 2 merlons per segment
		for k = 0, 1 do
			local mx = -sl/2 + sl*(k*2 + 1)/4
			P(parent, V(sl/4 + 0.6, 4.4, 1.8), wc*CF(mx, top + 2.2, T/2 - 0.9), STONE, L.M.limestone, nil, 'Merlon')
			P(parent, V(sl/4 + 1.0, 0.6, 2.2), wc*CF(mx, top + 4.7, T/2 - 0.9), CAP, L.M.limestone)
		end
		-- low inner parapet
		P(parent, V(sl + 0.05, 2.4, 1.2), wc*CF(0, top + 1.2, -T/2 + 0.6), STONE2, L.M.limestone)
		-- arrow slit on outer face
		if i % 2 == 1 then P(parent, V(1.2, 5, 0.4), wc*CF(0, top - 9, T/2 + 0.05), Color3.fromRGB(26,24,24), L.M.slate, nil, 'Slit') end
	end
end

local function cone(parent, pos, d, h, color)
	local tiers = 9
	for i = 0, tiers-1 do
		local t = i/tiers
		L.cyl(parent, h/tiers + 0.2, d*(1 - t) + 0.6, CF(pos + V(0, h*t + h/tiers/2, 0)), color, L.M.slate)
	end
	L.cyl(parent, 4, 0.5, CF(pos + V(0, h + 2, 0)), L.C.iron, L.M.metal)
	L.ball(parent, 1.4, CF(pos + V(0, h + 4.2, 0)), L.C.gold, L.M.metal)
end

local function tower(x, z, d, ht)
	local m = L.model(f, 'Tower')
	local g = math.min(L.ground(x, z), 2)
	local top = 2 + ht
	L.cyl(m, top - g + 8, d, CF(x, (top + g - 8)/2, z), STONE, L.M.limestone)
	L.cyl(m, 5, d + 3, CF(x, g + 1.5, z), STONE2, L.M.cobble)
	-- banding
	for _, yy in ipairs({top*0.45, top - 0.5}) do L.cyl(m, 1.2, d + 1, CF(x, yy, z), CAP, L.M.limestone) end
	-- machicolated crown
	L.cyl(m, 3, d + 4, CF(x, top + 1.5, z), STONE2, L.M.limestone)
	local K = 12
	for k = 0, K-1 do
		local a = k/K*math.pi*2
		local r = d/2 + 1.2
		P(m, V(3.4, 4, 1.8), CF(x + math.cos(a)*r, top + 5, z + math.sin(a)*r)*A(0, -a + math.pi/2, 0), STONE, L.M.limestone, nil, 'Merlon')
		-- windows (slits) around
		if k % 3 == 0 then
			P(m, V(1.6, 6, 0.6), CF(x + math.cos(a)*(d/2 + 0.1), top*0.7, z + math.sin(a)*(d/2 + 0.1))*A(0, -a + math.pi/2, 0), Color3.fromRGB(26,24,24), L.M.slate, nil, 'Slit')
		end
	end
	-- conical roof on a recessed drum
	L.cyl(m, 6, d - 6, CF(x, top + 6, z), STONE2, L.M.limestone)
	cone(m, V(x, top + 9, z), d - 1, d*0.95, ROOF)
	-- flag on top
	local pole = V(x, top + 9 + d*0.95 + 4, z)
	L.cyl(m, 10, 0.4, CF(pole + V(0, 5, 0)), L.C.iron, L.M.metal)
	P(m, V(0.2, 3.4, 6), CF(pole + V(0, 8, 3)), PURPLE, L.M.fabric, nil, 'Flag')
	return m
end

local function gatehouse(cf, name)
	local m = L.model(f, name)
	local gw, gh = 30, 26     -- opening
	local tw = 22             -- flanking tower width
	local top = 2 + H + 10
	for _, sx in ipairs({-1, 1}) do
		local c = cf*CF(sx*(gw/2 + tw/2), 0, 0)
		P(m, V(tw, top + 8, tw), c*CF(0, (top - 8)/2, 0), STONE, L.M.limestone, nil, 'GateTower')
		P(m, V(tw + 3, 5, tw + 3), c*CF(0, 2.5, 0), STONE2, L.M.cobble)
		P(m, V(tw + 2, 1.2, tw + 2), c*CF(0, top - 0.6, 0), CAP, L.M.limestone)
		for k = -1, 1 do
			for _, sz in ipairs({-1, 1}) do
				P(m, V(4.4, 4.4, 1.8), c*CF(k*7.6, top + 2.2, sz*(tw/2 + 0.2)), STONE, L.M.limestone, nil, 'Merlon')
				P(m, V(1.8, 4.4, 4.4), c*CF(sz*(tw/2 + 0.2), top + 2.2, k*7.6), STONE, L.M.limestone, nil, 'Merlon')
			end
		end
		-- pyramid-ish roof (stacked slabs)
		for i = 0, 15 do
			local s = (tw + 3)*(1 - i/16) + 0.4
			P(m, V(s, 1.05, s), c*CF(0, top + 5.5 + i*1.0, 0), ROOF, L.M.slate, nil, 'Roof')
		end
		L.cyl(m, 5, 0.5, c*CF(0, top + 23, 0), L.C.iron, L.M.metal)
		L.ball(m, 1.6, c*CF(0, top + 26, 0), L.C.gold, L.M.metal)
		-- windows and banners on outer face
		L.window(m, c*CF(0, top - 9, tw/2 + 0.1), 3.6, 5, {shutters = false, lit = true})
		L.banner(m, c*CF(0, 15, tw/2 + 0.6), PURPLE, 14, L.C.gold)
		-- torch sconce at gate side
		local tp = c*CF(-sx*(tw/2 - 1.5), 12, tw/2 + 1.2)
		local fp = P(m, V(1.4, 1, 1.4), tp, Color3.fromRGB(255,140,60), L.M.neon, nil, 'Torch')
		local fire = Instance.new('Fire'); fire.Size = 3; fire.Heat = 6; fire.Parent = fp
		L.light(fp, Color3.fromRGB(255,170,90), 1.2, 22, false)
		P(m, V(0.6, 2.4, 1.4), tp*CF(0, -1.6, -0.6), L.C.iron, L.M.metal)
	end
	-- lintel block + arch ring over the opening
	local over = top - (2 + gh)
	P(m, V(gw + 1, over, tw - 2), cf*CF(0, 2 + gh + over/2, 0), STONE2, L.M.limestone, nil, 'Lintel')
	local K = 14
	for k = 0, K do
		local a = math.pi*k/K
		for _, sz in ipairs({-1, 1}) do
			P(m, V(3.8, 2.4, 1.2), cf*CF(math.cos(a)*(gw/2 - 1), 2 + gh - 6 + math.sin(a)*7, sz*(tw/2 - 0.6))*A(0, 0, a - math.pi/2), (k % 2 == 0) and CAP or STONE, L.M.limestone, nil, 'Voussoir')
		end
	end
	-- arch infill corners (make the opening read as a round-headed arch)
	for _, sx in ipairs({-1, 1}) do
		for k = 1, 6 do
			local ax = gw/2 - k*1.4 + 0.7
			local hh = 6 - 7*math.sqrt(math.max(0, 1 - (ax/(gw/2 - 1))^2))
			if hh > 0.3 then
				P(m, V(1.45, hh, tw - 3), cf*CF(sx*ax, 2 + gh - hh/2, 0), STONE2, L.M.limestone)
			end
		end
	end
	-- raised portcullis (bars visible at the top of the opening)
	for k = -6, 6 do
		P(m, V(0.6, 7, 0.6), cf*CF(k*2.2, 2 + gh - 3.5, tw/2 - 3), L.C.iron, L.M.iron, nil, 'Portcullis')
		L.wedge(m, V(0.6, 1.2, 0.6), cf*CF(k*2.2, 2 + gh - 7.6, tw/2 - 3)*A(math.pi, 0, 0), L.C.iron, L.M.iron)
	end
	P(m, V(gw, 0.6, 0.6), cf*CF(0, 2 + gh - 5, tw/2 - 3), L.C.iron, L.M.iron)
	-- big open doors swung inward against the passage walls
	for _, sx in ipairs({-1, 1}) do
		local d = P(m, V(1.2, gh - 4, gw/2 - 1), cf*CF(sx*(gw/2 - 0.8), 2 + (gh - 4)/2, -tw/2 - gw/4 + 1), Color3.fromRGB(96,62,38), L.M.planks, nil, 'GateDoor')
		for _, yy in ipairs({0.25, 0.5, 0.75}) do
			P(m, V(1.5, 0.8, gw/2 - 1), cf*CF(sx*(gw/2 - 0.8), 2 + (gh - 4)*yy, -tw/2 - gw/4 + 1), L.C.iron, L.M.metal)
		end
	end
	-- crest plaque
	local crest = P(m, V(10, 10, 0.6), cf*CF(0, 2 + gh + over/2 + 1, tw/2 - 0.6)*A(0, 0, rad(45)), Color3.fromRGB(60,36,104), L.M.slate, nil, 'Crest')
	P(m, V(6, 6, 0.8), cf*CF(0, 2 + gh + over/2 + 1, tw/2 - 0.5)*A(0, 0, rad(45)), L.C.gold, L.M.metal)
	-- walkway over the gate
	P(m, V(gw, 0.6, tw - 4), cf*CF(0, top + 0.3, 0), Color3.fromRGB(110,104,98), L.M.cobble)
	return m
end

-- ===== frames for the 4 sides (local +Z outward, local X along the wall) =====
local sides = {
	{name = 'S', cf = CF(0, 0, W), a = -W, b = W},
	{name = 'N', cf = CF(0, 0, -WN)*A(0, math.pi, 0), a = -W, b = W},
	-- E frame: world z = -localX ; W frame: world z = localX
	{name = 'E', cf = CF(W, 0, 0)*A(0, rad(90), 0), a = -W, b = WN},
	{name = 'W', cf = CF(-W, 0, 0)*A(0, rad(-90), 0), a = -WN, b = W},
}
local gateGap = 26 + 22  -- half opening incl. gate towers
for _, s in ipairs(sides) do
	local wf = L.model(f, 'Wall_' .. s.name)
	local cuts = {}
	if s.name ~= 'N' then table.insert(cuts, {-gateGap, gateGap}) end
	-- river crossings (E and W sides)
	if s.name == 'E' or s.name == 'W' then
		local xr = (s.name == 'E') and W or -W
		local rz = riverZ(xr)
		-- local X for E frame: world z = -localX ; for W: world z = localX
		local lx = (s.name == 'E') and -rz or rz
		table.insert(cuts, {lx - 26, lx + 26})
	end
	table.sort(cuts, function(a, b) return a[1] < b[1] end)
	local x = s.a
	for _, c in ipairs(cuts) do
		if c[1] > x then wallRun(wf, s.cf, x, c[1]) end
		x = c[2]
	end
	if x < s.b then wallRun(wf, s.cf, x, s.b) end
	-- water gates over the river
	if s.name == 'E' or s.name == 'W' then
		local xr = (s.name == 'E') and W or -W
		local rz = riverZ(xr)
		local lx = (s.name == 'E') and -rz or rz
		local c = s.cf*CF(lx, 0, 0)
		local wg = L.model(f, 'WaterGate_' .. s.name)
		P(wg, V(52, 12, T), c*CF(0, 2 + H - 6, 0), STONE, L.M.limestone, nil, 'Span')
		P(wg, V(52, 1, T + 1), c*CF(0, 2 + H - 0.5, 0), CAP, L.M.limestone)
		P(wg, V(52, 0.6, T - 2), c*CF(0, 2 + H + 0.3, -0.6), Color3.fromRGB(110,104,98), L.M.cobble)
		for k = -5, 5 do P(wg, V(4.4, 4.4, 1.8), c*CF(k*4.7, 2 + H + 2.2, T/2 - 0.9), STONE, L.M.limestone, nil, 'Merlon') end
		for k = -11, 11 do P(wg, V(0.7, 22, 0.7), c*CF(k*2.2, 2 + H - 23, T/2 - 1), L.C.iron, L.M.iron, nil, 'Grate') end
		P(wg, V(52, 0.8, 0.8), c*CF(0, 2 + H - 20, T/2 - 1), L.C.iron, L.M.iron)
		P(wg, V(52, 0.8, 0.8), c*CF(0, 2 + H - 30, T/2 - 1), L.C.iron, L.M.iron)
	end
end

-- corner towers + intermediate towers (skip gates and river)
local towers = {}
for _, sx in ipairs({-1, 1}) do
	table.insert(towers, {sx*W, W, 30, 40}); table.insert(towers, {sx*W, -WN, 30, 40})
end
for _, t in ipairs({-210, 210}) do
	table.insert(towers, {t, W, 22, 32}); table.insert(towers, {t, -WN, 22, 32})
	table.insert(towers, {W, t, 22, 32}); table.insert(towers, {-W, t, 22, 32})
end
for _, t in ipairs({-105, 105}) do table.insert(towers, {t, -WN, 22, 32}) end
-- extra towers along the lengthened E/W walls
for _, t in ipairs({-405, -590}) do table.insert(towers, {W, t, 22, 32}); table.insert(towers, {-W, t, 22, 32}) end
for _, t in ipairs(towers) do
	-- avoid placing on the river or gates
	local ok = true
	if math.abs(t[1]) == W and math.abs(t[2] - riverZ(t[1])) < 34 then ok = false end
	if ok then tower(t[1], t[2], t[3], t[4]) end
end
-- towers flanking the water gates
for _, xr in ipairs({W, -W}) do
	local rz = riverZ(xr)
	tower(xr, rz - 30, 20, 30); tower(xr, rz + 30, 20, 30)
end

-- gatehouses (local +Z outward)
gatehouse(CF(0, 0, W), 'SouthGate')
gatehouse(CF(W, 0, 0)*A(0, rad(90), 0), 'EastGate')
gatehouse(CF(-W, 0, 0)*A(0, rad(-90), 0), 'WestGate')

local n = 0; for _, d in ipairs(f:GetDescendants()) do if d:IsA('BasePart') then n = n + 1 end end
return 'walls ok parts=' .. n
