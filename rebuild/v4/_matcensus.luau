-- material census: read-only. Counts top-surface terrain materials on land (h>3) over the island, and inside the Town 1 zone separately.
local T = workspace.Terrain
local rp = RaycastParams.new(); rp.FilterType = Enum.RaycastFilterType.Include; rp.FilterDescendantsInstances = { T }; rp.IgnoreWater = true
local land, t1 = {}, {}
local nLand, nT1 = 0, 0
local cnt = 0
for x = -3400, 3400, 40 do
  for z = -3400, 2400, 40 do
    local r = workspace:Raycast(Vector3.new(x, 900, z), Vector3.new(0, -1500, 0), rp)
    if r and r.Position.Y > 3 then
      local n = r.Material.Name
      if x >= -330 and x <= 330 and z >= -560 and z <= 320 then t1[n] = (t1[n] or 0) + 1; nT1 += 1
      else land[n] = (land[n] or 0) + 1; nLand += 1 end
    end
    cnt += 1
    if cnt % 800 == 0 then task.wait() end
  end
end
local function fmt(t)
  local a = {}
  for k, v in pairs(t) do a[#a + 1] = { k, v } end
  table.sort(a, function(p, q) return p[2] > q[2] end)
  local s = {}
  for _, p in ipairs(a) do s[#s + 1] = p[1] .. '=' .. p[2] end
  return table.concat(s, ' ')
end
-- also materials present in the Town 1 zone BELOW the surface down to 12 studs (voxel columns, coarse)
local sub = {}
for x = -320, 320, 48 do
  for z = -550, 310, 48 do
    local ok, m = pcall(function() return T:ReadVoxels(Region3.new(Vector3.new(x, -8, z), Vector3.new(x + 4, 24, z + 4)), 4) end)
    if ok and m then for j = 1, #m[1] do local n = m[1][j][1].Name; if n ~= 'Air' and n ~= 'Water' then sub[n] = (sub[n] or 0) + 1 end end end
  end
end
return 'LAND (' .. nLand .. '): ' .. fmt(land) .. '\nTOWN1 surface (' .. nT1 .. '): ' .. fmt(t1) .. '\nTOWN1 sub-surface cells: ' .. fmt(sub)
