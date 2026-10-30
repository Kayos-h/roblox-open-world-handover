-- Break up flat grey cliff faces: Rock -> patches of Slate / Basalt / Rock, only on the mountain ranges (y > 60 and not near towns).
local T = workspace.Terrain
local M = Enum.Material
local CELL = 16
local rp = RaycastParams.new()
rp.FilterType = Enum.RaycastFilterType.Include
rp.FilterDescendantsInstances = { T }
local function ground(x, z) local r = workspace:Raycast(Vector3.new(x, 700, z), Vector3.new(0, -1400, 0), rp) return r and r.Position.Y, r and r.Material end
local boxes = {
  { 950, 1850, -1950, -600 },   -- tower massif + east ridge
  { -2150, -850, -1700, 300 },  -- elf mountains + north-west ridge
  { -1000, 200, -2100, -1500 }, -- northern ridge
}
local counts = { Slate = 0, Basalt = 0, Limestone = 0, skipped = 0 }
local n = 0
for _, b in ipairs(boxes) do
  for x = b[1], b[2] - CELL, CELL do
    for z = b[3], b[4] - CELL, CELL do
      local cx, cz = x + CELL / 2, z + CELL / 2
      local gy, gm = ground(cx, cz)
      if gm == M.Rock and gy > 60 then
        local a = math.noise(cx / 70, cz / 70, 2.2)
        local c = math.noise(cx / 23, cz / 23, 6.8)
        local to
        if a > 0.18 + 0.1 * c then to = M.Slate
        elseif a < -0.22 + 0.1 * c then to = M.Basalt
        elseif c > 0.45 then to = M.Limestone end
        if to then
          local reg = Region3.new(Vector3.new(x, gy - 24, z), Vector3.new(x + CELL, gy + 4, z + CELL)):ExpandToGrid(4)
          T:ReplaceMaterial(reg, 4, M.Rock, to)
          counts[to.Name] += 1
        end
      else
        counts.skipped += 1
      end
      n += 1
      if n % 300 == 0 then task.wait() end
    end
  end
end
return string.format("rock faces varied: Slate=%d Basalt=%d Limestone=%d skipped=%d", counts.Slate, counts.Basalt, counts.Limestone, counts.skipped)
