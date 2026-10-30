local keys = {}
for k in string.gmatch([==[__KEYS__]==], '[^,%s]+') do keys[k] = true end
local claims = _G.P1Claims or {}
local n = 0
for _, m in ipairs(workspace.Phase1Map:GetDescendants()) do
  if m:IsA('Model') and m.Parent then
    local k = m:GetAttribute('PlanKey')
    if k and keys[k] then m:Destroy(); n += 1 end
  end
end
for k in pairs(keys) do claims[k] = nil end
return 'removed ' .. n
