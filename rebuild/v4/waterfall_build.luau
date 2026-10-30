-- waterfall_build: a natural waterfall down the steep descent path (data: {"path":[[x,z,y],...]}). Plain parts only: no Neon, no lights, no particles.
--  * ribbon of thin translucent water boxes hugging the terrain, 12 studs wide (tapering), pale blue-white, Glass material
--  * foam bands at the ledges (white, 0.45 transparency) and a splash pool of foam at the base
--  * the old R05_01 slab is archived. Replayable: rebuilds Phase1Map.v4_waterfall from scratch.
local HS = game:GetService('HttpService')
local D = HS:JSONDecode([==[__DATA__]==])
local T = workspace.Terrain
local SS = game:GetService('ServerStorage')
local rp = RaycastParams.new(); rp.FilterType = Enum.RaycastFilterType.Include; rp.FilterDescendantsInstances = { T }; rp.IgnoreWater = true
local function ground(x, z) local r = workspace:Raycast(Vector3.new(x, 600, z), Vector3.new(0, -900, 0), rp); return r and r.Position.Y or nil end
local root = workspace.Phase1Map
local old = root:FindFirstChild('v4_waterfall'); if old then old:Destroy() end
local F = Instance.new('Folder'); F.Name = 'v4_waterfall'; F.Parent = root
local arch = SS:FindFirstChild('Phase1Archive_v4') or Instance.new('Folder'); arch.Name = 'Phase1Archive_v4'; arch.Parent = SS
-- archive the old slab
local moved = 0
for _, m in ipairs(root:GetDescendants()) do
  if m:IsA('Model') and m.Name == 'R05_01_waterfall_cliff_large_01' then m.Parent = arch; moved += 1 end
end
local P = D.path
-- resample the path every 5 studs
local pts = {}
for i = 1, #P - 1 do
  local a, b = Vector3.new(P[i][1], 0, P[i][2]), Vector3.new(P[i + 1][1], 0, P[i + 1][2])
  local L = (b - a).Magnitude
  local n = math.max(1, math.floor(L / 5))
  for k = 0, n - 1 do
    local p = a:Lerp(b, k / n)
    pts[#pts + 1] = p
  end
end
pts[#pts + 1] = Vector3.new(P[#P][1], 0, P[#P][2])
local function mk(name, size, cf, color, tr, mat)
  local p = Instance.new('Part'); p.Name = name; p.Anchored = true; p.CanCollide = false; p.CanTouch = false; p.CanQuery = false; p.CastShadow = false
  p.Size = size; p.CFrame = cf; p.Color = color; p.Transparency = tr; p.Material = mat
  p.Parent = F
  return p
end
local made = 0
local water, foam = Color3.fromRGB(176, 214, 232), Color3.fromRGB(240, 248, 252)
for i = 1, #pts - 1 do
  local a, b = pts[i], pts[i + 1]
  local ga, gb = ground(a.X, a.Z), ground(b.X, b.Z)
  if ga and gb then
    local pa, pb = Vector3.new(a.X, ga + 0.5, a.Z), Vector3.new(b.X, gb + 0.5, b.Z)
    local mid = (pa + pb) / 2
    local len = (pb - pa).Magnitude
    local t = (i - 1) / (#pts - 1)
    local width = 13 - 5 * t
    local cf = CFrame.lookAt(mid, pb) * CFrame.Angles(0, 0, 0)
    -- ribbon: a long thin box along the path; the box's local Z runs along the path
    mk('Fall', Vector3.new(width, 0.5, len + 0.4), cf, water, 0.28, Enum.Material.Glass)
    mk('FallWhite', Vector3.new(width * 0.45, 0.3, len + 0.4), cf * CFrame.new(0, 0.2, 0), foam, 0.35, Enum.Material.SmoothPlastic)
    made += 2
    -- foam ledges where the slope changes quickly
    local drop = ga - gb
    if drop / math.max(len, 0.1) > 0.9 and i % 3 == 0 then
      mk('LedgeFoam', Vector3.new(width + 3, 0.4, 3), CFrame.lookAt(pb + Vector3.new(0, 0.3, 0), pb + (pb - pa)) , foam, 0.25, Enum.Material.SmoothPlastic)
      made += 1
    end
  end
end
-- splash pool: foam discs at the base
local last = pts[#pts]
local gl = ground(last.X, last.Z) or 16
for k = 1, 4 do
  mk('Splash', Vector3.new(0.3, 14 + k * 6, 14 + k * 6), CFrame.new(last.X, gl + 0.3 + k * 0.05, last.Z) * CFrame.Angles(0, 0, math.rad(90)), foam, 0.35 + k * 0.12, Enum.Material.SmoothPlastic).Shape = Enum.PartType.Cylinder
  made += 1
end
-- a pool of water under the splash
local pool = mk('Pool', Vector3.new(0.4, 40, 40), CFrame.new(last.X, gl + 0.15, last.Z) * CFrame.Angles(0, 0, math.rad(90)), Color3.fromRGB(70, 130, 160), 0.35, Enum.Material.Glass)
pool.Shape = Enum.PartType.Cylinder
made += 1
return string.format('waterfall built: %d parts, old slab models archived: %d, base at (%.0f,%.1f,%.0f)', made, moved, last.X, gl, last.Z)
