local sc = game:GetService('ServerScriptService'):FindFirstChild('SkullBuilder')
if not sc then return 'no SkullBuilder script' end
sc.Source = [[
print('[SkullBuilder] start')
local ok, err = pcall(function()
	local build = require(game:GetService('ServerStorage'):WaitForChild('SkullBuild'))
	local town = workspace:WaitForChild('SpawnTown', 10)
	print('[SkullBuilder] town', town)
	local hq = town and town:FindFirstChild('SkullHQ6')
	print('[SkullBuilder] hq', hq, hq and #hq:GetChildren())
	if hq then for _, c in ipairs(hq:GetChildren()) do print('[SkullBuilder] child', c.Name, c.ClassName, c:IsA('BasePart') and tostring(c.Size) or '') end end
	for _, c in ipairs(hq:GetChildren()) do if c.Name == 'DemonSkull' then c:Destroy() end end
	local mp, a, b = build()
	print('[SkullBuilder] build ->', mp, a, b)
	if mp then mp.Parent = hq; print('[SkullBuilder] placed', mp.Position, mp.Size) end
end)
if not ok then warn('[SkullBuilder] ERROR ' .. tostring(err)) end
]]
return 'ok disabled=' .. tostring(sc.Disabled) .. ' enabled=' .. tostring(sc.Enabled)
