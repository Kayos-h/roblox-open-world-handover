-- Compress Town 1 to 70% around the plaza (0,0). Building sizes unchanged (skull unchanged).
local SS = game:GetService('ServerStorage')
local ST = workspace.SpawnTown
if ST:GetAttribute('V3Compressed') then return 'already compressed' end
local K = 0.7
local WALLX, WALLS, WALLN = 425, 425, -760
local function mapAxisX(x)
  if math.abs(math.abs(x) - WALLX) < 30 then return x - (x > 0 and 1 or -1) * WALLX * (1 - K) end
  return x * K
end
local function mapAxisZ(z)
  if math.abs(z - WALLS) < 30 then return z - WALLS * (1 - K) end
  if math.abs(z - WALLN) < 30 then return z - WALLN * (1 - K) end
  return z * K
end
local function moveModel(m)
  if not m:FindFirstChildWhichIsA('BasePart', true) then return end
  local pv = m:GetPivot()
  local cf, sz = m:GetBoundingBox()
  local nx, nz = mapAxisX(cf.X), mapAxisZ(cf.Z)
  m:PivotTo(pv + Vector3.new(nx - cf.X, 0, nz - cf.Z))
end
local function movePart(p)
  local nx, nz = mapAxisX(p.Position.X), mapAxisZ(p.Position.Z)
  p.CFrame = p.CFrame + Vector3.new(nx - p.Position.X, 0, nz - p.Position.Z)
end
-- linear wall model: compress along its axis, shift across
local function squashWall(m, axis)
  local cf, sz = m:GetBoundingBox()
  local shiftX = (axis == 'z') and (mapAxisX(cf.X) - cf.X) or 0
  local shiftZ = (axis == 'x') and (mapAxisZ(cf.Z) - cf.Z) or 0
  local wdir = (axis == 'x') and Vector3.xAxis or Vector3.zAxis
  for _, p in ipairs(m:GetDescendants()) do
    if p:IsA('BasePart') then
      local pos = p.Position
      local along = (axis == 'x') and pos.X or pos.Z
      local newAlong = along * K
      local np = (axis == 'x') and Vector3.new(newAlong, pos.Y, pos.Z + shiftZ) or Vector3.new(pos.X + shiftX, pos.Y, newAlong)
      local rot = p.CFrame - p.CFrame.Position
      -- which local axis lies along the wall?
      local ax = { p.CFrame.RightVector, p.CFrame.UpVector, p.CFrame.LookVector }
      local size = p.Size
      local comps = { size.X, size.Y, size.Z }
      for i = 1, 3 do
        if math.abs(ax[i]:Dot(wdir)) > 0.98 and comps[i] > 7 then comps[i] = comps[i] * K end
      end
      p.Size = Vector3.new(comps[1], comps[2], comps[3])
      p.CFrame = CFrame.new(np) * rot
    end
  end
end
local log = {}
-- walls folder
for _, m in ipairs(ST.Walls:GetChildren()) do
  if m:IsA('Model') then
    if m.Name == 'Wall_E' or m.Name == 'Wall_W' then squashWall(m, 'z')
    elseif m.Name == 'Wall_N' or m.Name == 'Wall_S' then squashWall(m, 'x')
    else moveModel(m) end
  end
end
-- everything else in SpawnTown (recurse into group models)
local GROUPS = { Clutter = true, Furniture = true, Stalls = true }
local function handle(inst)
  if inst:IsA('Model') then
    if GROUPS[inst.Name] then
      for _, c in ipairs(inst:GetChildren()) do handle(c) end
    else moveModel(inst) end
  elseif inst:IsA('BasePart') then movePart(inst)
  elseif inst:IsA('Folder') then for _, c in ipairs(inst:GetChildren()) do handle(c) end end
end
for _, f in ipairs(ST:GetChildren()) do
  if f.Name ~= 'Walls' then handle(f) end
end
-- Phase1Map Town 1 additions
for _, n in ipairs({ 'town1', 'town1_extra', 'town1_yard' }) do
  local f = workspace.Phase1Map:FindFirstChild(n)
  if f then for _, g in ipairs(f:GetChildren()) do handle(g) end end
end
ST:SetAttribute('V3Compressed', true)
-- overlap resolution: archive lower-priority houses that now intersect more important buildings
local arc = SS:FindFirstChild('Town1_Removed') or Instance.new('Folder'); arc.Name = 'Town1_Removed'; arc.Parent = SS
local bld = {}
local function addB(m, pri) local cf, sz = m:GetBoundingBox() table.insert(bld, { m = m, pri = pri, x0 = cf.X - sz.X / 2, x1 = cf.X + sz.X / 2, z0 = cf.Z - sz.Z / 2, z1 = cf.Z + sz.Z / 2, a = sz.X * sz.Z }) end
for _, m in ipairs(ST.Residential:GetChildren()) do if m:IsA('Model') then addB(m, 1) end end
for _, m in ipairs(ST.Market:GetChildren()) do if m:IsA('Model') and m.Name:find('Shop') then addB(m, 2) end end
for _, fn in ipairs({ 'Landmarks', 'Crafts', 'Farm' }) do for _, m in ipairs(ST[fn]:GetChildren()) do if m:IsA('Model') then addB(m, 5) end end end
for _, n in ipairs({ 'GrandEmporium', 'MarketHall', 'Warehouse' }) do local m = ST.Market:FindFirstChild(n) if m then addB(m, 5) end end
for _, m in ipairs(ST.Walls:GetChildren()) do if m:IsA('Model') and not m.Name:find('Wall_') then addB(m, 9) end end
local skf = workspace.Phase1Map.town1_extra:FindFirstChild('SkullHQ')
local sk = skf and skf:FindFirstChildWhichIsA('Model')
if sk then addB(sk, 9) end
local chf = workspace.Phase1Map.town1:FindFirstChild('Church')
local ch = chf and chf:FindFirstChildWhichIsA('Model')
if ch then addB(ch, 8) end
local removed = {}
for i = 1, #bld do
  local a = bld[i]
  if a.m.Parent and a.pri < 5 then
    for j = 1, #bld do
      local b = bld[j]
      if i ~= j and b.m.Parent and b.m.Parent ~= arc and (b.pri > a.pri or (b.pri == a.pri and j < i)) then
        local ix = math.min(a.x1, b.x1) - math.max(a.x0, b.x0)
        local iz = math.min(a.z1, b.z1) - math.max(a.z0, b.z0)
        if ix > 0 and iz > 0 and ix * iz > 0.12 * math.min(a.a, b.a) then
          a.m.Parent = arc; table.insert(removed, a.m.Name); break
        end
      end
    end
  end
end
return 'compressed; archived ' .. #removed .. ': ' .. table.concat(removed, ', ')
