-- roof_probe: read-only. For capital houses (outside the Walls folder), list part names/materials/colours that are above the building's mid-height and tile/slate/brick-like.
local cap = workspace.Phase1Map.v3_capital
local res = {}
local seenModels = {}
for _, g in ipairs(cap:GetChildren()) do
  if g.Name ~= 'Walls' and g.Name ~= 'Gardens' and g.Name ~= 'Lamps' then
    for _, m in ipairs(g:GetChildren()) do
      if m:IsA('Model') and not seenModels[m.Name] and #m:GetChildren() > 6 then
        seenModels[m.Name] = true
        local cf, size = m:GetBoundingBox()
        local top = cf.Position.Y + size.Y / 2
        local kinds = {}
        for _, p in ipairs(m:GetChildren()) do
          if p:IsA('BasePart') and p.Position.Y > top - size.Y * 0.4 and (p.Material == Enum.Material.Slate or p.Material == Enum.Material.Brick or p.Material == Enum.Material.Cobblestone or p.Material == Enum.Material.Metal or p.Material == Enum.Material.WoodPlanks) then
            local k = string.format('%s/%s/%d,%d,%d', p.Name, p.Material.Name, p.Color.R * 255, p.Color.G * 255, p.Color.B * 255)
            kinds[k] = (kinds[k] or 0) + math.floor(p.Size.X * p.Size.Z / 10)
          end
        end
        local arr = {}
        for k, a in pairs(kinds) do arr[#arr + 1] = { k, a } end
        table.sort(arr, function(a, b) return a[2] > b[2] end)
        local s = {}
        for i = 1, math.min(#arr, 3) do s[#s + 1] = arr[i][1] .. '(' .. arr[i][2] .. ')' end
        res[#res + 1] = string.format('%s [%s]: %s', m.Name, g.Name, table.concat(s, ' | '))
      end
    end
  end
end
table.sort(res)
return table.concat(res, '\n')
