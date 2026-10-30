"""v3 review fixes: eight extra placement plans. Run: python fixes3.py
Each plan is seeded with obstacles (existing placements + streets) so nothing overlaps.
"""
import json, math, random, sys, os
sys.path.insert(0, r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild')
from layout_lib import Plan, CAT, obb, face_rot, obb_overlap

MP = r'C:\Users\Nitro\.kiro\crew\workspace\town\mapplan'
RB = r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild'
W = json.load(open(RB + r'\world.json'))
PLANS = ['v3_capital', 'v3_rusty', 'v3_harbour', 'v3_elf', 'v3_alpine', 'v3_country', 'town1_graveyard']
EXIST = {}
for n in PLANS:
    try:
        EXIST[n] = json.load(open(f'{MP}\\{n}.json'))['placements']
    except Exception:
        EXIST[n] = []
# town1 own items live in the live map, not in a plan; approximate Town 1 as a no-go box for exterior plans
STREETS = W.get('streets', [])


def seed(P, bbox, pad=0.0, plans=None):
    x0, x1, z0, z1 = bbox
    n = 0
    for name in (plans or EXIST):
        for it in EXIST[name]:
            if x0 - 30 <= it['x'] <= x1 + 30 and z0 - 30 <= it['z'] <= z1 + 30 and it['model'] in CAT:
                m = CAT[it['model']]
                s = it.get('scale', 1) or 1
                P.blocks.append(obb(it['x'], it['z'], m['size_x'] * s / 2 + pad, m['size_z'] * s / 2 + pad, it.get('rot', 0)))
                n += 1
    return n


def seed_streets(P, bbox, extra=4.0):
    x0, x1, z0, z1 = bbox
    for st in STREETS:
        pts = st['pts']
        half = st['w'] if st['w'] >= 20 else st['w'] / 2 + extra
        for i in range(len(pts) - 1):
            a, b = pts[i], pts[i + 1]
            if max(a[0], b[0]) < x0 - 40 or min(a[0], b[0]) > x1 + 40 or max(a[1], b[1]) < z0 - 40 or min(a[1], b[1]) > z1 + 40:
                continue
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            if L < 0.1:
                continue
            d = ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
            P.sblocks.append(obb((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, L / 2 + 1, half, face_rot(-d[1], d[0])))


def ok(m):
    return m in CAT


def put_many(P, models, n, bbox, group, inside=None, scale=(0.9, 1.15), gap=1.5, block=False, rot=None, weights=None, tries=None):
    inside = inside or (lambda x, z: True)
    x0, x1, z0, z1 = bbox
    models = [m for m in models if ok(m)]
    if not models:
        return 0
    return P.scatter(inside, models, n, group, min_gap=gap, scale=scale, weights=weights, block=block, tries=tries or n * 40, rot=rot, bbox=bbox)


def ring(P, cx, cz, r, n, model, group, face='in', a0=0.0, skip=None, scale=None, block=False, yo=None):
    k = 0
    for i in range(n):
        a = a0 + math.tau * i / n
        x, z = cx + math.cos(a) * r, cz + math.sin(a) * r
        if skip and skip(x, z):
            continue
        fx, fz = (cx - x, cz - z) if face == 'in' else (x - cx, z - cz)
        if P.put(model, x, z, face_rot(fx, fz), group, block=block, pad=0.4, scale=scale, yo=yo, streets=False):
            k += 1
    return k


def save(P, name):
    P.area = name
    P.save(f'{MP}\\{name}.json')
    from collections import Counter
    c = Counter(i['model'] for i in P.items)
    print(f'{name}: {len(P.items)} items;', dict(c.most_common(6)))
    return len(P.items)


report = {}
# ============================================================ A) graveyard extras (town1_gy2)
P = Plan('town1_gy2', seed=4101)
BB = (-288, -190, 206, 286)
seed(P, (-300, -180, 195, 300), plans=['town1_graveyard'])
for it in EXIST['town1_graveyard']:  # fence/gate/lantern etc already seeded; add aisle corridor
    pass
P.sblocks.append(obb(-238, 246, 52, 5.5, 90))        # central aisle (long axis along world X)
P.sblocks.append(obb(-190, 246, 8, 12, 90))          # gate approach
inside_gy = lambda x, z: -284 <= x <= -194 and 211 <= z <= 281
put_many(P, ['D12_gravestone_1', 'D13_gravestone_2', 'D14_gravestone_3', 'D15_gravestone_4', 'D16_stone_cross'], 150, BB, 'Graves2', inside_gy, scale=(0.85, 1.2), gap=0.6, block=True, rot=None, tries=9000,
         weights={'D12_gravestone_1': 5, 'D13_gravestone_2': 5, 'D14_gravestone_3': 0.5, 'D15_gravestone_4': 5, 'D16_stone_cross': 4})
for it in P.items:                                   # graves face the church (east, rot ~90) with jitter
    it['rot'] = round(90 + P.rng.uniform(-9, 9), 1)
put_many(P, ['A35_dead_tree_1', 'A36_dead_tree_2'], 8, BB, 'DeadTrees', inside_gy, scale=(0.9, 1.3), gap=4, block=True)
for (x, z) in [(-218, 224), (-262, 268), (-206, 270), (-272, 222)]:
    P.put('D19_weeping_statue', x, z, face_rot(-157 - x, 245 - z), 'Statues2', block=True, pad=1.0, scale=1.05)
put_many(P, ['D10_church_pillar'], 4, BB, 'Ruins2', inside_gy, scale=(0.4, 0.55), gap=3, block=True)
put_many(P, ['D09_candle_stand'], 8, BB, 'Candles2', inside_gy, scale=(0.9, 1.0), gap=1.0)
put_many(P, ['A23_candle_cluster'], 16, BB, 'Candles2', inside_gy, scale=(0.7, 1.0), gap=0.6)
put_many(P, ['A56_rock_small_1', 'A57_rock_small_2', 'A58_rock_medium_1', 'A67_fallen_log', 'A70_branch_pile'], 22, BB, 'Debris2', inside_gy, scale=(0.8, 1.2), gap=1.2)
put_many(P, ['D33_broken_fence'], 6, BB, 'Debris2', lambda x, z: inside_gy(x, z) and (z < 218 or z > 274), scale=(0.9, 1.0), gap=1.0)
for (x, z) in [(-270, 262), (-210, 218)]:
    P.put('D17_mausoleum', x, z, 90, 'Crypts2', block=True, pad=2.0)
report['town1_gy2'] = save(P, 'town1_gy2')

# ============================================================ B) castle bailey (v3f_castle)
P = Plan('v3f_castle', seed=4102)
BB = (-195, 195, -2345, -2025)
seed(P, BB, plans=['v3_capital'])
CX, CZ = 0, -2140
P.sblocks.append(obb(0, -2140, 18, 18, 0))        # fountain basin kept clear
P.sblocks.append(obb(0, -2150, 9, 12, 0))         # central axis road
P.sblocks.append(obb(0, -2200, 6, 100, 0))
stalls = [m for m in ['A105_market_stall_fruit', 'A106_market_stall_cloth', 'A107_market_stall_potion'] if ok(m)]
for i in range(12):
    a = math.pi * 0.5 + (i - 5.5) * 0.34              # arc south of the fountain (toward the gate)
    x, z = CX + math.cos(a) * 66, CZ + math.sin(a) * 66
    if abs(x) < 14:
        continue
    P.put(stalls[i % len(stalls)], x, z, face_rot(CX - x, CZ - z), 'CastleMarket', block=True, pad=1.2, streets=False)
ring(P, CX, CZ, 44, 8, 'C22_knight_statue', 'Statues', face='out', a0=0.4, block=True, scale=1.0)
ring(P, CX, CZ, 52, 14, 'K34_ornate_lamp', 'Lamps', face='in', a0=0.2, block=False)
for z in range(-2050, -2260, -28):
    for sx in (-11, 11):
        P.put('K35_royal_banner', sx, z, 0, 'Banners', block=False, check=False, scale=0.9)
# barracks yard (west)
for m, n in [('A74_crate_large', 4), ('A71_barrel', 7), ('A84_table', 2), ('A82_bench_wood', 3), ('A21_brazier', 2), ('A99_anvil', 1), ('A93_notice_board', 1), ('A95_flag_pole', 2), ('A73_crate_small', 5)]:
    P.cluster(-112, -2095, [m], 'BarracksYard', n=n, radius=24)
# stable yard (east)
for m, n in [('A78_hay_bale', 8), ('A97_water_trough', 2), ('A80_wagon', 1), ('A79_hand_cart', 1), ('A71_barrel', 4), ('A87_bucket', 5), ('A82_bench_wood', 1)]:
    P.cluster(112, -2100, [m], 'StableYard', n=n, radius=24)
# keep forecourt
P.put('C23_obelisk', -48, -2205, 0, 'Forecourt', block=True, pad=1.0)
P.put('C23_obelisk', 48, -2205, 0, 'Forecourt', block=True, pad=1.0)
P.put('C22_knight_statue', -24, -2243, 0, 'Forecourt', block=True, pad=1.0)
P.put('C22_knight_statue', 24, -2243, 0, 'Forecourt', block=True, pad=1.0)
# rear gardens
gw = lambda x, z: -185 <= x <= -105 and -2335 <= z <= -2285
ge = lambda x, z: 105 <= x <= 185 and -2335 <= z <= -2285
for g in (gw, ge):
    put_many(P, ['A41_hedge_straight'], 8, BB, 'Gardens', g, scale=(1, 1), gap=1.2, block=True)
    put_many(P, ['A48_planter_box'], 6, BB, 'Gardens', g, scale=(1, 1), gap=1.2)
    put_many(P, ['A43_flowers_red', 'A44_flowers_yellow', 'A46_flowers_white', 'A47_flowers_blue', 'A45_flowers_purple'], 22, BB, 'Gardens', g, scale=(0.9, 1.3), gap=0.8)
    put_many(P, ['A34_fruit_tree', 'A26_oak_3'], 4, BB, 'Gardens', g, scale=(0.9, 1.1), gap=5, block=True)
    put_many(P, ['K33_ornate_bench'], 2, BB, 'Gardens', g, scale=(1, 1), gap=2)
P.put('A98_well', 138, -2300, 0, 'Gardens', block=True, pad=1.0)
report['v3f_castle'] = save(P, 'v3f_castle')

# ============================================================ C) Town 1 SE exterior (v3f_se)
P = Plan('v3f_se', seed=4103)
BB = (335, 540, 30, 300)
seed(P, BB)
seed_streets(P, BB)
P.sblocks.append(obb(330, 0, 150, 14, 90))        # east gate road
P.sblocks.append(obb(0, 330, 14, 60, 0))
plots = [(380, 85), (425, 85), (380, 130), (425, 130), (470, 105)]
for (px, pz) in plots:
    P.put('H08_vegetable_crop_rows' if (px + pz) % 2 else 'H07_wheat_crop_rows', px, pz, 0, 'FarmSE', block=True, pad=0.5, streets=False)
    P.put('H07_wheat_crop_rows', px, pz + 13, 0, 'FarmSE', block=True, pad=0.5, streets=False)
    P.line_of('A101_fence_rail', (px - 11, pz - 8), (px + 11, pz - 8), 'FarmSE', block=False, streets=False) if ok('A101_fence_rail') else None
    P.line_of('A101_fence_rail', (px - 11, pz + 21), (px + 11, pz + 21), 'FarmSE', block=False, streets=False) if ok('A101_fence_rail') else None
for (x, z) in [(402, 107), (447, 107), (402, 152), (452, 130)]:
    P.put('H09_scarecrow', x, z, P.rng.uniform(0, 360), 'FarmSE', block=False, check=False)
P.put('H10_working_windmill', 470, 200, 200, 'FarmSE', block=True, pad=2.0, streets=False)
P.put('A98_well', 410, 190, 0, 'FarmSE', block=True, pad=1.0, streets=False)
for m, n in [('A78_hay_bale', 9), ('A80_wagon', 1), ('A79_hand_cart', 1), ('A71_barrel', 4), ('A74_crate_large', 3)]:
    P.cluster(430, 190, [m], 'FarmSE', n=n, radius=18)
for gx in range(350, 520, 28):                    # orchard grid
    for gz in range(225, 295, 24):
        P.put('A34_fruit_tree', gx + P.rng.uniform(-3, 3), gz + P.rng.uniform(-3, 3), P.rng.uniform(0, 360), 'Orchard', block=True, pad=3.0, scale=P.rng.uniform(0.9, 1.1))
P.line_of('A41_hedge_straight', (338, 60), (338, 200), 'Hedge', block=False, streets=False) if ok('A41_hedge_straight') else None
put_many(P, ['A43_flowers_red', 'A44_flowers_yellow', 'A46_flowers_white', 'A47_flowers_blue'], 40, BB, 'Flowers', scale=(0.9, 1.4), gap=0.8)
put_many(P, ['A26_oak_3', 'A25_oak_2', 'A28_birch_2', 'A40_bush_3', 'A39_bush_2'], 24, BB, 'Trees', scale=(0.9, 1.2), gap=3, block=True)
report['v3f_se'] = save(P, 'v3f_se')

# ============================================================ D) alpine ice lake (v3f_alpine)
P = Plan('v3f_alpine', seed=4104)
BB = (1330, 1660, -1190, -940)
seed(P, BB)
seed_streets(P, BB)
ice = lambda x, z: 1345 <= x <= 1640 and -1175 <= z <= -1000 and ((x - 1490) / 165) ** 2 + ((z + 1080) / 105) ** 2 < 0.82
for (cx, cz) in [(1560, -1105), (1420, -1115), (1500, -1150)]:
    for m, n, r in [('A22_campfire', 1, 3), ('A82_bench_wood', 4, 9), ('E22_sled', 3, 12), ('A74_crate_large', 3, 10), ('A73_crate_small', 4, 10), ('A71_barrel', 4, 10), ('A87_bucket', 6, 12),
                    ('G17_net_rack', 2, 12), ('A90_firewood_stack', 2, 8), ('A17_lamp_wood_rustic', 3, 14), ('E25_snow_drift', 3, 16)]:
        P.cluster(cx, cz, [m], 'IceCamp2', n=n, radius=r)
put_many(P, ['G09_fishing_boat_2', 'G08_fishing_boat_1', 'G10_rowboat'], 5, BB, 'FrozenBoats', ice, scale=(0.8, 0.95), gap=14, block=True)
put_many(P, ['E16_snowy_rock_2', 'E15_snowy_rock_1', 'A60_boulder_1'], 14, BB, 'IceRocks', ice, scale=(1.2, 2.0), gap=8, block=True)
put_many(P, ['E26_icicle_cluster'], 14, BB, 'IceRocks', ice, scale=(1.4, 2.2), gap=6)
put_many(P, ['E12_snowy_pine_1', 'E13_snowy_pine_2', 'E14_snowy_pine_3'], 16, BB, 'RimPines', lambda x, z: 1340 <= x <= 1650 and -1190 <= z <= -1170 or 1330 <= x <= 1350, scale=(0.9, 1.2), gap=8, block=True)
# the 30-stud step along the south rim: rock wall, frozen fall, icicles
for x in range(1400, 1620, 17):
    z = -985 + P.rng.uniform(-3, 3)
    P.put(P.rng.choice(['A63_cliff_2', 'A62_cliff_1', 'A64_cliff_3', 'E16_snowy_rock_2']), x, z, P.rng.choice([0, 90, 180, 270]), 'RimWall', block=True, pad=-2.0, scale=P.rng.uniform(1.0, 1.5), streets=False)
P.put('A110_waterfall_rocks', 1520, -982, 0, 'RimWall', block=True, pad=0, scale=1.6, streets=False)
for x in range(1405, 1620, 14):
    P.put('E26_icicle_cluster', x + P.rng.uniform(-3, 3), -990, 0, 'RimWall', block=False, check=False, scale=P.rng.uniform(1.4, 2.4))
report['v3f_alpine'] = save(P, 'v3f_alpine')

# extra part-built items (igloos, shanties, holes) are appended to parts_plan.json
pp = json.load(open(RB + r'\parts_plan.json'))
for _k, _n in (('igloos', 12), ('shanties', 5), ('fishing_holes', 8)):   # idempotent: always start from the v3 originals
    pp[_k] = pp[_k][:_n]
rng = random.Random(77)
used = [(i['x'], i['z']) for k in ('igloos', 'shanties', 'fishing_holes') for i in pp.get(k, [])]
def free(x, z, d):
    return all(math.hypot(x - a, z - b) > d for a, b in used)
n0 = {k: len(pp[k]) for k in ('igloos', 'shanties', 'fishing_holes')}
tries = 0
while len(pp['shanties']) < n0['shanties'] + 8 and tries < 600:
    tries += 1
    x, z = rng.uniform(1360, 1620), rng.uniform(-1165, -1010)
    if ((x - 1490) / 165) ** 2 + ((z + 1080) / 105) ** 2 < 0.7 and free(x, z, 36):
        pp['shanties'].append({'x': round(x), 'z': round(z), 'y': 152, 'rot': rng.choice([0, 90, 180, 270]) + rng.randint(-20, 20)}); used.append((x, z))
        for k in range(2):
            a = rng.uniform(0, 6.28)
            hx, hz = x + math.cos(a) * rng.uniform(9, 14), z + math.sin(a) * rng.uniform(9, 14)
            pp['fishing_holes'].append({'x': round(hx), 'z': round(hz), 'y': 152}); used.append((hx, hz))
tries = 0
while len(pp['fishing_holes']) < n0['fishing_holes'] + 22 and tries < 600:
    tries += 1
    x, z = rng.uniform(1360, 1620), rng.uniform(-1165, -1010)
    if ((x - 1490) / 165) ** 2 + ((z + 1080) / 105) ** 2 < 0.75 and free(x, z, 14):
        pp['fishing_holes'].append({'x': round(x), 'z': round(z), 'y': 152}); used.append((x, z))
alp_blocks = [obb(i['x'], i['z'], CAT[i['model']]['size_x'] / 2, CAT[i['model']]['size_z'] / 2, i.get('rot', 0)) for i in EXIST['v3_alpine'] if i['model'] in CAT and 1380 < i['x'] < 1830 and -1010 < i['z'] < -690]
tries = 0
while len(pp['igloos']) < n0['igloos'] + 8 and tries < 1500:
    tries += 1
    x, z = rng.uniform(1400, 1790), rng.uniform(-960, -700)
    box = obb(x, z, 12, 12, 0)
    if free(x, z, 30) and not any(obb_overlap(box, b, 2) for b in alp_blocks) and not any(obb_overlap(box, b, 2) for b in P.sblocks):
        pp['igloos'].append({'x': round(x), 'z': round(z), 'y': 122, 'rot': rng.randint(0, 359), 'd': rng.choice([14, 16, 18])}); used.append((x, z))
        alp_blocks.append(box)
json.dump(pp, open(RB + r'\parts_plan.json', 'w'))
print('parts_plan now', {k: len(pp[k]) for k in ('huts', 'igloos', 'shanties', 'fishing_holes')})

# ============================================================ E) elf valley (v3f_elf)
P = Plan('v3f_elf', seed=4105)
BB = (-2000, -1150, -860, 80)
seed(P, BB)
seed_streets(P, BB, extra=2.5)
for (z0, z1) in [(-474, -378)]:                      # rope bridge chain between treehouses 1 and 2
    for z in (-474, -426, -378):
        P.put('F08_rope_bridge_long', -1776, z, 90, 'Bridges', block=False, check=False, yo=22)
for (cx, cz, tx, tz) in [(-1500, -526, -1560, -470), (-1344, -356, -1445, -420)]:
    d = math.hypot(tx - cx, tz - cz)
    n = max(1, int(d // 16))
    for i in range(n):
        t = (i + 0.5) / n
        P.put('F07_rope_bridge_short', cx + (tx - cx) * t, cz + (tz - cz) * t, face_rot(tz - cz, -(tx - cx)) if False else math.degrees(math.atan2(tx - cx, tz - cz)) + 90, 'Bridges', block=False, check=False, yo=20)
valley = lambda x, z: -1960 <= x <= -1180 and -830 <= z <= 60
put_many(P, ['F14_jungle_tree_1', 'F15_jungle_tree_2'], 14, BB, 'Canopy2', valley, scale=(0.9, 1.05), gap=6, block=True)
put_many(P, ['F16_jungle_palm'], 36, BB, 'Canopy2', valley, scale=(0.9, 1.3), gap=4, block=True)
put_many(P, ['F21_giant_fern', 'F22_giant_leaf_plant'], 70, BB, 'Under2', valley, scale=(0.9, 1.4), gap=2)
put_many(P, ['F23_glow_mushroom_1', 'F24_glow_mushroom_2'], 70, BB, 'Glow2', valley, scale=(0.8, 1.5), gap=2)
put_many(P, ['F25_glow_flower_1', 'F26_glow_flower_2'], 90, BB, 'Glow2', valley, scale=(0.9, 1.5), gap=1.5)
put_many(P, ['F34_crystal_cluster'], 14, BB, 'Glow2', valley, scale=(0.9, 1.6), gap=8)
put_many(P, ['F29_lotus'], 16, BB, 'Glow2', lambda x, z: -1640 <= x <= -1480 and -140 <= z <= -20, scale=(1.0, 1.5), gap=3)
for st in STREETS:                                    # lanterns along every elf path
    if not st['name'].startswith('v3_elf'):
        continue
    pts = st['pts']
    acc = 0
    for i in range(1, len(pts)):
        a, b = pts[i - 1], pts[i]
        acc += math.hypot(b[0] - a[0], b[1] - a[1])
        if acc >= 24:
            acc = 0
            d = (b[0] - a[0], b[1] - a[1]); L = math.hypot(*d) or 1
            nx, nz = -d[1] / L, d[0] / L
            side = 1 if (i // 1) % 2 == 0 else -1
            off = st['w'] / 2 + 2.2
            P.put('F28_elf_standing_lantern', a[0] + nx * off * side, a[1] + nz * off * side, 0, 'PathLights', block=False, check=False)
report['v3f_elf'] = save(P, 'v3f_elf')

# ============================================================ F) harbour quay + boats (v3f_harbour)
P = Plan('v3f_harbour', seed=4106)
BB = (-640, -150, 1770, 1900)
seed(P, BB)
seed_streets(P, BB)
land = lambda x, z: -630 <= x <= -160 and (1778 <= z <= 1800 or 1816 <= z <= 1832)
for m, n, g in [('G17_net_rack', 7, 3), ('G18_rope_coil', 10, 2), ('G21_lobster_trap', 14, 1.5), ('G33_cargo_pallet', 9, 2), ('G15_fish_market_stall', 4, 5), ('G19_anchor', 3, 5),
                ('A71_barrel', 14, 1.5), ('A73_crate_small', 12, 1.5), ('A74_crate_large', 7, 2), ('A75_crate_stack', 4, 4), ('A77_sack_pile', 6, 2), ('A87_bucket', 8, 1)]:
    put_many(P, [m], n, BB, 'Quay2', land, scale=(0.95, 1.1), gap=g, block=True)
sea = lambda x, z: -640 <= x <= -160 and 1835 <= z <= 1895
put_many(P, ['G08_fishing_boat_1', 'G09_fishing_boat_2'], 4, BB, 'Boats2', sea, scale=(0.95, 1.05), gap=20, block=True)
put_many(P, ['G10_rowboat'], 5, BB, 'Boats2', sea, scale=(0.95, 1.1), gap=10, block=True)
put_many(P, ['G20_buoy'], 9, BB, 'Boats2', lambda x, z: -640 <= x <= -160 and 1845 <= z <= 1895, scale=(1.0, 1.1), gap=12)
report['v3f_harbour'] = save(P, 'v3f_harbour')

# ============================================================ G) rusty town debris (v3f_rusty)
P = Plan('v3f_rusty', seed=4107)
BB = (1020, 1480, 970, 1300)
seed(P, BB)
for _h in json.load(open(RB + r'\parts_plan.json'))['huts']:      # part-built huts are not in any plan file
    P.blocks.append(obb(_h['x'], _h['z'], _h['w'] / 2 + 2, _h['d'] / 2 + 2, _h.get('rot', 0)))
seed_streets(P, BB, extra=2.5)
main = next(s for s in STREETS if s['name'] == 'v3_rusty_0')
mp = main['pts']
def along(i0, i1, off0, off1):
    i = P.rng.randint(i0, i1 - 1)
    a, b = mp[i], mp[i + 1]
    t = P.rng.random()
    x, z = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
    d = (b[0] - a[0], b[1] - a[1]); L = math.hypot(*d) or 1
    nx, nz = -d[1] / L, d[0] / L
    side = P.rng.choice([-1, 1]); off = P.rng.uniform(off0, off1)
    return x + nx * off * side, z + nz * off * side
for m, n, o0, o1, blk in [('D30_scrap_pile', 16, 8, 30, True), ('D31_rusted_cart', 7, 7, 20, True), ('D32_broken_barrel', 18, 6, 22, False), ('D35_collapsed_wall', 6, 12, 36, True),
                          ('D29_patched_tent', 7, 14, 40, True), ('D36_old_well_pump', 2, 10, 24, True), ('A35_dead_tree_1', 8, 16, 46, True), ('A36_dead_tree_2', 8, 14, 44, True),
                          ('A70_branch_pile', 10, 6, 28, False), ('A58_rock_medium_1', 12, 8, 36, False), ('D37_crooked_lamp', 10, 5, 8, False)]:
    k = tries = 0
    while k < n and tries < n * 50:
        tries += 1
        x, z = along(0, len(mp) - 1, o0, o1)
        if P.put(m, x, z, P.rng.uniform(0, 360), 'Debris3', block=blk, pad=1.5, scale=P.rng.uniform(0.9, 1.15)):
            k += 1
report['v3f_rusty'] = save(P, 'v3f_rusty')

# ============================================================ H) countryside (v3f_country)
P = Plan('v3f_country', seed=4108)
BB = (440, 760, -400, -180)
seed(P, BB)
seed_streets(P, BB)
for r in W.get('roads', []):                         # keep off carved roads
    pts = r['pts'] if isinstance(r, dict) else r
    half = (r.get('w', 12) if isinstance(r, dict) else 12) / 2 + 6
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        if L < 0.1:
            continue
        d = ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
        P.sblocks.append(obb((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, L / 2 + 1, half, face_rot(-d[1], d[0])))
farm_pts = []
for (px, pz) in [(500, -340), (545, -340), (500, -300), (545, -300), (590, -320), (640, -250), (690, -250)]:
    if P.put('H07_wheat_crop_rows', px, pz, 0, 'Farm3', block=True, pad=0.5):
        farm_pts.append((px, pz))
        P.put('H08_vegetable_crop_rows', px, pz + 13, 0, 'Farm3', block=True, pad=0.5)
        for dx in (-10, 10):
            P.put('A101_fence_rail', px + dx, pz - 8, 0, 'Farm3', block=False, check=False)
            P.put('A101_fence_rail', px + dx, pz + 21, 0, 'Farm3', block=False, check=False)
for (x, z) in [(520, -320), (610, -300), (665, -235)]:
    P.put('H09_scarecrow', x, z, P.rng.uniform(0, 360), 'Farm3', block=False, check=False)
P.put('E08_barn', 580, -245, 180, 'Farm3', block=True, pad=2.0)
P.put('H10_working_windmill', 470, -250, 90, 'Farm3', block=True, pad=2.0)
P.put('A98_well', 560, -265, 0, 'Farm3', block=True, pad=1.0)
for m, n in [('A78_hay_bale', 10), ('A80_wagon', 2), ('A79_hand_cart', 1), ('A71_barrel', 5), ('A77_sack_pile', 3)]:
    P.cluster(585, -222, [m], 'Farm3', n=n, radius=20)
P.put('H01_roadside_shrine', 455, -190, 20, 'Landmarks3', block=True, pad=1.0)
P.put('H01_roadside_shrine', 740, -390, 200, 'Landmarks3', block=True, pad=1.0)
P.put('H04_ruins_2', 700, -330, 40, 'Landmarks3', block=True, pad=2.0)
put_many(P, ['A26_oak_3', 'A25_oak_2', 'A28_birch_2', 'A27_birch_1', 'A32_maple_autumn', 'A24_oak_1'], 40, BB, 'Trees3', scale=(0.9, 1.25), gap=6, block=True)
put_many(P, ['A38_bush_1', 'A39_bush_2', 'A40_bush_3'], 30, BB, 'Trees3', scale=(0.9, 1.3), gap=2)
put_many(P, ['A43_flowers_red', 'A44_flowers_yellow', 'A46_flowers_white', 'A47_flowers_blue', 'A45_flowers_purple'], 60, BB, 'Flowers3', scale=(0.9, 1.5), gap=0.8)
report['v3f_country'] = save(P, 'v3f_country')

print('TOTAL new items', sum(report.values()))
json.dump(report, open(RB + r'\fixes3_report.json', 'w'))
