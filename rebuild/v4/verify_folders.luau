-- verify_folders: counts models per Phase1Map folder (by PlanKey) and flags hovering / buried / underwater ones. Args: {"folders":[...]}
local D = game:GetService('HttpService'):JSONDecode([==[__DATA__]==])
local T = workspace.Terrain
local rp = RaycastParams.new(); rp.FilterType = Enum.RaycastFilterType.Include; rp.FilterDescendantsInstances = { T }; rp.IgnoreWater = true
local out = {}
for _, fname in ipairs(D.folders) do
  local f = workspace.Phase1Map:FindFirstChild(fname)
  if not f then out[#out + 1] = fname .. ': MISSING' else
    local n, hover, buried, uw = 0, 0, 0, 0
    local ex = {}
    for _, m in ipairs(f:GetDescendants()) do
      if m:IsA('Model') and m:GetAttribute('PlanKey') then
        n += 1
        local cf, size = m:GetBoundingBox()
        local r = workspace:Raycast(Vector3.new(cf.Position.X, 900, cf.Position.Z), Vector3.new(0, -1300, 0), rp)
        if r then
          local bottom = cf.Position.Y - size.Y / 2
          local gap = bottom - r.Position.Y
          if r.Position.Y < -0.5 then uw += 1
          elseif gap > 3.5 then hover += 1; if #ex < 3 then ex[#ex + 1] = string.format('%s (%.0f,%.0f) gap %.1f', m.Name, cf.Position.X, cf.Position.Z, gap) end
          elseif gap < -6 then buried += 1 end
        end
      end
    end
    out[#out + 1] = string.format('%s: models=%d hover=%d buried=%d underwater=%d %s', fname, n, hover, buried, uw, table.concat(ex, ' | '))
  end
end
return table.concat(out, '\n')
