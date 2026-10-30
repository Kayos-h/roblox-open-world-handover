local kit = _G.loadAsset(2129051912):FindFirstChild('Medieval Interior Kit')
local old = workspace:FindFirstChild('TEST_Show'); if old then old:Destroy() end
local f = Instance.new('Folder'); f.Name = 'TEST_Show'; f.Parent = workspace
local x = 0
local G = _G.L.ground(200, -700) + 40
local pl = Instance.new('Part'); pl.Anchored = true; pl.Size = Vector3.new(170, 1, 30); pl.CFrame = CFrame.new(225, G - 0.5, -700)
pl.Material = Enum.Material.WoodPlanks; pl.Color = Color3.fromRGB(120,84,52); pl.Parent = f
for _, c in ipairs(kit:GetChildren()) do
	if c:IsA('Model') then
		local _, sz = c:GetBoundingBox()
		_G.place(c, f, CFrame.new(150 + x, G, -700), sz.Y)
		x += math.max(sz.X, sz.Z) + 3
	end
end
return 'shown x=' .. x
