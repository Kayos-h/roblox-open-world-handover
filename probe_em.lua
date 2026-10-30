-- probe: can we build a mesh in Studio and publish it?
local AS = game:GetService('AssetService')
local out = {}
local ok, em = pcall(function() return AS:CreateEditableMesh() end)
table.insert(out, 'create=' .. tostring(ok) .. ' ' .. (ok and '' or tostring(em)))
if ok then
	local a = em:AddVertex(Vector3.new(0, 0, 0))
	local b = em:AddVertex(Vector3.new(4, 0, 0))
	local c = em:AddVertex(Vector3.new(0, 4, 0))
	em:AddTriangle(a, b, c)
	local ok2, mp = pcall(function() return AS:CreateMeshPartAsync(Content.fromObject(em)) end)
	table.insert(out, 'meshpart=' .. tostring(ok2) .. ' ' .. (ok2 and mp.ClassName or tostring(mp)))
	local ok3, res, id = pcall(function()
		return AS:CreateAssetAsync(em, Enum.AssetType.Mesh, { Name = 'probe_tri', Description = 'probe' })
	end)
	table.insert(out, 'publish=' .. tostring(ok3) .. ' ' .. tostring(res) .. ' ' .. tostring(id))
end
return table.concat(out, ' | ')
