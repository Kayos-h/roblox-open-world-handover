"""Build terrain_clip.luau from terrain_gen.luau: same height model, but only clears solid terrain above the designed surface."""
import re
RB = r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild'
src = open(RB + r'\terrain_gen.luau', encoding='utf-8').read()
head = src[:src.index('local function doChunk')]
head = head.replace('-- Phase 1 terrain generator.', '-- Phase 1 terrain CLIP pass (derived from terrain_gen.luau).', 1)
tail = r'''
local Y0, Y1 = -64, 520
local MARGIN = 24
local CLIP = { i = 0, cleared = 0, cols = 0, chunks = 0, errs = {}, done = false, started = os.clock(), tag = OPT.tag, maxcut = 0 }
local function doChunk(cx0, cz0)
  local N = CH / RES
  local segs = {}
  local cx1, cz1 = cx0 + CH, cz0 + CH
  for _, s in ipairs(SEGS) do if s.bx1 > cx0 and s.bx0 < cx1 and s.bz1 > cz0 and s.bz0 < cz1 then table.insert(segs, s) end end
  local reg = Region3.new(Vector3.new(cx0, Y0, cz0), Vector3.new(cx1, Y1, cz1))
  local mats, occ = T:ReadVoxels(reg, RES)
  local nx, ny, nz = #mats, #mats[1], #mats[1][1]
  local changed = false
  for i = 1, nx do
    local mi, oi = mats[i], occ[i]
    for k = 1, nz do
      local x, z = cx0 + (i - 1) * RES + 2, cz0 + (k - 1) * RES + 2
      local inT1 = SNAP and T1 and abs(x) <= T1.x and z >= T1.z0 and z <= T1.z1
      if not inT1 then
        local h = column(x, z, segs)
        local cut = false
        for j = 1, ny do
          local yb = Y0 + (j - 1) * RES
          if yb > h + MARGIN then
            local m = mi[j][k]
            if m ~= M.Air and m ~= M.Water and oi[j][k] > 0 then
              mi[j][k] = M.Air; oi[j][k] = 0
              CLIP.cleared += 1; cut = true
              if yb - h > CLIP.maxcut then CLIP.maxcut = yb - h end
            end
          end
        end
        if cut then changed = true; CLIP.cols += 1 end
      end
    end
  end
  if changed then T:WriteVoxels(reg, RES, mats, occ); CLIP.chunks += 1 end
end
local list = {}
local x0, x1, z0, z1 = OPT.x0, OPT.x1, OPT.z0, OPT.z1
for cz = z0, z1 - 1, CH do for cx = x0, x1 - 1, CH do table.insert(list, { cx, cz }) end end
CLIP.n = #list
_G.CLIP = CLIP
task.spawn(function()
  for idx, c in ipairs(list) do
    if _G.CLIP ~= CLIP then return end
    local ok, err = pcall(doChunk, c[1], c[2])
    if not ok then table.insert(CLIP.errs, c[1] .. ',' .. c[2] .. ': ' .. tostring(err):sub(1, 160)) end
    CLIP.i = idx
    task.wait()
  end
  CLIP.done = true; CLIP.secs = os.clock() - CLIP.started
end)
return 'clip started ' .. #list .. ' chunks'
'''
open(RB + r'\terrain_clip.luau', 'w', encoding='utf-8').write(head + tail)
print('written', len(head + tail), 'chars; head lines', head.count('\n'))
