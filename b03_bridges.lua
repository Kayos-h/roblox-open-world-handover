local L = _G.L
local V, CF, A, rad = L.V, L.CF, L.A, math.rad
local P = L.part
local town = workspace:FindFirstChild('SpawnTown') or Instance.new('Folder')
town.Name = 'SpawnTown'; town.Parent = workspace
local f = L.folder(town, 'Bridges')
local STONE = Color3.fromRGB(150,144,134)
local STONE2 = Color3.fromRGB(124,118,110)

local function riverZ(x) return 250 + 22*math.sin(x/90) end

-- ===== MAIN STONE BRIDGE (x=0) =====
local function stoneBridge(x, zc, width, span, rise)
	local m = L.model(f, 'StoneBridge')
	local y0 = 1.9
	local half = span/2
	local function yAt(dz) return y0 + rise*(1 - (dz/half)^2) end
	local N = 18
	for i = 0, N-1 do
		local za = -half + span*i/N; local zb = -half + span*(i+1)/N
		local pa = V(x, yAt(za), zc + za); local pb = V(x, yAt(zb), zc + zb)
		local mid = (pa + pb)/2; local len = (pb - pa).Magnitude + 0.3
		local cf = CF(mid, pb)
		-- deck (cobble) + structural body below
		P(m, V(width, 1.2, len), cf*CF(0, -0.6, 0), Color3.fromRGB(132,126,118), L.M.cobble, nil, 'Deck')
		P(m, V(width + 2, 2.4, len), cf*CF(0, -2.2, 0), STONE2, L.M.limestone, nil, 'Body')
		-- parapets
		for _, sx in ipairs({-1, 1}) do
			P(m, V(1.6, 3.4, len), cf*CF(sx*(width/2 + 0.2), 1.7, 0), STONE, L.M.limestone, nil, 'Parapet')
			P(m, V(2.2, 0.7, len), cf*CF(sx*(width/2 + 0.2), 3.75, 0), L.C.stoneLight, L.M.limestone, nil, 'Cap')
		end
	end
	-- arches: two openings, built as voussoir rings on each face, with a central pier
	local spans = {{-half*0.5, half*0.31}, {half*0.5, half*0.31}}
	for _, s in ipairs(spans) do
		local czz, r = s[1], s[2]
		local cy = -3
		for _, sx in ipairs({-1, 1}) do
			local K = 14
			for k = 0, K do
				local a = math.pi * k / K
				local p = V(x + sx*(width/2 + 0.6), cy + math.sin(a)*r, zc + czz + math.cos(a)*r)
				local blk = P(m, V(1.6, 2.2, 3.4), CF(p)*A(-(a - math.pi/2), 0, 0), (k % 2 == 0) and L.C.stoneLight or STONE, L.M.limestone, nil, 'Voussoir')
			end
		end
		-- spandrel fill above each arch, between arch and deck (solid walls on both faces with an arch-shaped look)
		for _, sx in ipairs({-1, 1}) do
			for k = 1, 6 do
				local dz = (k - 3.5)/3 * r
				local top = yAt(czz + dz) - 2
				local bot = cy + math.sqrt(math.max(0, r*r - dz*dz)) + 0.8
				if top > bot then
					P(m, V(1.4, top - bot, r/3 + 0.2), CF(x + sx*(width/2 + 0.3), (top + bot)/2, zc + czz + dz), STONE, L.M.limestone, nil, 'Spandrel')
				end
			end
		end
	end
	-- central pier with cutwaters
	P(m, V(width + 3, 19, 6), CF(x, -1.5, zc), STONE2, L.M.limestone, nil, 'Pier')
	for _, sx in ipairs({-1, 1}) do
		local w = P(m, V(4.4, 12, 4.4), CF(x + sx*(width/2 + 1.5), -5, zc)*A(0, rad(45), 0), STONE2, L.M.limestone, nil, 'Cutwater')
	end
	-- end abutments + newel posts with lanterns
	for _, sz in ipairs({-1, 1}) do
		local zz = zc + sz*(half + 2)
		for _, sx in ipairs({-1, 1}) do
			local px = x + sx*(width/2 + 0.6)
			P(m, V(3.6, 6, 3.6), CF(px, y0 + 3, zz), L.C.stoneLight, L.M.limestone, nil, 'Newel')
			P(m, V(4.2, 0.8, 4.2), CF(px, y0 + 6.4, zz), STONE, L.M.limestone)
			L.cyl(m, 4, 0.6, CF(px, y0 + 8.8, zz), L.C.iron, L.M.metal)
			local g = P(m, V(1.6, 2, 1.6), CF(px, y0 + 11.6, zz), Color3.fromRGB(255,206,130), L.M.neon, nil, 'Glow')
			P(m, V(2.4, 0.4, 2.4), CF(px, y0 + 10.5, zz), L.C.iron, L.M.metal)
			L.wedge(m, V(2.4, 1, 1.2), CF(px, y0 + 13.1, zz + 0.6)*A(0, math.pi, 0), L.C.iron, L.M.metal)
			L.wedge(m, V(2.4, 1, 1.2), CF(px, y0 + 13.1, zz - 0.6), L.C.iron, L.M.metal)
			L.light(g, Color3.fromRGB(255,196,128), 1.4, 24, false)
		end
		-- paved approach apron
		P(m, V(width + 6, 1, 8), CF(x, y0 - 0.4, zz + sz*3), Color3.fromRGB(132,126,118), L.M.cobble, nil, 'Apron')
	end
	-- banners hung on the outer faces at the crown
	for _, sx in ipairs({-1, 1}) do
		L.banner(m, CF(x + sx*(width/2 + 1.8), y0 + rise - 5, zc)*A(0, sx*rad(90), 0), Color3.fromRGB(70,40,120), 9, L.C.gold)
	end
	return m
end
stoneBridge(0, 250, 30, 64, 8)

-- ===== WOODEN FOOTBRIDGES =====
local function woodBridge(x, zc, width, span, rise, yaw)
	local m = L.model(f, 'WoodBridge')
	local base = CF(x, 0, zc)*A(0, yaw or 0, 0)
	local y0 = 2
	local half = span/2
	local wc, wd = Color3.fromRGB(128,90,56), Color3.fromRGB(96,66,42)
	local function yAt(dz) return y0 + rise*(1 - (dz/half)^2) end
	local N = math.floor(span/1.6)
	for i = 0, N do
		local dz = -half + span*i/N
		P(m, V(width, 0.5, 1.4), base*CF(0, yAt(dz), dz)*A(math.atan(2*rise*dz/(half*half)), 0, 0), (i % 3 == 0) and wd or wc, L.M.planks, nil, 'Plank')
	end
	-- stringers, posts and rails
	local M = 10
	for _, sx in ipairs({-1, 1}) do
		for i = 0, M-1 do
			local za = -half + span*i/M; local zb = -half + span*(i+1)/M
			L.beam(m, base*V(sx*(width/2 - 0.4), yAt(za) - 0.6, za), base*V(sx*(width/2 - 0.4), yAt(zb) - 0.6, zb), 0.8, wd, L.M.wood, 1.2)
			L.beam(m, base*V(sx*(width/2), yAt(za) + 3.6, za), base*V(sx*(width/2), yAt(zb) + 3.6, zb), 0.5, wc, L.M.wood, 0.7)
			L.beam(m, base*V(sx*(width/2), yAt(za) + 1.9, za), base*V(sx*(width/2), yAt(zb) + 1.9, zb), 0.4, wc, L.M.wood, 0.5)
		end
		for i = 0, M do
			local dz = -half + span*i/M
			P(m, V(0.8, 4.6, 0.8), base*CF(sx*(width/2), yAt(dz) + 1.8, dz), wd, L.M.wood, nil, 'Post')
		end
		-- piles in the water
		for _, dz in ipairs({-half*0.5, 0, half*0.5}) do
			L.cyl(m, 14, 1.4, base*CF(sx*(width/2 - 0.4), yAt(dz) - 7.5, dz), wd, L.M.wood)
		end
	end
	-- rope-wrapped lantern posts at each end
	for _, sz in ipairs({-1, 1}) do
		local lp = base*V(width/2 + 1.2, y0, sz*(half + 1))
		L.lamp(f, lp)
	end
	return m
end
woodBridge(-260, riverZ(-260), 10, 50, 3, -math.atan(22/90*math.cos(-260/90)))
woodBridge(250, riverZ(250), 12, 50, 3, -math.atan(22/90*math.cos(250/90)))

local n = 0; for _, d in ipairs(f:GetDescendants()) do if d:IsA('BasePart') then n = n + 1 end end
return 'bridges ok parts=' .. n
