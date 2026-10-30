local hq = workspace.SpawnTown.SkullHQ6
local n = 0
for _, c in ipairs(hq:GetChildren()) do
	if c.Name == 'DemonSkull' then c.Archivable = false; n += 1 end
end
-- make the client script log so we can see it runs
local ls = game:GetService('StarterPlayer').StarterPlayerScripts:FindFirstChild('SkullClient')
if ls and not string.find(ls.Source, 'SkullClient] built', 1, true) then
	ls.Source = ls.Source .. "\nprint('[SkullClient] built', hq:FindFirstChild('DemonSkullLive'))\n"
end
return 'preview non-archivable: ' .. n
