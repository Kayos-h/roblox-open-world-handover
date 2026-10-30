-- r3_fix1: global look fixes from the round-3 reviews. Replayable (grass shrink is guarded by the attribute Shrunk).
--  1 lighting: higher sun + stronger skylight so the elf valley is no longer dusk; 2 terrain/water colours; 3 grass and tuft models shrink to realistic height;
--  4 elf bark brighter; 5 church green panes -> amber; 6 training yard fence dark wood + garden strays archived + 2 striped stalls archived.
local L = game:GetService('Lighting')
local T = workspace.Terrain
local SS = game:GetService('ServerStorage')
local pm = workspace.Phase1Map
local out = {}
local function C(r, g, b) return Color3.fromRGB(r, g, b) end

-- 1. lighting
L.ClockTime = 13.1
L.Ambient = C(80, 88, 108)
L.OutdoorAmbient = C(124, 134, 152)
L.EnvironmentDiffuseScale = 0.75
L.ExposureCompensation = 0.1
out[#out + 1] = 'lighting clock ' .. L.ClockTime

-- 2. colours
local colors = { Grass = C(80, 140, 52), LeafyGrass = C(52, 108, 42), Snow = C(222, 230, 240), Limestone = C(218, 188, 138) }
for n, c in pairs(colors) do pcall(function() T:SetMaterialColor(Enum.Material[n], c) end) end
pcall(function()
  T.WaterColor = C(16, 84, 136)
  T.WaterTransparency = 0.7
  T.WaterReflectance = 0.25
end)

-- 3. grass shrink
local factor = { A49_tall_grass_1 = 0.4, A50_tall_grass_2 = 0.4, F05_09_grass_tall_a = 0.45, F05_10_grass_tall_b = 0.45, F05_11_sea_oats = 0.45, F05_12_dune_tuft = 0.5 }
local shrunk = 0
for _, f in ipairs(pm:GetChildren()) do
  if f:IsA('Folder') then
    for _, m in ipairs(f:GetDescendants()) do
      if m:IsA('Model') and factor[m.Name] and not m:GetAttribute('Shrunk') then
        local ok = pcall(function() m:ScaleTo(m:GetScale() * factor[m.Name]) end)
        if ok then m:SetAttribute('Shrunk', true); shrunk += 1 end
        if shrunk % 400 == 0 then task.wait() end
      end
    end
  end
end
out[#out + 1] = 'grass models shrunk: ' .. shrunk

-- 4. elf bark brighter (ancient trees and world tree)
local elf = pm:FindFirstChild('v4_elf')
local nb = 0
if elf then
  for _, m in ipairs(elf:GetDescendants()) do
    if m:IsA('Model') and (string.sub(m.Name, 1, 3) == 'D05') then
      for _, p in ipairs(m:GetChildren()) do
        if p:IsA('BasePart') and (p.Name == 'ev_bark' or p.Name == 'ev_bark_light' or p.Name == 'ev_wood_dark' or p.Name == 'bronze') and not p:GetAttribute('Brightened') then
          p.Color = Color3.new(math.min(p.Color.R * 1.3, 1), math.min(p.Color.G * 1.27, 1), math.min(p.Color.B * 1.22, 1))
          p:SetAttribute('Brightened', true); nb += 1
        end
      end
    end
  end
end
out[#out + 1] = 'elf bark parts brightened: ' .. nb

-- 5. church green panes -> amber
local nc = 0
for _, p in ipairs(workspace:GetDescendants()) do
  if p:IsA('BasePart') and p.Material == Enum.Material.Glass then
    local c = p.Color
    local pos = p.Position
    if (Vector2.new(pos.X, pos.Z) - Vector2.new(1406, 1244)).Magnitude < 90 and c.G > c.R * 1.2 and c.G > c.B * 1.2 then
      p.Color = C(214, 160, 76); nc += 1
    end
  end
end
out[#out + 1] = 'church green panes recoloured: ' .. nc

-- 6. training yard retheme
local arch = SS:FindFirstChild('Phase1Archive_v4') or Instance.new('Folder')
arch.Name = 'Phase1Archive_v4'; arch.Parent = SS
local nf, ns = 0, 0
local fence = pm:FindFirstChild('v4_dress_castle') and pm.v4_dress_castle:FindFirstChild('CastleYardFence')
if fence then
  for _, p in ipairs(fence:GetDescendants()) do
    if p:IsA('BasePart') then p.Color = C(92, 66, 44); p.Material = Enum.Material.WoodPlanks; nf += 1 end
  end
end
for _, d in ipairs(pm:GetDescendants()) do
  if d:IsA('Model') and d:GetAttribute('PlanKey') then
    local p = d:GetPivot().Position
    local n = d.Name
    if p.X > -150 and p.X < -60 and p.Z > -2232 and p.Z < -2165 and (n == 'K27_topiary_spiral' or n == 'A44_flowers_yellow' or n == 'A45_flowers_purple' or n == 'A47_flowers_blue' or n == 'A46_flowers_white' or n == 'A43_flowers_red') then
      d.Parent = arch; ns += 1
    elseif p.X > -80 and p.X < -55 and p.Z > -2170 and p.Z < -2130 and (n == 'A106_market_stall_cloth' or n == 'A107_market_stall_potion') then
      d.Parent = arch; ns += 1
    end
  end
end
out[#out + 1] = string.format('yard fence parts recoloured %d, strays archived %d', nf, ns)
return table.concat(out, '\n')
