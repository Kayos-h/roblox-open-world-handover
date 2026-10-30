-- v4 look pass 3 (after terrain v4d): seabed colour ramp (Sand -> Concrete -> Asphalt -> Brick are the shallow-to-deep steps, they are unused on land),
-- lighter river beds, shaded snow, tan limestone roads, more aerial haze. Replayable via execute_luau.
local T = workspace.Terrain
local L = game:GetService("Lighting")
local out = {}
local function C(r, g, b) return Color3.fromRGB(r, g, b) end

local colors = {
  Grass = C(74, 146, 46), LeafyGrass = C(48, 112, 40), Mud = C(104, 92, 62), Sand = C(232, 214, 160),
  Rock = C(118, 112, 102), Slate = C(86, 90, 100), Basalt = C(58, 60, 66), Ground = C(176, 130, 84),
  Snow = C(232, 238, 246), Glacier = C(206, 228, 244), Ice = C(160, 206, 232), Sandstone = C(196, 128, 80),
  Limestone = C(204, 178, 134), Salt = C(176, 138, 96), Cobblestone = C(150, 140, 128), Pavement = C(170, 160, 146),
  Concrete = C(66, 178, 178), Asphalt = C(26, 108, 160), Brick = C(10, 46, 98),
}
for name, col in pairs(colors) do
  local ok, err = pcall(function() T:SetMaterialColor(Enum.Material[name], col) end)
  if not ok then out[#out + 1] = "color fail " .. name .. ": " .. tostring(err) end
end

pcall(function()
  T.WaterColor = C(20, 98, 146)
  T.WaterTransparency = 0.8
  T.WaterReflectance = 0.45
  T.WaterWaveSize = 0.22
  T.WaterWaveSpeed = 12
end)

local atm = L:FindFirstChildOfClass("Atmosphere")
if atm then
  atm.Density = 0.14; atm.Offset = 0.1; atm.Color = C(198, 214, 236); atm.Decay = C(96, 122, 160); atm.Glare = 0.1; atm.Haze = 1.5
  atm:SetAttribute("GameDensity", 0.14); atm:SetAttribute("GameHaze", 1.5); atm:SetAttribute("GameOffset", 0.1)
end
out[#out + 1] = "water " .. tostring(T.WaterColor) .. " t=" .. T.WaterTransparency .. (atm and (" atm=" .. atm.Density .. "/" .. atm.Haze) or "")
return table.concat(out, "\n")
