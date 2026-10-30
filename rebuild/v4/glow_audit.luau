-- glow_audit: read-only. Counts anything emissive inside the elf valley (x -2200..-1000, z -1100..200): Neon material, PointLight/SpotLight/SurfaceLight, ParticleEmitter, Beam, Fire, Sparkles, Trail, Atmosphere-like glow parts (Glass named lit/glow/lantern).
local out = {}
local counts, ex = {}, {}
local function bump(k, inst)
  counts[k] = (counts[k] or 0) + 1
  if (ex[k] == nil or #ex[k] < 3) then
    ex[k] = ex[k] or {}
    local p = inst:IsA('BasePart') and inst.Position or (inst.Parent and inst.Parent:IsA('BasePart') and inst.Parent.Position) or Vector3.zero
    local m = inst:FindFirstAncestorOfClass('Model')
    table.insert(ex[k], string.format('%s/%s (%.0f,%.0f,%.0f)', m and m.Name or '?', inst.Name, p.X, p.Y, p.Z))
  end
end
local function inElf(p) return p.X > -2200 and p.X < -1000 and p.Z > -1100 and p.Z < 200 end
for _, d in ipairs(workspace:GetDescendants()) do
  if d:IsA('BasePart') then
    if inElf(d.Position) then
      if d.Material == Enum.Material.Neon then bump('Neon part', d) end
      local n = string.lower(d.Name)
      if d.Material == Enum.Material.Glass and (string.find(n, 'lit', 1, true) or string.find(n, 'glow', 1, true) or string.find(n, 'lantern', 1, true)) then bump('lit-glass part', d) end
      if string.find(n, 'neon', 1, true) or string.find(n, 'glow', 1, true) then bump('glow-named part', d) end
    end
  elseif d:IsA('Light') or d:IsA('ParticleEmitter') or d:IsA('Beam') or d:IsA('Fire') or d:IsA('Sparkles') or d:IsA('Trail') or d:IsA('Smoke') then
    local par = d.Parent
    if par and par:IsA('BasePart') and inElf(par.Position) then bump(d.ClassName, d) end
  end
end
for k, n in pairs(counts) do out[#out + 1] = string.format('%s: %d  e.g. %s', k, n, table.concat(ex[k], ' | ')) end
if #out == 0 then out[1] = 'CLEAN: no neon, lights, particles, beams, fire or glow-named parts in the elf valley' end
return table.concat(out, '\n')
