-- skull candidate showcase (temporary): place skull meshes side by side, report mesh info
local old = workspace:FindFirstChild('TEST_Skull') if old then old:Destroy() end
local f = Instance.new('Model'); f.Name = 'TEST_Skull'; f.Parent = workspace
local ids = {1362561045, 83623137673707, 581784375, 16673452471}
local out = {}
local rp = RaycastParams.new(); rp.FilterType = Enum.RaycastFilterType.Include; rp.FilterDescendantsInstances = {workspace.Terrain}
for i, id in ipairs(ids) do
	local ok, holder = pcall(_G.loadAsset, id)
	if ok and holder and holder:GetChildren()[1] then
		local t = holder:GetChildren()[1]
		local x = 130 + (i - 1)*60
		local hit = workspace:Raycast(Vector3.new(x, 300, -700), Vector3.new(0, -600, 0), rp)
		local gy = hit and hit.Position.Y or 0
		local info = t.ClassName .. ' '
		for _, d in ipairs(holder:GetDescendants()) do
			if d:IsA('MeshPart') then info = info .. 'MeshPart ' .. d.MeshId .. ' tex=' .. d.TextureID .. ' sz=' .. tostring(d.Size) .. '; '
			elseif d:IsA('SpecialMesh') then info = info .. 'SpecialMesh ' .. d.MeshId .. ' tex=' .. d.TextureId .. ' scale=' .. tostring(d.Scale) .. ' psz=' .. tostring(d.Parent.Size) .. '; ' end
		end
		local ok2, err = pcall(function() _G.place(t, f, CFrame.new(x, gy, -700) * CFrame.Angles(0, (i == 2) and 0 or math.pi, 0), 40) end)
		table.insert(out, id .. ' gy=' .. math.floor(gy) .. ' place=' .. tostring(ok2) .. ' ' .. tostring(err or '') .. ' | ' .. info:sub(1, 400))
	else
		table.insert(out, id .. ' FAIL ' .. tostring(holder))
	end
end
return table.concat(out, '\n')
