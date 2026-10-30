-- census: instance + part counts per top-level group of Phase1Map, workspace children, ServerStorage children (read-only)
local out = {}
local function count(inst)
  local n, parts, meshes = 0, 0, 0
  for _, d in ipairs(inst:GetDescendants()) do
    n += 1
    if d:IsA('BasePart') then parts += 1; if d:IsA('MeshPart') then meshes += 1 end end
  end
  return n, parts, meshes
end
local pm = workspace:FindFirstChild('Phase1Map')
if pm then
  for _, area in ipairs(pm:GetChildren()) do
    local n, p, m = count(area)
    local models = 0
    for _, c in ipairs(area:GetChildren()) do
      if c:IsA('Folder') then for _ in ipairs(c:GetChildren()) do models += 1 end else models += 1 end
    end
    out[#out + 1] = string.format('P1Map.%s  inst=%d parts=%d mesh=%d top-level models~%d', area.Name, n, p, m, models)
  end
end
for _, c in ipairs(workspace:GetChildren()) do
  if c.Name ~= 'Phase1Map' and c.Name ~= 'Terrain' then
    local n, p = count(c)
    if n > 50 then out[#out + 1] = string.format('workspace.%s  inst=%d parts=%d', c.Name, n, p) end
  end
end
local ss = game:GetService('ServerStorage')
for _, c in ipairs(ss:GetChildren()) do
  local n, p = count(c)
  out[#out + 1] = string.format('ServerStorage.%s  inst=%d parts=%d', c.Name, n, p)
end
out[#out + 1] = 'StreamingEnabled=' .. tostring(workspace.StreamingEnabled)
return table.concat(out, '\n')
