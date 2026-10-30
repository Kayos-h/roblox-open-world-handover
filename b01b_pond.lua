local T = workspace.Terrain
local E = Enum.Material
local V, CF = Vector3.new, CFrame.new
T:FillBlock(CF(-300,20,-40), V(90,46,90), E.Air)      -- remove everything above y=-3
T:FillBlock(CF(-300,-1.5,-40), V(90,3,90), E.Air)
-- restore grass ring around the pond to ground level
for i = 0, 35 do
	local a = i/36*math.pi*2
	T:FillBlock(CF(-300 + math.cos(a)*40, -2, -40 + math.sin(a)*40)*CFrame.Angles(0,-a,0), V(14,4,12), E.Grass)
end
T:FillBall(V(-300,-30,-40), 30, E.Sand)
T:FillBall(V(-300,-27,-40), 26, E.Water)
T:FillBlock(CF(-300,10,-40), V(70,26,70), E.Air)
-- water surface fill to y=-3
T:FillCylinder(CF(-300,-6,-40), 6, 52, E.Water)
T:FillBlock(CF(-300,0,-40), V(70,6,70), E.Air)
-- sandy shore ring at ground
for i = 0, 35 do
	local a = i/36*math.pi*2
	T:FillBlock(CF(-300 + math.cos(a)*29, -2.5, -40 + math.sin(a)*29)*CFrame.Angles(0,-a,0), V(8,4,8), E.Sand)
end
return 'pond fixed'
