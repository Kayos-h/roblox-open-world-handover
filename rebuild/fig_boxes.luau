-- Bounding boxes of major structures for the 3D figure. Output: area|name|x|y|z|sx|sy|sz|rotY
local out = {}
local pats = { "^[CKDGTH]%d", "^E0[1-9]", "^E1[01]", "^F0[1-9]", "^F1[0-3]", "^F32" }
local function wanted(n)
  for _, p in ipairs(pats) do if n:find(p) then return true end end
  return false
end
local function addModel(area, m, always)
  local cf, sz = m:GetBoundingBox()
  if not always and (math.max(sz.X, sz.Z) < 6 or sz.Y < 5) then return end
  local _, ry = cf:ToEulerAnglesYXZ()
  out[#out + 1] = string.format("%s|%s|%.1f|%.1f|%.1f|%.1f|%.1f|%.1f|%.0f", area, m.Name, cf.X, cf.Y, cf.Z, sz.X, sz.Y, sz.Z, math.deg(ry))
end
local n = 0
local function walk(areaName, root)
  for _, d in ipairs(root:GetDescendants()) do
    if d:IsA("Model") and d.Parent:IsA("Folder") and wanted(d.Name) then
      addModel(areaName, d, false)
      n += 1
      if n % 300 == 0 then task.wait() end
    end
  end
end
local pm = workspace.Phase1Map
for _, a in ipairs(pm:GetChildren()) do
  if a.Name == "Enterable" then
    for _, m in ipairs(a:GetChildren()) do if m:IsA("Model") then addModel("enterable", m, true) end end
  elseif a.Name == "PartBuilt" then
    for _, f in ipairs(a:GetChildren()) do
      for _, m in ipairs(f:GetChildren()) do if m:IsA("Model") then addModel("partbuilt_" .. f.Name, m, true) end end
    end
  elseif a.Name ~= "v3_interiors" then
    walk(a.Name, a)
  end
end
local st = workspace:FindFirstChild("SpawnTown")
if st then walk("town1_spawn", st) end
-- Town 1 plaza, wall and gate positions for markers
return table.concat(out, "\n")
