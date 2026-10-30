-- foam_build: builds thin translucent foam strips along the real waterline (two rings: a bright narrow one and a faint wide one).
-- Data (JSON): {"segments":[[x1,z1,x2,z2],...],"seed":N,"maxParts":N}. Replays safely: rebuilds the folder Phase1Map.v4_foam from scratch.
local HS = game:GetService('HttpService')
local D = HS:JSONDecode([==[__DATA__]==])
local T = workspace.Terrain
local rp = RaycastParams.new(); rp.FilterType = Enum.RaycastFilterType.Include; rp.FilterDescendantsInstances = { T }; rp.IgnoreWater = true
local function ground(x, z)
  local r = workspace:Raycast(Vector3.new(x, 600, z), Vector3.new(0, -900, 0), rp)
  return r and r.Position.Y or -60
end
local root = workspace.Phase1Map
local old = root:FindFirstChild('v4_foam'); if old then old:Destroy() end
local folder = Instance.new('Folder'); folder.Name = 'v4_foam'; folder.Parent = root
local rng = Random.new(D.seed or 7)
local made, skipped = 0, 0
local LV = -0.6
local function mk(cx, cz, ang, len, wid, tr, y, name)
  local p = Instance.new('Part')
  p.Name = name; p.Anchored = true; p.CanCollide = false; p.CanTouch = false; p.CanQuery = false; p.CastShadow = false
  p.Material = Enum.Material.SmoothPlastic
  p.Color = Color3.fromRGB(236, 246, 250)
  p.Transparency = tr
  p.Size = Vector3.new(len, 0.12, wid)
  p.CFrame = CFrame.new(cx, y, cz) * CFrame.Angles(0, ang, 0)
  p.Parent = folder
  made += 1
end
for idx, s in ipairs(D.segments) do
  if made >= (D.maxParts or 9000) then break end
  local ax, az, bx, bz = s[1], s[2], s[3], s[4]
  local mx, mz = (ax + bx) / 2, (az + bz) / 2
  local dx, dz = bx - ax, bz - az
  local len = math.sqrt(dx * dx + dz * dz)
  if len > 0.5 then
    local ux, uz = dx / len, dz / len
    local nx, nz = -uz, ux
    -- choose the seaward normal: ground gets lower going that way
    if ground(mx + nx * 14, mz + nz * 14) > ground(mx - nx * 14, mz - nz * 14) then nx, nz = -nx, -nz end
    -- bisect t in [-26, 26] for ground(t) == LV (ground decreases with t)
    local lo, hi = -26, 26
    local gl, gh = ground(mx + nx * lo, mz + nz * lo), ground(mx + nx * hi, mz + nz * hi)
    if gl > LV and gh < LV then
      for _ = 1, 8 do
        local mid = (lo + hi) / 2
        if ground(mx + nx * mid, mz + nz * mid) > LV then lo = mid else hi = mid end
      end
      local t = (lo + hi) / 2
      local cx, cz = mx + nx * t, mz + nz * t
      local ang = math.atan2(-uz, ux)
      local w1 = 3.2 + rng:NextNumber() * 1.6
      mk(cx + nx * (w1 * 0.25), cz + nz * (w1 * 0.25), ang, len + 1.5, w1, 0.32 + rng:NextNumber() * 0.12, 0.14, 'FoamA')
      if idx % 2 == 0 then
        mk(cx + nx * 7, cz + nz * 7, ang, len + 2, 7 + rng:NextNumber() * 3, 0.78 + rng:NextNumber() * 0.08, 0.1, 'FoamB')
      end
    else
      skipped += 1
    end
  end
  if idx % 150 == 0 then task.wait() end
end
return string.format('foam parts made=%d skipped segments=%d of %d', made, skipped, #D.segments)
