local T = workspace.Terrain
local out = {}
local EMPTY = { [Enum.Material.Air] = true, [Enum.Material.Water] = true }
local function slice(y, x0, x1, z)
  local mats = T:ReadVoxels(Region3.new(Vector3.new(x0, y, z), Vector3.new(x1, y + 4, z + 4)), 4)
  local row = {}
  local runs, cur = {}, nil
  local nx = #mats
  for i = 1, nx do
    local solid = not EMPTY[mats[i][1][1]]
    if not cur or cur.s ~= solid then cur = { s = solid, a = i, b = i }; table.insert(runs, cur) else cur.b = i end
  end
  local parts = {}
  for _, r in ipairs(runs) do if r.s then table.insert(parts, string.format("%d..%d", x0 + (r.a - 1) * 4, x0 + r.b * 4)) end end
  return table.concat(parts, " ")
end
for _, y in ipairs({ 60, 100, 150, 200, 250, 290, 310 }) do
  table.insert(out, string.format("y=%d z=-1300 solid x: %s", y, slice(y, 800, 2000, -1300)))
end
-- N-S slice through massif centre
local function sliceZ(y, z0, z1, x)
  local mats = T:ReadVoxels(Region3.new(Vector3.new(x, y, z0), Vector3.new(x + 4, y + 4, z1)), 4)
  local runs, cur = {}, nil
  local nz = #mats[1][1]
  for k = 1, nz do
    local solid = not EMPTY[mats[1][1][k]]
    if not cur or cur.s ~= solid then cur = { s = solid, a = k, b = k }; table.insert(runs, cur) else cur.b = k end
  end
  local parts = {}
  for _, r in ipairs(runs) do if r.s then table.insert(parts, string.format("%d..%d", z0 + (r.a - 1) * 4, z0 + r.b * 4)) end end
  return table.concat(parts, " ")
end
for _, y in ipairs({ 100, 200, 290 }) do
  table.insert(out, string.format("y=%d x=1380 solid z: %s", y, sliceZ(y, -1900, -700, 1380)))
end
return table.concat(out, "\n")
