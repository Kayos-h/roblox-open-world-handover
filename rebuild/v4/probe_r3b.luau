-- probe_r3b: read-only. (1) capital part kinds by count, (2) elf river path + world tree canopy parts, (3) floating terrain in the alpine zone, (4) all K35 banners.
local out = {}
local function P(s) out[#out + 1] = s end
local pm = workspace.Phase1Map
local cap = pm.v3_capital
local kinds = {}
for _, p in ipairs(cap:GetDescendants()) do
  if p:IsA('BasePart') then
    local k = string.format('%s|%s|%d,%d,%d', p.Name, p.Material.Name, p.Color.R * 255, p.Color.G * 255, p.Color.B * 255)
    kinds[k] = (kinds[k] or 0) + 1
  end
end
local ka = {}
for k, n in pairs(kinds) do ka[#ka + 1] = { k, n } end
table.sort(ka, function(a, b) return a[2] > b[2] end)
P('CAPITAL part kinds (top 22):')
for i = 1, math.min(#ka, 22) do P(string.format('   %s x%d', ka[i][1], ka[i][2])) end

local elf = pm.v4_elf
local can = {}
for _, m in ipairs(elf:GetDescendants()) do
  if m:IsA('Model') and (string.sub(m.Name, 1, 6) == 'D05_03' or string.sub(m.Name, 1, 6) == 'D05_04' or string.sub(m.Name, 1, 6) == 'D05_09' or string.sub(m.Name, 1, 6) == 'D05_10') then
    for _, p in ipairs(m:GetChildren()) do
      if p:IsA('BasePart') then can[#can + 1] = string.format('%s/%s cast=%s size=%.0fx%.0fx%.0f', m.Name, p.Name, tostring(p.CastShadow), p.Size.X, p.Size.Y, p.Size.Z) end
    end
  end
end
P('ELF canopy/ancient-tree parts: ' .. #can)
for i = 1, math.min(#can, 8) do P('   ' .. can[i]) end

local ice = {}
for _, p in ipairs(workspace:GetDescendants()) do
  if p:IsA('BasePart') and p.Parent and p.Parent:IsA('Model') and p.Parent.Name == 'K35_royal_banner' then ice[#ice + 1] = p end
end
P('K35 banner parts: ' .. #ice)
return table.concat(out, '\n')
