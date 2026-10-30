local rp = RaycastParams.new()
rp.FilterType = Enum.RaycastFilterType.Include
rp.FilterDescendantsInstances = { workspace.Terrain }
rp.IgnoreWater = false
local pts = {
  igloo1 = {1504, -822}, igloo2 = {1456, -834}, igloo3 = {1425, -988},
  shanty1 = {1460, -1080}, hole1 = {1469, -1076}, icelake_c = {1490, -1080},
  alpine_sq = {1630, -872}, lodge = {1585, -880},
  elf_tree = {-1560, -430}, elf_path = {-1430, -425}, elf_temple = {-1490, -170},
  elf_house1 = {-1730, -300},
  castle = {0, -2140}, cap_gate = {0, -1225}, cap_sq = {0, -1500},
  rusty_church = {1406, 1244}, hut1 = {1185, 1141}, hut_street = {1160, 1180},
  harbour_quay = {-390, 1808}, tavern = {-428, 1764}, harbour_sea = {-600, 1900},
  t1_gate_s = {0, 320}, t1_corner_se = {320, 320}, t1_plaza = {0, 0}, t1_skull = {0, -402},
  gy_in = {-200, 230}, gy_mid = {-238, 246}, church_front = {-60, 245},
  tower_top = {1380, -1300}, silverrun = {-700, -200},
}
local out = {}
for k, v in pairs(pts) do
  local r = workspace:Raycast(Vector3.new(v[1], 800, v[2]), Vector3.new(0, -1600, 0), rp)
  table.insert(out, string.format("%s,%d,%d,%.1f,%s", k, v[1], v[2], r and r.Position.Y or -999, r and tostring(r.Material) or "none"))
end
table.sort(out)
return table.concat(out, "\n")
