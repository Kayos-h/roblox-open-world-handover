-- Floating-terrain finder, background version: runs in its own thread and leaves the report in _G.FLOATREP (poll it).
-- Args injected as JSON: {"x0","x1","z0","z1","step"}
_G.FLOATREP = nil
_G.FLOATSTART = os.clock()
task.spawn(function()
  local ok, res = pcall(function()
    local D = game:GetService("HttpService"):JSONDecode([==[__DATA__]==])
    local T = workspace.Terrain
    local Y0, Y1 = -64, 500
    local EMPTY = { [Enum.Material.Air] = true, [Enum.Material.Water] = true }
    local found, cols, errs = {}, 0, 0
    for x = D.x0, D.x1, D.step do
      for z = D.z0, D.z1, D.step do
        local ok2, mats = pcall(function()
          local m = T:ReadVoxels(Region3.new(Vector3.new(x, Y0, z), Vector3.new(x + 4, Y1, z + 4)), 4)
          return m
        end)
        if ok2 and mats then
          local col = mats[1]
          local n = #col
          local runs, s = {}, nil
          for i = 1, n do
            local solid = not EMPTY[col[i][1]]
            if solid and not s then s = i end
            if (not solid) and s then table.insert(runs, { s, i - 1 }); s = nil end
          end
          if s then table.insert(runs, { s, n }) end
          for k = 2, #runs do
            local gap = runs[k][1] - runs[k - 1][2] - 1
            if gap >= 7 then
              table.insert(found, { x = x, z = z, lo = Y0 + (runs[k][1] - 1) * 4, hi = Y0 + runs[k][2] * 4, gap = gap * 4, below = Y0 + runs[k - 1][2] * 4 })
            end
          end
        else
          errs += 1
        end
        cols += 1
        if cols % 300 == 0 then task.wait() end
      end
    end
    local out = { string.format("cols=%d errs=%d floaters=%d secs=%.0f", cols, errs, #found, os.clock() - _G.FLOATSTART) }
    local B = {}
    for _, f in ipairs(found) do
      local k = math.floor(f.x / 160) .. "," .. math.floor(f.z / 160)
      local b = B[k] or { n = 0, x0 = 1e9, x1 = -1e9, z0 = 1e9, z1 = -1e9, lo = 1e9, hi = -1e9, below = 1e9, gap = 0 }
      b.n += 1; b.x0 = math.min(b.x0, f.x); b.x1 = math.max(b.x1, f.x); b.z0 = math.min(b.z0, f.z); b.z1 = math.max(b.z1, f.z)
      b.lo = math.min(b.lo, f.lo); b.hi = math.max(b.hi, f.hi); b.below = math.min(b.below, f.below); b.gap = math.max(b.gap, f.gap)
      B[k] = b
    end
    local keys = {}
    for k in pairs(B) do table.insert(keys, k) end
    table.sort(keys, function(a, b) return B[a].n > B[b].n end)
    for i = 1, math.min(25, #keys) do
      local b = B[keys[i]]
      table.insert(out, string.format("bucket %s n=%d x[%d..%d] z[%d..%d] floaterY[%d..%d] groundBelow<=%d maxgap=%d", keys[i], b.n, b.x0, b.x1, b.z0, b.z1, b.lo, b.hi, b.below, b.gap))
    end
    return table.concat(out, "\n")
  end)
  _G.FLOATREP = ok and res or ("ERROR " .. tostring(res))
end)
return "floater scan started"
