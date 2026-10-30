-- far_sea: a flat ring of dark-blue slabs beyond the generated ocean (+-5376) out to +-13000, top face 0.6 studs below the water surface so it blends in. Replayable.
local root = workspace.Phase1Map
local old = root:FindFirstChild('v4_farsea'); if old then old:Destroy() end
local f = Instance.new('Folder'); f.Name = 'v4_farsea'; f.Parent = root
local E0, E1 = 5376 - 8, 13000
local S = 2048
local n = 0
local col = Color3.fromRGB(6, 50, 104)
local function slab(x0, x1, z0, z1)
  local w, d = x1 - x0, z1 - z0
  local cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
  local p = Instance.new('Part')
  p.Name = 'FarSea'; p.Anchored = true; p.CanCollide = false; p.CanTouch = false; p.CanQuery = false; p.CastShadow = false
  p.Material = Enum.Material.SmoothPlastic; p.Color = col; p.Reflectance = 0
  p.Size = Vector3.new(w, 1, d)
  p.CFrame = CFrame.new(cx, -1.1, cz)
  p.Parent = f
  n += 1
end
local function strip(x0, x1, z0, z1)
  local xs = math.ceil((x1 - x0) / S)
  local zs = math.ceil((z1 - z0) / S)
  for i = 0, xs - 1 do
    for j = 0, zs - 1 do
      slab(x0 + i * ((x1 - x0) / xs), x0 + (i + 1) * ((x1 - x0) / xs), z0 + j * ((z1 - z0) / zs), z0 + (j + 1) * ((z1 - z0) / zs))
    end
  end
end
strip(-E1, E1, -E1, -E0)      -- north
strip(-E1, E1, E0, E1)        -- south
strip(-E1, -E0, -E0, E0)      -- west
strip(E0, E1, -E0, E0)        -- east
return 'far sea slabs: ' .. n
