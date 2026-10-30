-- t1_plants: read-only. Everything plant-like inside the Town 1 plaza area (x -120..120, z -140..160): models and loose parts by name, count, height; plus terrain materials.
local out = {}
local function P(s) out[#out + 1] = s end
local seen = {}
local function consider(inst, topName)
  local ok, cf, size = false, nil, nil
  if inst:IsA('Model') then ok, cf, size = pcall(function() return inst:GetBoundingBox() end)
  elseif inst:IsA('BasePart') then ok, cf, size = true, inst.CFrame, inst.Size end
  if not ok then return end
  if cf.X > -120 and cf.X < 120 and cf.Z > -140 and cf.Z < 160 then
    local n = string.lower(inst.Name)
    local plant = string.find(n, 'grass') or string.find(n, 'bush') or string.find(n, 'fern') or string.find(n, 'flower') or string.find(n, 'hedge') or string.find(n, 'plant') or string.find(n, 'shrub') or string.find(n, 'weed') or string.find(n, 'tuft') or string.find(n, 'topiary') or string.find(n, 'reed')
    if plant then
      local k = topName .. '/' .. inst.Name
      local e = seen[k] or { n = 0, h = 0, hmax = 0 }
      e.n += 1; e.h += size.Y; if size.Y > e.hmax then e.hmax = size.Y end
      seen[k] = e
    end
  end
end
for _, root in ipairs({ workspace.Phase1Map, workspace:FindFirstChild('SpawnTown') }) do
  if root then
    for _, c in ipairs(root:GetChildren()) do
      for _, d in ipairs(c:GetDescendants()) do
        if d:IsA('Model') or (d:IsA('BasePart') and d.Parent == c) then consider(d, root.Name .. '.' .. c.Name) end
      end
      consider(c, root.Name)
    end
  end
end
local arr = {}
for k, e in pairs(seen) do arr[#arr + 1] = { k, e } end
table.sort(arr, function(a, b) return a[2].n > b[2].n end)
P('plant-like objects in the Town 1 plaza area: ' .. #arr .. ' kinds')
for i = 1, math.min(#arr, 26) do P(string.format('   %s  n=%d avgH=%.1f maxH=%.1f', arr[i][1], arr[i][2].n, arr[i][2].h / arr[i][2].n, arr[i][2].hmax)) end
return table.concat(out, '\n')
