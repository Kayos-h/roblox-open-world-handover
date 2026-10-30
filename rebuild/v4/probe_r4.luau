-- probe_r4: read-only facts for the round-4 fixes
local out = {}
local function P(s) out[#out + 1] = s end
local pm = workspace.Phase1Map
-- 1. waterfall cliff model(s)
for _, m in ipairs(pm.v4_pieces:GetDescendants()) do end
local function findModels(root, prefix, cb)
  for _, m in ipairs(root:GetDescendants()) do
    if m:IsA('Model') and string.sub(m.Name, 1, #prefix) == prefix then cb(m) end
  end
end
for _, root in ipairs({ pm.v4_elf, pm.v4_pieces, pm.v4_rocks }) do
  findModels(root, 'R05_01', function(m)
    local cf, size = m:GetBoundingBox()
    P(string.format('R05_01 in %s at (%.0f,%.0f,%.0f) size %.0fx%.0fx%.0f yaw=%.0f', root.Name, cf.X, cf.Y, cf.Z, size.X, size.Y, size.Z, math.deg(math.atan2(-cf.LookVector.X, -cf.LookVector.Z))))
    for _, p in ipairs(m:GetChildren()) do
      if p:IsA('BasePart') then P(string.format('     part %s %s rgb(%d,%d,%d) tr=%.2f size %.0fx%.0fx%.0f', p.Name, p.Material.Name, p.Color.R * 255, p.Color.G * 255, p.Color.B * 255, p.Transparency, p.Size.X, p.Size.Y, p.Size.Z)) end
    end
  end)
end
-- also search the whole map for R05
local n = 0
for _, m in ipairs(pm:GetDescendants()) do
  if m:IsA('Model') and string.sub(m.Name, 1, 3) == 'R05' and n < 6 then
    n += 1
    local cf = m:GetPivot()
    P(string.format('R05 anywhere: %s in %s at (%.0f,%.0f,%.0f)', m.Name, m.Parent and m.Parent.Name or '?', cf.X, cf.Y, cf.Z))
  end
end
-- 2. blue-ish large parts in the elf valley centre
P('BLUE parts (b > r*1.3 and b > 0.35) larger than 8 studs in x -1800..-1400, z -700..-300:')
local c = 0
for _, p in ipairs(workspace:GetDescendants()) do
  if p:IsA('BasePart') and p.Name ~= 'Terrain' and c < 14 then
    local pos = p.Position
    if pos.X > -1800 and pos.X < -1400 and pos.Z > -700 and pos.Z < -300 and math.max(p.Size.X, p.Size.Y, p.Size.Z) > 8 then
      local col = p.Color
      if col.B > col.R * 1.3 and col.B > 0.35 then
        c += 1
        local m = p:FindFirstAncestorOfClass('Model')
        P(string.format('   %s/%s part %s %s rgb(%d,%d,%d) at (%.0f,%.0f,%.0f) size %.0fx%.0fx%.0f', p.Parent and p.Parent.Name or '?', m and m.Name or '-', p.Name, p.Material.Name, col.R * 255, col.G * 255, col.B * 255, pos.X, pos.Y, pos.Z, p.Size.X, p.Size.Y, p.Size.Z))
      end
    end
  end
end
-- 3. models near the castle pen far edge (gazebo etc.)
P('MODELS in x -150..-55, z -2275..-2212:')
for _, d in ipairs(pm:GetDescendants()) do
  if d:IsA('Model') and d:GetAttribute('PlanKey') or (d:IsA('Model') and d.Parent and d.Parent.Name == 'RoyalGarden') then
    local p = d:GetPivot().Position
    if p.X > -150 and p.X < -55 and p.Z > -2275 and p.Z < -2212 then
      local _, s = d:GetBoundingBox()
      P(string.format('   %s/%s (%.0f,%.0f) size %.0fx%.0fx%.0f', d.Parent and d.Parent.Name or '?', d.Name, p.X, p.Z, s.X, s.Y, s.Z))
    end
  end
end
-- 4. floating slab near (1600,205,-1020)
P('PARTS > 12 studs within 60 of (1600,205,-1020), not terrain:')
local k = 0
for _, p in ipairs(workspace:GetDescendants()) do
  if p:IsA('BasePart') and p.Name ~= 'Terrain' and k < 10 then
    if (p.Position - Vector3.new(1600, 205, -1020)).Magnitude < 60 and math.max(p.Size.X, p.Size.Y, p.Size.Z) > 12 then
      k += 1
      local m = p:FindFirstAncestorOfClass('Model')
      P(string.format('   %s/%s part %s %s at (%.0f,%.0f,%.0f) size %.0fx%.0fx%.0f', p.Parent and p.Parent.Name or '?', m and m.Name or '-', p.Name, p.Material.Name, p.Position.X, p.Position.Y, p.Position.Z, p.Size.X, p.Size.Y, p.Size.Z))
    end
  end
end
return table.concat(out, '\n')
