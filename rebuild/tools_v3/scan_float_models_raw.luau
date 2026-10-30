-- Float/sink scan over every placed item in Phase1Map. Read-only.
local rp = RaycastParams.new()
rp.FilterType = Enum.RaycastFilterType.Include
rp.FilterDescendantsInstances = { workspace.Terrain }
rp.IgnoreWater = false
local function gy(x, z)
  local r = workspace:Raycast(Vector3.new(x, 700, z), Vector3.new(0, -1500, 0), rp)
  return r and r.Position.Y or nil
end
local skip = { PartBuilt = true, Enterable = true, v3_interiors = true }
local res, counts = {}, {}
local scanned = 0
local function check(area, inst)
  local cf, sz
  if inst:IsA("Model") then cf, sz = inst:GetBoundingBox() else cf, sz = inst.CFrame, inst.Size end
  if math.max(sz.X, sz.Z) > 70 then return end
  local hx, hz = sz.X / 2 * 0.8, sz.Z / 2 * 0.8
  local lo, hi = math.huge, -math.huge
  for _, o in ipairs({ {0,0}, {hx,hz}, {-hx,hz}, {hx,-hz}, {-hx,-hz} }) do
    local g = gy(cf.X + o[1], cf.Z + o[2])
    if g then lo = math.min(lo, g); hi = math.max(hi, g) end
  end
  if lo == math.huge then return end
  scanned += 1
  local bottom = cf.Y - sz.Y / 2
  local top = cf.Y + sz.Y / 2
  local rel = bottom - lo
  local kind
  if rel > 3 then kind = "FLOAT" elseif top < hi - 1 then kind = "BURIED" end
  if kind then
    counts[area] = counts[area] or { FLOAT = 0, BURIED = 0 }
    counts[area][kind] += 1
    table.insert(res, { area = area, kind = kind, name = inst.Name, x = cf.X, y = cf.Y, z = cf.Z, rel = rel, h = sz.Y, path = inst:GetFullName() })
  end
end
for _, area in ipairs(workspace.Phase1Map:GetChildren()) do
  if not skip[area.Name] then
    for _, d in ipairs(area:GetDescendants()) do
      local isItem = false
      if d:IsA("Model") and (d.Parent:IsA("Folder") ) then isItem = true end
      if d:IsA("BasePart") and d.Parent:IsA("Folder") then isItem = true end
      if isItem then check(area.Name, d) end
    end
  end
end
table.sort(res, function(a, b) return math.abs(a.rel) > math.abs(b.rel) end)
local out = { "scanned=" .. scanned .. " flagged=" .. #res }
for a, c in pairs(counts) do table.insert(out, string.format("AREA %s FLOAT=%d BURIED=%d", a, c.FLOAT, c.BURIED)) end
for i = 1, math.min(45, #res) do
  local r = res[i]
  table.insert(out, string.format("%s %s %s (%.0f,%.0f,%.0f) rel=%.1f h=%.1f", r.kind, r.area, r.name, r.x, r.y, r.z, r.rel, r.h))
end
return table.concat(out, "\n")
