local HS = game:GetService('HttpService')
local T = workspace.Terrain
local D = HS:JSONDecode([==[__DATA__]==])
local op, STEP, PROT = D.op, D.step, D.protect
local BOTTOM, CEIL = -60, 420
local M = Enum.Material
local AIR, WATER = M.Air, M.Water
local function mat(n) local ok, v = pcall(function() return M[n] end) return ok and v or M.Grass end
local SUB = { Grass = 'Ground', LeafyGrass = 'Ground', Mud = 'Ground', Ground = 'Ground', Sand = 'Sand', Sandstone = 'Sandstone',
  Rock = 'Rock', Snow = 'Rock', Glacier = 'Rock', Cobblestone = 'Ground', Pavement = 'Ground' }
local top = mat(op.material or 'Grass')
local sub = mat(SUB[op.material or 'Grass'] or 'Ground')
local ROADLIKE = { Cobblestone = true, Pavement = true, Ground = true, Mud = true }
local SHOULDER = ROADLIKE[op.material or ''] and M.Grass or top
local rp = RaycastParams.new(); rp.FilterType = Enum.RaycastFilterType.Include; rp.FilterDescendantsInstances = { T }; rp.IgnoreWater = true
local function ground(x, z)
  local r = workspace:Raycast(Vector3.new(x, CEIL + 50, z), Vector3.new(0, -(CEIL + 50 - BOTTOM), 0), rp)
  return r and r.Position.Y or BOTTOM
end
local function protected(x, z)
  for _, r in ipairs(PROT) do if x >= r[1] and x <= r[2] and z >= r[3] and z <= r[4] then return true end end
  return false
end
local n = 0
local function tick() n += 1; if n % 300 == 0 then task.wait() end end
local function column(x, z, h, tm, sm)
  h = math.clamp(h, BOTTOM + 6, CEIL - 10)
  T:FillBlock(CFrame.new(x, (BOTTOM + h - 4) / 2, z), Vector3.new(STEP, h - 4 - BOTTOM, STEP), sm or sub)
  T:FillBlock(CFrame.new(x, h - 2, z), Vector3.new(STEP, 4, STEP), tm or top)
  T:FillBlock(CFrame.new(x, (h + CEIL) / 2, z), Vector3.new(STEP, CEIL - h, STEP), AIR)
  tick()
end
local function smooth(t) t = math.clamp(t, 0, 1) return t * t * (3 - 2 * t) end
local x0, x1, z0, z1 = D.bx0, D.bx1, D.bz0, D.bz1
local cells = 0
for z = z0, z1 - 1, STEP do
  for x = x0, x1, STEP do
    local cx, cz = x + STEP / 2, z + STEP / 2
    if not protected(cx, cz) then
      local o = op.op
      if o == 'plateau' then
        local dx, dz = (cx - op.cx) / op.rx, (cz - op.cz) / op.rz
        local e = math.sqrt(dx * dx + dz * dz)
        if e <= 1 then column(cx, cz, op.top_y); cells += 1
        else
          local dist = (e - 1) * math.min(op.rx, op.rz)
          if dist < op.slope then
            local g = ground(cx, cz)
            column(cx, cz, g + (op.top_y - g) * (1 - smooth(dist / op.slope))); cells += 1
          end
        end
      elseif o == 'hill' then
        local d = math.sqrt((cx - op.cx) ^ 2 + (cz - op.cz) ^ 2)
        if d < op.r then
          local add = op.h * (math.cos(math.pi * d / op.r) + 1) / 2
          if add > 0.8 then column(cx, cz, ground(cx, cz) + add); cells += 1 end
        end
      elseif o == 'flatten' then
        if cx >= math.min(op.x0, op.x1) and cx <= math.max(op.x0, op.x1) and cz >= math.min(op.z0, op.z1) and cz <= math.max(op.z0, op.z1) then
          column(cx, cz, op.y); cells += 1
        end
      elseif o == 'ramp' then
        local ax, az = op.x1 - op.x0, op.z1 - op.z0
        local L2 = ax * ax + az * az
        local t = L2 > 0 and (((cx - op.x0) * ax + (cz - op.z0) * az) / L2) or 0
        if t >= -0.02 and t <= 1.02 then
          local tc = math.clamp(t, 0, 1)
          local px, pz = op.x0 + ax * tc, op.z0 + az * tc
          local perp = math.sqrt((cx - px) ^ 2 + (cz - pz) ^ 2)
          local hw = op.width / 2
          local band = math.max(10, math.min(op.width * 0.6, 60))
          local hy = op.y0 + (op.y1 - op.y0) * tc
          if perp <= hw then column(cx, cz, hy); cells += 1
          elseif perp <= hw + band then
            local g = ground(cx, cz)
            local f = 1 - smooth((perp - hw) / band)
            column(cx, cz, g + (hy - g) * f, SHOULDER); cells += 1
          end
        end
      elseif o == 'water' then
        if cx >= math.min(op.x0, op.x1) and cx <= math.max(op.x0, op.x1) and cz >= math.min(op.z0, op.z1) and cz <= math.max(op.z0, op.z1) then
          local bed = op.y - (op.depth or 6)
          column(cx, cz, bed, M.Mud, M.Ground)
          T:FillBlock(CFrame.new(cx, (bed + op.y) / 2, cz), Vector3.new(STEP, op.y - bed, STEP), WATER)
          cells += 1
        end
      elseif o == 'paint' then
        local d = math.sqrt((cx - op.cx) ^ 2 + (cz - op.cz) ^ 2)
        if d < op.r then
          local hit = workspace:Raycast(Vector3.new(cx, CEIL + 50, cz), Vector3.new(0, -(CEIL + 50 - BOTTOM), 0), rp)
          local g = hit and hit.Position.Y or BOTTOM
          local hm = hit and hit.Material
          local natural = hm == M.Grass or hm == M.LeafyGrass or hm == M.Ground or hm == M.Mud or hm == M.Sand or hm == M.Snow or hm == M.Rock or hm == M.Sandstone
          if natural and g > BOTTOM + 8 then T:FillBlock(CFrame.new(cx, g - 1.5, cz), Vector3.new(STEP, 3.2, STEP), top); tick(); cells += 1 end
        end
      end
    end
  end
end
return 'ok cells=' .. cells
