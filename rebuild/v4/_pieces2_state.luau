local f = workspace.Phase1Map:FindFirstChild('v4_pieces2')
if not f then return 'no folder' end
local by = {}
local keys, dup, total = {}, 0, 0
for _, d in ipairs(f:GetDescendants()) do
  if d:IsA('Model') and d:GetAttribute('PlanKey') then
    total += 1
    local k = d:GetAttribute('PlanKey')
    if keys[k] then dup += 1 else keys[k] = true end
    by[d.Parent.Name] = (by[d.Parent.Name] or 0) + 1
  end
end
local s = {}
for k, v in pairs(by) do s[#s + 1] = k .. '=' .. v end
return string.format('v4_pieces2 models=%d distinct=%d dup=%d groups: %s', total, total - dup, dup, table.concat(s, ' '))
