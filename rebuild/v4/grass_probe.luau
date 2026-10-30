-- grass_probe: tries to read and set the terrain grass decoration safely. Never throws.
local T = workspace.Terrain
local out = {}
local ok1, v1 = pcall(function() return T.Decoration end)
out[#out + 1] = 'Decoration read ok=' .. tostring(ok1) .. ' value=' .. tostring(v1)
local ok2, v2 = pcall(function() return T.GrassLength end)
out[#out + 1] = 'GrassLength read ok=' .. tostring(ok2) .. ' value=' .. tostring(v2)
local ok3, e3 = pcall(function() T.GrassLength = 0.4 end)
out[#out + 1] = 'GrassLength set 0.4 ok=' .. tostring(ok3) .. ' ' .. tostring(e3 or '')
local ok4, v4 = pcall(function() return T.GrassLength end)
out[#out + 1] = 'GrassLength after ok=' .. tostring(ok4) .. ' value=' .. tostring(v4)
local ok5, e5 = pcall(function() T.Decoration = false end)
out[#out + 1] = 'Decoration set false ok=' .. tostring(ok5) .. ' ' .. tostring(e5 or '')
local ok6, v6 = pcall(function() return T.Decoration end)
out[#out + 1] = 'Decoration after ok=' .. tostring(ok6) .. ' value=' .. tostring(v6)
local MS = game:GetService('MaterialService')
local ok7, v7 = pcall(function() return MS.Use2022Materials end)
out[#out + 1] = 'Use2022Materials ' .. tostring(v7)
return table.concat(out, '\n')
