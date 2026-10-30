-- Pass 2: handle solids that sit above a WATER layer (stale remnants). Args as JSON: {"x0","x1","z0","z1","tag"}
local D = game:GetService("HttpService"):JSONDecode([==[__DATA__]==])
local T = workspace.Terrain
local RES, CH = 4, 128
local Y0, Y1 = -64, 520
local M = Enum.Material
local AIR, WATER, ROCK = M.Air, M.Water, M.Rock
local list = {}
for cz = D.z0, D.z1 - 1, CH do for cx = D.x0, D.x1 - 1, CH do table.insert(list, { cx, cz }) end end
_G.FILL2 = { i = 0, n = #list, deletedVox = 0, filledVox = 0, delCols = 0, fillCols = 0, errs = {}, done = false, started = os.clock(), tag = D.tag, maxdel = 0 }
local G = _G.FILL2
local function inTown1(x, z) return x >= -312 and x <= 312 and z >= -548 and z <= 316 end
task.spawn(function()
  for idx, c in ipairs(list) do
    if _G.FILL2 ~= G then return end
    local ok, err = pcall(function()
      local cx0, cz0 = c[1], c[2]
      local reg = Region3.new(Vector3.new(cx0, Y0, cz0), Vector3.new(cx0 + CH, Y1, cz0 + CH))
      local mats, occ = T:ReadVoxels(reg, RES)
      local nx, ny, nz = #mats, #mats[1], #mats[1][1]
      local changed = false
      for i = 1, nx do
        local mi, oi = mats[i], occ[i]
        for k = 1, nz do
          local x, z = cx0 + (i - 1) * RES + 2, cz0 + (k - 1) * RES + 2
          if not inTown1(x, z) then
            local lastKind, airRun = nil, 0
            local j = 1
            local delHere, fillHere = false, false
            while j <= ny do
              local m, o = mi[j][k], oi[j][k]
              local kind
              if m == AIR or o <= 0.05 then kind = "air" elseif m == WATER then kind = "water" else kind = "solid" end
              if kind == "solid" then
                if lastKind == "water" and airRun > 0 then
                  -- thickness of this solid run
                  local e = j
                  while e + 1 <= ny do
                    local m2, o2 = mi[e + 1][k], oi[e + 1][k]
                    if m2 == AIR or o2 <= 0.05 or m2 == WATER then break end
                    e += 1
                  end
                  local thick = e - j + 1
                  local gap = airRun * RES
                  if gap <= 100 and thick >= 3 and airRun > 0 then
                    for q = j - airRun, j - 1 do mi[q][k] = ROCK; oi[q][k] = 1 end
                    G.filledVox += airRun; fillHere = true; changed = true
                    lastKind = "solid"; airRun = 0
                    j = e + 1
                  else
                    for q = j, e do mi[q][k] = AIR; oi[q][k] = 0 end
                    G.deletedVox += thick; delHere = true; changed = true
                    if (gap + thick * RES) > G.maxdel then G.maxdel = gap + thick * RES end
                    airRun += thick   -- stays "water" lastKind: later solids are judged against the water top
                    j = e + 1
                  end
                else
                  if lastKind == "solid" and airRun >= 2 then
                    for q = j - airRun, j - 1 do mi[q][k] = ROCK; oi[q][k] = 1 end
                    G.filledVox += airRun; fillHere = true; changed = true
                  end
                  lastKind = "solid"; airRun = 0
                  j += 1
                end
              elseif kind == "water" then
                lastKind = "water"; airRun = 0
                j += 1
              else
                airRun += 1
                j += 1
              end
            end
            if delHere then G.delCols += 1 end
            if fillHere then G.fillCols += 1 end
          end
        end
      end
      if changed then T:WriteVoxels(reg, RES, mats, occ) end
    end)
    if not ok then table.insert(G.errs, c[1] .. "," .. c[2] .. ": " .. tostring(err):sub(1, 160)) end
    G.i = idx
    task.wait()
  end
  G.done = true; G.secs = os.clock() - G.started
end)
return "started " .. #list .. " chunks"
