"""Countryside dressing outside the towns -> mapplan/v2_country.json"""
import json, math, random
from layout_lib import Plan, obb, norm, face_rot, Polyline, CAT
import world as W

rng = random.Random(77)
WORLD = json.load(open(r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\world.json'))
P = Plan('v3_country', seed=77)

# ------------------------------------------------------------ exclusion helpers
BUCK = 60
road_pts = {}
def addpts(pts, w):
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        n = max(1, int(L / 8))
        for k in range(n + 1):
            x = a[0] + (b[0] - a[0]) * k / n; z = a[1] + (b[1] - a[1]) * k / n
            road_pts.setdefault((int(x // BUCK), int(z // BUCK)), []).append((x, z, w))
for r in WORLD['roads']:
    addpts(r['pts'], r['w'])
for r in WORLD.get('streets', []):
    addpts(r['pts'], r['w'])
for r in WORLD['rivers']:
    addpts(r['pts'], r['w'] + 6)

def road_dist(x, z):
    bx, bz = int(x // BUCK), int(z // BUCK)
    best = 1e9
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            for (px, pz, w) in road_pts.get((bx + i, bz + j), []):
                d = math.hypot(x - px, z - pz) - w
                if d < best:
                    best = d
    return best

def in_lake(x, z, grow=1.25):
    for L in WORLD['lakes']:
        if math.hypot((x - L['cx']) / L['rx'], (z - L['cz']) / L['rz']) < grow:
            return True
    return False

def pad_w(x, z):
    m = 0
    for p in W.PADS:
        if p['name'] == 'town1ring':
            continue
        m = max(m, W.pad_mask(p, x, z))
    return m

def slope(x, z):
    e = 6
    gx = (W.ground_no_noise(x + e, z) - W.ground_no_noise(x - e, z)) / (2 * e)
    gz = (W.ground_no_noise(x, z + e) - W.ground_no_noise(x, z - e)) / (2 * e)
    return math.hypot(gx, gz)

def in_mtn(x, z):
    return W.ground_no_noise(x, z) > 235

def biome(x, z):
    best, bw = 'plains', 0.3
    for b in WORLD['biomes']:
        d = math.hypot(x - b[1], z - b[2])
        wt = 1 - W.smoothstep(0.5 * b[3], b[3], d)
        if wt > bw:
            best, bw = b[0], wt
    return best

def ok(x, z, road_gap=8, allow_steep=0.55):
    if abs(x) > 2300 or abs(z) > 2500:
        return False
    if -360 <= x <= 360 and -585 <= z <= 345:
        return False
    if pad_w(x, z) > 0.25:
        return False
    if in_mtn(x, z):
        return False
    g = W.ground_no_noise(x, z)
    if g < 2.5:
        return False
    if in_lake(x, z):
        return False
    if road_dist(x, z) < road_gap:
        return False
    if slope(x, z) > allow_steep:
        return False
    return True

# ------------------------------------------------------------ vegetation sets
SETS = {
    'forest': (['A24_oak_1', 'A25_oak_2', 'A27_birch_1', 'A28_birch_2', 'A29_pine_1', 'A30_pine_2', 'A32_maple_autumn', 'A26_oak_3'],
               {'A24_oak_1': 2, 'A25_oak_2': 2, 'A27_birch_1': 1.5, 'A28_birch_2': 1.5, 'A29_pine_1': 1, 'A30_pine_2': 1, 'A32_maple_autumn': 1, 'A26_oak_3': 1}),
    'plains': (['A24_oak_1', 'A25_oak_2', 'A26_oak_3', 'A27_birch_1', 'A32_maple_autumn', 'A34_fruit_tree', 'A33_willow'],
               {'A24_oak_1': 2, 'A25_oak_2': 2, 'A26_oak_3': 1.5, 'A27_birch_1': 1, 'A32_maple_autumn': 1, 'A34_fruit_tree': 0.6, 'A33_willow': 0.4}),
    'jungle': (['F14_jungle_tree_1', 'F15_jungle_tree_2', 'F16_jungle_palm', 'A33_willow'],
               {'F14_jungle_tree_1': 1, 'F15_jungle_tree_2': 1.3, 'F16_jungle_palm': 2.5, 'A33_willow': 0.6}),
    'alpine': (['A29_pine_1', 'A30_pine_2', 'A31_pine_3', 'E12_snowy_pine_1', 'E13_snowy_pine_2'],
               {'A29_pine_1': 2, 'A30_pine_2': 2, 'A31_pine_3': 1.5, 'E12_snowy_pine_1': 0.6, 'E13_snowy_pine_2': 0.6}),
    'dry': (['A35_dead_tree_1', 'A36_dead_tree_2', 'A26_oak_3'], {'A35_dead_tree_1': 2, 'A36_dead_tree_2': 2, 'A26_oak_3': 0.3}),
}
UNDER = {
    'forest': ['A38_bush_1', 'A39_bush_2', 'A51_fern', 'A67_fallen_log', 'A68_stump_1', 'A54_mushroom_cluster', 'A58_rock_medium_1', 'A50_tall_grass_2', 'A70_branch_pile'],
    'plains': ['A38_bush_1', 'A40_bush_3', 'A43_flowers_red', 'A44_flowers_yellow', 'A46_flowers_white', 'A47_flowers_blue', 'A49_tall_grass_1', 'A56_rock_small_1', 'A57_rock_small_2'],
    'jungle': ['F21_giant_fern', 'F22_giant_leaf_plant', 'A51_fern', 'A39_bush_2', 'F23_glow_mushroom_1'],
    'alpine': ['E15_snowy_rock_1', 'E17_snowy_bush', 'A58_rock_medium_1', 'A31_pine_3', 'E18_edelweiss'],
    'dry': ['A56_rock_small_1', 'A58_rock_medium_1', 'A60_boulder_1', 'A49_tall_grass_1', 'D32_broken_barrel'],
}
DENS = {'forest': (26, 150), 'jungle': (20, 120), 'alpine': (14, 120), 'plains': (7, 210), 'dry': (4, 260)}   # trees per cluster, cluster spacing


def forests():
    cells = 0
    for gx in range(-3300, 3301, 90):
        for gz in range(-3300, 3301, 90):
            x = gx + rng.uniform(-40, 40); z = gz + rng.uniform(-40, 40)
            b = biome(x, z)
            if b == 'alpine' and W.ground_no_noise(x, z) < 35:
                b = 'plains'
            n, spacing = DENS[b]
            if rng.random() > (90.0 / spacing) ** 2 * (1.0 if b != 'plains' else 0.55):
                continue
            if not ok(x, z, road_gap=14):
                continue
            cells += 1
            models, wts = SETS[b]
            k = 0
            radius = 30 + n * 2.2
            for _ in range(n * 4):
                if k >= n:
                    break
                tx = x + rng.gauss(0, radius * 0.5); tz = z + rng.gauss(0, radius * 0.5)
                if not ok(tx, tz, road_gap=9, allow_steep=0.7):
                    continue
                m = rng.choices(models, [wts[q] for q in models])[0]
                if P.put(m, tx, tz, rng.uniform(0, 360), f'Trees_{b}', block=False, pad=1.5, scale=rng.uniform(0.75, 1.2)):
                    k += 1
            for _ in range(int(n * 1.1)):
                ux = x + rng.gauss(0, radius * 0.6); uz = z + rng.gauss(0, radius * 0.6)
                if ok(ux, uz, road_gap=4, allow_steep=0.7):
                    P.put(rng.choice(UNDER[b]), ux, uz, rng.uniform(0, 360), f'Under_{b}', block=False, pad=0.4, scale=rng.uniform(0.8, 1.3))
    return cells


def farm(cx, cz, rot, cols=4, rows=3, name='Farm'):
    t = math.radians(rot)
    ux, uz = (math.cos(t), -math.sin(t)), (math.sin(t), math.cos(t))
    def pt(a, b):
        return cx + ux[0] * a + uz[0] * b, cz + ux[1] * a + uz[1] * b
    fw, fd = 20, 16
    for i in range(cols):
        for j in range(rows):
            x, z = pt((i - (cols - 1) / 2) * (fw + 4), (j - (rows - 1) / 2) * (fd + 4))
            P.put('H07_wheat_crop_rows' if (i + j) % 3 else 'H08_vegetable_crop_rows', x, z, rot, name, block=True, pad=0.5, check=False)
    W2 = cols * (fw + 4) / 2 + 4; D2 = rows * (fd + 4) / 2 + 4
    P.line_of('A101_fence_rail', pt(-W2, D2), pt(-6, D2), name, block=False)
    P.line_of('A101_fence_rail', pt(6, D2), pt(W2, D2), name, block=False)
    P.put('A104_wooden_gate', *pt(0, D2), rot, name, block=False, check=False)
    P.line_of('A101_fence_rail', pt(W2, D2), pt(W2, -D2), name, block=False)
    P.line_of('A101_fence_rail', pt(W2, -D2), pt(-W2, -D2), name, block=False)
    P.line_of('A101_fence_rail', pt(-W2, -D2), pt(-W2, D2), name, block=False)
    P.put('H09_scarecrow', *pt(4, 2), rot + 20, name, block=False, check=False)
    P.put('H10_working_windmill', *pt(-W2 - 30, -6), rot + 90, name, check=False)
    for k in range(5):
        P.put('A78_hay_bale', *pt(W2 + 10 + rng.uniform(-3, 3), -D2 + 6 + k * 7), rng.uniform(0, 360), name, block=False, check=False)
    P.put('A80_wagon', *pt(W2 + 14, D2 - 6), rot + 80, name, block=False, check=False)
    P.put('A97_water_trough', *pt(-W2 - 12, D2 - 4), rot, name, block=False, check=False)
    P.put('A98_well', *pt(-W2 - 14, D2 + 10), rot, name, check=False)
    P.put('A81_wheelbarrow', *pt(W2 + 6, D2 + 4), rot + 30, name, block=False, check=False)


def road_furniture():
    roads = {r['name']: r for r in WORLD['roads']}
    for name, r in roads.items():
        pts = [(p[0], p[1]) for p in r['pts']]
        line = Polyline(pts)
        w = r['w']
        main = name not in ('ring_east', 'ring_west')
        # milestones
        s = 300
        while s < line.L - 150:
            (px, pz), d = line.at(s)
            R = (-d[1], d[0])
            P.put('A14_milestone', px + R[0] * (w + 2.5), pz + R[1] * (w + 2.5), face_rot(-R[0], -R[1]), 'Roadside', block=False, check=False)
            s += 420
        # rustic lamps near both ends of main roads
        if main:
            for (s0, s1) in ((15, 260), (max(0, line.L - 260), line.L - 15)):
                s = s0; k = 0
                while s <= s1:
                    (px, pz), d = line.at(s)
                    R = (-d[1], d[0]); sd = 1 if k % 2 == 0 else -1
                    x, z = px + R[0] * sd * (w + 2.2), pz + R[1] * sd * (w + 2.2)
                    if not (-458 <= x <= 458 and -781 <= z <= 446):
                        P.put('A17_lamp_wood_rustic', x, z, face_rot(-R[0] * sd, -R[1] * sd), 'RoadLamps', block=False, check=False)
                    s += 46; k += 1
        # bushes / flowers / rocks along road edges
        s = 20
        while s < line.L - 20:
            (px, pz), d = line.at(s)
            R = (-d[1], d[0])
            for sd in (1, -1):
                if rng.random() < 0.35:
                    off = w + rng.uniform(4, 12)
                    x, z = px + R[0] * sd * off, pz + R[1] * sd * off
                    if ok(x, z, road_gap=2.5, allow_steep=0.7):
                        b = biome(x, z)
                        P.put(rng.choice(UNDER[b]), x, z, rng.uniform(0, 360), 'Roadside', block=False, pad=0.3, scale=rng.uniform(0.8, 1.2))
            s += 14


def arch(name, s_from_end, rot_extra=0):
    r = [q for q in WORLD['roads'] if q['name'] == name][0]
    line = Polyline([(p[0], p[1]) for p in r['pts']])
    (px, pz), d = line.at(line.L - s_from_end)
    # front faces back toward the traveller (opposite to travel direction)
    P.put('H12_region_entrance_arch', px, pz, face_rot(-d[0], -d[1]) + rot_extra, 'Arches', check=False)
    for sd in (1, -1):
        R = (-d[1], d[0])
        P.put('A21_brazier', px + R[0] * sd * 17 - d[0] * 4, pz + R[1] * sd * 17 - d[1] * 4, 0, 'Arches', block=False, check=False)


def signposts():
    for (x, z, r) in ((22, 470, 120), (16, -575, 0), (345, -36, 90), (-345, -36, 270), (16, 345, 180), (1515, -540, 290), (-1545, -110, 100), (1390, 930, 330), (-460, 1392, 180)):
        P.put('A13_signpost', x, z, r, 'Signposts', block=False, check=False)


def landmarks():
    spots = [
        ('H03_ruins_1', -760, -985, 20), ('H04_ruins_2', -720, -950, 110), ('H11_standing_stone_circle', 760, 470, 0),
        ('H02_abandoned_watchtower', 600, -700, 35), ('H05_traveller_campsite', -900, -170, 200), ('H05_traveller_campsite', 1640, 120, 90),
        ('H06_wagon_wreck', 760, 860, 140), ('H01_roadside_shrine', -470, -40, 90), ('H01_roadside_shrine', 520, -95, 250),
        ('H01_roadside_shrine', 40, -800, 180), ('H01_roadside_shrine', -90, 780, 20), ('H03_ruins_1', 520, -1150, 300),
        ('H10_working_windmill', -1000, 1350, 30), ('H02_abandoned_watchtower', -880, -1660, 0), ('H11_standing_stone_circle', -900, 300, 0),
        ('A65_rock_arch', -1050, 700, 40), ('A65_rock_arch', 1450, 1600, 120), ('H06_wagon_wreck', -1250, 600, 60),
        ('H02_abandoned_watchtower', 1700, 300, 10), ('H03_ruins_1', 120, 1450, 80), ('H11_standing_stone_circle', -330, -950, 0),
    ]
    for (m, x, z, r) in spots:
        if ok(x, z, road_gap=6, allow_steep=0.6):
            P.put(m, x, z, r, 'Landmarks', pad=2)
        else:
            for _ in range(40):
                x2, z2 = x + rng.uniform(-80, 80), z + rng.uniform(-80, 80)
                if ok(x2, z2, road_gap=6, allow_steep=0.6) and P.put(m, x2, z2, r, 'Landmarks', pad=2):
                    break
    # campfires and crates at campsites
    for it in [i for i in P.items if i['model'] == 'H05_traveller_campsite']:
        P.cluster(it['x'] + 12, it['z'] + 4, ['A71_barrel', 'A73_crate_small', 'A76_sack', 'A90_firewood_stack'], 'Landmarks', n=4, radius=5)


def lakes_and_coast():
    for L in WORLD['lakes']:
        if L['level'] > 50:
            continue
        for k in range(int(L['rx'] / 5)):
            a = rng.uniform(0, math.tau)
            rr = rng.uniform(1.02, 1.18)
            x, z = L['cx'] + math.cos(a) * L['rx'] * rr, L['cz'] + math.sin(a) * L['rz'] * rr
            P.put(rng.choice(['A52_reeds', 'A52_reeds', 'A58_rock_medium_1', 'A49_tall_grass_1']), x, z, rng.uniform(0, 360), 'Lakeside', block=False, pad=0.2, check=False)
        for k in range(int(L['rx'] / 12)):
            a = rng.uniform(0, math.tau); rr = rng.uniform(0.55, 0.9)
            P.put('A53_lily_pads', L['cx'] + math.cos(a) * L['rx'] * rr, L['cz'] + math.sin(a) * L['rz'] * rr, rng.uniform(0, 360), 'Lakeside', block=False, check=False)
        P.put('A33_willow', L['cx'] + L['rx'] * 1.3, L['cz'] - L['rz'] * 0.4, 30, 'Lakeside', check=False)
        P.put('A82_bench_wood', L['cx'] - L['rx'] * 1.25, L['cz'] + L['rz'] * 0.2, 90, 'Lakeside', block=False, check=False)
    # coastal boulders
    for k in range(200):
        a = rng.uniform(0, math.tau)
        for rr in range(2250, 1500, -25):
            x, z = math.cos(a) * rr, math.sin(a) * rr * (2480 / 2200 if math.sin(a) < 0 else 2000 / 2200)
            g = W.ground_no_noise(x, z)
            if 2.5 < g < 9:
                if not in_mtn(x, z) and pad_w(x, z) < 0.2:
                    P.put(rng.choice(['A60_boulder_1', 'A61_boulder_2', 'A62_cliff_1', 'A64_cliff_3', 'A58_rock_medium_1']), x, z, rng.uniform(0, 360), 'Coast', block=False, pad=1, scale=rng.uniform(0.8, 1.6))
                break


if __name__ == '__main__':
    # farms first (they block space), then landmarks, roads, forests
    farm(-560, 620, 20, name='Farm_West')
    farm(270, 770, -10, name='Farm_East')
    farm(-560, 1010, 25, cols=3, rows=3, name='Farm_South')
    farm(-380, -760, 5, cols=3, rows=2, name='Farm_North')
    for name, s in (('north', 90), ('west', 70), ('south', 90), ('southeast', 90), ('east', 560)):
        arch(name, s)
    signposts()
    landmarks()
    road_furniture()
    lakes_and_coast()
    cells = forests()
    P.save(r'C:\Users\Nitro\.kiro\crew\workspace\town\mapplan\v3_country.json')
    import collections
    c = collections.Counter(i['group'] for i in P.items)
    print('clusters', cells, 'items', len(P.items))
    print(c.most_common())
