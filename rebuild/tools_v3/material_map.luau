local out = {}
local rp = RaycastParams.new()
rp.FilterType = Enum.RaycastFilterType.Include
rp.FilterDescendantsInstances = { workspace.Terrain }
rp.IgnoreWater = false
local function ray(x, z) return workspace:Raycast(Vector3.new(x, 800, z), Vector3.new(0, -1600, 0), rp) end
local sym = { [Enum.Material.Ground] = "g", [Enum.Material.Mud] = "m", [Enum.Material.Grass] = ".", [Enum.Material.LeafyGrass] = ",", [Enum.Material.Sand] = "s",
  [Enum.Material.Sandstone] = "S", [Enum.Material.Rock] = "R", [Enum.Material.Slate] = "R", [Enum.Material.Cobblestone] = "c", [Enum.Material.Pavement] = "p", [Enum.Material.Water] = "~", [Enum.Material.Snow] = "*" }
table.insert(out, "x from 700 to 1900 step 40 (31 cols); rows z 560..1700 step 40")
for z = 560, 1700, 40 do
  local row = {}
  for x = 700, 1900, 40 do
    local r = ray(x, z)
    row[#row + 1] = r and (sym[r.Material] or "?") or " "
  end
  table.insert(out, string.format("%4d %s", z, table.concat(row)))
end
-- tower_south grey rectangle: sample materials at foreground (camera 1380,210,-450 looking north)
table.insert(out, "grey patch probe, x 1300..1700, z -760..-560 step 40")
for z = -760, -560, 40 do
  local row = {}
  for x = 1300, 1700, 40 do
    local r = ray(x, z)
    row[#row + 1] = r and string.format("%s%.0f", sym[r.Material] or "?", r.Position.Y) or "none"
  end
  table.insert(out, string.format("%5d %s", z, table.concat(row, " ")))
end
return table.concat(out, "\n")
