local T = workspace.Terrain
local E = Enum.Material
local V, CF = Vector3.new, CFrame.new
local c = V(-300, 0, -40)
T:FillBlock(CF(c + V(0,20,0)), V(140,40,140), E.Air)
T:FillBlock(CF(c + V(0,-12,0)), V(140,24,140), E.Grass)
T:FillBall(c + V(0,-14,0), 32, E.Sand)
T:FillBlock(CF(c + V(0,20,0)), V(140,40,140), E.Air)
T:FillBall(c + V(0,-12,0), 28, E.Air)
T:FillBlock(CF(c + V(0,-1.5,0)), V(140,3,140), E.Air)
T:FillBall(c + V(0,-12,0), 26.5, E.Water)
T:FillBlock(CF(c + V(0,-1.5,0)), V(140,3,140), E.Air)
-- re-lay grass top layer outside shore, keep sand beach ring
for i = 0, 47 do
	local a = i/48*math.pi*2
	T:FillBlock(CF(c + V(math.cos(a)*40, -2, math.sin(a)*40))*CFrame.Angles(0,-a,0), V(16,4,10), E.Grass)
end
-- stones around the shore
for i = 0, 11 do
	local a = i/12*math.pi*2 + 0.2
	T:FillBall(c + V(math.cos(a)*30, -1, math.sin(a)*30), 3 + (i % 3), E.Rock)
end
-- path back across west road
T:FillBlock(CF(c + V(40,-2,-2)), V(30,4,12), E.Ground)
return 'pond rebuilt'
