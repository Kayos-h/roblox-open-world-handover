-- b14: lighting, atmosphere, post effects, ambient particles
local L = _G.L
local V, CF = L.V, L.CF
local Lighting = game:GetService('Lighting')
local town = workspace:FindFirstChild('SpawnTown')

pcall(function() Lighting.Technology = Enum.Technology.Future end)
Lighting.ClockTime = 15.2
Lighting.GeographicLatitude = 35
Lighting.Brightness = 2.6
Lighting.Ambient = Color3.fromRGB(70, 70, 82)
Lighting.OutdoorAmbient = Color3.fromRGB(128, 126, 140)
Lighting.EnvironmentDiffuseScale = 0.6
Lighting.EnvironmentSpecularScale = 0.6
Lighting.ShadowSoftness = 0.25
Lighting.GlobalShadows = true

for _, c in ipairs(Lighting:GetChildren()) do
	if c:IsA('Atmosphere') or c:IsA('BloomEffect') or c:IsA('ColorCorrectionEffect') or c:IsA('SunRaysEffect') or c:IsA('DepthOfFieldEffect') then c:Destroy() end
end
local atm = Instance.new('Atmosphere')
atm.Density = 0.28; atm.Offset = 0.15
atm.Color = Color3.fromRGB(200, 214, 230); atm.Decay = Color3.fromRGB(110, 120, 150)
atm.Glare = 0.25; atm.Haze = 1.2
atm.Parent = Lighting

local bloom = Instance.new('BloomEffect'); bloom.Intensity = 0.6; bloom.Size = 28; bloom.Threshold = 1.6; bloom.Parent = Lighting
local cc = Instance.new('ColorCorrectionEffect'); cc.Brightness = 0.02; cc.Contrast = 0.08; cc.Saturation = 0.12
cc.TintColor = Color3.fromRGB(255, 250, 240); cc.Parent = Lighting
local rays = Instance.new('SunRaysEffect'); rays.Intensity = 0.06; rays.Spread = 0.7; rays.Parent = Lighting

local clouds = workspace.Terrain:FindFirstChildOfClass('Clouds') or Instance.new('Clouds')
clouds.Cover = 0.55; clouds.Density = 0.6; clouds.Color = Color3.fromRGB(255, 255, 255)
clouds.Parent = workspace.Terrain

-- water look
local T = workspace.Terrain
T.WaterColor = Color3.fromRGB(40, 140, 170); T.WaterReflectance = 0.45
T.WaterTransparency = 0.6; T.WaterWaveSize = 0.12; T.WaterWaveSpeed = 8

-- ambient particles: drifting leaves + evening fireflies in green areas
local f = L.folder(town, 'Ambience')
local function emitterBox(pos, size, name, props)
	local p = Instance.new('Part'); p.Name = name; p.Size = size; p.CFrame = CF(pos)
	p.Anchored, p.CanCollide, p.CanTouch, p.CanQuery = true, false, false, false
	p.Transparency = 1; p.Parent = f
	local e = Instance.new('ParticleEmitter')
	for k, v in pairs(props) do e[k] = v end
	e.Parent = p
	return p
end
local leafProps = {
	Texture = 'rbxasset://textures/particles/sparkles_main.dds',
	Color = ColorSequence.new(Color3.fromRGB(150, 200, 90), Color3.fromRGB(230, 180, 80)),
	Size = NumberSequence.new(0.35), Transparency = NumberSequence.new({NumberSequenceKeypoint.new(0,1), NumberSequenceKeypoint.new(0.2,0.2), NumberSequenceKeypoint.new(0.8,0.2), NumberSequenceKeypoint.new(1,1)}),
	Lifetime = NumberRange.new(6, 10), Rate = 4, Speed = NumberRange.new(1, 3),
	SpreadAngle = Vector2.new(60, 60), Acceleration = V(1.5, -0.8, 0.6), RotSpeed = NumberRange.new(-90, 90),
	Rotation = NumberRange.new(0, 360), LightEmission = 0.1,
}
local flyProps = {
	Texture = 'rbxasset://textures/particles/sparkles_main.dds',
	Color = ColorSequence.new(Color3.fromRGB(255, 240, 140)), LightEmission = 1,
	Size = NumberSequence.new({NumberSequenceKeypoint.new(0,0), NumberSequenceKeypoint.new(0.5,0.5), NumberSequenceKeypoint.new(1,0)}),
	Lifetime = NumberRange.new(3, 6), Rate = 3, Speed = NumberRange.new(0.3, 1.2),
	SpreadAngle = Vector2.new(180, 180), Acceleration = V(0, 0.2, 0),
}
local spots = {V(-220, 0, -150), V(220, 0, 150), V(-150, 0, 120), V(60, 0, -200), V(-300, 0, -40), V(300, 0, -150), V(-120, 0, 330), V(0, 0, -390)}
for i, s in ipairs(spots) do
	local g = L.ground(s.X, s.Z)
	emitterBox(V(s.X, g + 22, s.Z), V(80, 4, 80), 'Leaves' .. i, leafProps)
	emitterBox(V(s.X, g + 4, s.Z), V(60, 4, 60), 'Fireflies' .. i, flyProps)
end
-- pond glow
emitterBox(V(-300, L.ground(-300, -40) + 3, -40), V(40, 2, 40), 'PondFireflies', flyProps)

return 'lighting ok'
