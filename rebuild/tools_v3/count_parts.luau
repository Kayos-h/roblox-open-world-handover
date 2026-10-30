local out = {}
local function add(s) table.insert(out, s) end
add("T1SNAP=" .. tostring(_G.T1SNAP ~= nil))
add("TG=" .. tostring(_G.TG ~= nil))
local pm = workspace:FindFirstChild("Phase1Map")
if not pm then
  add("NO Phase1Map")
  return table.concat(out, "\n")
end
local total, unanch = 0, 0
for _, d in ipairs(pm:GetDescendants()) do
  if d:IsA("BasePart") then
    total += 1
    if not d.Anchored then unanch += 1 end
  end
end
add("Phase1Map parts=" .. total .. " unanchored=" .. unanch)
for _, c in ipairs(pm:GetChildren()) do
  local n = 0
  for _, d in ipairs(c:GetDescendants()) do if d:IsA("BasePart") then n += 1 end end
  add("  " .. c.Name .. " (" .. c.ClassName .. ") children=" .. #c:GetChildren() .. " parts=" .. n)
end
local pb = pm:FindFirstChild("PartBuilt")
if pb then
  for _, c in ipairs(pb:GetChildren()) do
    add("  PartBuilt." .. c.Name .. " kids=" .. #c:GetChildren())
  end
end
local st = game.ServerStorage
for _, c in ipairs(st:GetChildren()) do add("SS." .. c.Name) end
local st1 = pm:FindFirstChild("town1")
if st1 then
  local ch = st1:FindFirstChild("Church")
  add("Church V3Done=" .. tostring(ch and ch:GetAttribute("V3Done")))
end
local sp = pm:FindFirstChild("SpawnTown")
add("SpawnTown V3Compressed=" .. tostring(sp and sp:GetAttribute("V3Compressed")))
add("Camera=" .. tostring(workspace.CurrentCamera.CFrame.Position))
return table.concat(out, "\n")
