-- quick banner test at an open spot south of the plaza
local L = _G.L
local f = L.folder(workspace, 'TEST_Banner')
local G = L.ground(0, 130)
L.cyl(f, 20, 0.8, L.CF(0, G + 10, 129), L.C.iron, L.M.metal)
L.banner(f, L.CF(-4, G + 12, 130), Color3.fromRGB(70,40,120), 12, L.C.gold)
L.banner(f, L.CF(4, G + 12, 130), Color3.fromRGB(150,40,48), 12, L.C.gold)
return 'banner test ok'
