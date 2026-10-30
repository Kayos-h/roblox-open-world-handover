-- r3_fix3: (a) soft foam, (b) islet / sea stack plinths, (c) mottled lake ice, (d) harbour plaza paving, (e) mesa variety, (f) elf house jitter, (g) harbour hover scan
-- Replayable except where noted (guards via attributes).
local pm = workspace.Phase1Map
local T = workspace.Terrain
local rp = RaycastParams.new(); rp.FilterType = Enum.RaycastFilterType.Include; rp.FilterDescendantsInstances = { T }; rp.IgnoreWater = true
local function ground(x, z) local r = workspace:Raycast(Vector3.new(x, 900, z), Vector3.new(0, -1300, 0), rp); return r and r.Position.Y or nil end
local out = {}
local rng = Random.new(8808)

-- (a) soft foam: two wide translucent layers, no bright inner strip
local nf = 0
local foam = pm:FindFirstChild('v4_foam')
if foam then
  for _, p in ipairs(foam:GetChildren()) do
    if p:IsA('BasePart') and not p:GetAttribute('Soft') then
      if p.Name == 'FoamA' then
        p.Size = Vector3.new(p.Size.X + 2.0, 0.1, p.Size.Z * 1.9)
        p.Transparency = 0.7 + rng:NextNumber() * 0.12
      else
        p.Size = Vector3.new(p.Size.X + 3.0, 0.08, p.Size.Z * 1.6)
        p.Transparency = 0.9 + rng:NextNumber() * 0.05
      end
      p.Color = Color3.fromRGB(226, 242, 250)
      p:SetAttribute('Soft', true); nf += 1
    end
  end
end
out[#out + 1] = 'foam softened: ' .. nf

-- (b) plinths under islets and sea stacks (solid rock from the sea floor up to the model base)
local np = 0
local pieces = pm:FindFirstChild('v4_pieces')
if pieces then
  for _, g in ipairs(pieces:GetChildren()) do
    if g.Name == 'Islets' or g.Name == 'SeaStacks' then
      for _, m in ipairs(g:GetChildren()) do
        if m:IsA('Model') and not m:GetAttribute('Plinth') then
          local cf, size = m:GetBoundingBox()
          local bottom = cf.Position.Y - size.Y / 2
          local rad = 0.34 * math.max(size.X, size.Z)
          if g.Name == 'SeaStacks' then rad = 0.3 * math.max(size.X, size.Z) end
          rad = math.clamp(rad, 10, 60)
          local top = bottom + 5
          local lowY = -46
          if top > lowY + 4 then
            pcall(function()
              local sea = math.min(top, -4)
              T:FillCylinder(CFrame.new(cf.X, (lowY + sea) / 2, cf.Z), sea - lowY, rad, Enum.Material.Basalt)
              if top > -4 then T:FillCylinder(CFrame.new(cf.X, (-4 + top) / 2, cf.Z), top - (-4), rad * 0.97, Enum.Material.Rock) end
            end)
            m:SetAttribute('Plinth', true); np += 1
          end
        end
      end
    end
  end
end
out[#out + 1] = 'plinths filled: ' .. np

-- (c) mottled ice: 18 boxes of Ice -> Glacier on the frozen lake (centre 1490,-1080 level 131)
local nice = 0
for i = 1, 18 do
  local a = rng:NextNumber() * math.pi * 2
  local r = math.sqrt(rng:NextNumber()) * 0.8
  local x, z = 1490 + math.cos(a) * 170 * r, -1080 + math.sin(a) * 108 * r
  local sx, sz = 16 + rng:NextNumber() * 30, 12 + rng:NextNumber() * 26
  local ok = pcall(function() T:ReplaceMaterial(Region3.new(Vector3.new(x - sx / 2, 122, z - sz / 2), Vector3.new(x + sx / 2, 136, z + sz / 2)):ExpandToGrid(4), 4, Enum.Material.Ice, Enum.Material.Glacier) end)
  if ok then nice += 1 end
end
out[#out + 1] = 'ice patches: ' .. nice

-- (d) harbour plaza paving at (-420, 1560): grass-type cells in a 44x44 box become cobblestone
local gy = ground(-420, 1560) or 14
local npv = 0
for _, from in ipairs({ Enum.Material.Grass, Enum.Material.LeafyGrass, Enum.Material.Ground }) do
  local ok = pcall(function() T:ReplaceMaterial(Region3.new(Vector3.new(-442, gy - 6, 1538), Vector3.new(-398, gy + 5, 1582)):ExpandToGrid(4), 4, from, Enum.Material.Cobblestone) end)
  if ok then npv += 1 end
end
out[#out + 1] = string.format('harbour plaza paved at ground %.1f (%d passes)', gy, npv)

-- (e) mesa variety: tilt, partial sinking, tint
local nm = 0
local p2 = pm:FindFirstChild('v4_pieces2')
local mesas = p2 and p2:FindFirstChild('Mesas')
if mesas then
  for _, m in ipairs(mesas:GetChildren()) do
    if m:IsA('Model') and not m:GetAttribute('Varied') then
      local cf, size = m:GetBoundingBox()
      local piv = m:GetPivot()
      local tilt = CFrame.Angles(math.rad((rng:NextNumber() - 0.5) * 9), 0, math.rad((rng:NextNumber() - 0.5) * 9))
      local sink = size.Y * (rng:NextNumber() * 0.22)
      m:PivotTo(CFrame.new(piv.Position - Vector3.new(0, sink, 0)) * tilt * (piv - piv.Position))
      local k = rng:NextNumber()
      local tint = k < 0.33 and Color3.fromRGB(214, 150, 96) or (k < 0.66 and Color3.fromRGB(150, 98, 70) or Color3.fromRGB(226, 196, 150))
      for _, p in ipairs(m:GetDescendants()) do if p:IsA('BasePart') then p.Color = p.Color:Lerp(tint, 0.22) end end
      m:SetAttribute('Varied', true); nm += 1
    end
  end
end
out[#out + 1] = 'mesas varied: ' .. nm

-- (f) elf houses: scale jitter 0.88..1.12 for treehouses and round houses
local ne = 0
for _, m in ipairs(pm.v4_elf:GetDescendants()) do
  if m:IsA('Model') and not m:GetAttribute('Jit') and (string.sub(m.Name, 1, 6) == 'D01_01' or string.sub(m.Name, 1, 3) == 'D01' or string.sub(m.Name, 1, 6) == 'D04_01' or string.sub(m.Name, 1, 6) == 'D04_02' or string.sub(m.Name, 1, 6) == 'D04_03') then
    pcall(function() m:ScaleTo(m:GetScale() * (0.88 + rng:NextNumber() * 0.24)) end)
    m:SetAttribute('Jit', true); ne += 1
  end
end
out[#out + 1] = 'elf houses scale-jittered: ' .. ne

-- (g) harbour hover / buried scan (report only)
local rep = {}
local hb = pm:FindFirstChild('v3_harbour')
for _, g in ipairs(hb:GetChildren()) do
  for _, m in ipairs(g:GetChildren()) do
    if m:IsA('Model') then
      local cf, size = m:GetBoundingBox()
      if size.X > 14 and size.Y > 12 then
        local hx, hz = size.X * 0.4, size.Z * 0.4
        local lo, hi = 1e9, -1e9
        for _, o in ipairs({ { hx, hz }, { -hx, hz }, { hx, -hz }, { -hx, -hz } }) do
          local gg = ground(cf.X + o[1], cf.Z + o[2])
          if gg then if gg < lo then lo = gg end; if gg > hi then hi = gg end end
        end
        local bottom = cf.Position.Y - size.Y / 2
        if lo < 1e8 and (bottom - lo > 3.5 or hi - bottom > 6) and #rep < 10 then
          rep[#rep + 1] = string.format('%s (%.0f,%.0f) bottom %.1f ground %.1f..%.1f', m.Name, cf.X, cf.Z, bottom, lo, hi)
        end
      end
    end
  end
end
out[#out + 1] = 'harbour buildings hovering/buried: ' .. #rep
for _, r in ipairs(rep) do out[#out + 1] = '   ' .. r end
return table.concat(out, '\n')
