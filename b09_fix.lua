-- b09 fix: hide humanoid name tags in training yard, report archery target orientation
local yard = workspace.SpawnTown:FindFirstChild('Crafts', true) or workspace.SpawnTown
local n = 0
for _, d in ipairs(workspace.SpawnTown:GetDescendants()) do
	if d:IsA('Humanoid') then
		d.DisplayDistanceType = Enum.HumanoidDisplayDistanceType.None
		d.HealthDisplayType = Enum.HumanoidHealthDisplayType.AlwaysOff
		d.NameDisplayDistance = 0
		n += 1
	end
end
local out = {'humanoids=' .. n}
-- archery targets: models near z=-321 band
for _, m in ipairs(workspace.SpawnTown:GetDescendants()) do
	if m:IsA('Model') and m.Name == 'Target' then
		local cf, sz = m:GetBoundingBox()
		if cf.Position.Z < -315 and cf.Position.Z > -328 then
			-- find decal / textured face
			local info = ''
			for _, p in ipairs(m:GetDescendants()) do
				if p:IsA('Decal') or p:IsA('Texture') then
					info = info .. p.Parent.Name .. ':' .. p.Face.Name .. ' lv=' .. tostring(p.Parent.CFrame.LookVector) .. '; '
				elseif p:IsA('MeshPart') then
					info = info .. 'mesh ' .. p.Name .. ' sz=' .. tostring(p.Size) .. ' lv=' .. tostring(p.CFrame.LookVector) .. '; '
				end
			end
			table.insert(out, string.format('T %.0f,%.0f sz=%s | %s', cf.Position.X, cf.Position.Z, tostring(sz), info:sub(1, 300)))
		end
	end
end
return table.concat(out, '\n')
