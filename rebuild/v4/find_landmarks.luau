-- find_landmarks: read-only. Bounding boxes of named landmark models.
local want = { 'B08_01_town1_church_01', 'town1_church', 'skull', 'Skull', 'K01_main_keep', 'K40_barracks', 'K41_stables', 'K43_royal_carriage', 'G28_seawall' }
local out = {}
local roots = { workspace.Phase1Map, workspace:FindFirstChild('SpawnTown') }
local n = 0
for _, root in ipairs(roots) do
  if root then
    for _, d in ipairs(root:GetDescendants()) do
      if d:IsA('Model') then
        for _, w in ipairs(want) do
          if string.find(d.Name, w, 1, true) then
            local ok, cf, size = pcall(function() return d:GetBoundingBox() end)
            if ok and size.X > 6 and #out < 24 and (w ~= 'G28_seawall' or #out < 3) then
              out[#out + 1] = string.format('%s [%s] at (%.0f,%.0f,%.0f) size %.0fx%.0fx%.0f yaw=%.0f', d.Name, d.Parent and d.Parent.Name or '?', cf.X, cf.Y, cf.Z, size.X, size.Y, size.Z, math.deg(math.atan2(-cf.LookVector.X, -cf.LookVector.Z)))
            end
            break
          end
        end
      end
      n += 1
      if n % 6000 == 0 then task.wait() end
    end
  end
end
return table.concat(out, '\n')
