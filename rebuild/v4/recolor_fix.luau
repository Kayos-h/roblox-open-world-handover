-- recolor_fix: (1) Town 1 blue tower/gate roofs: lerp toward slate grey by 45 percent; (2) rusty church stone: Limestone/Sandstone parts within 75 studs of (1406,1244) go from salmon to weathered ochre sandstone.
-- Replayable (idempotent through attributes: Recolored = true). Does not touch anything else.
local out = {}
local function C(r, g, b) return Color3.fromRGB(r, g, b) end
local grey = C(96, 102, 112)
local roots = { workspace.Phase1Map, workspace:FindFirstChild('SpawnTown') }
local nRoof, nChurch = 0, 0
local cnt = 0
for _, root in ipairs(roots) do
  if root then
    for _, p in ipairs(root:GetDescendants()) do
      if p:IsA('BasePart') then
        cnt += 1
        local pos = p.Position
        local c = p.Color
        -- 1. Town 1 zone roofs
        if pos.X > -330 and pos.X < 330 and pos.Z > -560 and pos.Z < 320 and p.Material == Enum.Material.Slate and not p:GetAttribute('Recolored') then
          if c.B > c.R * 1.35 and c.B > c.G * 1.1 and c.B > 0.3 then
            p.Color = c:Lerp(grey, 0.45)
            p:SetAttribute('Recolored', true); nRoof += 1
          end
        end
        -- 2. rusty church
        local dx, dz = pos.X - 1406, pos.Z - 1244
        if dx * dx + dz * dz < 75 * 75 and not p:GetAttribute('Recolored') then
          local m = p.Material
          if m == Enum.Material.Limestone or m == Enum.Material.Sandstone then
            local lum = (c.R + c.G + c.B) / 3
            -- keep light trims lighter, walls become warm ochre sandstone
            local target
            if lum > 0.78 then target = C(206, 184, 146) elseif lum > 0.55 then target = C(178, 146, 102) else target = C(150, 118, 82) end
            p.Color = c:Lerp(target, 0.85)
            p.Material = Enum.Material.Sandstone
            p:SetAttribute('Recolored', true); nChurch += 1
          end
        end
        if cnt % 8000 == 0 then task.wait() end
      end
    end
  end
end
return string.format('parts scanned %d | Town 1 roofs recoloured %d | rusty church parts recoloured %d', cnt, nRoof, nChurch)
