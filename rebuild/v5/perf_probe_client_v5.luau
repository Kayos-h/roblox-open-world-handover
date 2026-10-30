-- perf_probe_client_v5.luau : PLAY-MODE frame-rate probe. DRAFT, not yet run (Studio is not installed).
-- Run it on the CLIENT of a playtest: start_playtest(mode='play'), then execute_luau(target='client-1', code=<this file with __DATA__ replaced>).
-- __DATA__ = {"spots":[{"name":"capital_gate","x":0,"z":-1100}, ...], "wait":6, "sample":5}
-- For each spot: teleport the character 10 studs above the terrain, wait for streaming, sample Heartbeat for `sample` seconds, report fps, worst frame, streamed instance count.
-- Pass mark for the first playable version: 30 fps or better at every spot on the machine used, worst frame under 120 ms, no spot with more than 60,000 streamed instances.
local HS = game:GetService('HttpService')
local RS = game:GetService('RunService')
local Players = game:GetService('Players')
local Stats = game:GetService('Stats')
local D = HS:JSONDecode([==[__DATA__]==])
local plr = Players.LocalPlayer
local char = plr.Character or plr.CharacterAdded:Wait()
local hrp = char:WaitForChild('HumanoidRootPart')
local rp = RaycastParams.new()
rp.FilterType = Enum.RaycastFilterType.Include
rp.FilterDescendantsInstances = { workspace.Terrain }
rp.IgnoreWater = true
local function groundAt(x, z)
	local r = workspace:Raycast(Vector3.new(x, 1500, z), Vector3.new(0, -2000, 0), rp)
	return r and r.Position.Y or nil
end
local function stat(name)
	local ok, v = pcall(function() return Stats[name] end)
	return ok and v or nil
end
local out = {}
for _, s in ipairs(D.spots) do
	local g = groundAt(s.x, s.z) or 100
	hrp.Anchored = true
	hrp.CFrame = CFrame.new(s.x, g + 10, s.z)
	task.wait(D.wait or 6)
	local g2 = groundAt(s.x, s.z) or g
	hrp.CFrame = CFrame.new(s.x, g2 + 10, s.z)
	local n, worst = 0, 0
	local last = os.clock()
	local t0 = last
	local conn = RS.Heartbeat:Connect(function()
		local now = os.clock()
		local dt = now - last
		last = now
		n += 1
		if dt > worst then worst = dt end
	end)
	task.wait(D.sample or 5)
	conn:Disconnect()
	local el = os.clock() - t0
	out[#out + 1] = {
		spot = s.name, fps = math.floor(n / el * 10) / 10, worst_ms = math.floor(worst * 1000),
		streamed_instances = #workspace:GetDescendants(), instance_count_stat = stat('InstanceCount'),
		heartbeat_ms = stat('HeartbeatTimeMs'), physics_ms = stat('PhysicsStepTimeMs'),
	}
end
hrp.Anchored = false
return HS:JSONEncode(out)
