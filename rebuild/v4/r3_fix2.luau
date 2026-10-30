-- r3_fix2: (1) canopy shadows off, (2) hovering big rocks sink, (3) banner thinning, (4) capital roof colour variety, (5) forest variety (scale + tint of round deciduous trees).
local pm = workspace.Phase1Map
local T = workspace.Terrain
local SS = game:GetService('ServerStorage')
local arch = SS:FindFirstChild('Phase1Archive_v4') or Instance.new('Folder')
arch.Name = 'Phase1Archive_v4'; arch.Parent = SS
local rp = RaycastParams.new(); rp.FilterType = Enum.RaycastFilterType.Include; rp.FilterDescendantsInstances = { T }; rp.IgnoreWater = true
local function ground(x, z) local r = workspace:Raycast(Vector3.new(x, 900, z), Vector3.new(0, -1300, 0), rp); return r and r.Position.Y or nil end
local out = {}
local rng = Random.new(5150)

-- 1. shadows: world tree canopy, ancient trees and canopies stop casting valley-wide shadows
local n1 = 0
for _, m in ipairs(pm.v4_elf:GetDescendants()) do
  if m:IsA('Model') and (string.sub(m.Name, 1, 6) == 'D05_03' or string.sub(m.Name, 1, 6) == 'D05_01' or string.sub(m.Name, 1, 6) == 'D05_02') then
    for _, p in ipairs(m:GetChildren()) do if p:IsA('BasePart') and p.CastShadow then p.CastShadow = false; n1 += 1 end end
  elseif m:IsA('BasePart') and m.Size.Magnitude > 60 and m.CastShadow and m.Parent and m.Parent:IsA('Model') and string.sub(m.Parent.Name, 1, 3) == 'D05' then
    m.CastShadow = false; n1 += 1
  end
end
out[#out + 1] = 'canopy/tree parts with shadows off: ' .. n1

-- 2. hovering big rocks
local sunk, checked = 0, 0
for _, fname in ipairs({ 'v4_rocks', 'v4_pieces' }) do
  local f = pm:FindFirstChild(fname)
  if f then
    for _, m in ipairs(f:GetDescendants()) do
      if m:IsA('Model') and m:GetAttribute('PlanKey') then
        local cf, size = m:GetBoundingBox()
        if math.max(size.X, size.Z) >= 18 then
          checked += 1
          local hx, hz = size.X * 0.4, size.Z * 0.4
          local gmin = 1e9
          for _, o in ipairs({ { 0, 0 }, { hx, 0 }, { -hx, 0 }, { 0, hz }, { 0, -hz }, { hx * 0.8, hz * 0.8 }, { -hx * 0.8, hz * 0.8 }, { hx * 0.8, -hz * 0.8 }, { -hx * 0.8, -hz * 0.8 } }) do
            local g = ground(cf.X + o[1], cf.Z + o[2])
            if g and g < gmin then gmin = g end
          end
          local bottom = cf.Position.Y - size.Y / 2
          if gmin < 1e8 and bottom - gmin > 3.5 and gmin > -3 then
            local d = math.min(bottom - gmin + 1.2, 40)
            m:PivotTo(m:GetPivot() - Vector3.new(0, d, 0)); sunk += 1
          end
          if checked % 150 == 0 then task.wait() end
        end
      end
    end
  end
end
out[#out + 1] = string.format('big rocks checked %d, sunk to the lowest footprint ground: %d', checked, sunk)

-- 3. banner thinning in the castle (keep every third K35 banner of the central rows)
local nb = 0
local ban = pm:FindFirstChild('v3f_castle') and pm.v3f_castle:FindFirstChild('Banners')
if ban then
  local list = ban:GetChildren()
  table.sort(list, function(a, b) return a:GetPivot().Z > b:GetPivot().Z end)
  for i, m in ipairs(list) do if i % 3 ~= 1 then m.Parent = arch; nb += 1 end end
end
local dc = pm:FindFirstChild('v4_dress_castle') and pm.v4_dress_castle:FindFirstChild('CastleBanners')
if dc then
  local list = dc:GetChildren()
  for i, m in ipairs(list) do if i % 2 == 0 then m.Parent = arch; nb += 1 end end
end
out[#out + 1] = 'banners archived: ' .. nb

-- 4. capital roof colours
local variants = {
  { Color3.fromRGB(176, 96, 62), 25 }, { Color3.fromRGB(94, 100, 110), 15 }, { Color3.fromRGB(120, 88, 64), 15 }, { Color3.fromRGB(70, 118, 110), 10 },
  { Color3.fromRGB(188, 148, 86), 10 }, { Color3.fromRGB(60, 74, 104), 15 }, { Color3.fromRGB(100, 114, 92), 10 },
}
local function pickVariant(seed)
  local r = (math.abs(seed) % 100)
  local acc = 0
  for _, v in ipairs(variants) do acc += v[2]; if r < acc then return v[1] end end
  return variants[1][1]
end
local nr, nm = 0, 0
local cap = pm.v3_capital
for _, m in ipairs(cap:GetDescendants()) do
  if m:IsA('Model') and m:GetAttribute('PlanKey') and not m:GetAttribute('RoofVaried') then
    local touched = false
    local pos = m:GetPivot().Position
    local seed = math.floor(pos.X * 7.13 + pos.Z * 3.71)
    local col = pickVariant(seed)
    for _, p in ipairs(m:GetChildren()) do
      if p:IsA('BasePart') and (p.Name == 'tile_b' or p.Name == 'terracotta') then
        local j = 1 + (((seed + nr) % 7) - 3) * 0.015
        p.Color = Color3.new(math.clamp(col.R * j, 0, 1), math.clamp(col.G * j, 0, 1), math.clamp(col.B * j, 0, 1))
        nr += 1; touched = true
      end
    end
    if touched then m:SetAttribute('RoofVaried', true); nm += 1 end
  end
end
out[#out + 1] = string.format('capital roofs: %d parts on %d buildings recoloured', nr, nm)

-- 5. forest variety: round deciduous trees get scale jitter 0.8..1.3 and a tint variation on their leaves
local round = { A24_oak_1 = true, A25_oak_2 = true, A26_oak_3 = true, A32_maple_autumn = true, A27_birch_1 = true, A28_birch_2 = true }
local nt, tick = 0, 0
for _, g in ipairs(pm.v4_forest:GetChildren()) do
  for _, m in ipairs(g:GetChildren()) do
    if m:IsA('Model') and round[m.Name] and not m:GetAttribute('Varied') then
      local s = 0.8 + rng:NextNumber() * 0.5
      if rng:NextNumber() < 0.12 then s = s * 1.25 end
      pcall(function() m:ScaleTo(m:GetScale() * s) end)
      local tintKind = rng:NextNumber()
      for _, p in ipairs(m:GetChildren()) do
        if p:IsA('BasePart') and p.Material == Enum.Material.LeafyGrass then
          local c = p.Color
          if tintKind < 0.3 then p.Color = c:Lerp(Color3.fromRGB(32, 78, 38), 0.35)
          elseif tintKind < 0.45 then p.Color = c:Lerp(Color3.fromRGB(150, 168, 64), 0.28)
          elseif tintKind < 0.52 then p.Color = c:Lerp(Color3.fromRGB(190, 120, 44), 0.35) end
        end
      end
      m:SetAttribute('Varied', true); nt += 1
      tick += 1
      if tick % 400 == 0 then task.wait() end
    end
  end
end
out[#out + 1] = 'round trees varied: ' .. nt
return table.concat(out, '\n')
