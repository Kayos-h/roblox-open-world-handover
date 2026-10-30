local T = workspace.Terrain
local E = Enum.Material
local V, CF = Vector3.new, CFrame.new
local c = V(-300, 0, -40)
T:FillBlock(CF(c + V(0,21.5,0)), V(140,43,140), E.Air)
-- water surface slightly below grass (-3): remove water between -3 and 0
T:FillBlock(CF(c + V(0,-1.5,0)), V(56,3,56), E.Air)
-- repaint roads
local function road(p1, p2, w, mat)
	local len = (p2-p1).Magnitude
	T:FillBlock(CF((p1+p2)/2, p2)*CF(0,-2,0), V(w, 4, len + w*0.5), mat)
end
road(V(-230,0,0), V(-380,0,0), 24, E.Cobblestone)
road(V(-260,0,-110), V(-260,0,-75), 12, E.Ground)
road(V(-260,0,-8), V(-260,0,20), 12, E.Ground)
return 'pond clipped, roads repainted'
