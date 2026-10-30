local out = {}
for _, id in ipairs({92960550414449, 10140126732, 131782675995926, 698770549, 11900295788}) do
	local ok, r = pcall(_G.loadAsset, id)
	if not ok then table.insert(out, id .. ' ERR ' .. tostring(r)) else
		local s = id .. ':'
		for _, c in ipairs(r:GetChildren()) do
			local sz = ''
			if c:IsA('Model') then local _, b = c:GetBoundingBox(); sz = string.format('%.1fx%.1fx%.1f', b.X, b.Y, b.Z)
			elseif c:IsA('BasePart') then sz = string.format('%.1fx%.1fx%.1f', c.Size.X, c.Size.Y, c.Size.Z) end
			s = s .. ' [' .. c.ClassName .. ' ' .. c.Name .. ' ' .. sz .. ' n=' .. #c:GetDescendants() .. ']'
		end
		table.insert(out, s)
	end
end
return table.concat(out, ' || ')
