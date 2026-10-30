-- census of v4_pieces groups + claim state
local f = workspace.Phase1Map:FindFirstChild('v4_pieces')
local out = {}
if f then
  for _, g in ipairs(f:GetChildren()) do out[#out + 1] = g.Name .. '=' .. #g:GetChildren() end
end
local n = 0
if _G.P1Claims then for k in pairs(_G.P1Claims) do if string.sub(k, 1, 10) == 'v4_pieces#' then n += 1 end end end
return 'v4_pieces groups: ' .. table.concat(out, ' ') .. ' | claim keys still set: ' .. n .. ' | scanned flag: ' .. tostring(_G.P1ClaimsScanned and _G.P1ClaimsScanned['v4_pieces'])
