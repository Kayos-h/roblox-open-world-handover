local out = {}
local box = workspace:GetPartBoundsInBox(CFrame.new(0, 80, -520), Vector3.new(260, 140, 140))
local seen = {}
for _, p in ipairs(box) do
	if p.Size.Magnitude > 30 and not seen[p] then
		seen[p] = true
		out[#out+1] = p:GetFullName() .. ' ' .. p.ClassName .. ' size=' .. tostring(p.Size) .. ' tr=' .. p.Transparency
	end
end
for _, d in ipairs(workspace:GetDescendants()) do
	if (d:IsA('Decal') or d:IsA('Texture') or d:IsA('SurfaceGui')) and d.Parent and d.Parent:IsA('BasePart') then
		local pp = d.Parent.Position
		if math.abs(pp.X) < 150 and pp.Z < -420 and pp.Z > -700 then out[#out+1] = 'GFX ' .. d:GetFullName() end
	end
end
return #out .. ' | ' .. table.concat(out, ' || ')
