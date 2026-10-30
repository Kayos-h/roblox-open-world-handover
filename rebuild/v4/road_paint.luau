-- road_paint: widens roads and trails by painting terrain material only. Data: {"samples":[[x,z,y|null,half,"Limestone"|"Ground"],...]}. Background thread, poll _G.ROADPAINT.
-- Per sample: for each of Grass, LeafyGrass, Ground, Mud and Sand? (Sand is left alone) ReplaceMaterial inside a box of half width around the sample, y from surface-5 to surface+3.
local HS = game:GetService('HttpService')
local D = HS:JSONDecode([==[__DATA__]==])
local T = workspace.Terrain
local rp = RaycastParams.new(); rp.FilterType = Enum.RaycastFilterType.Include; rp.FilterDescendantsInstances = { T }; rp.IgnoreWater = true
local SRC = { Enum.Material.Grass, Enum.Material.LeafyGrass, Enum.Material.Ground, Enum.Material.Mud }
local R = { done = false, i = 0, n = #D.samples, calls = 0, skippedWater = 0, errs = 0, started = os.clock() }
_G.ROADPAINT = R
task.spawn(function()
  for i, s in ipairs(D.samples) do
    R.i = i
    local x, z, y, half, matName = s[1], s[2], s[3], s[4], s[5]
    local tgt = Enum.Material[matName]
    local r = workspace:Raycast(Vector3.new(x, 900, z), Vector3.new(0, -1300, 0), rp)
    if r and r.Position.Y > 1.5 then
      local sy = r.Position.Y
      local reg = Region3.new(Vector3.new(x - half, sy - 5, z - half), Vector3.new(x + half, sy + 3, z + half)):ExpandToGrid(4)
      for _, from in ipairs(SRC) do
        if from ~= tgt then
          local ok = pcall(function() T:ReplaceMaterial(reg, 4, from, tgt) end)
          R.calls += 1
          if not ok then R.errs += 1 end
        end
      end
    else
      R.skippedWater += 1
    end
    if i % 40 == 0 then task.wait() end
  end
  R.done = true; R.secs = os.clock() - R.started
end)
return 'road paint started: ' .. #D.samples .. ' samples'
