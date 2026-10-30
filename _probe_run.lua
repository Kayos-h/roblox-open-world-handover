_G.__probeIds = {79689531752352,12605122162,9203561683}
-- probe: try loading assets via game:GetObjects and summarize
local ids = _G.__probeIds or {}
local out = {}
for _, id in ipairs(ids) do
	local ok, res = pcall(function() return game:GetObjects('rbxassetid://' .. id) end)
	if not ok then
		table.insert(out, id .. ' FAIL ' .. tostring(res):sub(1, 80))
	else
		local parts, meshes, scripts, models = 0, 0, 0, 0
		local names = {}
		for _, root in ipairs(res) do
			for _, d in ipairs(root:GetDescendants()) do
				if d:IsA('BasePart') then parts += 1 end
				if d:IsA('MeshPart') then meshes += 1 end
				if d:IsA('LuaSourceContainer') then scripts += 1 end
				if d:IsA('Model') then models += 1 end
			end
			for _, c in ipairs(root:GetChildren()) do if #names < 14 then table.insert(names, c.Name .. ':' .. c.ClassName) end end
			root:Destroy()
		end
		table.insert(out, string.format('%s OK roots=%d parts=%d mesh=%d scripts=%d models=%d | %s', id, #res, parts, meshes, scripts, models, table.concat(names, ', ')))
	end
end
return table.concat(out, '\n')
