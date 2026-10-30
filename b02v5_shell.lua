-- skull v5 step 1: realistic skull mesh shell at HQ site (old HQ moved to ServerStorage backup)
local town = workspace.SpawnTown
local SS = game:GetService('ServerStorage')
local oldHQ = town:FindFirstChild('SkullHQ')
if oldHQ and not SS:FindFirstChild('SkullHQ_v4_backup') then oldHQ.Name = 'SkullHQ_v4_backup'; oldHQ.Parent = SS
elseif oldHQ then oldHQ:Destroy() end
local t = workspace:FindFirstChild('TEST_Skull') if t then t:Destroy() end
local hq = town:FindFirstChild('SkullHQ5') if hq then hq:Destroy() end
hq = Instance.new('Model'); hq.Name = 'SkullHQ5'; hq.Parent = town

local G, Z0, H = 18, -575, 230
local src = _G.loadAsset(16673452471):GetChildren()[1]
local mp = src:IsA('MeshPart') and src or src:FindFirstChildWhichIsA('MeshPart', true)
local m = mp:Clone()
m.Size = m.Size * (H / m.Size.Y)
m.Anchored = true
m.Color = Color3.fromRGB(58, 52, 58)
m.Material = Enum.Material.Slate
m.CanCollide = false          -- walk-through visual shell; collision comes from built walls
m.CastShadow = true
m.Name = 'SkullMesh'
-- mesh's face points along local -Y after the yaw; pitch -90deg about world X so it faces +Z (town)
m.CFrame = CFrame.new(0, G + m.Size.Z/2 - 4, Z0) * CFrame.Angles(0, math.pi, 0) * CFrame.Angles(math.pi/2, 0, 0) * CFrame.Angles(0, math.pi, 0)
m.Parent = hq
return string.format('shell ok size=%.0f,%.0f,%.0f', m.Size.X, m.Size.Y, m.Size.Z)
