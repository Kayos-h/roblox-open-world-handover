"""Builds a read-only probe from terrain_gen.luau: same functions, but instead of generating it evaluates given columns and prints h / water / material / voxel plan."""
import json
RB = r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild'
src = open(RB + r'\terrain_gen.luau', encoding='utf-8').read()
head = src[:src.index('local list = {}')]
tail = r'''
local PTS = D.opt.pts
local out = {}
local function segsFor(x, z)
  local segs = {}
  for _, s in ipairs(SEGS) do if s.bx1 > x - 140 and s.bx0 < x + 140 and s.bz1 > z - 140 and s.bz0 < z + 140 then table.insert(segs, s) end end
  return segs
end
for _, p in ipairs(PTS) do
  local x, z = p[1], p[2]
  local h, rm, wl, c, st, pm = column(x, z, segsFor(x, z))
  local line = string.format('(%d,%d) h=%.2f water=%s coast=%.3f roadMat=%s', x, z, h, tostring(wl), c, tostring(rm))
  local cells = {}
  local sm = M.Grass
  if wl and h < wl - 1 then
    local dp = wl - h
    sm = (dp < 5) and M.Sand or ((dp < 30) and M.Mud or M.Basalt)
  end
  for j = 1, 24 do
    local yb = -64 + (j - 1) * RES
    local o = (h - yb) / RES
    local tag = '.'
    if o >= 1 then tag = ((h - yb > 14) and 'R' or string.sub(sm.Name, 1, 1))
    elseif o > 0 then
      if wl and yb < wl and o < 0.5 then tag = 'w' else tag = string.sub(sm.Name, 1, 1):lower() .. string.format('%.1f', o) end
    elseif wl and yb < wl then tag = '~' end
    cells[#cells + 1] = yb .. tag
  end
  out[#out + 1] = line
  out[#out + 1] = '   ' .. table.concat(cells, ' ')
end
return table.concat(out, '\n')
'''
open(RB + r'\v4\_probe_gen.luau', 'w', encoding='utf-8').write(head + tail)
print('probe written', len(head + tail))
