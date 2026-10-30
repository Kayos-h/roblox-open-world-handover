local out = {}
local function add(s) table.insert(out, s) end
local ch = workspace.Phase1Map.town1.Church:FindFirstChild("D01_church")
add("Church V3Done=" .. tostring(ch and ch:GetAttribute("V3Done")))
if ch then
  local cf, sz = ch:GetBoundingBox()
  add(string.format("Church at (%.0f,%.0f,%.0f) size (%.0f,%.0f,%.0f)", cf.X, cf.Y, cf.Z, sz.X, sz.Y, sz.Z))
end
local st = workspace:FindFirstChild("SpawnTown")
add("SpawnTown V3Compressed=" .. tostring(st and st:GetAttribute("V3Compressed")))

local rp = RaycastParams.new()
rp.FilterType = Enum.RaycastFilterType.Include
rp.FilterDescendantsInstances = { workspace.Terrain }
local function groundY(x, z)
  local r = workspace:Raycast(Vector3.new(x, 600, z), Vector3.new(0, -1200, 0), rp)
  return r and r.Position.Y or nil
end
local pb = workspace.Phase1Map.PartBuilt
for _, folder in ipairs(pb:GetChildren()) do
  local floatN, sinkN, okN, noGround = 0, 0, 0, 0
  local worst = 0
  for _, m in ipairs(folder:GetChildren()) do
    local cf, sz
    if m:IsA("Model") then cf, sz = m:GetBoundingBox() else cf, sz = m.CFrame, m.Size end
    local g = groundY(cf.X, cf.Z)
    if not g then
      noGround += 1
    else
      local bottom = cf.Y - sz.Y / 2
      local d = bottom - g
      if math.abs(d) > math.abs(worst) then worst = d end
      if d > 2 then floatN += 1 elseif d < -3 then sinkN += 1 else okN += 1 end
    end
  end
  add(string.format("PartBuilt.%s: n=%d ok=%d floating=%d sunk=%d noGround=%d worstOffset=%.1f", folder.Name, #folder:GetChildren(), okN, floatN, sinkN, noGround, worst))
end
return table.concat(out, "\n")
