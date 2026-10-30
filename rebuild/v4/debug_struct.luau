-- debug_struct: read-only
local pm = workspace.Phase1Map
local out = {}
local function P(s) out[#out + 1] = s end
-- forest: top-level children names and counts
local byName, varied, total = {}, 0, 0
for _, g in ipairs(pm.v4_forest:GetChildren()) do
  P('forest child: ' .. g.ClassName .. ' ' .. g.Name .. ' n=' .. #g:GetChildren())
  for _, m in ipairs(g:GetChildren()) do
    total += 1
    byName[m.Name] = (byName[m.Name] or 0) + 1
    if m:GetAttribute('Varied') then varied += 1 end
  end
end
P('forest models ' .. total .. ' varied ' .. varied)
local arr = {}
for k, n in pairs(byName) do arr[#arr + 1] = { k, n } end
table.sort(arr, function(a, b) return a[2] > b[2] end)
local s = {}
for i = 1, math.min(#arr, 12) do s[#s + 1] = arr[i][1] .. '=' .. arr[i][2] end
P('names: ' .. table.concat(s, ' '))
-- elf world tree
local cnt = 0
for _, m in ipairs(pm.v4_elf:GetDescendants()) do
  if m:IsA('Model') and string.find(m.Name, 'world_tree', 1, true) then
    cnt += 1
    local parts, shadows = 0, 0
    for _, p in ipairs(m:GetDescendants()) do if p:IsA('BasePart') then parts += 1; if p.CastShadow then shadows += 1 end end end
    P(string.format('elf %s parent=%s parts=%d castShadow=%d', m.Name, m.Parent and m.Parent.Name or '?', parts, shadows))
  end
end
P('world tree models: ' .. cnt)
-- capital structure
local cap = pm.v3_capital
local ex = 0
for _, p in ipairs(cap:GetDescendants()) do
  if p:IsA('BasePart') and (p.Name == 'tile_b' or p.Name == 'terracotta') and ex < 3 then
    ex += 1
    local chain = {}
    local a = p.Parent
    while a and a ~= pm do chain[#chain + 1] = a.ClassName .. ':' .. a.Name; a = a.Parent end
    P('capital roof part ' .. p.Name .. ' ancestors: ' .. table.concat(chain, ' < '))
  end
end
-- banners
for _, fname in ipairs({ 'v3f_castle', 'v4_dress_castle', 'v3_capital' }) do
  local f = pm:FindFirstChild(fname)
  local n, names = 0, {}
  if f then
    for _, m in ipairs(f:GetDescendants()) do
      if m:IsA('Model') and (m.Name == 'K35_royal_banner' or m.Name == 'B05_05_royal_banner') then n += 1; names[m.Parent.Name] = (names[m.Parent.Name] or 0) + 1 end
    end
  end
  local t = {}
  for k, v in pairs(names) do t[#t + 1] = k .. '=' .. v end
  P(fname .. ' banner models ' .. n .. ' in groups: ' .. table.concat(t, ' '))
end
return table.concat(out, '\n')
