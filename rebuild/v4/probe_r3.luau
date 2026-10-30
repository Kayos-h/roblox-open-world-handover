-- probe_r3: read-only facts behind the round-3 fixes
local out = {}
local function P(s) out[#out + 1] = s end
local pm = workspace.Phase1Map
local function bb(m) local cf, size = m:GetBoundingBox(); return cf, size end

-- 1. grass model heights
local grass = { A49_tall_grass_1 = 1, A50_tall_grass_2 = 1, F05_09_grass_tall_a = 1, F05_10_grass_tall_b = 1, A51_fern = 1, F05_11_sea_oats = 1, F05_12_dune_tuft = 1, D06_01_fern_a = 1, D06_02_fern_b = 1, D06_03_fern_c = 1 }
local stat = {}
for _, fname in ipairs({ 'v4_under', 'v4_dress_castle', 'v4_dress_capital', 'v4_elf', 'town1_dress', 'v4_shore' }) do
  local f = pm:FindFirstChild(fname)
  if f then
    for _, m in ipairs(f:GetDescendants()) do
      if m:IsA('Model') and grass[m.Name] then
        local _, s = bb(m)
        local e = stat[m.Name] or { n = 0, h = 0, hmax = 0 }
        e.n += 1; e.h += s.Y; if s.Y > e.hmax then e.hmax = s.Y end
        stat[m.Name] = e
      end
    end
  end
end
for k, e in pairs(stat) do P(string.format('GRASS %s count=%d avgH=%.1f maxH=%.1f', k, e.n, e.h / e.n, e.hmax)) end

-- 2. things near the reported floating cubes
local function near(x, y, z, r, label)
  P('NEAR ' .. label)
  local n = 0
  for _, d in ipairs(workspace:GetDescendants()) do
    if d:IsA('BasePart') and d.Name ~= 'Terrain' then
      local p = d.Position
      if (p - Vector3.new(x, y, z)).Magnitude < r and d.Size.Magnitude > 20 and n < 8 then
        local m = d:FindFirstAncestorOfClass('Model')
        P(string.format('   %s / %s (%.0f,%.0f,%.0f) size %.0fx%.0fx%.0f %s', d.Parent and d.Parent.Name or '?', m and m.Name or d.Name, p.X, p.Y, p.Z, d.Size.X, d.Size.Y, d.Size.Z, d.Material.Name))
        n += 1
      end
    end
  end
end
near(1500, 210, -1050, 90, 'cube 1')
near(1750, 250, -650, 90, 'cube 2')

-- 3. elf: waterfall models and world tree parts
local elf = pm:FindFirstChild('v4_elf')
local wf = {}
local tree = {}
if elf then
  for _, m in ipairs(elf:GetDescendants()) do
    if m:IsA('Model') then
      local nm = m.Name
      if string.sub(nm, 1, 3) == 'D09' or string.sub(nm, 1, 6) == 'F10_03' or string.sub(nm, 1, 6) == 'F10_04' or string.sub(nm, 1, 6) == 'F10_05' then
        local cf = m:GetPivot()
        wf[#wf + 1] = string.format('%s (%.0f,%.0f,%.0f)', nm, cf.X, cf.Y, cf.Z)
      end
      if string.sub(nm, 1, 6) == 'D05_01' or string.sub(nm, 1, 6) == 'D05_02' or string.sub(nm, 1, 6) == 'D05_03' then
        for _, p in ipairs(m:GetChildren()) do
          if p:IsA('BasePart') then
            tree[#tree + 1] = string.format('%s/%s %s rgb(%d,%d,%d)', nm, p.Name, p.Material.Name, p.Color.R * 255, p.Color.G * 255, p.Color.B * 255)
          end
        end
      end
    end
  end
end
P('ELF waterfall-type models: ' .. #wf)
for i = 1, math.min(#wf, 14) do P('   ' .. wf[i]) end
P('ELF world tree parts: ' .. #tree)
for i = 1, math.min(#tree, 14) do P('   ' .. tree[i]) end

-- 4. capital roofs
local roofs = {}
local cap = pm:FindFirstChild('v3_capital')
local nroof = 0
if cap then
  for _, p in ipairs(cap:GetDescendants()) do
    if p:IsA('BasePart') and string.find(string.lower(p.Name), 'roof', 1, true) then
      nroof += 1
      local k = string.format('%s %s rgb(%d,%d,%d)', p.Name, p.Material.Name, p.Color.R * 255, p.Color.G * 255, p.Color.B * 255)
      roofs[k] = (roofs[k] or 0) + 1
    end
  end
end
P('CAPITAL roof-named parts: ' .. nroof)
local ra = {}
for k, n in pairs(roofs) do ra[#ra + 1] = { k, n } end
table.sort(ra, function(a, b) return a[2] > b[2] end)
for i = 1, math.min(#ra, 14) do P(string.format('   %s x%d', ra[i][1], ra[i][2])) end

-- 5. church glass
local glass = {}
for _, p in ipairs(workspace:GetDescendants()) do
  if p:IsA('BasePart') and p.Material == Enum.Material.Glass then
    local pos = p.Position
    if (Vector2.new(pos.X, pos.Z) - Vector2.new(1406, 1244)).Magnitude < 90 then
      local k = string.format('%s rgb(%d,%d,%d) tr=%.2f', p.Name, p.Color.R * 255, p.Color.G * 255, p.Color.B * 255, p.Transparency)
      glass[k] = (glass[k] or 0) + 1
    end
  end
end
for k, n in pairs(glass) do P('CHURCH glass ' .. k .. ' x' .. n) end

-- 6. training yard strays
P('YARD strays (centres inside x -148..-62, z -2230..-2165):')
for _, d in ipairs(pm:GetDescendants()) do
  if d:IsA('Model') and (d:GetAttribute('PlanKey') or d.Parent == pm.v4_castle_yard) then
    local p = d:GetPivot().Position
    if p.X > -148 and p.X < -62 and p.Z > -2230 and p.Z < -2165 then
      P(string.format('   %s / %s (%.0f,%.0f,%.0f)', d.Parent and d.Parent.Name or '?', d.Name, p.X, p.Y, p.Z))
    end
  end
end
return table.concat(out, '\n')
