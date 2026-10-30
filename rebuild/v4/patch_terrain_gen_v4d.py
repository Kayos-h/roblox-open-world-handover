"""Terrain generator v4d patch (applied on top of the v4c generator; backup of v4c kept as rebuild/v4/terrain_gen_v4c.luau).
Replayable: python patch_terrain_gen_v4d.py   (always starts from the v4c backup, so running it twice is safe)

Changes
  A  clear-before-write: FillBlock(Air) over y -64..524 of every chunk before WriteVoxels. Root cause of the floating
     sand/mud plates and the dark flat sea floor: WriteVoxels(Water) onto an old partly solid cell leaves the solid cell.
  B  gentler offshore shelf (depth below sea level halved down to 30, then 1:1), shoreline unchanged (h = 0 crossing)
  C  sand skirt around every islet / sea stack (looks rooted)
  D  seabed material ramp by depth (Sand, Concrete, Asphalt, Brick are recoloured teal / blue / navy by look_pass3); rivers and lakes keep Sand/Mud
  E  ragged biome borders (extra high-frequency noise in biomeAt)
  F  alpine ground: snow reaches down to y 70..95 in patches, steeper snow-dusted rock, so the village sits in a snow-dusted band
  G  no hard 'pad' seam: Grass-only inside pads removed except for the jungle (elf valley)
"""
import os, shutil

RB = r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild'
V4 = RB + r'\v4'
src_path = RB + r'\terrain_gen.luau'
bak = V4 + r'\terrain_gen_v4c.luau'
if not os.path.exists(bak):
    shutil.copy(src_path, bak)
s = open(bak, encoding='utf-8').read()


def rep(old, new):
    global s
    n = s.count(old)
    assert n == 1, ('pattern count', n, old[:80])
    s = s.replace(old, new)


# ---------------------------------------------------------------- B: gentler offshore shelf, shoreline unchanged
rep("  h = lerp(h, (CO.floor - (CO.deep or 0) * ss(1.0, 1.15, cd)) + 4 * noise(x / 300, z / 300, 6.6), c)\n  h = postH(h, x, z)\n",
    "  h = lerp(h, (CO.floor - (CO.deep or 0) * ss(1.0, 1.15, cd)) + 4 * noise(x / 300, z / 300, 6.6), c)\n"
    "  if c > 0.05 and h < 0 then\n"
    "    local dd = -h\n"
    "    h = -(dd <= 10 and dd or (dd <= 40 and 10 + (dd - 10) * 0.5 or 25 + (dd - 40)))\n"
    "  end\n"
    "  h = postH(h, x, z)\n")

# ---------------------------------------------------------------- C: islet / sea stack skirt
a = s.index('local function postH(h, x, z)')
b = s.index('local function ridged(x, z)')
NEW_POST = '''local function postH(h, x, z)
  for _, f in ipairs(POST) do
    local d = sqrt((x - f[1]) ^ 2 + (z - f[2]) ^ 2)
    local r = f[3] * (1 + 0.15 * noise(x / 45, z / 45, f[1] * 0.002))
    if d < r * 2.6 then
      local v
      if d < r then
        local top = f[4] + 2.5 * noise(x / 30, z / 30, 1.9)
        v = lerp(top, -1.5, ss(r * 0.55, r, d))
      else
        v = lerp(-1.5, -40, ss(r, r * 2.6, d))
      end
      if v > h then h = v end
    end
  end
  return h
end
'''
s = s[:a] + NEW_POST + s[b:]

# ---------------------------------------------------------------- E: ragged biome borders
rep("local wgt = 1 - ss(0.5 * b[4], b[4], d + 60 * noise(x / 300, z / 300, 8.1))",
    "local wgt = 1 - ss(0.5 * b[4], b[4], d + 60 * noise(x / 300, z / 300, 8.1) + 40 * noise(x / 52, z / 52, 3.9))")

# ---------------------------------------------------------------- F, G: land materials
a = s.index('local function surfMat(')
b = s.index('local function inRect(')
NEW_SURF = '''local function surfMat(x, z, h, slope, roadMat, coastal, street, inPad)
  if roadMat then return MAT[roadMat] end
  local wx = x + 90 * noise(x / 200, z / 200, 1.1)
  local wz = z + 90 * noise(x / 200, z / 200, 2.2)
  local b = biomeAt(wx, wz)
  local n1 = noise(x / 140, z / 140, 3.7)
  local n2 = noise(x / 47, z / 47, 8.2)
  local n3 = noise(x / 71, z / 71, 12.3)
  local n4 = noise(x / 260, z / 260, 15.1)
  if h > 262 + 20 * n1 and slope < 0.6 then return M.Snow end
  if h < 3.4 and coastal > 0.05 then return (h < -6 and n1 > 0.1) and M.Mud or M.Sand end
  if h < 7 and coastal > 0.02 and n3 > 0.1 then return M.Sand end
  if b == 'dry' then
    if slope > 0.8 then return n2 > 0.2 and M.Rock or M.Sandstone end
    if slope > 0.45 then return M.Sandstone end
    if n3 > 0.38 then return M.Sandstone end
    if n4 > 0.35 then return M.Salt end
    return M.Ground
  end
  if b == 'alpine' then
    local sn = 150 + 25 * n1
    if slope > 0.8 then return n2 > 0.25 and M.Rock or M.Slate end
    if slope > 0.55 then return (n3 > 0.2 and h > 100) and M.Snow or M.Rock end
    if h > sn then return M.Snow end
    if h > 95 and n3 > -0.3 then return M.Snow end
    if h > 70 and n3 > 0.25 then return M.Snow end
    if h > 85 and n2 > 0.5 then return M.Rock end
    return (n1 > 0.3) and M.LeafyGrass or M.Grass
  end
  if slope > 0.9 then return n2 > 0.1 and M.Rock or M.Slate end
  if slope > 0.62 then return n2 > 0.1 and M.Rock or M.LeafyGrass end
  if b == 'jungle' then
    if inPad and inPad > 0.5 and n2 > -0.15 then return M.LeafyGrass end
    return n2 > 0.36 and M.Grass or M.LeafyGrass
  end
  if b == 'plains' then
    if n3 > 0.72 and slope < 0.3 then return M.Ground end
    return (n1 + 0.5 * n4 > 0.4) and M.LeafyGrass or M.Grass
  end
  if n3 > 0.7 and slope < 0.3 then return M.Ground end
  if slope > 0.45 and n2 > 0.0 then return M.Rock end
  return (n1 * 0.6 + n4 * 0.4 > 0.25) and M.Grass or M.LeafyGrass
end

'''
s = s[:a] + NEW_SURF + s[b:]

# ---------------------------------------------------------------- D: seabed ramp
rep("          if dp < 5 then sm = M.Sand elseif dp < 30 then sm = M.Mud else sm = M.Basalt end\n",
    "          if wl > 1.5 then\n"
    "            if dp < 2.2 then sm = M.Sand else sm = M.Mud end\n"
    "          elseif dp < 4 then sm = M.Sand\n"
    "          elseif dp < 9 then sm = M.Concrete\n"
    "          elseif dp < 17 then sm = M.Asphalt\n"
    "          else sm = M.Brick end\n")

# ---------------------------------------------------------------- A: clear before write
rep("  T:WriteVoxels(reg, RES, mats, occ)\n  if not (hitMtn or hitTown) and yHi < 360 then\n"
    "    T:FillBlock(CFrame.new(cx0 + CH / 2, (yHi + 380) / 2, cz0 + CH / 2), Vector3.new(CH, 380 - yHi, CH), M.Air)\n  end\n",
    "  if not (hitMtn or hitTown) then\n"
    "    -- v4d: clear the full height range first (WriteVoxels(Water) does not remove old partly solid cells)\n"
    "    T:FillBlock(CFrame.new(cx0 + CH / 2, (yLo + 524) / 2, cz0 + CH / 2), Vector3.new(CH, 524 - yLo, CH), M.Air)\n"
    "  end\n"
    "  T:WriteVoxels(reg, RES, mats, occ)\n")

s = s.replace('(v4: relief, west cliffs, robust rivers, default biome)', '(v4d: clear-before-write, gentle shelf, seabed ramp, ragged biomes)', 1)
open(src_path, 'w', encoding='utf-8').write(s)
print('terrain_gen.luau v4d written,', len(s), 'chars')


# the clip pass is derived from terrain_gen.luau (same height model), so rebuild it
import subprocess, sys
r = subprocess.run([sys.executable, V4 + r'\build_clip_v4.py'], capture_output=True, text=True)
print('clip rebuilt:', r.stdout.strip(), r.stderr.strip()[:300])
