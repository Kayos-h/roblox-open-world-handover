-- look_pass3b: Basalt becomes the deep-sea navy (Brick was swapped to Basalt). Land has no Basalt on its surface (census), so this only changes the seabed.
local T = workspace.Terrain
T:SetMaterialColor(Enum.Material.Basalt, Color3.fromRGB(10, 46, 98))
return 'Basalt ' .. tostring(T:GetMaterialColor(Enum.Material.Basalt))
