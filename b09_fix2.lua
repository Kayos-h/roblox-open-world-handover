-- b09 fix2: rotate archery targets so the painted face points +Z (toward shooting line)
local n = 0
for _, m in ipairs(workspace.SpawnTown:GetDescendants()) do
	if m:IsA('Model') and m.Name == 'Target' then
		local cf = m:GetBoundingBox()
		if cf.Position.Z < -315 and cf.Position.Z > -328 then
			local piv = m:GetPivot()
			local c = CFrame.new(cf.Position)
			m:PivotTo(c * CFrame.Angles(0, math.rad(-90), 0) * c:Inverse() * piv)
			n += 1
		end
	end
end
-- verify painted face normal
local out = {'rotated=' .. n}
for _, m in ipairs(workspace.SpawnTown:GetDescendants()) do
	if m:IsA('Model') and m.Name == 'Target' then
		local cf = m:GetBoundingBox()
		if cf.Position.Z < -315 and cf.Position.Z > -328 then
			for _, d in ipairs(m:GetDescendants()) do
				if d:IsA('Decal') then
					local p = d.Parent
					local nrm = p.CFrame:VectorToWorldSpace(Vector3.FromNormalId(d.Face))
					table.insert(out, string.format('%.0f nrm=%.2f,%.2f,%.2f', cf.Position.X, nrm.X, nrm.Y, nrm.Z))
				end
			end
		end
	end
end
return table.concat(out, '\n')
