local t = workspace:FindFirstChild('SpawnTown')
return 'pong; SpawnTown=' .. tostring(t ~= nil) .. ' csg=' .. tostring(workspace:FindFirstChild('_csg') ~= nil)
