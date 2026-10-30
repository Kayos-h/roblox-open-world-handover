-- probe7: load store packs and describe their contents
local out = {}
for _, id in ipairs({2199756085, 121230482146932}) do
	local ok, r = pcall(function() return _G.describe(_G.loadAsset(id), 3) end)
	table.insert(out, '== ' .. id .. '\n' .. tostring(r):sub(1, 2500))
end
return table.concat(out, '\n')
