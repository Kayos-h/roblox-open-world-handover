-- glow_fix: removes every emissive thing inside the elf valley (x -2200..-1000, z -1100..200).
--  * glow-named models whole (F23_glow_mushroom, F25_glow_flower, F34_crystal_cluster...) are archived: they exist only as glow props
--  * lamps / arches keep their shape: Neon parts become SmoothPlastic warm cream, lit glass becomes plain amber-tinted glass (no emission), Lights destroyed
-- The valley houses a few lamp posts in the Town-1 style (A17 rustic lamps): lights off is correct for the elf look.
local SS = game:GetService('ServerStorage')
local arch = SS:FindFirstChild('Phase1Archive_v4') or Instance.new('Folder')
arch.Name = 'Phase1Archive_v4'; arch.Parent = SS
local holder = arch:FindFirstChild('ElfGlowProps') or Instance.new('Folder')
holder.Name = 'ElfGlowProps'; holder.Parent = arch
local function inElf(p) return p.X > -2200 and p.X < -1000 and p.Z > -1100 and p.Z < 200 end
local out = {}
local archived, neon, lit, lights = 0, 0, 0, 0
local models = {}
for _, d in ipairs(workspace.Phase1Map:GetDescendants()) do
  if d:IsA('Model') and d:GetAttribute('PlanKey') then
    local n = string.lower(d.Name)
    if (string.find(n, 'glow', 1, true) or string.find(n, 'crystal', 1, true) or string.find(n, 'neon', 1, true)) and inElf(d:GetPivot().Position) then models[#models + 1] = d end
  end
end
for _, m in ipairs(models) do m.Parent = holder; archived += 1 end
for _, d in ipairs(workspace:GetDescendants()) do
  if d:IsA('BasePart') and inElf(d.Position) then
    if d.Material == Enum.Material.Neon then d.Material = Enum.Material.SmoothPlastic; d.Color = Color3.fromRGB(226, 214, 186); neon += 1 end
    local n = string.lower(d.Name)
    if d.Material == Enum.Material.Glass and (string.find(n, 'lit', 1, true) or string.find(n, 'glow', 1, true) or string.find(n, 'lantern', 1, true)) then
      d.Color = Color3.fromRGB(190, 170, 126); d.Transparency = 0.35; d.Material = Enum.Material.Glass; lit += 1
    end
  elseif (d:IsA('Light') or d:IsA('ParticleEmitter') or d:IsA('Beam') or d:IsA('Fire') or d:IsA('Sparkles') or d:IsA('Trail') or d:IsA('Smoke')) and d.Parent and d.Parent:IsA('BasePart') and inElf(d.Parent.Position) then
    d:Destroy(); lights += 1
  end
end
return string.format('glow models archived %d | neon parts made plain %d | lit glass made plain %d | lights/emitters destroyed %d', archived, neon, lit, lights)
