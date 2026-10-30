local SS = game:GetService('ServerStorage')
local K = 0.7
local function mapX(x) if math.abs(math.abs(x) - 425) < 30 then return x - (x > 0 and 1 or -1) * 425 * (1 - K) end return x * K end
local function mapZ(z) if math.abs(z - 425) < 30 then return z - 425 * (1 - K) end if math.abs(z + 760) < 30 then return z + 760 * (1 - K) end return z * K end
local arc = SS.Town1_Removed
local old = arc:FindFirstChild('Lamps')
if old then old:Destroy() end
local src = SS.Town1_Backup.SpawnTown.Residential:FindFirstChild('Lamps')
if not src then return 'no Lamps in backup' end
local m = src:Clone()
local n = 0
for _, c in ipairs(m:GetChildren()) do
  if c:IsA('Model') and c:FindFirstChildWhichIsA('BasePart', true) then
    local cf = c:GetBoundingBox()
    c:PivotTo(c:GetPivot() + Vector3.new(mapX(cf.X) - cf.X, 0, mapZ(cf.Z) - cf.Z)); n += 1
  elseif c:IsA('BasePart') then
    c.CFrame = c.CFrame + Vector3.new(mapX(c.Position.X) - c.Position.X, 0, mapZ(c.Position.Z) - c.Position.Z); n += 1
  end
end
m.Parent = workspace.SpawnTown.Residential
return 'lamps restored: ' .. n .. ' children'
