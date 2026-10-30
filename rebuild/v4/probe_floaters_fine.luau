-- probe_floaters_fine: read-only. Looks for detached solid terrain (air gap >= 12 studs under solid terrain) at step 12 inside given rectangles.
-- Args (JSON): {"rects":[[x0,x1,z0,z1],...]}
local D = game:GetService('HttpService'):JSONDecode([==[__DATA__]==])
local T = workspace.Terrain
local Y0, Y1 = -64, 520
local EMPTY = { [Enum.Material.Air] = true, [Enum.Material.Water] = true }
local out = {}
for ri, r in ipairs(D.rects) do
  local found, cols = {}, 0
  for x = r[1], r[2], 12 do
    for z = r[3], r[4], 12 do
      local ok, m = pcall(function() return T:ReadVoxels(Region3.new(Vector3.new(x, Y0, z), Vector3.new(x + 4, Y1, z + 4)), 4) end)
      if ok and m then
        local col = m[1]
        local runs, s = {}, nil
        for i = 1, #col do
          local solid = not EMPTY[col[i][1]]
          if solid and not s then s = i end
          if (not solid) and s then runs[#runs + 1] = { s, i - 1 }; s = nil end
        end
        if s then runs[#runs + 1] = { s, #col } end
        for k = 2, #runs do
          local gap = (runs[k][1] - runs[k - 1][2] - 1) * 4
          if gap >= 12 then found[#found + 1] = { x = x, z = z, lo = Y0 + (runs[k][1] - 1) * 4, hi = Y0 + runs[k][2] * 4, gap = gap, below = Y0 + runs[k - 1][2] * 4 } end
        end
      end
      cols += 1
      if cols % 400 == 0 then task.wait() end
    end
  end
  out[#out + 1] = string.format('rect %d [%d..%d, %d..%d]: cols=%d floaters=%d', ri, r[1], r[2], r[3], r[4], cols, #found)
  local shown = 0
  for _, f in ipairs(found) do
    if shown < 6 then out[#out + 1] = string.format('   x=%d z=%d floater y %d..%d gap %d groundBelow<=%d', f.x, f.z, f.lo, f.hi, f.gap, f.below); shown += 1 end
  end
end
return table.concat(out, '\n')
