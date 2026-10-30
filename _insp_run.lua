-- assets.lua: shared asset cache (ServerStorage.TownAssets/<id>), appended by batches that need store models
local SS = game:GetService('ServerStorage')
local lib = SS:FindFirstChild('TownAssets') or Instance.new('Folder')
lib.Name = 'TownAssets'; lib.Parent = SS
_G.TownAssets = lib

-- load asset once; strips any scripts for safety; returns the cached root folder/model
function _G.loadAsset(id)
	local key = tostring(id)
	local have = lib:FindFirstChild(key)
	if have then return have end
	local objs = game:GetObjects('rbxassetid://' .. key)
	local holder = Instance.new('Folder'); holder.Name = key
	for _, o in ipairs(objs) do
		for _, d in ipairs(o:GetDescendants()) do
			if d:IsA('LuaSourceContainer') then d:Destroy() end
		end
		if o:IsA('LuaSourceContainer') then o:Destroy() else o.Parent = holder end
	end
	holder.Parent = lib
	return holder
end

-- describe models in a folder: name, extents
function _G.describe(root, depth)
	local out = {}
	local function walk(inst, d)
		for _, c in ipairs(inst:GetChildren()) do
			if c:IsA('Model') then
				local _, size = c:GetBoundingBox()
				table.insert(out, string.rep(' ', d) .. c:GetFullName():gsub('ServerStorage.TownAssets.', '') .. string.format(' [%.1f %.1f %.1f] n=%d', size.X, size.Y, size.Z, #c:GetDescendants()))
			elseif c:IsA('BasePart') and d <= 2 then
				table.insert(out, string.rep(' ', d) .. c.Name .. ':' .. c.ClassName .. string.format(' [%.1f %.1f %.1f]', c.Size.X, c.Size.Y, c.Size.Z))
			elseif c:IsA('Folder') then
				table.insert(out, string.rep(' ', d) .. c.Name .. '/')
				if d < depth then walk(c, d + 1) end
			end
		end
	end
	walk(root, 0)
	return table.concat(out, '\n')
end


-- move every MaterialVariant in an asset into MaterialService so custom materials render
function _G.installVariants(root)
	local MS = game:GetService('MaterialService')
	for _, d in ipairs(root:GetDescendants()) do
		if d:IsA('MaterialVariant') and not MS:FindFirstChild(d.Name) then d:Clone().Parent = MS end
	end
end

-- find a template model by path inside an asset holder, e.g. tpl(id, 'Models_Trees/Models/Tree_01')
function _G.tpl(id, path)
	local node = _G.loadAsset(id)
	for seg in string.gmatch(path, '[^/]+') do
		local nxt
		for _, c in ipairs(node:GetChildren()) do if c.Name == seg then nxt = c break end end
		if not nxt then for _, c in ipairs(node:GetChildren()) do nxt = c:FindFirstChild(seg, true) if nxt then break end end end
		node = nxt
		if not node then error('tpl missing ' .. path) end
	end
	return node
end

-- clone template, scale so its height == h (or by factor s if h nil), place bottom-centre at cf
function _G.place(template, parent, cf, h, s)
	local m = template:Clone()
	if not m:IsA('Model') then
		local w = Instance.new('Model'); w.Name = m.Name; m.Parent = w; m = w
	end
	local bcf, size = m:GetBoundingBox()
	local k = s or (h and h / size.Y) or 1
	if math.abs(k - 1) > 1e-3 then m:ScaleTo(m:GetScale() * k) end
	bcf, size = m:GetBoundingBox()
	local piv = m:GetPivot()
	m:PivotTo(CFrame.new(cf.Position) * (cf - cf.Position) * (piv - piv.Position))
	bcf, size = m:GetBoundingBox()
	local bottom = bcf.Position - Vector3.new(0, size.Y / 2, 0)
	m:PivotTo(m:GetPivot() + (cf.Position - bottom))
	for _, d in ipairs(m:GetDescendants()) do
		if d:IsA('BasePart') then d.Anchored = true end
	end
	m.Parent = parent
	return m
end

-- ---------- nature overrides: store models replace primitive trees/bushes/flowers ----------
local L = _G.L or {}
local TREE_PACK = 79689531752352
local NAT = nil
local nrng = Random.new(4242)
local function natInit()
	if NAT then return NAT end
	NAT = {trees = {}, tall = {}, bushes = {}, flowers = {}}
	_G.installVariants(_G.loadAsset(TREE_PACK))
	for i = 1, 19 do
		local t = _G.tpl(TREE_PACK, 'Models_Trees/Models/Tree_' .. string.format('%02d', i))
		local _, sz = t:GetBoundingBox()
		if sz.Y / math.max(sz.X, sz.Z) > 1.7 then table.insert(NAT.tall, t) else table.insert(NAT.trees, t) end
	end
	for i = 1, 3 do table.insert(NAT.bushes, _G.tpl(TREE_PACK, 'Models_Bushes/Models/Bush_0' .. i)) end
	local fb = _G.loadAsset(1353190583):GetChildren()[1]
	NAT.flowerBush = fb
	-- single-flower templates (each wrapped as a Model)
	local function add(inst) table.insert(NAT.flowers, inst) end
	for _, mp in ipairs(_G.loadAsset(16428845157):GetChildren()[1]:GetChildren()) do if mp:IsA('BasePart') then add(mp) end end
	for _, mp in ipairs(_G.loadAsset(743377736):GetChildren()) do if mp:IsA('BasePart') then add(mp) end end
	add(_G.loadAsset(711333951):GetChildren()[1])
	add(_G.loadAsset(16071638063):GetChildren()[1])
	add(_G.loadAsset(136744769027061):GetChildren()[1])
	return NAT
end
_G.natInit = natInit

local function noCollideSmall(m)
	for _, d in ipairs(m:GetDescendants()) do if d:IsA('BasePart') then d.CanCollide = false; d.CastShadow = true end end
end

L._oldTree, L._oldBush, L._oldFlowers = L._oldTree or L.tree, L._oldBush or L.bush, L._oldFlowers or L.flowers
function L.tree(parent, pos, s, kind)
	local N = natInit(); s = s or 1
	local list = (kind == 'pine' and #N.tall > 0) and N.tall or N.trees
	local t = list[nrng:NextInteger(1, #list)]
	local h = ((kind == 'pine') and 40 or 32) * s * nrng:NextNumber(0.9, 1.12)
	local m = _G.place(t, parent, CFrame.new(pos - Vector3.new(0, 0.4, 0)) * CFrame.Angles(0, nrng:NextNumber(0, 6.28), 0), h)
	m.Name = 'Tree'
	-- leaves shouldn't block players; trunks stay solid
	for _, d in ipairs(m:GetDescendants()) do
		if d:IsA('BasePart') and not d.Name:lower():find('trunk') and not d.Name:lower():find('root') and not d.Name:lower():find('bark') then d.CanCollide = false end
	end
	return m
end
function L.bush(parent, pos, s)
	local N = natInit(); s = s or 1
	local m
	if nrng:NextNumber() < 0.3 then
		m = _G.place(N.flowerBush, parent, CFrame.new(pos) * CFrame.Angles(0, nrng:NextNumber(0, 6.28), 0), 4.2 * s)
	else
		m = _G.place(N.bushes[nrng:NextInteger(1, #N.bushes)], parent, CFrame.new(pos - Vector3.new(0, 0.3, 0)) * CFrame.Angles(0, nrng:NextNumber(0, 6.28), 0), 4.5 * s)
	end
	m.Name = 'Bush'; noCollideSmall(m)
	return m
end
function L.flowers(parent, center, radius, count)
	local N = natInit()
	local m = Instance.new('Model'); m.Name = 'Flowers'; m.Parent = parent
	local n = math.clamp(math.floor(count / 2.5), 3, 10)
	-- a patch favours 2 species so it reads as a planted cluster
	local a, b = N.flowers[nrng:NextInteger(1, #N.flowers)], N.flowers[nrng:NextInteger(1, #N.flowers)]
	for i = 1, n do
		local ang = nrng:NextNumber() * 6.283; local r = math.sqrt(nrng:NextNumber()) * radius
		local p = center + Vector3.new(math.cos(ang) * r, 0, math.sin(ang) * r)
		local g = workspace:Raycast(p + Vector3.new(0, 6, 0), Vector3.new(0, -14, 0))
		if g then p = g.Position end
		_G.place((i % 2 == 0) and a or b, m, CFrame.new(p) * CFrame.Angles(0, nrng:NextNumber(0, 6.28), 0), nrng:NextNumber(2.6, 4))
	end
	noCollideSmall(m)
	return m
end

if workspace:FindFirstChild('_AssetTest') then workspace._AssetTest:Destroy() end return 'ok'