local T = workspace.Terrain
local rp = RaycastParams.new()
rp.FilterType = Enum.RaycastFilterType.Include
rp.FilterDescendantsInstances = { T }
rp.IgnoreWater = false
local out = {}
local function dump(x, z)
  local x4, z4 = math.floor(x / 4) * 4, math.floor(z / 4) * 4
  local mats, occ = T:ReadVoxels(Region3.new(Vector3.new(x4, -64, z4), Vector3.new(x4 + 4, 500, z4 + 4)), 4)
  local col, oc = mats[1], occ[1]
  local runs, cur = {}, nil
  for i = 1, #col do
    local m = col[i][1]
    local o = oc[i][1]
    local solid = (m ~= Enum.Material.Air) and (m ~= Enum.Material.Water) and o > 0.05
    local key = solid and tostring(m):sub(15) or (m == Enum.Material.Water and "~water" or "air")
    if not cur or cur.k ~= key then cur = { k = key, s = i, e = i, o = o }; table.insert(runs, cur) else cur.e = i end
  end
  local parts = {}
  for _, r in ipairs(runs) do table.insert(parts, string.format("%s[%d..%d]", r.k, -64 + (r.s - 1) * 4, -64 + r.e * 4)) end
  local hit = workspace:Raycast(Vector3.new(x4 + 2, 800, z4 + 2), Vector3.new(0, -1600, 0), rp)
  table.insert(out, string.format("(%d,%d) topray=%s | %s", x4, z4, hit and string.format("%.0f %s", hit.Position.Y, tostring(hit.Material):sub(15)) or "none", table.concat(parts, " ")))
end
for _, p in ipairs({ {1500,-1500}, {1500,-1480}, {1512,-1536}, {-1200,-1500}, {-1200,-1020}, {1200,-1350}, {1380,-1300}, {1000,-1100} }) do dump(p[1], p[2]) end
return table.concat(out, "\n")
