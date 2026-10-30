-- probe6: list every stall with its folder and position
local out = {}
for _, d in ipairs(workspace.SpawnTown:GetDescendants()) do
	if d:IsA('Model') and d.Name:lower():find('stall') then
		local cf = d:GetBoundingBox()
		local top = d
		while top.Parent ~= workspace.SpawnTown do top = top.Parent end
		table.insert(out, string.format('%s/%s (%.0f,%.0f)', top.Name, d.Parent.Name, cf.X, cf.Z))
	end
end
return #out .. ' | ' .. table.concat(out, ' ; ')
