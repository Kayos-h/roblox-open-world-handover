local out = {}
local st = workspace.SpawnTown
local skip = { Ambience = true, NPCMarkers = true }
local function box(area, m)
  local cf, sz = m:GetBoundingBox()
  if math.max(sz.X, sz.Z) < 5 or sz.Y < 4 then return end
  if math.max(sz.X, sz.Z) > 400 then return end
  local _, ry = cf:ToEulerAnglesYXZ()
  out[#out + 1] = string.format("%s|%s|%.1f|%.1f|%.1f|%.1f|%.1f|%.1f|%.0f", area, m.Name, cf.X, cf.Y, cf.Z, sz.X, sz.Y, sz.Z, math.deg(ry))
end
for _, f in ipairs(st:GetChildren()) do
  if f:IsA("Folder") and not skip[f.Name] then
    for _, c in ipairs(f:GetChildren()) do
      if c:IsA("Model") then box("town1_" .. f.Name, c)
      elseif c:IsA("Folder") then
        for _, m in ipairs(c:GetChildren()) do if m:IsA("Model") then box("town1_" .. f.Name, m) end end
      end
    end
  end
end
return table.concat(out, "\n")
