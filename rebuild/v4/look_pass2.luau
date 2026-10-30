-- v4 look pass 2 (after round-2 review): deeper sea, far less fog, richer greens, warmer road/ground colours.
-- Replayable via execute_luau. Never reads Lighting.Technology or Terrain.Decoration.
-- Gameplay atmosphere values are stored as attributes on the Atmosphere object so photo_mode.luau can toggle and restore them.
local T = workspace.Terrain
local L = game:GetService("Lighting")
local out = {}
local function C(r, g, b) return Color3.fromRGB(r, g, b) end

local colors = {
  Grass = C(74, 146, 46), LeafyGrass = C(48, 112, 40), Mud = C(84, 62, 46), Sand = C(226, 208, 156),
  Rock = C(118, 112, 102), Slate = C(86, 90, 100), Basalt = C(58, 60, 66), Ground = C(176, 130, 84),
  Snow = C(246, 249, 253), Glacier = C(206, 228, 244), Ice = C(160, 206, 232), Sandstone = C(196, 128, 80),
  Limestone = C(222, 204, 164), Salt = C(176, 138, 96), Cobblestone = C(150, 140, 128), Pavement = C(170, 160, 146),
}
for name, col in pairs(colors) do
  local ok, err = pcall(function() T:SetMaterialColor(Enum.Material[name], col) end)
  if not ok then out[#out + 1] = "color fail " .. name .. ": " .. tostring(err) end
end

pcall(function()
  T.WaterColor = C(14, 62, 104)
  T.WaterTransparency = 0.74
  T.WaterReflectance = 0.5
  T.WaterWaveSize = 0.24
  T.WaterWaveSpeed = 14
end)

L.Brightness = 2.7
L.ClockTime = 15.2
L.GeographicLatitude = 28
L.ExposureCompensation = 0.15
L.Ambient = C(66, 74, 94)
L.OutdoorAmbient = C(104, 114, 136)
L.ColorShift_Top = C(255, 236, 204)
L.EnvironmentDiffuseScale = 0.6
L.EnvironmentSpecularScale = 0.45
pcall(function() L.ShadowSoftness = 0.25 end)

local function ensure(class, name)
  local o = L:FindFirstChildOfClass(class)
  if not o then o = Instance.new(class); o.Name = name; o.Parent = L end
  return o
end
local atm = ensure("Atmosphere", "Atmosphere")
atm.Density = 0.20; atm.Offset = 0.12; atm.Color = C(190, 208, 232); atm.Decay = C(98, 124, 160); atm.Glare = 0.1; atm.Haze = 0.8
atm:SetAttribute("GameDensity", 0.20); atm:SetAttribute("GameHaze", 0.8); atm:SetAttribute("GameOffset", 0.12)
local cc = ensure("ColorCorrectionEffect", "ColorCorrection")
cc.Brightness = 0; cc.Contrast = 0.14; cc.Saturation = 0.16; cc.TintColor = C(255, 248, 240)
local bl = ensure("BloomEffect", "Bloom")
bl.Intensity = 0.25; bl.Size = 20; bl.Threshold = 1.0
local sr = ensure("SunRaysEffect", "SunRays")
sr.Intensity = 0.03; sr.Spread = 0.5

out[#out + 1] = "water " .. tostring(T.WaterColor) .. " t=" .. T.WaterTransparency .. " clock=" .. L.ClockTime .. " atm=" .. atm.Density .. "/" .. atm.Haze
return table.concat(out, "\n")
