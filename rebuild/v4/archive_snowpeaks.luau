-- archive_snowpeaks: moves the (buried) SnowPeaks group of v4_pieces2 into ServerStorage.Phase1Archive_v4, then reports mesa protrusion.
local SS = game:GetService('ServerStorage')
local arch = SS:FindFirstChild('Phase1Archive_v4') or Instance.new('Folder')
arch.Name = 'Phase1Archive_v4'; arch.Parent = SS
local f = workspace.Phase1Map.v4_pieces2
local sp = f:FindFirstChild('SnowPeaks')
local n = 0
if sp then
  local holder = Instance.new('Folder'); holder.Name = 'SnowPeaks_buried_' .. os.time(); holder.Parent = arch
  for _, m in ipairs(sp:GetChildren()) do m.Parent = holder; n += 1 end
  sp:Destroy()
end
local T = workspace.Terrain
local rp = RaycastParams.new(); rp.FilterType = Enum.RaycastFilterType.Include; rp.FilterDescendantsInstances = { T }; rp.IgnoreWater = true
local mes = f:FindFirstChild('Mesas')
local out, buried, hover = {}, 0, 0
if mes then
  for _, m in ipairs(mes:GetChildren()) do
    local cf, size = m:GetBoundingBox()
    local bottom, top = cf.Position.Y - size.Y / 2, cf.Position.Y + size.Y / 2
    local lo, hi = 1e9, -1e9
    for _, o in ipairs({ { 0, 0 }, { 0.4, 0 }, { -0.4, 0 }, { 0, 0.4 }, { 0, -0.4 } }) do
      local r = workspace:Raycast(Vector3.new(cf.Position.X + o[1] * size.X, 900, cf.Position.Z + o[2] * size.Z), Vector3.new(0, -1300, 0), rp)
      local g = r and r.Position.Y or -50
      if g < lo then lo = g end
      if g > hi then hi = g end
    end
    if top < hi + 5 then buried += 1 end
    if bottom > lo + 6 then hover += 1 end
    if #out < 8 then out[#out + 1] = string.format('%s (%.0f,%.0f) size %.0fx%.0fx%.0f ground %.0f..%.0f bottom %.0f top %.0f', m.Name, cf.Position.X, cf.Position.Z, size.X, size.Y, size.Z, lo, hi, bottom, top) end
  end
end
return string.format('archived snow peaks: %d | mesas buried(top<ground+5)=%d hovering(bottom>lowest+6)=%d\n%s', n, buried, hover, table.concat(out, '\n'))
