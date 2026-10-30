-- yard_probe: read-only. (1) every model inside the training pen with its height, (2) heights of grass-type models after the shrink, per model name.
local out = {}
local function P(s) out[#out + 1] = s end
local pm = workspace.Phase1Map
local inside = {}
for _, d in ipairs(pm:GetDescendants()) do
  if d:IsA('Model') and not d:FindFirstAncestorOfClass('Model') then
    local ok, cf, size = pcall(function() return d:GetBoundingBox() end)
    if ok and cf.X > -148 and cf.X < -62 and cf.Z > -2230 and cf.Z < -2165 then
      inside[#inside + 1] = string.format('%s/%s (%.0f,%.0f) h=%.1f w=%.1f scale=%.2f', d.Parent and d.Parent.Name or '?', d.Name, cf.X, cf.Z, size.Y, math.max(size.X, size.Z), d:GetScale())
    end
  end
end
table.sort(inside)
P('MODELS inside the pen: ' .. #inside)
for i = 1, math.min(#inside, 40) do P('   ' .. inside[i]) end
-- grass-like heights
local names = { 'A49_tall_grass_1', 'A50_tall_grass_2', 'F05_09_grass_tall_a', 'F05_10_grass_tall_b', 'A51_fern', 'F05_11_sea_oats', 'F05_12_dune_tuft', 'D06_01_fern_a', 'D06_02_fern_b', 'D06_03_fern_c', 'F06_19_flowers_wild', 'A38_bush_1', 'A39_bush_2', 'A40_bush_3', 'F05_01_bush_round', 'F05_04_bush_juniper', 'A44_flowers_yellow' }
local want = {}
for _, n in ipairs(names) do want[n] = { n = 0, h = 0, hmax = 0, sc = 0 } end
for _, f in ipairs(pm:GetChildren()) do
  if f:IsA('Folder') then
    for _, m in ipairs(f:GetDescendants()) do
      if m:IsA('Model') and want[m.Name] then
        local _, s = m:GetBoundingBox()
        local e = want[m.Name]
        e.n += 1; e.h += s.Y; e.sc += m:GetScale(); if s.Y > e.hmax then e.hmax = s.Y end
      end
    end
  end
end
for _, n in ipairs(names) do
  local e = want[n]
  if e.n > 0 then P(string.format('HEIGHT %-24s count=%-5d avgH=%.1f maxH=%.1f avgScale=%.2f', n, e.n, e.h / e.n, e.hmax, e.sc / e.n)) end
end
return table.concat(out, '\n')
