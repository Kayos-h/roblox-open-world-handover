local out = {}
-- 1) replace needle-like E16_snowy_rock_2 on the ice with flat clones of E15_snowy_rock_1
local rp = RaycastParams.new()
rp.FilterType = Enum.RaycastFilterType.Include
rp.FilterDescendantsInstances = { workspace.Terrain }
local function g(x, z) local r = workspace:Raycast(Vector3.new(x, 800, z), Vector3.new(0, -1600, 0), rp) return r and r.Position.Y end
local folder = workspace.Phase1Map:FindFirstChild("v3f_alpine") and workspace.Phase1Map.v3f_alpine:FindFirstChild("IceRocks")
if folder then
  local src
  for _, m in ipairs(folder:GetChildren()) do if m.Name:find("E15_snowy_rock") then src = m break end end
  local rng = Random.new(5)
  local repl = 0
  if src then
    for _, m in ipairs(folder:GetChildren()) do
      if m:IsA("Model") and m.Name:find("E16_snowy_rock") then
        local cf = m:GetBoundingBox()
        m:Destroy()
        local c = src:Clone()
        c:SetAttribute("PlanKey", nil)
        c.Parent = folder
        c:PivotTo(CFrame.new(cf.X, 200, cf.Z) * CFrame.Angles(0, rng:NextNumber(0, 6.28), 0))
        c:ScaleTo(c:GetScale() * rng:NextNumber(1.2, 2.2) / math.max(0.01, 1))
        local bb, sz = c:GetBoundingBox()
        local gy = g(cf.X, cf.Z) or 152
        c:PivotTo(c:GetPivot() + Vector3.new(0, (gy - 0.4) - (bb.Y - sz.Y / 2), 0))
        repl += 1
      end
    end
  end
  table.insert(out, "ice rocks replaced: " .. repl)
else
  table.insert(out, "no IceRocks folder")
end
-- 2) atmosphere: less haze so distant districts and mountains keep their colour
local at = game:GetService("Lighting"):FindFirstChildWhichIsA("Atmosphere")
if at then
  at.Density = 0.17
  at.Haze = 0.35
  table.insert(out, string.format("Atmosphere now Density=%.2f Haze=%.2f Offset=%.2f", at.Density, at.Haze, at.Offset))
end
return table.concat(out, "\n")
