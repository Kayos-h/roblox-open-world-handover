-- scan_colors: read-only. Cobalt roofs, pink church parts, near-black big parts near the alpine peak, skull apron.
local out = {}
local function P(s) out[#out + 1] = s end
local function hsv(c) local h, s, v = c:ToHSV(); return h * 360, s, v end
local cobalt = {}   -- key = area/model -> {n, sample color}
local nCob = 0
local pink = {}
local dark = {}
local apron = {}
local cnt = 0
local roots = { workspace.Phase1Map, workspace:FindFirstChild('SpawnTown') }
for _, root in ipairs(roots) do
  if root then
    for _, p in ipairs(root:GetDescendants()) do
      if p:IsA('BasePart') then
        cnt += 1
        local c = p.Color
        local h, s, v = hsv(c)
        local pos = p.Position
        -- cobalt: blue hue 205..235, saturation > 0.55, value 0.35..0.8
        if h >= 205 and h <= 240 and s > 0.55 and v > 0.35 and v < 0.85 and (p.Size.X + p.Size.Y + p.Size.Z) > 8 then
          local m = p:FindFirstAncestorOfClass('Model')
          local top = p
          while top.Parent and top.Parent ~= root and top.Parent.Parent ~= root do top = top.Parent end
          local key = (top.Parent and top.Parent.Name or '?') .. '/' .. (m and m.Name or p.Name)
          local e = cobalt[key] or { n = 0, c = c, mat = p.Material.Name, nm = p.Name }
          e.n += 1; cobalt[key] = e; nCob += 1
        end
        -- pink/salmon near the rusty church
        if (pos - Vector3.new(1400, 20, 1250)).Magnitude < 130 and h >= 0 and h <= 25 and s > 0.15 and s < 0.6 and v > 0.6 then
          local k = string.format('%s rgb(%d,%d,%d) %s', p.Name, c.R * 255, c.G * 255, c.B * 255, p.Material.Name)
          pink[k] = (pink[k] or 0) + 1
        end
        -- near-black big parts around the alpine peak
        if v < 0.12 and math.max(p.Size.X, p.Size.Y, p.Size.Z) > 8 and (pos - Vector3.new(1450, 150, -1050)).Magnitude < 420 then
          dark[#dark + 1] = string.format('%s/%s (%.0f,%.0f,%.0f) size %.0fx%.0fx%.0f rgb(%d,%d,%d) %s', p.Parent and p.Parent.Name or '?', p.Name, pos.X, pos.Y, pos.Z, p.Size.X, p.Size.Y, p.Size.Z, c.R * 255, c.G * 255, c.B * 255, p.Material.Name)
        end
        -- skull apron: flat wide parts around the skull
        if (Vector2.new(pos.X, pos.Z) - Vector2.new(0, -402)).Magnitude < 160 and p.Size.Y < 4 and math.max(p.Size.X, p.Size.Z) > 30 then
          apron[#apron + 1] = string.format('%s/%s (%.0f,%.1f,%.0f) size %.0fx%.1fx%.0f %s', p.Parent and p.Parent.Name or '?', p.Name, pos.X, pos.Y, pos.Z, p.Size.X, p.Size.Y, p.Size.Z, p.Material.Name)
        end
        if cnt % 6000 == 0 then task.wait() end
      end
    end
  end
end
P('scanned parts: ' .. cnt .. '; cobalt parts: ' .. nCob)
local ck = {}
for k, e in pairs(cobalt) do ck[#ck + 1] = { k, e } end
table.sort(ck, function(a, b) return a[2].n > b[2].n end)
for i = 1, math.min(#ck, 14) do
  local e = ck[i][2]
  P(string.format('  cobalt %-46s parts=%-4d part=%s rgb(%d,%d,%d) %s', ck[i][1], e.n, e.nm, e.c.R * 255, e.c.G * 255, e.c.B * 255, e.mat))
end
local pk = {}
for k, n in pairs(pink) do pk[#pk + 1] = { k, n } end
table.sort(pk, function(a, b) return a[2] > b[2] end)
P('pink/salmon-ish part kinds near rusty church: ' .. #pk)
for i = 1, math.min(#pk, 14) do P(string.format('  pink  %-60s x%d', pk[i][1], pk[i][2])) end
P('near-black big parts near the alpine peak: ' .. #dark)
for i = 1, math.min(#dark, 8) do P('  dark  ' .. dark[i]) end
P('flat wide parts near the skull: ' .. #apron)
for i = 1, math.min(#apron, 8) do P('  apron ' .. apron[i]) end
return table.concat(out, '\n')
