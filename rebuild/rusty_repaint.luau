-- Patchy repaint of the dry (rusty) biome so it is not one flat brown. Roads/streets are skipped. Args: JSON with street polylines.
local D = game:GetService("HttpService"):JSONDecode([==[__DATA__]==])
local T = workspace.Terrain
local M = Enum.Material
local CELL = 12
local X0, X1, Z0, Z1 = 700, 1860, 560, 1570
local rp = RaycastParams.new()
rp.FilterType = Enum.RaycastFilterType.Include
rp.FilterDescendantsInstances = { T }
local function ground(x, z) local r = workspace:Raycast(Vector3.new(x, 600, z), Vector3.new(0, -1200, 0), rp) return r and r.Position.Y, r and r.Material end
-- road distance
local segs = {}
for _, s in ipairs(D.streets) do
  for i = 1, #s.pts - 1 do
    local a, b = s.pts[i], s.pts[i + 1]
    table.insert(segs, { a[1], a[2], b[1], b[2], s.w })
  end
end
local function nearRoad(x, z)
  for _, s in ipairs(segs) do
    local vx, vz = s[3] - s[1], s[4] - s[2]
    local L2 = vx * vx + vz * vz
    local t = 0
    if L2 > 0 then t = math.clamp(((x - s[1]) * vx + (z - s[2]) * vz) / L2, 0, 1) end
    local px, pz = s[1] + vx * t, s[2] + vz * t
    local d = math.sqrt((x - px) ^ 2 + (z - pz) ^ 2)
    if d < math.max(s[5], 4) + 10 then return true end
  end
  return false
end
local counts = { Sandstone = 0, Sand = 0, Grass = 0, Mud = 0, Rock = 0, skippedRoad = 0, skippedOther = 0 }
local n = 0
for x = X0, X1 - CELL, CELL do
  for z = Z0, Z1 - CELL, CELL do
    local cx, cz = x + CELL / 2, z + CELL / 2
    local gy, gm = ground(cx, cz)
    if gm == M.Ground then
      if nearRoad(cx, cz) then
        counts.skippedRoad += 1
      else
        local n1 = math.noise(cx / 110, cz / 110, 4.1)          -- big patches
        local n2 = math.noise(cx / 38, cz / 38, 9.7)             -- small breakup
        local n3 = math.noise(cx / 210, cz / 210, 1.3)           -- regions
        local to
        if n1 > 0.22 + 0.15 * n2 then to = M.Sandstone
        elseif n1 < -0.28 + 0.12 * n2 then to = M.Sand
        elseif n3 > 0.2 and n2 > 0.12 then to = M.Grass
        elseif n3 < -0.25 and n2 < -0.2 then to = M.Mud
        elseif n2 > 0.42 then to = M.Rock end
        if to then
          local reg = Region3.new(Vector3.new(x, gy - 10, z), Vector3.new(x + CELL, gy + 4, z + CELL)):ExpandToGrid(4)
          T:ReplaceMaterial(reg, 4, M.Ground, to)
          counts[to.Name] += 1
        end
      end
    else
      counts.skippedOther += 1
    end
    n += 1
    if n % 400 == 0 then task.wait() end
  end
end
local parts = {}
for k, v in pairs(counts) do table.insert(parts, k .. "=" .. v) end
table.sort(parts)
return "rusty biome repaint: " .. table.concat(parts, " ")
