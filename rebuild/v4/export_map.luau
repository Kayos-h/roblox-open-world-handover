-- Exports a coarse map of the real terrain for the environment generator. Args JSON: {"x0","x1","z0","z1","step"}
-- Returns rows: one string per z row, 6 chars per x cell: hh (ground height base36, offset +100), m (material letter), ww (water surface base36 offset +100, "--" = none)
local D = game:GetService("HttpService"):JSONDecode([==[__DATA__]==])
local ws = game:GetService("Workspace")
local T = ws.Terrain
local rpG = RaycastParams.new(); rpG.FilterType = Enum.RaycastFilterType.Include; rpG.FilterDescendantsInstances = { T }; rpG.IgnoreWater = true
local rpW = RaycastParams.new(); rpW.FilterType = Enum.RaycastFilterType.Include; rpW.FilterDescendantsInstances = { T }; rpW.IgnoreWater = false
local CODE = {
  Grass = "G", LeafyGrass = "L", Sand = "S", Mud = "M", Rock = "R", Slate = "T", Basalt = "B", Snow = "N", Ice = "I", Glacier = "I",
  Ground = "D", Sandstone = "A", Cobblestone = "C", Pavement = "P", Limestone = "K", Salt = "H", Asphalt = "P", Concrete = "P", Brick = "C", WoodPlanks = "C",
}
local DIG = "0123456789abcdefghijklmnopqrstuvwxyz"
local function b36(n)
  n = math.clamp(math.floor(n + 0.5), 0, 1295)
  return DIG:sub(math.floor(n / 36) + 1, math.floor(n / 36) + 1) .. DIG:sub(n % 36 + 1, n % 36 + 1)
end
local rows = {}
for z = D.z0, D.z1, D.step do
  local parts = table.create(math.floor((D.x1 - D.x0) / D.step) + 1)
  for x = D.x0, D.x1, D.step do
    local g = ws:Raycast(Vector3.new(x, 900, z), Vector3.new(0, -1500, 0), rpG)
    if g then
      local w = ws:Raycast(Vector3.new(x, 900, z), Vector3.new(0, -1500, 0), rpW)
      local wl = "--"
      if w and w.Material == Enum.Material.Water then wl = b36(w.Position.Y + 100) end
      parts[#parts + 1] = b36(g.Position.Y + 100) .. (CODE[g.Material.Name] or "E") .. wl
    else
      parts[#parts + 1] = "00" .. "X" .. "--"
    end
  end
  rows[#rows + 1] = table.concat(parts)
end
return game:GetService("HttpService"):JSONEncode(rows)
