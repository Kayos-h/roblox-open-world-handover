-- b16: extend the map north (wall moves -425 -> -760) and raise a big plateau for the giant skull HQ
local L = _G.L
local V, CF, A = L.V, L.CF, L.A
local T = workspace.Terrain
local E = Enum.Material
local rng = Random.new(16)
local ZN = -760          -- new north wall line
local ZP = -570          -- new plateau centre
local RP = 165           -- plateau radius

-- 1) clear the old outer hills / rocks inside the new northern area, re-lay flat grass
T:FillBlock(CF(0, 119, (ZN - 40 + -425)/2), V(900, 238, (-425) - (ZN - 40)), E.Air)
T:FillBlock(CF(0, -12, (ZN - 40 + -425)/2), V(900, 24, (-425) - (ZN - 40)), E.Grass)
-- remove the old north ring track and the old plateau's northern rim rocks (repaint as grass)
T:FillBlock(CF(0, -2, -410), V(840, 4, 12), E.Grass)
T:FillBlock(CF(0, 70, -400), V(220, 104, 90), E.Air)
-- 2) new big plateau (same 16-top recipe as the old one so heights match at y~17.8)
T:FillCylinder(CF(0, -8, ZP), 48, RP + 8, E.Grass)
T:FillCylinder(CF(0, 4, ZP), 24, RP, E.Grass)
T:FillCylinder(CF(0, 10, ZP), 12, RP - 6, E.Grass)
-- land bridge joining the old courtyard plateau to the new one
T:FillBlock(CF(0, -8, -400), V(150, 48, 90), E.Grass)
T:FillBlock(CF(0, 4, -400), V(140, 24, 90), E.Grass)
T:FillBlock(CF(0, 10, -400), V(130, 12, 90), E.Grass)
-- 3) rocky rim around the new plateau, open on the south where it meets the courtyard
for i = 0, 70 do
	local a = i/70*math.pi*2
	local x, z = math.cos(a)*(RP + 2), ZP + math.sin(a)*(RP + 2)
	if z < -470 then T:FillBall(V(x, 8, z), rng:NextNumber(9, 14), E.Rock) end
end
-- 4) paved processional way from the courtyard to the skull stairs
T:FillBlock(CF(0, 14, -405), V(44, 4, 100), E.Pavement)
T:FillBlock(CF(0, 14, -405), V(34, 4, 100), E.Cobblestone)
-- forecourt in front of the skull
T:FillCylinder(CF(0, 14, -470), 4, 78, E.Pavement)
-- 5) new outer hills beyond the new north wall, and ring track along it
for _, h in ipairs({{-400, -1010, 170}, {0, -1040, 190}, {400, -1010, 170}, {-660, -760, 150}, {660, -760, 150}}) do
	T:FillBall(V(h[1], -h[3]*0.45, h[2]), h[3], E.Grass)
	T:FillBall(V(h[1]*1.02, -h[3]*0.2, h[2]*1.02), h[3]*0.55, E.LeafyGrass)
end
local function road(p1, p2, w, mat)
	local cf = CF((p1 + p2)/2, p2)
	T:FillBlock(cf*CF(0, -2, 0), V(w, 4, (p2 - p1).Magnitude + w*0.5), mat)
end
road(V(-410, 0, ZN + 15), V(410, 0, ZN + 15), 10, E.Ground)
road(V(410, 0, -410), V(410, 0, ZN + 15), 10, E.Ground)
road(V(-410, 0, -410), V(-410, 0, ZN + 15), 10, E.Ground)
-- a few leafy patches for colour variation in the new meadows
for i = 1, 18 do
	local x, z = rng:NextNumber(-400, 400), rng:NextNumber(ZN + 30, -440)
	if math.abs(x) > RP + 30 then
		T:FillBlock(CF(x, -2, z)*A(0, rng:NextNumber(0, 3), 0), V(rng:NextNumber(20, 60), 4, rng:NextNumber(20, 60)), E.LeafyGrass)
	end
end
local function h(x, z) local r = workspace:Raycast(V(x, 300, z), V(0, -600, 0)); return r and string.format('%.1f %s', r.Position.Y, r.Material.Name) or 'nil' end
return 'north ok plateau:' .. h(60, -600) .. ' way:' .. h(0, -420) .. ' court:' .. h(30, -300) .. ' meadow:' .. h(-300, -600) .. ' ring:' .. h(410, -600)
