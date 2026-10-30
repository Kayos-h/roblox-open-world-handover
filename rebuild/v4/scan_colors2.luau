-- scan_colors2: read-only. (1) blue-dominant parts inside the Town 1 zone, (2) colours of parts within 70 studs of the rusty church, (3) skull apron by minimum dimension.
local out = {}
local function P(s) out[#out + 1] = s end
local blue, church, apron = {}, {}, {}
local cnt = 0
local roots = { workspace.Phase1Map, workspace:FindFirstChild('SpawnTown') }
for _, root in ipairs(roots) do
  if root then
    for _, p in ipairs(root:GetDescendants()) do
      if p:IsA('BasePart') then
        cnt += 1
        local c = p.Color
        local pos = p.Position
        if pos.X > -330 and pos.X < 330 and pos.Z > -560 and pos.Z < 320 then
          if c.B > c.R * 1.35 and c.B > c.G * 1.1 and c.B > 0.25 then
            local top = p
            while top.Parent and top.Parent ~= root do top = top.Parent end
            local k = string.format('%s/%s part=%s %s rgb(%d,%d,%d)%s', top.Name, p.Parent and p.Parent.Name or '?', p.Name, p.Material.Name, c.R * 255, c.G * 255, c.B * 255, p:IsA('MeshPart') and ' mesh' or '')
            blue[k] = (blue[k] or 0) + 1
          end
        end
        if (Vector2.new(pos.X, pos.Z) - Vector2.new(1406, 1244)).Magnitude < 70 and p.Position.Y > 10 then
          local k = string.format('%s %s rgb(%d,%d,%d)', p.Name, p.Material.Name, c.R * 255, c.G * 255, c.B * 255)
          local e = church[k] or { n = 0, vol = 0 }
          e.n += 1; e.vol += p.Size.X * p.Size.Y * p.Size.Z; church[k] = e
        end
        local mn = math.min(p.Size.X, p.Size.Y, p.Size.Z)
        local mx = math.max(p.Size.X, p.Size.Y, p.Size.Z)
        if (Vector2.new(pos.X, pos.Z) - Vector2.new(0, -402)).Magnitude < 170 and mn < 4 and mx > 40 then
          apron[#apron + 1] = string.format('%s/%s (%.0f,%.1f,%.0f) size %.0fx%.1fx%.0f %s rgb(%d,%d,%d)', p.Parent and p.Parent.Name or '?', p.Name, pos.X, pos.Y, pos.Z, p.Size.X, p.Size.Y, p.Size.Z, p.Material.Name, c.R * 255, c.G * 255, c.B * 255)
        end
        if cnt % 6000 == 0 then task.wait() end
      end
    end
  end
end
local function top(t, n, fmt)
  local a = {}
  for k, v in pairs(t) do a[#a + 1] = { k, v } end
  table.sort(a, function(x, y) return (type(x[2]) == 'table' and x[2].vol or x[2]) > (type(y[2]) == 'table' and y[2].vol or y[2]) end)
  for i = 1, math.min(#a, n) do
    local v = a[i][2]
    P('  ' .. fmt(a[i][1], v))
  end
end
P('Town1-zone blue-dominant part kinds:')
top(blue, 12, function(k, v) return string.format('%s  x%d', k, v) end)
P('rusty church colours (by volume):')
top(church, 14, function(k, v) return string.format('%s  parts=%d vol=%.0f', k, v.n, v.vol) end)
P('skull apron candidates: ' .. #apron)
for i = 1, math.min(#apron, 8) do P('  ' .. apron[i]) end
return table.concat(out, '\n')
