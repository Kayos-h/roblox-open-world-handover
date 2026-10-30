local out = {}
for _, d in ipairs(workspace:GetDescendants()) do
	if d:IsA('MeshPart') and (d.Name:lower():find('skull') or d.Size.X > 150) then
		out[#out + 1] = d:GetFullName() .. ' ' .. tostring(d.Position) .. ' ' .. tostring(d.Size)
	end
end
local hq = workspace.SpawnTown:FindFirstChild('SkullHQ6')
if hq then for _, c in ipairs(hq:GetChildren()) do out[#out + 1] = 'HQ6 child: ' .. c.Name .. ' ' .. c.ClassName end end
return table.concat(out, '\n')
