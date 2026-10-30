"""Patches the v3 terrain generator into the v4 generator (backup of v3 kept in rebuild/v4/terrain_gen_v3.luau).
Changes: relief parameters, west cliff coast, rivers robust against noise, default biome, higher snow line in the alpine biome.
Then builds terrain_clip.luau with a Town 1 guard that works without _G.T1SNAP. Replayable: python patch_terrain_gen.py
"""
import os, shutil, subprocess, sys

RB = r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild'
V4 = RB + r'\v4'
src_path = RB + r'\terrain_gen.luau'
bak = V4 + r'\terrain_gen_v3.luau'
if not os.path.exists(bak):
    shutil.copy(src_path, bak)
s = open(bak, encoding='utf-8').read()


def rep(old, new):
    global s
    n = s.count(old)
    assert n == 1, ('pattern count', n, old[:70])
    s = s.replace(old, new)


rep("local FEAT = W.features\n", "local FEAT = W.features\nlocal RL = W.relief or {}\n")
rep("local POST = W.post or {}\n",
    "local function coastStart(x, z)\n  local ws = CO.west_start\n  if not ws then return CO.start end\n  return lerp(CO.start, ws, ss(900, 1700, -x))\nend\nlocal POST = W.post or {}\n")
rep("local amp = (8 + 0.10 * max(0, h - 6)) * (1 - c)", "local amp = ((RL.base or 8) + (RL.slope or 0.10) * max(0, h - 6)) * (1 - c)")
rep("local c = ss(CO.start, CO['end'], cd)", "local c = ss(coastStart(x, z), CO['end'], cd)")
rep("if h0 >= lv + 0.8 then", "if h0 >= lv - 8 then")
rep("local best, bw = 'plains', 0.3", "local best, bw = (W.default_biome or 'plains'), 0.3")
rep("local sn = 215 + 25 * n1", "local sn = 165 + 25 * n1")
rep("if h > 165 and n2 > 0.25 then return M.Snow end", "if h > 130 and n2 > 0.3 then return M.Snow end")
# ---- v4c: rewrite the whole column from y=-64 so no stale voxels from older generations can survive below the surface
#      (the old void-fill 2 pass deleted new mountains standing on former ocean, so v4 does not use fill_voids at all)
rep("yLo = max(-60, floor((lo - 16) / RES) * RES)", "yLo = -64")
s = s.replace('-- Phase 1 terrain generator.', '-- Phase 1 terrain generator (v4: relief, west cliffs, robust rivers, default biome).', 1)

# ---- v4b additions: irregular coast, deeper ocean shelf, richer ground materials, seabed materials
rep("0.05 * noise(x / 900, z / 900, 3.3) + 0.018 * noise(x / 260, z / 260, 7.7)",
    "0.055 * noise(x / 900, z / 900, 3.3) + 0.03 * noise(x / 420, z / 420, 5.5) + 0.018 * noise(x / 180, z / 180, 7.7)")
rep("h = lerp(h, CO.floor + 4 * noise(x / 300, z / 300, 6.6), c)",
    "h = lerp(h, (CO.floor - (CO.deep or 0) * ss(1.0, 1.15, cd)) + 4 * noise(x / 300, z / 300, 6.6), c)")
rep("        local wl = WL[i][k]\n",
    "        local wl = WL[i][k]\n        if wl and h < wl - 1 and sm ~= M.Ice then\n          local dp = wl - h\n          if dp < 5 then sm = M.Sand elseif dp < 30 then sm = M.Mud else sm = M.Basalt end\n        end\n")
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
    local sn = 165 + 25 * n1
    if slope > 0.75 then return n2 > 0.25 and M.Rock or M.Slate end
    if slope > 0.5 then return M.Rock end
    if h > sn then return M.Snow end
    if h > 130 and n2 > 0.3 then return M.Snow end
    if h > 100 and n3 > 0.45 then return M.Snow end
    if h > 90 and n2 > 0.55 then return M.Rock end
    return (n1 > 0.3 and not inPad) and M.LeafyGrass or M.Grass
  end
  if slope > 0.9 then return n2 > 0.1 and M.Rock or M.Slate end
  if slope > 0.62 then return n2 > 0.1 and M.Rock or M.LeafyGrass end
  if inPad and inPad > 0.5 then return (b == 'jungle' and n2 > -0.15) and M.LeafyGrass or M.Grass end
  if b == 'jungle' then return n2 > 0.36 and M.Grass or M.LeafyGrass end
  if b == 'plains' then
    if n3 > 0.62 and slope < 0.3 then return M.Ground end
    return (n1 + 0.5 * n4 > 0.5) and M.LeafyGrass or M.Grass
  end
  if n3 > 0.6 and slope < 0.3 then return M.Ground end
  if slope > 0.45 and n2 > 0.0 then return M.Rock end
  return (n1 * 0.6 + n4 * 0.4 > 0.25) and M.Grass or M.LeafyGrass
end

'''
s = s[:a] + NEW_SURF + s[b:]
open(src_path, 'w', encoding='utf-8').write(s)
print('terrain_gen.luau patched,', len(s), 'chars')

# clip pass: protect Town 1 through the keep rectangle (no _G.T1SNAP needed)
c = open(RB + r'\build_clip.py', encoding='utf-8').read()
old = "local inT1 = SNAP and T1 and abs(x) <= T1.x and z >= T1.z0 and z <= T1.z1"
new = "local inT1 = (KT and inRect(KT, x, z)) or (SNAP and T1 and abs(x) <= T1.x and z >= T1.z0 and z <= T1.z1)"
assert c.count(old) == 1
open(V4 + r'\build_clip_v4.py', 'w', encoding='utf-8').write(c.replace(old, new))
r = subprocess.run([sys.executable, V4 + r'\build_clip_v4.py'], capture_output=True, text=True)
print(r.stdout.strip(), r.stderr.strip()[:300])
