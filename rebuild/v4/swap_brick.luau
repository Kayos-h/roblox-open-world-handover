-- swap_brick: replaces terrain Brick (deep seabed step of the v4d ramp) with Basalt over the whole map, in small tiles. Replayable and idempotent.
local T = workspace.Terrain
local S, E = -5600, 5600
local STEP = 560
local n, errs = 0, {}
for x = S, E - STEP, STEP do
  for z = S, E - STEP, STEP do
    local ok, err = pcall(function()
      T:ReplaceMaterial(Region3.new(Vector3.new(x, -72, z), Vector3.new(x + STEP, 8, z + STEP)):ExpandToGrid(4), 4, Enum.Material.Brick, Enum.Material.Basalt)
    end)
    n += 1
    if not ok then errs[#errs + 1] = x .. ',' .. z .. ': ' .. tostring(err):sub(1, 120) end
    if n % 4 == 0 then task.wait() end
  end
end
return string.format('tiles=%d errors=%d %s', n, #errs, table.concat(errs, ' | '))
