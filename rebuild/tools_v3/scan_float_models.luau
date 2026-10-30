-- Grouped float/bury scan, excluding items that are meant to hang or sit in trees. Read-only.
local rp = RaycastParams.new()
rp.FilterType = Enum.RaycastFilterType.Include
rp.FilterDescendantsInstances = { workspace.Terrain }
rp.IgnoreWater = false
local function gy(x, z)
  local r = workspace:Raycast(Vector3.new(x, 700, z), Vector3.new(0, -1500, 0), rp)
  return r and r.Position.Y or nil
end
local skipArea = { PartBuilt = true, Enterable = true, v3_interiors = true }
local ignoreName = { "hanging", "platform", "bridge", "rope", "canopy", "treehouse", "branch", "lantern", "banner", "flag" }
local function ignored(n)
  n = n:lower()
  for _, k in ipairs(ignoreName) do if n:find(k, 1, true) then return true end end
  return false
end
local groups = {}
local examples = {}
for _, area in ipairs(workspace.Phase1Map:GetChildren()) do
  if not skipArea[area.Name] then
    for _, d in ipairs(area:GetDescendants()) do
      if (d:IsA("Model") or d:IsA("BasePart")) and d.Parent:IsA("Folder") and not ignored(d.Name) then
        local cf, sz
        if d:IsA("Model") then cf, sz = d:GetBoundingBox() else cf, sz = d.CFrame, d.Size end
        if math.max(sz.X, sz.Z) <= 70 then
          local hx, hz = sz.X / 2 * 0.8, sz.Z / 2 * 0.8
          local lo, hi = math.huge, -math.huge
          for _, o in ipairs({ {0,0}, {hx,hz}, {-hx,hz}, {hx,-hz}, {-hx,-hz} }) do
            local g = gy(cf.X + o[1], cf.Z + o[2])
            if g then lo = math.min(lo, g); hi = math.max(hi, g) end
          end
          if lo ~= math.huge then
            local bottom, top = cf.Y - sz.Y / 2, cf.Y + sz.Y / 2
            local kind
            if bottom - lo > 4 then kind = "FLOAT" elseif top < hi - 0.5 then kind = "BURIED" end
            if kind then
              local base = d.Name:gsub("_%d+$", "")
              local key = kind .. "|" .. area.Name .. "|" .. base
              groups[key] = (groups[key] or 0) + 1
              local ex = examples[key]
              if not ex or math.abs(bottom - lo) > math.abs(ex.rel) then
                examples[key] = { x = cf.X, y = cf.Y, z = cf.Z, rel = (kind == "FLOAT") and (bottom - lo) or (top - hi), h = sz.Y }
              end
            end
          end
        end
      end
    end
  end
end
local keys = {}
for k in pairs(groups) do table.insert(keys, k) end
table.sort(keys, function(a, b) return groups[a] > groups[b] end)
local out = {}
for i = 1, math.min(60, #keys) do
  local k = keys[i]
  local e = examples[k]
  table.insert(out, string.format("%3d  %s  worst@(%.0f,%.0f,%.0f) rel=%.1f h=%.1f", groups[k], k, e.x, e.y, e.z, e.rel, e.h))
end
return table.concat(out, "\n")
