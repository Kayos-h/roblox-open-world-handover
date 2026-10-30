local cap = workspace.Phase1Map.v3_capital
local varied, houses = 0, 0
local cols = {}
for _, g in ipairs(cap:GetChildren()) do
  for _, m in ipairs(g:GetChildren()) do
    if m:IsA('Model') and string.match(m.Name, '^C%d%d_') and g.Name ~= 'Walls' then
      houses += 1
      if m:GetAttribute('RoofVaried') then varied += 1 end
      for _, p in ipairs(m:GetChildren()) do
        if p:IsA('BasePart') and p.Name == 'tile_a' then
          local k = string.format('%d,%d,%d', p.Color.R * 255, p.Color.G * 255, p.Color.B * 255)
          cols[k] = (cols[k] or 0) + 1
        end
      end
    end
  end
end
local arr = {}
for k, n in pairs(cols) do arr[#arr + 1] = k .. 'x' .. n end
return string.format('capital C-models %d, with RoofVaried %d | tile_a colour kinds: %s', houses, varied, table.concat(arr, ' '))
