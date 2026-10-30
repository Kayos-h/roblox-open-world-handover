-- perf_scan_v5.luau : read-only inventory of the whole place (edit mode). Returns one JSON string. DRAFT, not yet run (Studio is not installed).
-- Use before and after every v5 area: total instances, parts, lights, emitters, neon (must be 0), unanchored (must be 0), busiest 500x500 cells,
-- biggest models, per-area counts, streaming settings. Budget for v5: at most +30,000 instances over the 270,000 of the v4 map.
local HS = game:GetService('HttpService')
local CELL = 500
local counts, cells = {}, {}
local total, parts, neon, unanchored, lights, emitters, sounds, collMesh = 0, 0, 0, 0, 0, 0, 0, 0
for _, inst in ipairs(workspace:GetDescendants()) do
	total += 1
	local cn = inst.ClassName
	counts[cn] = (counts[cn] or 0) + 1
	if inst:IsA('BasePart') then
		parts += 1
		if not inst.Anchored then unanchored += 1 end
		if inst.Material == Enum.Material.Neon then neon += 1 end
		if inst:IsA('MeshPart') and inst.CanCollide then collMesh += 1 end
		local p = inst.Position
		local key = math.floor(p.X / CELL) .. ',' .. math.floor(p.Z / CELL)
		cells[key] = (cells[key] or 0) + 1
	elseif inst:IsA('Light') then
		lights += 1
	elseif inst:IsA('ParticleEmitter') or inst:IsA('Beam') or inst:IsA('Trail') or inst:IsA('Fire') or inst:IsA('Smoke') or inst:IsA('Sparkles') then
		emitters += 1
	elseif inst:IsA('Sound') then
		sounds += 1
	end
end
local classList = {}
for k, v in pairs(counts) do classList[#classList + 1] = { k, v } end
table.sort(classList, function(a, b) return a[2] > b[2] end)
local topClasses = {}
for i = 1, math.min(12, #classList) do topClasses[#topClasses + 1] = classList[i][1] .. '=' .. classList[i][2] end
local cellList = {}
for k, v in pairs(cells) do cellList[#cellList + 1] = { k, v } end
table.sort(cellList, function(a, b) return a[2] > b[2] end)
local hot = {}
for i = 1, math.min(15, #cellList) do hot[#hot + 1] = cellList[i][1] .. '=' .. cellList[i][2] end
local areas, models = {}, {}
local root = workspace:FindFirstChild('Phase1Map')
if root then
	for _, a in ipairs(root:GetChildren()) do
		local d = a:GetDescendants()
		local pc = 0
		for _, i in ipairs(d) do if i:IsA('BasePart') then pc += 1 end end
		areas[#areas + 1] = { a.Name, #d, pc }
		for _, g in ipairs(a:GetChildren()) do
			for _, m in ipairs(g:GetChildren()) do
				if m:IsA('Model') then models[#models + 1] = { a.Name .. '/' .. g.Name .. '/' .. m.Name, #m:GetDescendants() } end
			end
		end
	end
end
table.sort(areas, function(a, b) return a[2] > b[2] end)
table.sort(models, function(a, b) return a[2] > b[2] end)
local areaOut, modelOut = {}, {}
for i = 1, math.min(40, #areas) do areaOut[#areaOut + 1] = areas[i][1] .. ': ' .. areas[i][2] .. ' inst, ' .. areas[i][3] .. ' parts' end
for i = 1, math.min(15, #models) do modelOut[#modelOut + 1] = models[i][1] .. ' = ' .. models[i][2] end
local tower = 0
for _, m in ipairs(models) do if string.find(m[1], 'WT0') or string.find(m[1], 'WT1') then tower += m[2] end end
return HS:JSONEncode({
	total_instances = total, base_parts = parts, mesh_parts_colliding = collMesh,
	neon_parts_must_be_0 = neon, unanchored_parts_must_be_0 = unanchored,
	lights = lights, emitters = emitters, sounds = sounds,
	streaming = { enabled = workspace.StreamingEnabled, min_radius = workspace.StreamingMinRadius, target_radius = workspace.StreamingTargetRadius },
	top_classes = topClasses, busiest_cells_500 = hot, areas = areaOut, biggest_models = modelOut, wizard_tower_instances = tower,
	budget_note = 'v5 budget: at most +30,000 instances over the v4 map (about 270,000); heroes 60k tris, others 18k, each MeshPart 20k',
})
