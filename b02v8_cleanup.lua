-- b02v8: remove the checkered placeholder in Play.
local SSS = game:GetService('ServerScriptService')
local SPS = game:GetService('StarterPlayer'):WaitForChild('StarterPlayerScripts')

-- server: the saved edit-mode preview has no mesh data in a running game -> delete it at startup
local sc = SSS:FindFirstChild('SkullCleanup') or Instance.new('Script')
sc.Name = 'SkullCleanup'
sc.Source = [[
local hq = workspace:WaitForChild('SpawnTown'):WaitForChild('SkullHQ6')
for _, c in ipairs(hq:GetChildren()) do if c.Name == 'DemonSkull' then c:Destroy() end end
hq.ChildAdded:Connect(function(c) if c.Name == 'DemonSkull' then task.defer(c.Destroy, c) end end)
]]
sc.Parent = SSS

-- client: build its own copy under a different name, and drop any placeholder that still arrives
local ls = SPS:FindFirstChild('SkullClient') or Instance.new('LocalScript')
ls.Name = 'SkullClient'
ls.Source = [[
local RS = game:GetService('ReplicatedStorage')
local build = require(RS:WaitForChild('SkullBuild'))
RS:WaitForChild('SkullMeshData')
local hq = workspace:WaitForChild('SpawnTown'):WaitForChild('SkullHQ6')
local function kill(c) if c.Name == 'DemonSkull' then c:Destroy() end end
for _, c in ipairs(hq:GetChildren()) do kill(c) end
hq.ChildAdded:Connect(kill)
local ok, mp = pcall(build)
if ok and mp then mp.Name = 'DemonSkullLive'; mp.Parent = hq else warn('[SkullClient] build failed: ' .. tostring(mp)) end
]]
ls.Parent = SPS
-- edit mode: keep exactly one preview
local hq = workspace.SpawnTown.SkullHQ6
local keep, n = nil, 0
for _, c in ipairs(hq:GetChildren()) do
	if c.Name == 'DemonSkull' or c.Name == 'DemonSkullLive' then
		if keep then c:Destroy(); n += 1 else keep = c end
	end
end
-- list any other scripts that might be building skulls
local found = {}
for _, d in ipairs(game:GetDescendants()) do
	if d:IsA('LuaSourceContainer') and string.find(d.Source, 'SkullBuild', 1, true) then found[#found+1] = d:GetFullName() end
end
return 'ok removed ' .. n .. ' extra; scripts: ' .. table.concat(found, ', ')
