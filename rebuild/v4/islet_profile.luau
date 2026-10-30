-- islet_profile: read-only. For islet models in v4_pieces: radius (from centre, measured along +x and -x rays) at several heights, plus terrain height under the centre and at 0.5 R.
local pm = workspace.Phase1Map
local T = workspace.Terrain
local rpT = RaycastParams.new(); rpT.FilterType = Enum.RaycastFilterType.Include; rpT.FilterDescendantsInstances = { T }; rpT.IgnoreWater = true
local f = pm:FindFirstChild('v4_pieces')
local out = {}
local n = 0
for _, g in ipairs(f:GetChildren()) do
  if g.Name == 'Islets' or g.Name == 'SeaStacks' then
    for _, m in ipairs(g:GetChildren()) do
      n += 1
      if n <= 6 then
        local cf, size = m:GetBoundingBox()
        local rpM = RaycastParams.new(); rpM.FilterType = Enum.RaycastFilterType.Include; rpM.FilterDescendantsInstances = { m }
        local line = {}
        for _, y in ipairs({ -30, -20, -10, -4, 0, 4, 10, 18 }) do
          local best = 0
          for _, dir in ipairs({ Vector3.new(1, 0, 0), Vector3.new(-1, 0, 0), Vector3.new(0, 0, 1), Vector3.new(0, 0, -1) }) do
            local origin = Vector3.new(cf.X, y, cf.Z) + dir * (size.X * 0.8)
            local r = workspace:Raycast(origin, -dir * (size.X * 0.8), rpM)
            if r then
              local d = (Vector3.new(r.Position.X, 0, r.Position.Z) - Vector3.new(cf.X, 0, cf.Z)).Magnitude
              if d > best then best = d end
            end
          end
          line[#line + 1] = string.format('y%d:%.0f', y, best)
        end
        local g0 = workspace:Raycast(Vector3.new(cf.X, 500, cf.Z), Vector3.new(0, -800, 0), rpT)
        local g1 = workspace:Raycast(Vector3.new(cf.X + size.X * 0.35, 500, cf.Z), Vector3.new(0, -800, 0), rpT)
        out[#out + 1] = string.format('%s/%s (%.0f,%.0f) size %.0fx%.0fx%.0f y[%.0f..%.0f] terrain centre %.1f at +0.35W %.1f | radius by height: %s', g.Name, m.Name, cf.X, cf.Z, size.X, size.Y, size.Z, cf.Y - size.Y / 2, cf.Y + size.Y / 2, g0 and g0.Position.Y or -99, g1 and g1.Position.Y or -99, table.concat(line, ' '))
      end
    end
  end
end
return table.concat(out, '\n')
