-- place_v5_ph.luau : block PLACEHOLDERS for v5 models that are not built or uploaded yet, so the layout can be photographed and judged before Blender runs.
-- DRAFT, not yet run (Studio is not installed). Data (JSON) is injected below:
--   { area, items = [ { key, m, x, z, rot, g, yo, sx, sy, sz, c = [r,g,b] } ] }
-- Each item becomes Model "PH_<model>" (one Block part, SmoothPlastic, no collision, attribute Placeholder = true) inside Phase1Map/<area>/<group>.
-- Run again later with real models: archive Phase1Map/<area> placeholders (attribute Placeholder) first, then use build_v4.ps1 as usual.
local HS = game:GetService('HttpService')
local D = HS:JSONDecode([==[__DATA__]==])
local root = workspace:FindFirstChild('Phase1Map') or Instance.new('Folder')
root.Name = 'Phase1Map'
root.Parent = workspace
local area = root:FindFirstChild(D.area) or Instance.new('Folder')
area.Name = D.area
area.Parent = root
local done = _G.P1PH or {}
_G.P1PH = done
if not _G.P1PHScanned then _G.P1PHScanned = {} end
if not _G.P1PHScanned[D.area] then
	_G.P1PHScanned[D.area] = true
	for _, m in ipairs(area:GetDescendants()) do
		if m:IsA('Model') then
			local k = m:GetAttribute('PlanKey')
			if k then done[k] = true end
		end
	end
end
local rp = RaycastParams.new()
rp.FilterType = Enum.RaycastFilterType.Include
rp.FilterDescendantsInstances = { workspace.Terrain }
rp.IgnoreWater = true
local function groundAt(x, z)
	local r = workspace:Raycast(Vector3.new(x, 1500, z), Vector3.new(0, -2000, 0), rp)
	return r and r.Position.Y or nil
end
local placed, skipped, failed = 0, 0, 0
for _, it in ipairs(D.items) do
	if done[it.key] then
		skipped += 1
	else
		local gy = groundAt(it.x, it.z)
		if not gy then
			failed += 1
		else
			local grp = area:FindFirstChild(it.g) or Instance.new('Folder')
			grp.Name = it.g
			grp.Parent = area
			local m = Instance.new('Model')
			m.Name = 'PH_' .. it.m
			local p = Instance.new('Part')
			p.Name = 'Block'
			p.Size = Vector3.new(math.max(it.sx, 1), math.max(it.sy, 1), math.max(it.sz, 1))
			p.Anchored = true
			p.CanCollide = false
			p.CanTouch = false
			p.Material = Enum.Material.SmoothPlastic
			p.Color = Color3.fromRGB(it.c[1], it.c[2], it.c[3])
			p.Transparency = 0.08
			p.CFrame = CFrame.new(it.x, gy + (it.yo or 0) + p.Size.Y / 2, it.z) * CFrame.Angles(0, math.rad(it.rot or 0), 0)
			p.Parent = m
			m.PrimaryPart = p
			m:SetAttribute('PlanKey', it.key)
			m:SetAttribute('Placeholder', true)
			m.Parent = grp
			done[it.key] = true
			placed += 1
		end
	end
end
return HS:JSONEncode({ placed = placed, skipped = skipped, failed = failed })
