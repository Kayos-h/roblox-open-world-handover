local gy = workspace.Phase1Map:FindFirstChild("town1_graveyard")
if not gy then return "no graveyard folder" end
local old = gy:FindFirstChild("GraveMist")
if old then old:Destroy() end
local f = Instance.new("Folder"); f.Name = "GraveMist"; f.Parent = gy
local rp = RaycastParams.new()
rp.FilterType = Enum.RaycastFilterType.Include
rp.FilterDescendantsInstances = { workspace.Terrain }
local n = 0
for _, c in ipairs({ { -262, 222 }, { -262, 270 }, { -232, 232 }, { -232, 262 }, { -206, 224 }, { -206, 268 }, { -248, 246 }, { -218, 246 } }) do
  local r = workspace:Raycast(Vector3.new(c[1], 200, c[2]), Vector3.new(0, -400, 0), rp)
  if r then
    local p = Instance.new("Part")
    p.Name = "Mist"; p.Anchored = true; p.CanCollide = false; p.CanQuery = false; p.CanTouch = false; p.CastShadow = false
    p.Transparency = 1; p.Size = Vector3.new(34, 3, 34); p.Position = Vector3.new(c[1], r.Position.Y + 2.2, c[2]); p.Parent = f
    local e = Instance.new("ParticleEmitter")
    e.Texture = "rbxasset://textures/particles/smoke_main.dds"
    e.Color = ColorSequence.new(Color3.fromRGB(176, 182, 198))
    e.Transparency = NumberSequence.new({ NumberSequenceKeypoint.new(0, 1), NumberSequenceKeypoint.new(0.25, 0.84), NumberSequenceKeypoint.new(0.75, 0.88), NumberSequenceKeypoint.new(1, 1) })
    e.Size = NumberSequence.new({ NumberSequenceKeypoint.new(0, 9), NumberSequenceKeypoint.new(1, 16) })
    e.Lifetime = NumberRange.new(9, 13)
    e.Rate = 2.2
    e.Speed = NumberRange.new(0.2, 0.7)
    e.SpreadAngle = Vector2.new(180, 180)
    e.RotSpeed = NumberRange.new(-6, 6)
    e.Rotation = NumberRange.new(0, 360)
    e.LightEmission = 0
    e.LightInfluence = 1
    e.Acceleration = Vector3.new(0.15, 0, 0.05)
    e.Parent = p
    n += 1
  end
end
return "mist emitters: " .. n
