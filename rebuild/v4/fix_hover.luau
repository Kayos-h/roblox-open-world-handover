-- fix_hover: (1) archive R04 sea-cliff slabs, (2) seat hovering / underwater rocks and islets onto the terrain.
-- Replayable. Archive folder: ServerStorage.Phase1Archive_v4. Only touches models with a PlanKey in v4_pieces / v4_rocks / v4_shore.
local SS = game:GetService('ServerStorage')
local T = workspace.Terrain
local rp = RaycastParams.new(); rp.FilterType = Enum.RaycastFilterType.Include; rp.FilterDescendantsInstances = { T }; rp.IgnoreWater = true
local function ground(x, z)
  local r = workspace:Raycast(Vector3.new(x, 700, z), Vector3.new(0, -900, 0), rp)
  return r and r.Position.Y or nil
end
local arch = SS:FindFirstChild('Phase1Archive_v4') or Instance.new('Folder')
arch.Name = 'Phase1Archive_v4'; arch.Parent = SS
local pm = workspace.Phase1Map
local out = {}
local archived, moved, removedUW = 0, 0, 0

-- 1. R04 slabs
local list = {}
for _, d in ipairs(pm:GetDescendants()) do
  if d:IsA('Model') and d:GetAttribute('PlanKey') and string.sub(d.Name, 1, 4) == 'R04_' then list[#list + 1] = d end
end
for _, m in ipairs(list) do m.Parent = arch; archived += 1 end

-- 2. seat hovering models: footprint samples, lowest ground wins
for _, folderName in ipairs({ 'v4_pieces', 'v4_rocks' }) do
  local f = pm:FindFirstChild(folderName)
  if f then
    local n = 0
    for _, m in ipairs(f:GetDescendants()) do
      if m:IsA('Model') and m:GetAttribute('PlanKey') then
        n += 1
        local cf, size = m:GetBoundingBox()
        local bottom = cf.Position.Y - size.Y / 2
        local hx, hz = size.X * 0.4, size.Z * 0.4
        local lo, hi = 1e9, -1e9
        local pts = { { 0, 0 }, { hx, 0 }, { -hx, 0 }, { 0, hz }, { 0, -hz }, { hx * 0.8, hz * 0.8 }, { -hx * 0.8, hz * 0.8 }, { hx * 0.8, -hz * 0.8 }, { -hx * 0.8, -hz * 0.8 } }
        for _, o in ipairs(pts) do
          local g = ground(cf.Position.X + o[1], cf.Position.Z + o[2])
          if g then if g < lo then lo = g end; if g > hi then hi = g end end
        end
        if lo < 1e8 then
          local gap = bottom - lo
          local isWaterZone = hi < 2
          -- hovering over a lower footprint edge: sink so the lowest sample is covered (bounded to 40 studs)
          if gap > 6 and (isWaterZone or size.X > 25) then
            local d = math.min(gap + 1.0, 40)
            m:PivotTo(m:GetPivot() - Vector3.new(0, d, 0)); moved += 1
          end
        end
        if n % 300 == 0 then task.wait() end
      end
    end
  end
end

-- 3. rocks that sit fully under water (nobody sees them) go to the archive
local f = pm:FindFirstChild('v4_rocks')
if f then
  for _, m in ipairs(f:GetDescendants()) do
    if m:IsA('Model') and m:GetAttribute('PlanKey') then
      local cf, size = m:GetBoundingBox()
      if cf.Position.Y + size.Y / 2 < -1.5 then m.Parent = arch; removedUW += 1 end
    end
  end
end
return string.format('archived R04=%d, seated=%d, archived fully-underwater rocks=%d', archived, moved, removedUW)
