-- Fill air voids sandwiched between solid terrain layers (heightfield world => no real caves).
-- Args injected as JSON: {"x0":..,"x1":..,"z0":..,"z1":..,"tag":"..."}; background thread, progress in _G.FILL.
local D = game:GetService("HttpService"):JSONDecode([==[__DATA__]==])
local T = workspace.Terrain
local RES, CH = 4, 128
local Y0, Y1 = -64, 520
local M = Enum.Material
local AIR, WATER, ROCK = M.Air, M.Water, M.Rock
local MINGAP = 2          -- voxels (8 studs)
local list = {}
for cz = D.z0, D.z1 - 1, CH do for cx = D.x0, D.x1 - 1, CH do table.insert(list, { cx, cz }) end end
_G.FILL = { i = 0, n = #list, filled = 0, cols = 0, chunks = 0, skippedWater = 0, errs = {}, done = false, started = os.clock(), tag = D.tag, maxgap = 0 }
local G = _G.FILL
local function inTown1(x, z) return x >= -312 and x <= 312 and z >= -548 and z <= 316 end
task.spawn(function()
  for idx, c in ipairs(list) do
    if _G.FILL ~= G then return end
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
            -- walk bottom->top; remember last solid index; when next solid appears after a run of non-solid, decide
            local lastSolid, gapHasWater, gapStart = nil, false, nil
            for j = 1, ny do
              local m = mi[j][k]
              local o = oi[j][k]
              local solid = (m ~= AIR and m ~= WATER and o > 0.05)
              if solid then
                if lastSolid and j - lastSolid - 1 >= MINGAP then
                  if gapHasWater then
                    G.skippedWater += 1
                  else
                    for q = lastSolid + 1, j - 1 do mi[q][k] = ROCK; oi[q][k] = 1 end
                    G.filled += (j - lastSolid - 1)
                    if (j - lastSolid - 1) * RES > G.maxgap then G.maxgap = (j - lastSolid - 1) * RES end
                    changed = true
                  end
                end
                lastSolid = j; gapHasWater = false
              elseif m == WATER and o > 0.05 then
                gapHasWater = true
              end
            end
            G.cols += 1
          end
        end
      end
      if changed then T:WriteVoxels(reg, RES, mats, occ); G.chunks += 1 end
    end)
    if not ok then table.insert(G.errs, c[1] .. "," .. c[2] .. ": " .. tostring(err):sub(1, 160)) end
    G.i = idx
    task.wait()
  end
  G.done = true; G.secs = os.clock() - G.started
end)
return "started " .. #list .. " chunks"
