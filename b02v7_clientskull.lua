-- b02v7: make the demon skull visible in Play.
-- EditableMesh-built MeshParts do not replicate to clients, so each client builds its own copy.
local RS = game:GetService('ReplicatedStorage')
local SS = game:GetService('ServerStorage')
local SSS = game:GetService('ServerScriptService')
local SPS = game:GetService('StarterPlayer'):WaitForChild('StarterPlayerScripts')

-- 1) move mesh data + builder module where clients can read them
local data = SS:FindFirstChild('SkullMeshData') or RS:FindFirstChild('SkullMeshData')
if not data then return 'no SkullMeshData' end
data.Parent = RS
local mod = SS:FindFirstChild('SkullBuild') or RS:FindFirstChild('SkullBuild')
if not mod then return 'no SkullBuild' end
mod.Source = string.gsub(mod.Source, "game:GetService%('ServerStorage'%)", "game:GetService('ReplicatedStorage')")
mod.Parent = RS

-- 2) server script: only removes stale (empty) saved copies; server keeps no mesh
local sc = SSS:FindFirstChild('SkullBuilder')
if sc then sc:Destroy() end

-- 3) client builder
local ls = SPS:FindFirstChild('SkullClient') or Instance.new('LocalScript')
ls.Name = 'SkullClient'
ls.Source = [[
local RS = game:GetService('ReplicatedStorage')
local build = require(RS:WaitForChild('SkullBuild'))
RS:WaitForChild('SkullMeshData')
local town = workspace:WaitForChild('SpawnTown')
local hq = town:WaitForChild('SkullHQ6')
for _, c in ipairs(hq:GetChildren()) do if c.Name == 'DemonSkull' then c:Destroy() end end
local ok, mp = pcall(build)
if ok and mp then mp.Parent = hq else warn('[SkullClient] build failed: ' .. tostring(mp)) end
]]
ls.Parent = SPS

-- 4) edit mode: keep exactly one preview copy (saved file will contain an empty part; the client replaces it)
local hq = workspace.SpawnTown:FindFirstChild('SkullHQ6')
local n = 0
for _, c in ipairs(hq:GetChildren()) do if c.Name == 'DemonSkull' then c:Destroy(); n += 1 end end
local build = require(mod)
local mp = build()
mp.Parent = hq
return string.format('removed %d stale copies; module in RS=%s; client script ok; preview size=%s', n, tostring(mod.Parent == RS), tostring(mp.Size))
