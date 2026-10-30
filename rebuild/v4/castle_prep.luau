-- castle_prep: (1) archives the old K40 barracks / K41 stables (replaced by the V4 B04 buildings), (2) repaints the pavement slab of the courtyard flanks to lawn and the training yard to dirt.
local SS = game:GetService('ServerStorage')
local T = workspace.Terrain
local arch = SS:FindFirstChild('Phase1Archive_v4') or Instance.new('Folder')
arch.Name = 'Phase1Archive_v4'; arch.Parent = SS
local out = {}
local moved = 0
for _, d in ipairs(workspace.Phase1Map:GetDescendants()) do
  if d:IsA('Model') and (d.Name == 'K40_barracks' or d.Name == 'K41_stables') then
    local p = d:GetPivot().Position
    if math.abs(p.X) > 100 and p.Z < -2000 and p.Z > -2200 then d.Parent = arch; moved += 1 end
  end
end
out[#out + 1] = 'old castle buildings archived: ' .. moved
local function repl(x0, x1, z0, z1, to)
  local n = 0
  for _, from in ipairs({ Enum.Material.Pavement, Enum.Material.Cobblestone }) do
    local ok, err = pcall(function() T:ReplaceMaterial(Region3.new(Vector3.new(x0, 84, z0), Vector3.new(x1, 98, z1)):ExpandToGrid(4), 4, from, to) end)
    if not ok then out[#out + 1] = 'replace failed: ' .. tostring(err) else n += 1 end
  end
  return n
end
-- lawns on both flanks of the central plaza, whole slab depth
repl(-152, -62, -2238, -2042, Enum.Material.Grass)
repl(62, 152, -2238, -2042, Enum.Material.Grass)
-- training yard floor
repl(-141, -69, -2222, -2172, Enum.Material.Ground)
-- hard pads in front of the new buildings stay paved: re-paint small plazas back to pavement
local function paint(x0, x1, z0, z1, mat)
  pcall(function() T:FillBlock(CFrame.new((x0 + x1) / 2, 91, (z0 + z1) / 2), Vector3.new(x1 - x0, 2, z1 - z0), mat) end)
end
out[#out + 1] = 'lawns and yard floor painted'
return table.concat(out, '\n')
