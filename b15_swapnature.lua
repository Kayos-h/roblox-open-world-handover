-- b15: swap primitive Tree/Bush/Flowers models in all districts for store models (Nature folder already uses them)
local L = _G.L
local V, CF = L.V, L.CF
local town = workspace.SpawnTown
local swapped = {Tree = 0, Bush = 0, Flowers = 0}
local list = {}
for _, d in ipairs(town:GetDescendants()) do
	if d:IsA('Model') and swapped[d.Name] and not d:IsDescendantOf(town.Nature) and not d:GetAttribute('Store') then
		-- skip nested (e.g. a Bush inside something already listed) and store-made models (MeshParts)
		if not d:FindFirstChildWhichIsA('MeshPart', true) then table.insert(list, d) end
	end
end
for _, m in ipairs(list) do
	if m.Parent then
		local cf, size = m:GetBoundingBox()
		local bottom = cf.Position - V(0, size.Y / 2, 0)
		local parent = m.Parent
		local new
		if m.Name == 'Tree' then
			local balls = 0
			for _, p in ipairs(m:GetChildren()) do if p:IsA('Part') and p.Shape == Enum.PartType.Ball then balls += 1 end end
			local pine = balls < 3
			new = L.tree(parent, bottom, size.Y / (pine and 40 or 32), pine and 'pine' or 'oak')
		elseif m.Name == 'Bush' then
			new = L.bush(parent, bottom, math.max(size.Y / 4.5, 0.7))
		else
			new = L.flowers(parent, bottom, math.max(size.X, size.Z) / 2, #m:GetChildren() / 2)
		end
		new:SetAttribute('Store', true)
		m:Destroy()
		swapped[m.Name] += 1
	end
end
return string.format('swap ok trees=%d bushes=%d flowers=%d', swapped.Tree, swapped.Bush, swapped.Flowers)
