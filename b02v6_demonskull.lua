-- Demon skull HQ builder: turns ServerStorage.SkullMeshData into a MeshPart at the HQ site.
-- Used both in edit mode (preview) and at runtime by ServerScriptService.SkullBuilder.
local SKULL_SRC = [==[
local AS = game:GetService('AssetService')
local SS = game:GetService('ServerStorage')
local Z0, G = -575, 18
local function build()
	local fo = SS:FindFirstChild('SkullMeshData')
	if not fo then return nil, 'no data' end
	local parts = fo:GetChildren()
	table.sort(parts, function(a, b) return a.Name < b.Name end)
	local buf = {}
	for _, v in ipairs(parts) do buf[#buf + 1] = v.Value end
	local data = table.concat(buf)
	local vpart, fpart = string.match(data, '^(.-)|(.*)$')
	local em = AS:CreateEditableMesh()
	local ids = {}
	local minY = math.huge
	for x, y, z in string.gmatch(vpart, '(-?%d+),(-?%d+),(-?%d+)') do
		local yy = tonumber(y) / 10
		if yy < minY then minY = yy end
		ids[#ids + 1] = em:AddVertex(Vector3.new(tonumber(x) / 10, yy, tonumber(z) / 10))
	end
	local nt = 0
	for a, b, c in string.gmatch(fpart, '(%d+),(%d+),(%d+)') do
		-- data was stored with b/c swapped; the axis change is a pure rotation, so restore original winding
		em:AddTriangle(ids[tonumber(a) + 1], ids[tonumber(c) + 1], ids[tonumber(b) + 1])
		nt += 1
	end
	local mp = AS:CreateMeshPartAsync(Content.fromObject(em), { CollisionFidelity = Enum.CollisionFidelity.PreciseConvexDecomposition })
	mp.Name = 'DemonSkull'
	mp.Anchored = true
	mp.Material = Enum.Material.Limestone
	mp.Color = Color3.fromRGB(196, 186, 160)
	-- MeshPart origin = data origin (not bbox centre); data y=0 is the skull base. Sink 2 studs into the plateau.
	mp.CFrame = CFrame.new(0, G - 2 - minY, Z0)
	mp:SetAttribute('Bottom', G - 2)
	return mp, #ids, nt
end
return build
]==]

local SSS = game:GetService('ServerScriptService')
local SS = game:GetService('ServerStorage')
-- module holding the builder
local mod = SS:FindFirstChild('SkullBuild') or Instance.new('ModuleScript')
mod.Name = 'SkullBuild'; mod.Source = SKULL_SRC; mod.Parent = SS
-- runtime script
local sc = SSS:FindFirstChild('SkullBuilder') or Instance.new('Script')
sc.Name = 'SkullBuilder'
sc.Source = [[
local build = require(game:GetService('ServerStorage'):WaitForChild('SkullBuild'))
local hq = workspace:WaitForChild('SpawnTown'):WaitForChild('SkullHQ6')
for _, c in ipairs(hq:GetChildren()) do if c.Name == 'DemonSkull' then c:Destroy() end end
local mp = build()
if mp then mp.Parent = hq end
]]
sc.Parent = SSS

-- edit-mode preview build
local town = workspace.SpawnTown
local old5 = town:FindFirstChild('SkullHQ5') if old5 then old5:Destroy() end
local hq = town:FindFirstChild('SkullHQ6') or Instance.new('Model')
hq.Name = 'SkullHQ6'; hq.Parent = town
-- remove EVERY earlier copy (re-runs used to stack duplicates)
for _, c in ipairs(hq:GetChildren()) do if c.Name == 'DemonSkull' then c:Destroy() end end
local build = loadstring(SKULL_SRC)()
local mp, nv, nt = build()
if not mp then return 'build failed ' .. tostring(nv) end
mp.Parent = hq
-- measure real geometry bottom with a downward ray onto the mesh
local rp = RaycastParams.new(); rp.FilterType = Enum.RaycastFilterType.Include; rp.FilterDescendantsInstances = {mp}
-- geometry origin is not the bbox centre: find the true lowest point and snap it to the plateau (sunk 2)
local minY = math.huge
local G = 18
for _, x in ipairs({-80, -40, 0, 40, 80}) do
	for _, z in ipairs({-60, -20, 20, 60}) do
		local hit = workspace:Raycast(Vector3.new(x, -400, -575 + z), Vector3.new(0, 900, 0), rp)
		if hit and hit.Position.Y < minY then minY = hit.Position.Y end
	end
end
local snap = 0
if minY < math.huge then snap = (G - 2) - minY end
local lows = {}
for _, x in ipairs({-60, -30, 0, 30, 60}) do
	local hit = workspace:Raycast(Vector3.new(x, -200, -575 + 20), Vector3.new(0, 600, 0), rp)
	lows[#lows + 1] = hit and string.format('%.0f', hit.Position.Y) or '-'
end
return string.format('skull ok verts=%d tris=%d size=%.0f,%.0f,%.0f pos=%.0f snapErr=%.1f copies=%d lows=%s', nv, nt, mp.Size.X, mp.Size.Y, mp.Size.Z, mp.Position.Y, snap, #hq:GetChildren(), table.concat(lows, ','))
