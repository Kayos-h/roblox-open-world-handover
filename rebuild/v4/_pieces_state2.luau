local f = workspace.Phase1Map:FindFirstChild('v4_pieces')
local keys, dup, total = {}, 0, 0
local out = {}
for _, d in ipairs(f:GetDescendants()) do
  if d:IsA('Model') and d:GetAttribute('PlanKey') then
    total += 1
    local k = d:GetAttribute('PlanKey')
    if keys[k] then dup += 1 else keys[k] = true end
    if total <= 6 then local p = d:GetPivot().Position; out[#out + 1] = string.format('%s %s (%.0f,%.0f,%.0f)', k, d.Name, p.X, p.Y, p.Z) end
  end
end
return string.format('models with PlanKey=%d distinct=%d duplicates=%d\n%s', total, total - dup, dup, table.concat(out, '\n'))
