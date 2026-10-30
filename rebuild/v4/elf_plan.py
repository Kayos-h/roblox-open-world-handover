"""Elf village v4 (natural look, NO glow). Writes:
  rebuild/v4/elf_streets.json  (paths merged into world.json by world_v4.py, then the elf chunks are regenerated)
  mapplan/v4_elf.json          (placements; place with build_v4.ps1 -area v4_elf -noglow)
The village keeps the valley between the four mountains: world tree at (-1560,-430), ring path, spokes, treehouse pairs joined by rope bridges,
round houses, market stalls, watch posts, gates, bridges, statues, standing stones, waterfall cliff above the lake, forested slopes.
Existing enterables kept: temple (-1490,-170) and round house 1 (-1730,-300). Round house 2 (-1390,-560) is archived.
"""
import json, math, random, sys
sys.argv = [sys.argv[0]]
import env_plan as E

rng = random.Random(777)
C = (-1560.0, -430.0)
MP = E.MP
IDS = E.IDS
OUTP = []          # placements
FOOT = []          # (x, z, r) of everything placed (to avoid overlaps)


def free(x, z, r, extra=0.0):
    for (fx, fz, fr) in FOOT:
        if math.hypot(x - fx, z - fz) < r + fr + extra:
            return False
    return True


def put(model, x, z, rot, group, scale=None, yo=None, r=None):
    if model not in IDS:
        print('missing model', model)
        return False
    it = {'model': model, 'x': round(x, 1), 'z': round(z, 1), 'rot': round(rot % 360, 1), 'group': group}
    if scale and abs(scale - 1) > 1e-3:
        it['scale'] = round(scale, 2)
    if yo:
        it['y_offset'] = round(yo, 2)
    OUTP.append(it)
    if r:
        FOOT.append((x, z, r))
    return True


def polar(r, deg):
    a = math.radians(deg)
    return C[0] + r * math.cos(a), C[1] + r * math.sin(a)


def face(x, z, tx, tz):
    """rot so that the model front (+Z at rot 0) looks from (x,z) toward (tx,tz)."""
    return math.degrees(math.atan2(tx - x, tz - z)) % 360


# --------------------------------------------------------------------------- paths (terrain streets)
Y = 13.5
streets = []


def add_street(name, pts, w=3.0):
    streets.append({'name': name, 'w': w, 'mat': 'Ground', 'bank': 10, 'pts': [[round(p[0], 1), round(p[1], 1), Y] for p in pts]})


ring = [polar(125, d) for d in range(0, 361, 12)]
add_street('v4_elf_ring', ring, 3.4)
add_street('v4_elf_spoke_e', [polar(125, 0), (-1380, -425), (-1330, -412), (-1292, -404)], 3.2)
add_street('v4_elf_spoke_s', [polar(125, 75), (-1522, -300), (-1505, -240), (-1492, -200)], 3.0)
add_street('v4_elf_spoke_w', [polar(125, 180), (-1760, -432), (-1830, -436), (-1895, -438)], 3.2)
add_street('v4_elf_spoke_h1', [polar(125, 140), (-1672, -352), (-1705, -325), (-1722, -312)], 2.8)
add_street('v4_elf_spoke_n', [polar(125, 270), (-1566, -560), (-1590, -600), (-1625, -628)], 3.0)
add_street('v4_elf_spoke_ne', [polar(125, 315), (-1480, -520), (-1440, -548)], 2.6)
add_street('v4_elf_pond', [polar(125, 20), (-1470, -330), (-1448, -282)], 2.4)
json.dump(streets, open(E.V4 + r'\elf_streets.json', 'w'), separators=(',', ':'))
PATHS = [[(p[0], p[1]) for p in s['pts']] for s in streets]


def path_dist(x, z):
    best = 1e9
    for line in PATHS:
        for i in range(len(line) - 1):
            d = E.seg_dist(x, z, line[i][0], line[i][1], line[i + 1][0], line[i + 1][1]) if hasattr(E, 'seg_dist') else 1e9
            best = min(best, d)
    return best


def seg_dist(px, pz, ax, az, bx, bz):
    vx, vz = bx - ax, bz - az
    L2 = vx * vx + vz * vz
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((px - ax) * vx + (pz - az) * vz) / L2))
    return math.hypot(px - (ax + vx * t), pz - (az + vz * t))


def path_dist(x, z):
    best = 1e9
    for line in PATHS:
        for i in range(len(line) - 1):
            best = min(best, seg_dist(x, z, line[i][0], line[i][1], line[i + 1][0], line[i + 1][1]))
    return best


# --------------------------------------------------------------------------- existing structures that stay
FOOT.append((-1490, -170, 36))     # temple enterable
FOOT.append((-1730, -300, 22))     # round house 1 enterable
FOOT.append((C[0], C[1], 112))     # world tree and roots

# --------------------------------------------------------------------------- world tree (3 pieces share the centre; canopy lifted onto the trunk)
put('D05_02_world_tree_roots', C[0], C[1], 0, 'WorldTree')
put('D05_01_world_tree_trunk', C[0], C[1], 0, 'WorldTree', yo=2)
put('D05_03_world_tree_canopy', C[0], C[1], 0, 'WorldTree', yo=118)

# --------------------------------------------------------------------------- treehouse pairs joined by long rope bridges
DECK = {'D01_01_treehouse_a': 21.75, 'D01_03_treehouse_c': 17.74, 'D01_04_treehouse_d': 22.76, 'D01_05_treehouse_e': 20.75, 'D01_06_treehouse_f': 24.73}
pairs = [(40, 'D01_01_treehouse_a', 'D01_04_treehouse_d'), (105, 'D01_03_treehouse_c', 'D01_05_treehouse_e'),
         (212, 'D01_06_treehouse_f', 'D01_06_treehouse_f'), (297, 'D01_01_treehouse_a', 'D01_01_treehouse_a')]
for ang, m1, m2 in pairs:
    px, pz = polar(205, ang)
    tx, tz = -math.sin(math.radians(ang)), math.cos(math.radians(ang))
    h1 = (px - 36.2 * tx, pz - 36.2 * tz)
    h2 = (px + 36.2 * tx, pz + 36.2 * tz)
    put(m1, h1[0], h1[1], rng.choice([0, 90, 180, 270]) + rng.uniform(-10, 10), 'Treehouses', r=30)
    put(m2, h2[0], h2[1], rng.choice([0, 90, 180, 270]) + rng.uniform(-10, 10), 'Treehouses', r=30)
    deck = (DECK[m1] + DECK[m2]) / 2
    rot = math.degrees(math.atan2(-tz, tx))
    put('D03_06_rope_bridge_long', px, pz, rot, 'Bridges', yo=deck - 11.1)
# a lone two-level treehouse as the lookout by the lake
put('D01_02_treehouse_b', -1468, -612, 200, 'Treehouses', r=30)

# --------------------------------------------------------------------------- ground buildings on the ring (doors toward the tree)
houses = ['D04_01_round_house_a', 'D04_02_round_house_b', 'D04_03_round_house_c']
for ang in (20, 58, 96, 160, 226, 252, 338):
    x, z = polar(168, ang)
    if path_dist(x, z) < 12 or not free(x, z, 18):
        continue
    put(houses[len(OUTP) % 3], x, z, face(x, z, C[0], C[1]), 'Houses', r=18)
put('D04_16_workshop', *polar(172, 245), face(*polar(172, 245), C[0], C[1]), 'Houses', r=18)
FOOT.append((polar(172, 245)[0], polar(172, 245)[1], 18))
put('D04_05_palace', -1470, -655, 0, 'Palace', r=45)
put('D04_14_pavilion', -1722, -528, face(-1722, -528, C[0], C[1]), 'Houses', r=16)
put('D04_15_moon_pool', -1570, -615, 0, 'Palace', r=22)
# market stalls on the east side of the plaza
for ang, m in ((322, 'D04_08_stall_a'), (338, 'D04_09_stall_b'), (354, 'D04_10_stall_c'), (10, 'D04_08_stall_a')):
    x, z = polar(100, ang)
    put(m, x, z, face(x, z, C[0], C[1]), 'Market', r=9)
# watch posts at the passes, gate arches at the entries
for (x, z) in ((-1318, -452), (-1830, -392), (-1520, -118), (-1610, -742)):
    put('D04_11_watch_post', x, z, face(x, z, C[0], C[1]), 'Watch', r=10)
put('D04_06_gate_arch_a', -1300, -406, 90, 'Gates', r=20)
put('D04_07_gate_arch_b', -1885, -437, 90, 'Gates', r=20)

# --------------------------------------------------------------------------- bridges over the river, stepping stones
def bridge(model, x, z, along, attach, grp='Bridges'):
    d = (math.cos(math.radians(along)), -math.sin(math.radians(along)))
    banks = max(E.H(x + d[0] * 24, z + d[1] * 24), E.H(x - d[0] * 24, z - d[1] * 24))
    yo = banks - E.H(x, z) - attach + 0.4
    put(model, x, z, along, grp, yo=max(0.0, yo))


bridge('D04_12_stone_bridge_a', -1884, -437, 0, 5.2)
put('D09_03_stepping_stones', -1448, -278, 40, 'Bridges')
put('D09_04_plank_bridge_a', -1598, -612, 20, 'Bridges', yo=1.5)

# --------------------------------------------------------------------------- waterfall cliff above the lake and cascade steps at the outlet
put('R05_01_waterfall_cliff_large_01', -1655, -742, 0, 'Waterfall', yo=-6)
put('F10_04_waterfall_cascade', -1692, -566, 250, 'Waterfall')
put('F10_03_waterfall_step', -1735, -523, 235, 'Waterfall')

# --------------------------------------------------------------------------- lore props
for ang, m in ((90, 'D08_01_statue_a'), (210, 'D08_02_statue_b'), (330, 'D08_03_statue_c')):
    x, z = polar(104, ang)
    put(m, x, z, face(x, z, C[0], C[1]), 'Lore', r=8)
for ang, m in ((8, 'D08_10_banner_a'), (128, 'D08_11_banner_b'), (190, 'D08_12_banner_c'), (258, 'D08_10_banner_a'), (300, 'D08_11_banner_b')):
    x, z = polar(135, ang)
    if free(x, z, 6):
        put(m, x, z, face(x, z, C[0], C[1]), 'Lore', r=6)
for (m, x, z, r) in (('D08_06_standing_stone_a', -1415, -222, 0), ('D08_07_standing_stone_b', -1472, -214, 40), ('D08_04_ruin_arch_a', -1860, -250, 20),
                     ('D08_05_ruin_arch_b', -1260, -640, 200), ('D08_08_marker_a', -1280, -392, 90), ('D08_09_marker_b', -1900, -450, 270)):
    if free(x, z, 10):
        put(m, x, z, r, 'Lore', r=10)
# lanterns on posts along the ring (plain, unlit)
for k in range(0, 360, 20):
    x, z = polar(131, k)
    if path_dist(x, z) > 2.5 and free(x, z, 3, 0):
        put('D07_01_lantern_post_a' if k % 40 == 0 else 'D07_02_lantern_post_b', x, z, 0, 'Lanterns')
for ang in (90, 210, 330):
    x, z = polar(110, ang + 12)
    put('D07_05_brazier', x, z, 0, 'Lanterns')
for ang in (30, 150, 270):
    x, z = polar(112, ang)
    put('D07_06_candle_cluster', x, z, rng.uniform(0, 360), 'Lanterns')

# --------------------------------------------------------------------------- big old trees at the rim and fallen logs
rim = []
for k in range(14):
    ang = k * 25.7 + rng.uniform(-6, 6)
    r = rng.uniform(285, 345)
    x, z = polar(r, ang)
    if E.H(x, z) > 3 and E.slope(x, z) < 0.5 and free(x, z, 30):
        put(rng.choice(['D05_04_ancient_tree_a', 'D05_05_ancient_tree_b', 'D05_06_ancient_tree_c', 'D05_07_ancient_tree_d', 'D05_08_ancient_tree_e']), x, z, rng.uniform(0, 360), 'Ancients', scale=rng.uniform(0.85, 1.15), r=32)
for (x, z) in ((-1700, -150), (-1380, -120)):
    put('D05_17_hollow_tree', x, z, rng.uniform(0, 360), 'Ancients', r=26)
for k in range(26):
    ang, r = rng.uniform(0, 360), rng.uniform(150, 300)
    x, z = polar(r, ang)
    if path_dist(x, z) > 8 and free(x, z, 6) and E.H(x, z) > 3 and not E.has_water(x, z):
        put(rng.choice(['D05_12_stump_a', 'D05_13_stump_b', 'D05_14_stump_c', 'D05_15_log_a', 'D05_16_log_b', 'D05_18_sapling', 'D06_10_moss_rock_a', 'D06_11_moss_rock_b', 'D06_12_moss_rock_c']),
            x, z, rng.uniform(0, 360), 'Floor', scale=rng.uniform(0.9, 1.3))

# --------------------------------------------------------------------------- forest around and inside the valley, soft undergrowth
def lush(x, z, r):
    """tree/bush density by distance from the tree"""
    if r < 150:
        return 0.0
    if r < 240:
        return 0.10
    return 0.30 + 0.55 * min(1.0, (r - 240) / 160)


cnt = {'trees': 0, 'under': 0}
for gx in range(-2130, -990, 27):
    for gz in range(-1000, 130, 27):
        x, z = gx + rng.uniform(-10, 10), gz + rng.uniform(-10, 10)
        r = math.hypot(x - C[0], z - C[1])
        if r > 580:
            continue
        h = E.H(x, z)
        if h < 3 or E.has_water(x, z) or E.in_lake(x, z, 1.4) or E.M(x, z) in ('C', 'P', 'S', 'M', 'I', 'N'):
            continue
        sl = E.slope(x, z)
        if sl > 0.8 or h > 230:
            continue
        p = lush(x, z, r) * (1 - E.ss(0.5, 0.85, sl))
        if E.vnoise(x / 150, z / 150, 5) > 0.55:
            p *= 0.3
        if rng.random() > p or path_dist(x, z) < 9 or not free(x, z, 12) or E.RIVERS.dist(x, z) < 8:
            continue
        m = E.pick(E.TREES['forest'])
        if put(m, x, z, rng.uniform(0, 360), 'Trees', scale=rng.uniform(0.9, 1.3), yo=-0.4):
            cnt['trees'] += 1
for gx in range(-2130, -990, 18):
    for gz in range(-1000, 130, 18):
        x, z = gx + rng.uniform(-7, 7), gz + rng.uniform(-7, 7)
        r = math.hypot(x - C[0], z - C[1])
        if r > 580 or r < 135:
            continue
        h = E.H(x, z)
        if h < 3 or E.has_water(x, z) or E.in_lake(x, z, 1.3) or E.M(x, z) in ('C', 'P', 'S', 'M', 'I', 'N') or E.slope(x, z) > 0.7:
            continue
        p = 0.10 if r < 240 else 0.26
        if rng.random() > p or path_dist(x, z) < 4.5 or not free(x, z, 4):
            continue
        m = E.pick(E.UNDER['forest'] + (('D06_04_bush_a', 0.3), ('D06_06_bush_c', 0.3), ('D06_07_flower_a', 0.5), ('D06_09_flower_c', 0.5), ('D06_18_mushroom_a', 0.3), ('D06_01_fern_a', 0.4)))
        if put(m, x, z, rng.uniform(0, 360), 'Under', scale=rng.uniform(0.85, 1.3)):
            cnt['under'] += 1

json.dump({'area': 'v4_elf', 'terrain': [], 'placements': OUTP}, open(MP + r'\v4_elf.json', 'w'))
import collections
g = collections.Counter(i['group'] for i in OUTP)
print('elf placements', len(OUTP), dict(g), cnt)
