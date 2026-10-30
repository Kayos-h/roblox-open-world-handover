-- clear_pieces: removes the current v4_pieces models (they are re-placed from the plan on the new terrain). Template cache untouched.
local f = workspace.Phase1Map:FindFirstChild('v4_pieces')
if not f then return 'no v4_pieces folder' end
local n = 0
for _, g in ipairs(f:GetChildren()) do n += #g:GetChildren() end
f:ClearAllChildren()
if _G.P1ClaimsScanned then _G.P1ClaimsScanned['v4_pieces'] = nil end
if _G.P1Claims then
  for k in pairs(_G.P1Claims) do if string.sub(k, 1, 10) == 'v4_pieces#' then _G.P1Claims[k] = nil end end
end
return 'cleared v4_pieces models: ' .. n
