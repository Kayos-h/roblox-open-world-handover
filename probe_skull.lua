-- probe the realistic skull mesh at H=240: front depth map + CSG carve test
local old = workspace:FindFirstChild('TEST_Skull') if old then old:Destroy() end
local f = Instance.new('Model'); f.Name = 'TEST_Skull'; f.Parent = workspace
local holder = _G.loadAsset(16673452471)
local src = holder:GetChildren()[1]
local mp = src:IsA('MeshPart') and src or src:FindFirstChildWhichIsA('MeshPart', true)
local H = 240
local m = mp:Clone()
local k = H / m.Size.Y
m.Size = m.Size * k
m.Anchored = true
local base = Vector3.new(220, 2, -640)
m.CFrame = CFrame.new(base + Vector3.new(0, m.Size.Y/2, 0)) * CFrame.Angles(0, math.pi, 0)
m.Parent = f
local out = {string.format('size=%.1f,%.1f,%.1f', m.Size.X, m.Size.Y, m.Size.Z)}
local rp = RaycastParams.new(); rp.FilterType = Enum.RaycastFilterType.Include; rp.FilterDescendantsInstances = {m}
-- front depth map: rows y=0..H step 12, cols x=-84..84 step 12; digit = depth behind row's front-most (/6), '.' = miss
for y = H - 6, 0, -12 do
	local row, zs = {}, {}
	for x = -84, 84, 12 do
		local hit = workspace:Raycast(base + Vector3.new(x, y, 300), Vector3.new(0, 0, -600), rp)
		zs[#zs+1] = hit and hit.Position.Z or false
	end
	local front = -1e9
	for _, z in ipairs(zs) do if z and z > front then front = z end end
	for _, z in ipairs(zs) do
		if not z then row[#row+1] = '.' else row[#row+1] = tostring(math.min(9, math.floor((front - z)/6))) end
	end
	out[#out+1] = string.format('y%3d f=%6.1f %s', y, front - base.Z, table.concat(row, ''))
end
-- side profile at x=0: front z per y already in f column; also width per y
local ws = {}
for y = 0, H, 24 do
	local lo, hi = nil, nil
	local hit1 = workspace:Raycast(base + Vector3.new(-300, y, 0), Vector3.new(600, 0, 0), rp)
	local hit2 = workspace:Raycast(base + Vector3.new(300, y, 0), Vector3.new(-600, 0, 0), rp)
	ws[#ws+1] = string.format('%d:%s', y, (hit1 and hit2) and string.format('%.0f', hit2.Position.X - hit1.Position.X) or '-')
end
out[#out+1] = 'width@z0 ' .. table.concat(ws, ' ')
-- CSG test
local cut = Instance.new('Part'); cut.Anchored = true; cut.Size = Vector3.new(30, 40, 60)
cut.CFrame = CFrame.new(base + Vector3.new(0, 60, m.Size.Z/2)); cut.Parent = f
local ok, res = pcall(function() return m:SubtractAsync({cut}) end)
out[#out+1] = 'csg=' .. tostring(ok) .. ' ' .. (ok and res.ClassName or tostring(res))
if ok then res:Destroy() end
cut:Destroy()
return table.concat(out, '\n')
