-- b17: replace every old-style Banner model in SpawnTown with the new L.banner (same place, size, colours)
local L = _G.L
local town = workspace.SpawnTown
local tb = workspace:FindFirstChild('TEST_Banner'); if tb then tb:Destroy() end
local list = {}
for _, d in ipairs(town:GetDescendants()) do
	if d:IsA('Model') and d.Name == 'Banner' and not d:FindFirstChild('Cloth') then table.insert(list, d) end
end
local n = 0
for _, m in ipairs(list) do
	-- old layout: the cloth is the biggest flat Fabric part (5 x h x 0.25)
	local cloth, best = nil, 0
	for _, p in ipairs(m:GetChildren()) do
		if p:IsA('Part') and p.Material == Enum.Material.Fabric and p.Size.Z < 0.4 and p.Size.Y > best then cloth, best = p, p.Size.Y end
	end
	if cloth then
		local emb
		for _, p in ipairs(m:GetChildren()) do
			if p:IsA('Part') and p.Shape == Enum.PartType.Cylinder and p.Material == Enum.Material.SmoothPlastic then emb = p.Color break end
		end
		local parent = m.Parent
		local cf, h, col = cloth.CFrame, cloth.Size.Y, cloth.Color
		m:Destroy()
		L.banner(parent, cf, col, h, emb or L.C.gold)
		n += 1
	end
end
return 'banner swap ok n=' .. n
