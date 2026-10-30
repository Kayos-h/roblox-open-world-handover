local RS = game:GetService('RunService')
local out = {'running=' .. tostring(RS:IsRunning()), 'server=' .. tostring(RS:IsServer())}
local t = workspace:FindFirstChild('SpawnTown')
local hq = t and t:FindFirstChild('SkullHQ6')
out[#out+1] = 'hq=' .. tostring(hq)
if hq then for _, c in ipairs(hq:GetChildren()) do out[#out+1] = c.Name .. ':' .. c.ClassName .. (c:IsA('BasePart') and (' size=' .. tostring(c.Size) .. ' pos=' .. tostring(c.Position) .. ' mesh=' .. tostring(c:IsA('MeshPart') and c.MeshContent)) or '') end end
local ok, e = pcall(function()
	local em = game:GetService('AssetService'):CreateEditableMesh()
	return em
end)
out[#out+1] = 'createEM=' .. tostring(ok) .. ' ' .. tostring(e)
return table.concat(out, ' | ')
