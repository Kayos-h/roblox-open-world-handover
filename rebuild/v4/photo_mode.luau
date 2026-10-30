-- photo mode toggle for high-altitude pictures: MODE is replaced by on or off before sending.
local L = game:GetService("Lighting")
local atm = L:FindFirstChildOfClass("Atmosphere")
if not atm then return "no atmosphere" end
if "__MODE__" == "on" then
  atm.Density = 0.02; atm.Haze = 0.0; atm.Offset = 0.0
else
  atm.Density = atm:GetAttribute("GameDensity") or 0.20
  atm.Haze = atm:GetAttribute("GameHaze") or 0.8
  atm.Offset = atm:GetAttribute("GameOffset") or 0.12
end
return string.format("photo mode %s: density %.2f haze %.2f", "__MODE__", atm.Density, atm.Haze)
