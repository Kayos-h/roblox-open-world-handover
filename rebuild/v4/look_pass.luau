-- v4 look pass: terrain material colours, sea colour, lighting, atmosphere and post effects.
-- Replayable: run through execute_luau. Never reads Lighting.Technology or Terrain.Decoration.
local T = workspace.Terrain
local L = game:GetService("Lighting")
local out = {}
local function C(r, g, b) return Color3.fromRGB(r, g, b) end

local colors = {
  Grass = C(96, 150, 58), LeafyGrass = C(62, 118, 50), Mud = C(88, 66, 48), Sand = C(224, 205, 152),
  Rock = C(116, 112, 104), Slate = C(88, 92, 100), Basalt = C(66, 64, 66), Ground = C(160, 116, 76),
  Snow = C(246, 249, 253), Glacier = C(206, 228, 244), Ice = C(160, 206, 232), Sandstone = C(190, 124, 78),
  Limestone = C(214, 200, 168), Salt = C(170, 132, 92),
}
for name, col in pairs(colors) do
  local ok, err = pcall(function() T:SetMaterialColor(Enum.Material[name], col) end)
  if not ok then out[#out + 1] = "color fail " .. name .. ": " .. tostring(err) end
end

pcall(function()
  T.WaterColor = C(22, 98, 140)
  T.WaterTransparency = 0.9
  T.WaterReflectance = 0.55
  T.WaterWaveSize = 0.22
  T.WaterWaveSpeed = 14
end)

L.Brightness = 2.6
L.ClockTime = 15.6
L.GeographicLatitude = 28
L.ExposureCompensation = 0.1
L.Ambient = C(60, 70, 90)
L.OutdoorAmbient = C(96, 108, 132)
L.ColorShift_Top = C(255, 232, 196)
L.EnvironmentDiffuseScale = 0.55
L.EnvironmentSpecularScale = 0.45
pcall(function() L.ShadowSoftness = 0.25 end)

local function ensure(class, name)
  local o = L:FindFirstChildOfClass(class)
  if not o then o = Instance.new(class); o.Name = name; o.Parent = L end
  return o
end
local atm = ensure("Atmosphere", "Atmosphere")
atm.Density = 0.30; atm.Offset = 0.18; atm.Color = C(198, 212, 232); atm.Decay = C(104, 128, 164); atm.Glare = 0.12; atm.Haze = 1.6
local cc = ensure("ColorCorrectionEffect", "ColorCorrection")
cc.Brightness = 0; cc.Contrast = 0.12; cc.Saturation = 0.08; cc.TintColor = C(255, 247, 238)
local bl = ensure("BloomEffect", "Bloom")
bl.Intensity = 0.3; bl.Size = 22; bl.Threshold = 0.95
local sr = ensure("SunRaysEffect", "SunRays")
sr.Intensity = 0.04; sr.Spread = 0.55

local ok, res = pcall(function()
  local MS = game:GetService("MaterialService")
  MS.Use2022Materials = true
  return MS.Use2022Materials
end)
out[#out + 1] = "Use2022Materials=" .. tostring(res) .. " ok=" .. tostring(ok)
out[#out + 1] = "water " .. tostring(T.WaterColor) .. " t=" .. T.WaterTransparency .. " clock=" .. L.ClockTime .. " atm=" .. atm.Density .. "/" .. atm.Haze
return table.concat(out, "\n")
