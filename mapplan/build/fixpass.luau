local HS = game:GetService('HttpService')
local D = HS:JSONDecode([==[__DATA__]==])
local area = workspace.Phase1Map:FindFirstChild(D.area)
if not area then return 'no area' end
local rp = RaycastParams.new(); rp.FilterType = Enum.RaycastFilterType.Include; rp.FilterDescendantsInstances = { workspace.Terrain }; rp.IgnoreWater = false
local function g(x, z) local r = workspace:Raycast(Vector3.new(x, 600, z), Vector3.new(0, -700, 0), rp) return r and r.Position.Y end
local seen, dup, moved, n = {}, 0, 0, 0
local claims = _G.P1Claims or {}
_G.P1Claims = claims
for _, m in ipairs(area:GetDescendants()) do
  if m:IsA('Model') and m.Parent and m:GetAttribute('PlanKey') then
    local k = m:GetAttribute('PlanKey')
    if seen[k] then m:Destroy(); dup += 1
    else
      seen[k] = true; claims[k] = true
      local yo = m:GetAttribute('YOffset') or 0
      do
        local cf, sz = m:GetBoundingBox()
        local bottom = cf.Y - sz.Y / 2
        local gy
        if math.max(sz.X, sz.Z) < 12 or sz.Y < 1.5 then gy = g(cf.X, cf.Z)
        else
          local rot = cf - cf.Position
          for _, v in ipairs({ Vector3.new(0, 0, 0), Vector3.new(sz.X * 0.4, 0, sz.Z * 0.4), Vector3.new(-sz.X * 0.4, 0, sz.Z * 0.4), Vector3.new(sz.X * 0.4, 0, -sz.Z * 0.4), Vector3.new(-sz.X * 0.4, 0, -sz.Z * 0.4) }) do
            local w = rot * v
            local h = g(cf.X + w.X, cf.Z + w.Z)
            if h and (not gy or h < gy) then gy = h end
          end
        end
        if gy and yo == 0 and math.max(sz.X, sz.Z) < 30 then
          local fp = RaycastParams.new(); fp.FilterType = Enum.RaycastFilterType.Exclude; fp.FilterDescendantsInstances = { m }; fp.IgnoreWater = false
          local hit = workspace:Raycast(Vector3.new(cf.X, gy + 9, cf.Z), Vector3.new(0, -11, 0), fp)
          if hit and hit.Instance ~= workspace.Terrain and hit.Position.Y > gy + 0.4 and hit.Position.Y < gy + 3.5 then gy = hit.Position.Y + 0.25 end
        end
        if gy and sz.Y < 1.5 then gy = gy + 0.3 end
        if gy then
          local want = gy + yo - 0.25
          if math.abs(bottom - want) > 0.8 then m:PivotTo(m:GetPivot() + Vector3.new(0, want - bottom, 0)); moved += 1 end
        end
      end
    end
    n += 1; if n % 150 == 0 then task.wait() end
  end
end
return string.format('%s: kept=%d duplicatesRemoved=%d resnapped=%d', D.area, n - dup, dup, moved)
