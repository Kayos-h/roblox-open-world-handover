-- column dump 2: read-only. Several columns in the south sea and the east ribbon, y -64..16
local T = workspace.Terrain
local cols = { { 300, 2300 }, { 300, 2400 }, { 300, 2500 }, { 3000, -1700 }, { 3004, -1700 }, { 3040, -1700 } }
local out = {}
for _, c in ipairs(cols) do
  local m, o = T:ReadVoxels(Region3.new(Vector3.new(c[1], -64, c[2]), Vector3.new(c[1] + 4, 16, c[2] + 4)), 4)
  local s = {}
  local prev, run = nil, 0
  for j = 1, #m[1] do
    local y = -64 + (j - 1) * 4
    local name = string.sub(m[1][j][1].Name, 1, 4)
    local oc = o[1][j][1]
    local tag = name .. (oc < 0.99 and oc > 0.01 and string.format('%.1f', oc) or '')
    if tag == prev then run += 1 else
      if prev then s[#s + 1] = prev .. 'x' .. run end
      prev, run = tag, 1
      s[#s + 1] = '@' .. y
    end
  end
  s[#s + 1] = prev .. 'x' .. run
  out[#out + 1] = string.format('(%d,%d) %s', c[1], c[2], table.concat(s, ' '))
end
return table.concat(out, '\n')
