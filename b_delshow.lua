local t = workspace:FindFirstChild('TEST_Show') if t then t:Destroy() end
return 'show removed=' .. tostring(t ~= nil)
