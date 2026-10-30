-- road_check: read-only. Material of the terrain surface at every 6th road sample; plus how many forest trees stand within 14 / 26 studs of a main-road sample.
local HS = game:GetService('HttpService')
local D = HS:JSONDecode([==[__DATA__]==])
local T = workspace.Terrain
local rp = RaycastParams.new(); rp.FilterType = Enum.RaycastFilterType.Include; rp.FilterDescendantsInstances = { T }; rp.IgnoreWater = true
local mats, n = {}, 0
local grid = {}
local CELL = 40
for i, s in ipairs(D.samples) do
  if s[5] == 'Limestone' then
    local k = math.floor(s[1] / CELL) .. ',' .. math.floor(s[2] / CELL)
    grid[k] = grid[k] or {}
    table.insert(grid[k], s)
  end
  if i % 6 == 0 then
    local r = workspace:Raycast(Vector3.new(s[1], 900, s[2]), Vector3.new(0, -1300, 0), rp)
    if r then mats[r.Material.Name .. '/' .. s[5]] = (mats[r.Material.Name .. '/' .. s[5]] or 0) + 1; n += 1 end
  end
end
local a = {}
for k, c in pairs(mats) do a[#a + 1] = k .. '=' .. c end
table.sort(a)
local near14, near26, total = 0, 0, 0
for _, g in ipairs(workspace.Phase1Map.v4_forest:GetChildren()) do
  for _, m in ipairs(g:GetChildren()) do
    total += 1
    local p = m:GetPivot().Position
    local cx, cz = math.floor(p.X / CELL), math.floor(p.Z / CELL)
    local best = 1e9
    for dx = -1, 1 do for dz = -1, 1 do
      local list = grid[(cx + dx) .. ',' .. (cz + dz)]
      if list then for _, s in ipairs(list) do
        local d = math.sqrt((p.X - s[1]) ^ 2 + (p.Z - s[2]) ^ 2)
        if d < best then best = d end
      end end
    end end
    if best < 14 then near14 += 1 end
    if best < 26 then near26 += 1 end
  end
end
return string.format('road centre surface (every 6th sample, %d probes): %s\nforest trees %d: within 14 of a main road centreline %d, within 26: %d', n, table.concat(a, ' '), total, near14, near26)
