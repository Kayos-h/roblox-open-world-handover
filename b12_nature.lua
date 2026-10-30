-- b12: scatter trees, bushes, rocks and flowers over open grass (keeps roads/buildings clear)
local L = _G.L
local V, CF, A = L.V, L.CF, L.A
local town = workspace:FindFirstChild('SpawnTown')
local f = L.folder(town, 'Nature')
local R = Random.new(1212)

local rp = RaycastParams.new(); rp.IgnoreWater = false
rp.FilterType = Enum.RaycastFilterType.Exclude; rp.FilterDescendantsInstances = {f}
local op = OverlapParams.new(); op.FilterType = Enum.RaycastFilterType.Exclude; op.FilterDescendantsInstances = {f}
local GRASS = {[Enum.Material.Grass] = true, [Enum.Material.LeafyGrass] = true}

-- returns ground point if (x,z) is open grass with `clear` studs of free space
local function spot(x, z, clear)
	local hit = workspace:Raycast(V(x, 400, z), V(0, -800, 0), rp)
	if not hit or hit.Instance ~= workspace.Terrain or not GRASS[hit.Material] then return nil end
	for _, o in ipairs({V(clear,0,0), V(-clear,0,0), V(0,0,clear), V(0,0,-clear)}) do
		local h2 = workspace:Raycast(V(x, 400, z) + o, V(0, -800, 0), rp)
		if not h2 or h2.Instance ~= workspace.Terrain or not GRASS[h2.Material] then return nil end
		if math.abs(h2.Position.Y - hit.Position.Y) > clear*0.6 then return nil end -- too steep
	end
	local parts = workspace:GetPartBoundsInBox(CF(x, hit.Position.Y + 30, z), V(clear*2, 64, clear*2), op)
	if #parts > 0 then return nil end
	return hit.Position
end

local function near(p, list, d)
	for _, q in ipairs(list) do if (V(p.X,0,p.Z) - V(q.X,0,q.Z)).Magnitude < d then return true end end
	return false
end

local spawnP = V(0, 0, 50)
local placed = {}
local counts = {tree = 0, pine = 0, bush = 0, rock = 0, flower = 0}

local function scatter(n, tries, xmin, xmax, zmin, zmax, clear, gap, fn, key)
	local k = 0
	for _ = 1, tries do
		if k >= n then break end
		local x, z = R:NextNumber(xmin, xmax), R:NextNumber(zmin, zmax)
		if (V(x,0,z) - spawnP).Magnitude > 45 then
			local p = spot(x, z, clear)
			if p and not near(p, placed, gap) then
				fn(p); table.insert(placed, p); k += 1; counts[key] += 1
			end
		end
	end
end

local trees = L.folder(f, 'Trees')
local inner = 405
-- broadleaf trees inside the walls
scatter(95, 2500, -inner, inner, -inner, inner, 10, 22, function(p)
	L.tree(trees, p, R:NextNumber(0.85, 1.25), 'oak')
end, 'tree')
-- some pines mixed in
scatter(30, 1500, -inner, inner, -inner, inner, 8, 20, function(p)
	L.tree(trees, p, R:NextNumber(0.8, 1.15), 'pine')
end, 'pine')
-- grove ring around skull plateau
scatter(18, 600, -110, 110, -420, -230, 9, 16, function(p)
	L.tree(trees, p, R:NextNumber(1.0, 1.3), R:NextNumber() < 0.5 and 'pine' or 'oak')
end, 'tree')

-- forest belt outside the walls (backdrop)
local outer = L.folder(f, 'OuterForest')
for _ = 1, 900 do
	if counts.pine >= 150 then break end
	local side = R:NextInteger(1, 4)
	local a, b = R:NextNumber(-560, 560), R:NextNumber(445, 560)
	local x, z
	if side == 1 then x, z = a, b elseif side == 2 then x, z = a, -b elseif side == 3 then x, z = b, a else x, z = -b, a end
	local p = spot(x, z, 6)
	if p and not near(p, placed, 18) then
		L.tree(outer, p, R:NextNumber(1.0, 1.5), R:NextNumber() < 0.75 and 'pine' or 'oak')
		table.insert(placed, p); counts.pine += 1
	end
end

local small = L.folder(f, 'Undergrowth')
scatter(140, 2500, -inner, inner, -inner, inner, 4, 7, function(p)
	L.bush(small, p, R:NextNumber(0.8, 1.4))
end, 'bush')
scatter(45, 1500, -inner, inner, -inner, inner, 5, 10, function(p)
	L.rock(small, p - V(0, 0.6, 0), R:NextNumber(0.5, 1.1))
end, 'rock')
scatter(55, 1500, -inner, inner, -inner, inner, 5, 6, function(p)
	L.flowers(small, p, R:NextNumber(3, 6), R:NextInteger(8, 14))
end, 'flower')

local n = 0
for _, d in ipairs(f:GetDescendants()) do if d:IsA('BasePart') then n += 1 end end
return string.format('nature ok parts=%d trees=%d pines=%d bush=%d rock=%d flower=%d', n, counts.tree, counts.pine, counts.bush, counts.rock, counts.flower)
