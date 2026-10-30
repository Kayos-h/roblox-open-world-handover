-- r4_fix1: (1) castle pen: packed-earth floor, archive gazebo + rose arch + topiary strays near the pen, (2) elf ponds: sand collar -> grass, (3) NE snowline near the coast -> grass, (4) mountain scar stripes (Ground on slopes) -> Rock.
-- Replayable (material paints are idempotent, archives guarded by parent).
local pm = workspace.Phase1Map
local T = workspace.Terrain
local SS = game:GetService('ServerStorage')
local arch = SS:FindFirstChild('Phase1Archive_v4') or Instance.new('Folder'); arch.Name = 'Phase1Archive_v4'; arch.Parent = SS
local rp = RaycastParams.new(); rp.FilterType = Enum.RaycastFilterType.Include; rp.FilterDescendantsInstances = { T }; rp.IgnoreWater = true
local function ground(x, z) local r = workspace:Raycast(Vector3.new(x, 900, z), Vector3.new(0, -1300, 0), rp); return r end
local out = {}
local function repl(x0, x1, z0, z1, y0, y1, from, to)
  local ok = pcall(function() T:ReplaceMaterial(Region3.new(Vector3.new(x0, y0, z0), Vector3.new(x1, y1, z1)):ExpandToGrid(4), 4, from, to) end)
  return ok
end
-- 1. castle pen: dirt floor over the whole fenced rectangle (x -141..-69, z -2222..-2172, y around 94)
local passes = 0
for _, from in ipairs({ Enum.Material.Grass, Enum.Material.LeafyGrass, Enum.Material.Pavement, Enum.Material.Cobblestone, Enum.Material.Ground }) do
  if from ~= Enum.Material.Ground and repl(-143, -67, -2224, -2170, 88, 100, from, Enum.Material.Ground) then passes += 1 end
end
-- darker packed earth ring: Mud strips along the fence line is too dark; keep Ground
local n = 0
for _, d in ipairs(pm:GetDescendants()) do
  if d:IsA('Model') and (d.Name == 'K30_gazebo' or d.Name == 'K31_rose_arch' or d.Name == 'K27_topiary_spiral' or d.Name == 'K32_ornate_planter') then
    local p = d:GetPivot().Position
    if p.X > -155 and p.X < -55 and p.Z > -2280 and p.Z < -2205 then d.Parent = arch; n += 1 end
  end
end
out[#out + 1] = string.format('castle pen floor painted (%d passes), garden props archived: %d', passes, n)

-- 2. elf ponds: Sand/Sandstone collar -> Grass around (-1620,-360) and (-1700,-520) radius 60
local sp = 0
for _, c in ipairs({ { -1620, -360 }, { -1700, -520 }, { -1440, -250 } }) do
  for _, from in ipairs({ Enum.Material.Sand, Enum.Material.Sandstone, Enum.Material.Mud }) do
    if repl(c[1] - 60, c[1] + 60, c[2] - 60, c[2] + 60, 8, 22, from, Enum.Material.LeafyGrass) then sp += 1 end
  end
end
out[#out + 1] = 'elf pond collars repainted: ' .. sp

-- 3. NE coast snowline: Snow below y=70 within x 2300..3100, z -1700..-700 becomes LeafyGrass/Rock by slope
local sn = 0
for _, band in ipairs({ { -5, 40 }, { 40, 70 } }) do
  if repl(2300, 3100, -1700, -700, band[1], band[2], Enum.Material.Snow, Enum.Material.Rock) then sn += 1 end
end
out[#out + 1] = 'NE low snow repainted to rock: ' .. sn

-- 4. orange scar stripes: Ground on steep slopes above y=60 within the island interior -> Rock (sample every 40 studs and paint a 40x40 patch when the slope is steep)
local sc, tested = 0, 0
for x = -2600, 2600, 40 do
  for z = -2600, 1800, 40 do
    local r = ground(x, z)
    if r and r.Material == Enum.Material.Ground and r.Position.Y > 60 then
      tested += 1
      local r2 = ground(x + 8, z + 8)
      if r2 and math.abs(r2.Position.Y - r.Position.Y) > 6 then
        if repl(x - 20, x + 20, z - 20, z + 20, r.Position.Y - 8, r.Position.Y + 4, Enum.Material.Ground, Enum.Material.Rock) then sc += 1 end
      end
    end
  end
  if x % 400 == 0 then task.wait() end
end
out[#out + 1] = string.format('scar stripes: tested %d Ground cells above y60, repainted %d steep patches', tested, sc)
return table.concat(out, '\n')
