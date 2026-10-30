-- Height + material sampler for the 3D figure. Args are injected below as JSON {"z0":..,"z1":..,"step":..,"x0":..,"x1":..}
local D = game:GetService("HttpService"):JSONDecode([==[__DATA__]==])
local rp = RaycastParams.new()
rp.FilterType = Enum.RaycastFilterType.Include
rp.FilterDescendantsInstances = { workspace.Terrain }
rp.IgnoreWater = true
local names, idx = {}, {}
local function code(m)
  local n = tostring(m):sub(15)
  if not idx[n] then names[#names + 1] = n; idx[n] = #names - 1 end
  return idx[n]
end
-- fixed order so the index table is the same in every chunk
for _, n in ipairs({ "Grass", "LeafyGrass", "Ground", "Mud", "Sand", "Sandstone", "Rock", "Slate", "Basalt", "Cobblestone", "Pavement", "Snow", "Glacier", "Ice", "Limestone", "Salt", "Asphalt", "Brick", "Concrete", "WoodPlanks", "Water", "Air" }) do
  names[#names + 1] = n; idx[n] = #names - 1
end
local out = { "MATS " .. table.concat(names, ",") }
local count = 0
for z = D.z0, D.z1, D.step do
  local row = {}
  for x = D.x0, D.x1, D.step do
    local r = workspace:Raycast(Vector3.new(x, 900, z), Vector3.new(0, -1500, 0), rp)
    if r then
      row[#row + 1] = string.format("%d:%d", math.floor(r.Position.Y + 0.5), code(r.Material))
    else
      row[#row + 1] = "-70:4"
    end
    count += 1
  end
  out[#out + 1] = z .. "|" .. table.concat(row, ",")
  if count > 3000 then count = 0; task.wait() end
end
return table.concat(out, "\n")
