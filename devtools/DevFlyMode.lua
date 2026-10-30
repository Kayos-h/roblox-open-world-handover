-- DevFlyMode: testing tool. Works ONLY inside Roblox Studio (Play / Play Here); does nothing in the live game.
-- F = fly on/off | WASD = move | Space = up | Ctrl or Q = down | Shift = fast
-- [ and ] = slower / faster | N = noclip (fly through walls) | 1-7 = teleport to areas | H = hide help
local RunService = game:GetService('RunService')
if not RunService:IsStudio() then return end

local UIS = game:GetService('UserInputService')
local Players = game:GetService('Players')
local player = Players.LocalPlayer

local flying, noclip = false, false
local speed = 90
local lv, ao, att

local SPOTS = {
	[Enum.KeyCode.One]   = { 'Town 1 spawn',        Vector3.new(-66, 8, 245) },
	[Enum.KeyCode.Two]   = { 'Capital gate',        Vector3.new(0, 30, -1225) },
	[Enum.KeyCode.Three] = { 'Castle courtyard',    Vector3.new(0, 100, -2140) },
	[Enum.KeyCode.Four]  = { 'Alpine village',      Vector3.new(1630, 128, -872) },
	[Enum.KeyCode.Five]  = { 'Rusty town church',   Vector3.new(1310, 22, 1170) },
	[Enum.KeyCode.Six]   = { 'Harbour quay',        Vector3.new(-390, 10, 1808) },
	[Enum.KeyCode.Seven] = { 'Elf world tree',      Vector3.new(-1430, 22, -425) },
}

-- small on-screen help
local gui = Instance.new('ScreenGui')
gui.Name = 'DevFlyHelp'; gui.ResetOnSpawn = false; gui.IgnoreGuiInset = true
local label = Instance.new('TextLabel')
label.Size = UDim2.new(0, 430, 0, 118); label.Position = UDim2.new(0, 12, 1, -130)
label.BackgroundColor3 = Color3.fromRGB(20, 20, 26); label.BackgroundTransparency = 0.35
label.TextColor3 = Color3.fromRGB(240, 240, 240); label.Font = Enum.Font.GothamMedium; label.TextSize = 14
label.TextXAlignment = Enum.TextXAlignment.Left; label.TextYAlignment = Enum.TextYAlignment.Top
label.Parent = gui
local pad = Instance.new('UIPadding'); pad.PaddingLeft = UDim.new(0, 10); pad.PaddingTop = UDim.new(0, 8); pad.Parent = label
local corner = Instance.new('UICorner'); corner.CornerRadius = UDim.new(0, 8); corner.Parent = label
gui.Parent = player:WaitForChild('PlayerGui')

local function refresh(msg)
	label.Text = string.format('DEV FLY (Studio only)   Fly: %s   Noclip: %s   Speed: %d\n' ..
		'F fly  |  WASD move  |  Space up  |  Ctrl/Q down  |  Shift fast\n' ..
		'[ ] speed  |  N noclip  |  H hide this\n' ..
		'1 Town1  2 Capital  3 Castle  4 Alpine  5 Rusty  6 Harbour  7 Elf\n%s',
		flying and 'ON' or 'off', noclip and 'ON' or 'off', speed, msg or '')
end
refresh()

local function parts()
	local char = player.Character
	if not char then return end
	return char, char:FindFirstChildOfClass('Humanoid'), char:FindFirstChild('HumanoidRootPart')
end

local function stopFly()
	flying = false
	if lv then lv:Destroy() lv = nil end
	if ao then ao:Destroy() ao = nil end
	if att then att:Destroy() att = nil end
	local _, hum = parts()
	if hum then hum.PlatformStand = false; hum:ChangeState(Enum.HumanoidStateType.Freefall) end
	refresh()
end

local function startFly()
	local _, hum, root = parts()
	if not hum or not root then return end
	att = Instance.new('Attachment'); att.Name = 'DevFlyAtt'; att.Parent = root
	lv = Instance.new('LinearVelocity')
	lv.Attachment0 = att; lv.RelativeTo = Enum.ActuatorRelativeTo.World
	lv.MaxForce = math.huge; lv.VectorVelocity = Vector3.zero; lv.Parent = root
	ao = Instance.new('AlignOrientation')
	ao.Mode = Enum.OrientationAlignmentMode.OneAttachment; ao.Attachment0 = att
	ao.MaxTorque = math.huge; ao.Responsiveness = 60; ao.CFrame = root.CFrame; ao.Parent = root
	hum.PlatformStand = true
	flying = true
	refresh()
end

UIS.InputBegan:Connect(function(input, processed)
	if processed then return end
	local k = input.KeyCode
	if k == Enum.KeyCode.F then
		if flying then stopFly() else startFly() end
	elseif k == Enum.KeyCode.N then
		noclip = not noclip; refresh()
	elseif k == Enum.KeyCode.LeftBracket then
		speed = math.max(20, speed - 30); refresh()
	elseif k == Enum.KeyCode.RightBracket then
		speed = math.min(1500, speed + 30); refresh()
	elseif k == Enum.KeyCode.H then
		label.Visible = not label.Visible
	elseif SPOTS[k] then
		local _, _, root = parts()
		if root then
			root.AssemblyLinearVelocity = Vector3.zero
			root.CFrame = CFrame.new(SPOTS[k][2])
			refresh('Teleported: ' .. SPOTS[k][1])
		end
	end
end)

RunService.RenderStepped:Connect(function()
	if not flying then return end
	local _, hum, root = parts()
	if not root or not lv then stopFly() return end
	local cam = workspace.CurrentCamera
	local look, right = cam.CFrame.LookVector, cam.CFrame.RightVector
	local dir = Vector3.zero
	if UIS:IsKeyDown(Enum.KeyCode.W) then dir += look end
	if UIS:IsKeyDown(Enum.KeyCode.S) then dir -= look end
	if UIS:IsKeyDown(Enum.KeyCode.D) then dir += right end
	if UIS:IsKeyDown(Enum.KeyCode.A) then dir -= right end
	if UIS:IsKeyDown(Enum.KeyCode.Space) then dir += Vector3.yAxis end
	if UIS:IsKeyDown(Enum.KeyCode.LeftControl) or UIS:IsKeyDown(Enum.KeyCode.Q) then dir -= Vector3.yAxis end
	local s = speed * (UIS:IsKeyDown(Enum.KeyCode.LeftShift) and 3 or 1)
	lv.VectorVelocity = dir.Magnitude > 0 and dir.Unit * s or Vector3.zero
	local flat = Vector3.new(look.X, 0, look.Z)
	if flat.Magnitude > 0.01 then ao.CFrame = CFrame.lookAt(Vector3.zero, flat) end
end)

RunService.Stepped:Connect(function()
	if not noclip then return end
	local char = player.Character
	if not char then return end
	for _, p in ipairs(char:GetDescendants()) do
		if p:IsA('BasePart') then p.CanCollide = false end
	end
end)

player.CharacterAdded:Connect(function()
	flying = false; lv = nil; ao = nil; att = nil
	refresh()
end)
