local L = _G.L
local V, CF, A = L.V, L.CF, L.A
local f = L.folder(workspace, '_AssetTest')
local TREE = 79689531752352
_G.installVariants(_G.loadAsset(TREE))
for i = 1, 20 do
	local t = _G.tpl(TREE, 'Models_Trees/Models/Tree_' .. string.format('%02d', i))
	local x = -300 + (i-1)*32
	_G.place(t, f, L.at(x, 490), 30)
end
for i = 1, 3 do
	_G.place(_G.tpl(TREE, 'Models_Bushes/Models/Bush_0' .. i), f, L.at(-300 + i*14, 460), 5)
end
local fl = {711333951, 743377736, 16428845157, 1353190583, 16071638063, 136744769027061}
for i, id in ipairs(fl) do
	local root = _G.loadAsset(id)
	local item = root:GetChildren()[1]
	local m = Instance.new('Model'); for _, c in ipairs(root:GetChildren()) do c:Clone().Parent = m end
	_G.place(m, f, L.at(-220 + i*14, 460), (id == 1353190583) and 5 or 2.5)
	m:Destroy()
end
return 'test ok'
