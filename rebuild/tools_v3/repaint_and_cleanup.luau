local out = {}
local T = workspace.Terrain
local rp = RaycastParams.new()
rp.FilterType = Enum.RaycastFilterType.Include
rp.FilterDescendantsInstances = { T }
rp.IgnoreWater = false
local function ray(x, z) return workspace:Raycast(Vector3.new(x, 700, z), Vector3.new(0, -1500, 0), rp) end

-- A) remove deeply buried / floating small decor (generated, rebuildable)
local skipArea = { PartBuilt = true, Enterable = true, v3_interiors = true }
local keepName = { "hanging", "platform", "bridge", "rope", "canopy", "treehouse", "branch", "bunting", "torch", "banner", "flag" }
local function keep(n) n = n:lower(); for _, k in ipairs(keepName) do if n:find(k, 1, true) then return true end end return false end
local removed, byName = 0, {}
local scan = 0
for _, area in ipairs(workspace.Phase1Map:GetChildren()) do
  if not skipArea[area.Name] then
    for _, m in ipairs(area:GetDescendants()) do
      if m:IsA("Model") and m.Parent:IsA("Folder") and not keep(m.Name) and (m:GetAttribute("YOffset") or 0) < 2 then
        local cf, sz = m:GetBoundingBox()
        if math.max(sz.X, sz.Z) <= 40 then
          local r = ray(cf.X, cf.Z)
          if r then
            local g = r.Position.Y
            local bottom, top = cf.Y - sz.Y / 2, cf.Y + sz.Y / 2
            if top < g - 12 or bottom > g + 12 then
              byName[m.Name] = (byName[m.Name] or 0) + 1
              m:Destroy(); removed += 1
            end
          end
        end
        scan += 1
        if scan % 500 == 0 then task.wait() end
      end
    end
  end
end
local names = {}
for k, v in pairs(byName) do table.insert(names, k .. "x" .. v) end
table.insert(out, "A) removed " .. removed .. ": " .. table.concat(names, ", "))

-- helper: replace materials in a box, optionally patchy
local function rep(x0, x1, z0, z1, y0, y1, from, to)
  local reg = Region3.new(Vector3.new(x0, y0, z0), Vector3.new(x1, y1, z1)):ExpandToGrid(4)
  for _, m in ipairs(from) do T:ReplaceMaterial(reg, 4, m, to) end
end
local G, LG = Enum.Material.Grass, Enum.Material.LeafyGrass
local function patchy(x0, x1, z0, z1, y0, y1, cell, prob, from, to, seed)
  local rng = Random.new(seed)
  local n = 0
  for x = x0, x1 - cell, cell do
    for z = z0, z1 - cell, cell do
      if rng:NextNumber() < prob then rep(x, x + cell, z, z + cell, y0, y1, from, to); n += 1 end
    end
  end
  return n
end
-- B) alpine: village + shore grass -> snow, 85% of 16-stud cells
local nB = patchy(1380, 1830, -1010, -690, 95, 175, 16, 0.85, { G, LG }, Enum.Material.Snow, 11)
table.insert(out, "B) alpine snow cells=" .. nB)
-- C) graveyard: grass -> mud (70% of 6-stud cells), the rest dead-grass stays
local nC = patchy(-292, -186, 196, 298, -12, 24, 6, 0.72, { G, LG }, Enum.Material.Mud, 5)
table.insert(out, "C) graveyard mud cells=" .. nC)
-- D) elf: limestone paths -> sandstone (warm), ground around houses -> leafy grass
rep(-2000, -1200, -800, 0, -12, 60, { Enum.Material.Limestone }, Enum.Material.Sandstone)
for _, h in ipairs({ { -1730, -300 }, { -1390, -560 } }) do
  rep(h[1] - 26, h[1] + 26, h[2] - 26, h[2] + 26, -12, 40, { Enum.Material.Ground }, LG)
end
table.insert(out, "D) elf paths + house yards done")
-- E) harbour quay belt: tall-grass decoration off, grass -> sand beach
rep(-700, -150, 1780, 1900, -12, 24, { G, LG }, Enum.Material.Sand)
table.insert(out, "E) harbour belt sand done")
-- F) Town 1 SE field (outside walls) and general: nothing yet
return table.concat(out, "\n")
