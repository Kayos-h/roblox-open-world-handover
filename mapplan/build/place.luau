local HS = game:GetService('HttpService')
local IS = game:GetService('InsertService')
local SS = game:GetService('ServerStorage')
local D = HS:JSONDecode([==[__DATA__]==])
local PAL = D.pal
local root = workspace:FindFirstChild('Phase1Map') or Instance.new('Folder')
root.Name = 'Phase1Map'; root.Parent = workspace
local area = root:FindFirstChild(D.area) or Instance.new('Folder')
area.Name = D.area; area.Parent = root
local cache = SS:FindFirstChild('Phase1Cache') or Instance.new('Folder')
cache.Name = 'Phase1Cache'; cache.Parent = SS
local done = _G.P1Claims or {}
_G.P1Claims = done
for _, m in ipairs(area:GetDescendants()) do
  if m:IsA('Model') then local k = m:GetAttribute('PlanKey'); if k then done[k] = true end end
end
local rp = RaycastParams.new(); rp.FilterType = Enum.RaycastFilterType.Include; rp.FilterDescendantsInstances = { workspace.Terrain }; rp.IgnoreWater = false
local function groundAt(x, z)
  local r = workspace:Raycast(Vector3.new(x, 600, z), Vector3.new(0, -700, 0), rp)
  return r and r.Position.Y or nil
end
local function template(id)
  local key = 'A' .. id
  local t = cache:FindFirstChild(key)
  if t then return t end
  local ok, c = pcall(function() return IS:LoadAsset(id) end)
  if not ok or not c then return nil, tostring(c) end
  local kids = c:GetChildren()
  local m = (#kids == 1 and kids[1]:IsA('Model')) and kids[1] or c
  if m ~= c then m.Parent = nil; c:Destroy() end
  local mdl = m
  if not mdl:IsA('Model') then local w = Instance.new('Model'); mdl.Parent = w; mdl = w end
  for _, p in ipairs(mdl:GetDescendants()) do
    if p:IsA('BasePart') then
      local k = p.Name:gsub('_%d+$', '')
      local e = PAL[k]
      if e then
        p.Color = Color3.new(e.rgb[1] / 255, e.rgb[2] / 255, e.rgb[3] / 255)
        local okm, mm = pcall(function() return Enum.Material[e.material] end)
        if okm and mm then p.Material = mm end
        if e.material == 'Glass' then p.Transparency = 0.3 end
        if e.glow then p.CastShadow = false; p.CanCollide = false end
      end
      p.Anchored = true
      local s = p.Size
      if math.max(s.X, s.Y, s.Z) < 1.2 then p.CanCollide = false end
      p.CanTouch = false
    end
  end
  mdl.Name = key
  mdl.Parent = cache
  return mdl
end
local placed, skipped, failed, errs = 0, 0, 0, {}
for i, it in ipairs(D.items) do
  if done[it.key] then skipped += 1
  else
    done[it.key] = true
    local t, err = template(it.id)
    if not t then failed += 1; done[it.key] = nil; table.insert(errs, it.m .. ':' .. tostring(err))
    else
      local m = t:Clone()
      m.Name = it.m
      if it.s and it.s ~= 1 then pcall(function() m:ScaleTo(it.s) end) end
      local rot = CFrame.Angles(0, math.rad(it.rot or 0), 0)
      m:PivotTo(rot)
      local cf, size = m:GetBoundingBox()
      local off = cf.Position
      local hx, hz = size.X / 2 * 0.8, size.Z / 2 * 0.8
      local gy
      local cr = cf - cf.Position
      for _, v in ipairs({ Vector3.new(0, 0, 0), Vector3.new(hx, 0, hz), Vector3.new(-hx, 0, hz), Vector3.new(hx, 0, -hz), Vector3.new(-hx, 0, -hz) }) do
        local w = cr * v
        local g = groundAt(it.x + w.X, it.z + w.Z)
        if g and (not gy or g < gy) then gy = g end
      end
      gy = gy or 2
      local bottom = off.Y - size.Y / 2
      local target = Vector3.new(it.x, gy + (it.yo or 0) - 0.25, it.z)
      m:PivotTo(CFrame.new(target - Vector3.new(off.X, bottom, off.Z)) * rot)
      local grp = area:FindFirstChild(it.g) or Instance.new('Folder')
      grp.Name = it.g; grp.Parent = area
      m:SetAttribute('PlanKey', it.key)
      m:SetAttribute('YOffset', it.yo or 0)
      local glow, best = nil, 0
      for _, p in ipairs(m:GetDescendants()) do
        if p:IsA('BasePart') then
          local e = PAL[p.Name:gsub('_%d+$', '')]
          if e and e.glow and p.Size.Magnitude > best then glow = p; best = p.Size.Magnitude end
        end
      end
      if glow then
        local l = Instance.new('PointLight')
        local c = glow.Color
        l.Color = Color3.new(math.min(1, c.R * 1.05 + 0.05), math.min(1, c.G * 1.05 + 0.05), math.min(1, c.B * 1.05 + 0.05))
        l.Range = math.clamp(best * 5, 12, 26); l.Brightness = 1.4; l.Shadows = false
        l.Parent = glow
      end
      m.Parent = grp
      placed += 1
    end
  end
  if i % 8 == 0 then task.wait() end
end
return HS:JSONEncode({ placed = placed, skipped = skipped, failed = failed, errs = errs })
