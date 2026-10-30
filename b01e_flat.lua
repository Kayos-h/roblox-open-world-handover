local T = workspace.Terrain
T:FillBlock(CFrame.new(-300, 8, -40), Vector3.new(160, 16, 160), Enum.Material.Air)
-- ground-level path in matching material, flush
T:FillBlock(CFrame.new(-260,-2,-92), Vector3.new(10,4,32), Enum.Material.Ground)
T:FillBlock(CFrame.new(-260,-2,8), Vector3.new(10,4,28), Enum.Material.Ground)
T:FillBlock(CFrame.new(-300, 8, -40), Vector3.new(160, 16, 160), Enum.Material.Air)
return 'flattened'
