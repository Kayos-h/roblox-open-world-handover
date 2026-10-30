-- reseat_env v2: after a terrain change, re-seats every placed model of the given Phase1Map folders onto the new ground.
-- Args (JSON): {"folders":["v4_forest","v4_under","v4_rocks","v4_shore"],"killRoad":true}
-- Absolute placement (idempotent): small models bottom = centre ground + yo - 0.25; big models (>= 14 studs) are buried by half of the ground drop under
-- their footprint (max 8 studs) so slopes look natural. Models whose footprint is mostly over open water are archived (except shore items).
-- Vegetation on road materials is archived (Ground only counts for trees). Runs in a background thread; poll _G.RESEAT.
local D = game:GetService('HttpService'):JSONDecode([==[__DATA__]==])
local T = workspace.Terrain
local SS = game:GetService('ServerStorage')
local arch = SS:FindFirstChild('Phase1Archive_v4') or Instance.new('Folder')
arch.Name = 'Phase1Archive_v4'; arch.Parent = SS
local rp = RaycastParams.new(); rp.FilterType = Enum.RaycastFilterType.Include; rp.FilterDescendantsInstances = { T }; rp.IgnoreWater = true
local ROAD = { [Enum.Material.Limestone] = true, [Enum.Material.Cobblestone] = true, [Enum.Material.Pavement] = true }
local R = { done = false, checked = 0, moved = 0, big = 0, water = 0, road = 0, errs = {}, started = os.clock(), folder = '' }
_G.RESEAT = R
local function ray(x, z)
  local r = workspace:Raycast(Vector3.new(x, 900, z), Vector3.new(0, -1300, 0), rp)
  return r
end
task.spawn(function()
  local ok, err = pcall(function()
    local pm = workspace.Phase1Map
    for _, fname in ipairs(D.folders) do
      local f = pm:FindFirstChild(fname)
      if f then
        R.folder = fname
        local kids = {}
        for _, g in ipairs(f:GetChildren()) do
          if g:IsA('Folder') then for _, m in ipairs(g:GetChildren()) do kids[#kids + 1] = m end
          elseif g:IsA('Model') then kids[#kids + 1] = g end
        end
        for i, m in ipairs(kids) do
          if m:IsA('Model') and m.Parent then
            local cf, size = m:GetBoundingBox()
            local px, pz = cf.Position.X, cf.Position.Z
            local bottom = cf.Position.Y - size.Y / 2
            local c = ray(px, pz)
            R.checked += 1
            if c then
              local yo = m:GetAttribute('YOffset') or 0
              local grpName = m.Parent and m.Parent.Name or ''
              local pre = string.sub(grpName, 1, 5)
              local shore = pre == 'Beach' or grpName == 'Riverbank' or grpName == 'Lakeside' or grpName == 'LilyPads'
              local gc = c.Position.Y
              local gmin, over = gc, 0
              local big = math.max(size.X, size.Z) >= 14 and (fname == 'v4_rocks' or fname == 'v4_pieces')
              if big then
                local hx, hz = size.X * 0.35, size.Z * 0.35
                for _, o in ipairs({ { hx, 0 }, { -hx, 0 }, { 0, hz }, { 0, -hz } }) do
                  local r2 = ray(px + o[1], pz + o[2])
                  local g2 = r2 and r2.Position.Y or -60
                  if g2 < gmin then gmin = g2 end
                  if g2 < -1 then over += 1 end
                end
              end
              if (gc < 0.3 and not shore) or (big and over >= 3 and not shore) then
                m.Parent = arch; R.water += 1
              elseif D.killRoad and ((ROAD[c.Material] and (pre == 'Trees' or pre == 'Under' or fname == 'v4_rocks')) or (c.Material == Enum.Material.Ground and pre == 'Trees')) then
                m.Parent = arch; R.road += 1
              else
                local sink = 0
                if big then
                  if fname == 'v4_pieces' then sink = math.min(math.max(gc - gmin, 0), 40)
                  elseif math.max(size.X, size.Z) >= 30 then sink = math.min(math.max(gc - gmin, 0) * 0.85, 30)
                  else sink = math.min(math.max(gc - gmin, 0) * 0.5, 8) end
                end
                local delta = (gc + yo - 0.25 - sink) - bottom
                if math.abs(delta) > 0.5 and math.abs(delta) < 60 then
                  m:PivotTo(m:GetPivot() + Vector3.new(0, delta, 0)); R.moved += 1
                  if math.abs(delta) > 4 then R.big += 1 end
                end
              end
            end
            if i % 200 == 0 then task.wait() end
          end
        end
      end
    end
  end)
  if not ok then R.errs[#R.errs + 1] = tostring(err) end
  R.done = true; R.secs = os.clock() - R.started
end)
return 'reseat started'
