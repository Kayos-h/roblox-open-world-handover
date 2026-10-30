-- probe5: how far did the nature swap get?
local town = workspace.SpawnTown
local c = {store = 0, prim = 0}
local byFolder = {}
for _, d in ipairs(town:GetDescendants()) do
	if d:IsA('Model') and (d.Name == 'Tree' or d.Name == 'Bush' or d.Name == 'Flowers') then
		local isStore = d:FindFirstChildWhichIsA('MeshPart', true) ~= nil
		if isStore then c.store += 1 else c.prim += 1 end
		local top = d
		while top.Parent ~= town do top = top.Parent end
		byFolder[top.Name] = byFolder[top.Name] or {0, 0}
		byFolder[top.Name][isStore and 1 or 2] += 1
	end
end
local out = {string.format('store=%d prim=%d', c.store, c.prim)}
for k, v in pairs(byFolder) do table.insert(out, string.format('%s store=%d prim=%d', k, v[1], v[2])) end
local SS = game:GetService('ServerStorage')
table.insert(out, 'TownAssets=' .. tostring(SS:FindFirstChild('TownAssets') ~= nil))
return table.concat(out, ' | ')
