"""Environment generator v4. Reads the REAL terrain (rebuild/v4/terrain_map.json exported from Studio), world.json (v4) and the footprints of
existing models (rebuild/v4/occ_*.json), and writes placement plans for dense forests, undergrowth, rocks and set pieces.
Outputs (mapplan/): v4_forest.json, v4_under.json, v4_rocks.json, v4_pieces.json, v4_shore.json
Replayable: python env_plan.py   (then place each plan with rebuild/v4/build_v4.ps1)
"""
import json, math, random, os, glob, collections, sys

RB = r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild'
V4 = RB + r'\v4'
MP = r'C:\Users\Nitro\.kiro\crew\workspace\town\mapplan'
LIB = r'C:\Users\Nitro\.kiro\crew\workspace\town\library'
rng = random.Random(4242)

WORLD = json.load(open(RB + r'\world.json'))
TM = json.load(open(V4 + r'\terrain_map.json'))
IDS = set()
import csv
for row in csv.DictReader(open(r'C:\Users\Nitro\.kiro\crew\workspace\town\asset_ids.csv', encoding='utf-8-sig')):
    if row.get('asset_id'):
        IDS.add(row['name'])

# ------------------------------------------------------------------ terrain grid
X0, X1, Z0, Z1, STEP = TM['x0'], TM['x1'], TM['z0'], TM['z1'], TM['step']
NX = (X1 - X0) // STEP + 1
ROWS = TM['rows']
NZ = len(ROWS)
HG = [[0.0] * NX for _ in range(NZ)]
MG = [[' '] * NX for _ in range(NZ)]
WG = [[None] * NX for _ in range(NZ)]
for j, row in enumerate(ROWS):
    for i in range(NX):
        c = row[i * 5:i * 5 + 5]
        HG[j][i] = int(c[0:2], 36) - 100
        MG[j][i] = c[2]
        WG[j][i] = None if c[3:5] == '--' else int(c[3:5], 36) - 100


def clampi(v, lo, hi):
    return lo if v < lo else (hi if v > hi else v)


def H(x, z):
    fi, fj = (x - X0) / STEP, (z - Z0) / STEP
    i0, j0 = int(math.floor(fi)), int(math.floor(fj))
    ti, tj = fi - i0, fj - j0
    def g(i, j):
        return HG[clampi(j, 0, NZ - 1)][clampi(i, 0, NX - 1)]
    a = g(i0, j0) * (1 - ti) + g(i0 + 1, j0) * ti
    b = g(i0, j0 + 1) * (1 - ti) + g(i0 + 1, j0 + 1) * ti
    return a * (1 - tj) + b * tj


def M(x, z):
    i, j = clampi(int(round((x - X0) / STEP)), 0, NX - 1), clampi(int(round((z - Z0) / STEP)), 0, NZ - 1)
    return MG[j][i]


def has_water(x, z):
    i, j = clampi(int(round((x - X0) / STEP)), 0, NX - 1), clampi(int(round((z - Z0) / STEP)), 0, NZ - 1)
    w = WG[j][i]
    return w is not None and w > HG[j][i] - 0.5


def slope(x, z):
    e = STEP
    gx = (H(x + e, z) - H(x - e, z)) / (2 * e)
    gz = (H(x, z + e) - H(x, z - e)) / (2 * e)
    return math.hypot(gx, gz)


def in_map(x, z):
    return X0 + STEP <= x <= X1 - STEP and Z0 + STEP <= z <= Z1 - STEP


# distance (studs) to the sea, by BFS over the grid
SEA = [[1e9] * NX for _ in range(NZ)]
dq = collections.deque()
for j in range(NZ):
    for i in range(NX):
        if WG[j][i] is not None and WG[j][i] <= 1 and HG[j][i] < -1:
            SEA[j][i] = 0.0
            dq.append((i, j))
while dq:
    i, j = dq.popleft()
    d = SEA[j][i] + STEP
    for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ni, nj = i + di, j + dj
        if 0 <= ni < NX and 0 <= nj < NZ and SEA[nj][ni] > d and d < 900:
            SEA[nj][ni] = d
            dq.append((ni, nj))


def sea_dist(x, z):
    i, j = clampi(int(round((x - X0) / STEP)), 0, NX - 1), clampi(int(round((z - Z0) / STEP)), 0, NZ - 1)
    return SEA[j][i]


# ------------------------------------------------------------------ noise
def _h(ix, iz, seed):
    n = (ix * 374761393 + iz * 668265263 + seed * 1442695041) & 0xffffffff
    n = ((n ^ (n >> 13)) * 1274126177) & 0xffffffff
    return ((n ^ (n >> 16)) & 0xffff) / 32767.5 - 1.0


def vnoise(x, z, seed=0):
    ix, iz = math.floor(x), math.floor(z)
    fx, fz = x - ix, z - iz
    sx, sz = fx * fx * (3 - 2 * fx), fz * fz * (3 - 2 * fz)
    a, b, c, d = _h(ix, iz, seed), _h(ix + 1, iz, seed), _h(ix, iz + 1, seed), _h(ix + 1, iz + 1, seed)
    top = a + (b - a) * sx
    bot = c + (d - c) * sx
    return top + (bot - top) * sz


def fbm(x, z, seed):
    return 0.6 * vnoise(x / 520, z / 520, seed) + 0.3 * vnoise(x / 240, z / 240, seed + 1) + 0.1 * vnoise(x / 110, z / 110, seed + 2)


def ss(a, b, x):
    if b == a:
        return 1.0 if x >= b else 0.0
    t = min(1.0, max(0.0, (x - a) / (b - a)))
    return t * t * (3 - 2 * t)


# ------------------------------------------------------------------ line indexes (roads/trails/streets, rivers) and lakes, pads
BUCK = 64


class LineIndex:
    def __init__(self):
        self.b = {}

    def add(self, pts, w):
        for i in range(len(pts) - 1):
            a, b = pts[i], pts[i + 1]
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            n = max(1, int(L / 10))
            for k in range(n + 1):
                x = a[0] + (b[0] - a[0]) * k / n
                z = a[1] + (b[1] - a[1]) * k / n
                self.b.setdefault((int(x // BUCK), int(z // BUCK)), []).append((x, z, w))

    def dist(self, x, z):
        bx, bz = int(x // BUCK), int(z // BUCK)
        best = 1e9
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                for (px, pz, w) in self.b.get((bx + i, bz + j), ()):
                    d = math.hypot(x - px, z - pz) - w
                    if d < best:
                        best = d
        return best


ROADS = LineIndex()
RIVERS = LineIndex()
for r in WORLD['roads']:
    ROADS.add(r['pts'], r['w'])
for r in WORLD.get('streets', []):
    ROADS.add(r['pts'], r['w'])
for r in WORLD['rivers']:
    RIVERS.add(r['pts'], r['w'] + 3)
LAKES = WORLD['lakes']


def in_lake(x, z, grow=1.3):
    for L in LAKES:
        if math.hypot((x - L['cx']) / L['rx'], (z - L['cz']) / L['rz']) < grow:
            return True
    return False


def pad_mask(p, x, z):
    if p['shape'] == 'rect':
        dx = abs(x - p['cx']) - p['hx']
        dz = abs(z - p['cz']) - p['hz']
        out = 0.0 if (dx <= 0 and dz <= 0) else math.hypot(max(dx, 0), max(dz, 0))
    else:
        nx = (x - p['cx']) / p['rx']
        nz = (z - p['cz']) / p['rz']
        out = max(0.0, (math.hypot(nx, nz) - 1) * min(p['rx'], p['rz']))
    return 1 - ss(0, p['e'], out)


TOWN_PADS = [p for p in WORLD['pads'] if p['name'] not in ('town1ring',)]


def town_mask(x, z):
    m = 0.0
    for p in TOWN_PADS:
        m = max(m, pad_mask(p, x, z))
    return m


def in_town1_zone(x, z):
    return -400 <= x <= 400 and -640 <= z <= 400


# existing footprints (towns, farms, landmarks...) exported from Studio
OCC = {}
OBUCK = 48


def load_occupancy():
    n = 0
    for f in glob.glob(V4 + r'\occ_*.json'):
        for (x, z, hx, hz) in json.load(open(f)):
            for bi in range(int((x - hx) // OBUCK), int((x + hx) // OBUCK) + 1):
                for bj in range(int((z - hz) // OBUCK), int((z + hz) // OBUCK) + 1):
                    OCC.setdefault((bi, bj), []).append((x, z, hx, hz))
            n += 1
    return n


def occupied(x, z, margin=4.0):
    for (cx, cz, hx, hz) in OCC.get((int(x // OBUCK), int(z // OBUCK)), ()):
        if abs(x - cx) <= hx + margin and abs(z - cz) <= hz + margin:
            return True
    return False


def biome(x, z):
    best, bw = 'forest', 0.3
    for name, bx, bz, br in WORLD['biomes']:
        d = math.hypot(x - bx, z - bz) + 60 * vnoise(x / 300, z / 300, 8)
        wgt = 1 - ss(0.5 * br, br, d)
        if wgt > bw:
            best, bw = name, wgt
    return best


# ------------------------------------------------------------------ species
def W(*pairs):
    return pairs


TREES = {
    'forest': W(('F01_01_tree_heartland_01', 0.45), ('F01_02_tree_heartland_02', 0.45), ('F01_03_tree_heartland_03', 0.3), ('F01_04_tree_heartland_04', 0.5),
                ('F01_05_tree_heartland_05', 0.45), ('F01_06_tree_heartland_06', 0.5), ('A24_oak_1', 1.4), ('A25_oak_2', 1.4), ('A26_oak_3', 1.2),
                ('A27_birch_1', 1.0), ('A28_birch_2', 1.0), ('A29_pine_1', 2.0), ('A30_pine_2', 1.8), ('A31_pine_3', 1.2), ('A32_maple_autumn', 0.5)),
    'plains': W(('F01_04_tree_heartland_04', 0.8), ('F01_06_tree_heartland_06', 0.8), ('A24_oak_1', 1.5), ('A25_oak_2', 1.5), ('A26_oak_3', 1.2),
                ('A27_birch_1', 1.0), ('A28_birch_2', 1.0), ('A32_maple_autumn', 0.7), ('A34_fruit_tree', 0.5), ('A33_willow', 0.3)),
    'alpine': W(('F02_01_tree_alpine_01', 0.6), ('F02_02_tree_alpine_02', 0.6), ('F02_03_tree_alpine_03', 0.9), ('F02_04_tree_alpine_04', 0.9),
                ('F02_05_tree_alpine_05', 0.9), ('A29_pine_1', 2.0), ('A30_pine_2', 2.0), ('A31_pine_3', 1.5), ('E12_snowy_pine_1', 0.6), ('E13_snowy_pine_2', 0.6)),
    'dry': W(('F03_01_tree_dry_01', 1.5), ('F03_02_tree_dry_02', 1.5), ('F03_03_tree_dry_03', 1.5), ('E05_01_dead_tree_01', 0.7), ('E05_02_dead_tree_02', 0.7),
             ('E05_03_dead_tree_03', 0.7), ('E05_04_dead_tree_04', 0.5), ('E05_05_dead_tree_05', 0.7), ('E05_06_dead_tree_06', 0.7), ('A35_dead_tree_1', 1.0), ('A36_dead_tree_2', 1.0)),
    'coastal': W(('F04_01_tree_coastal_01', 1.5), ('F04_02_tree_coastal_02', 1.5), ('F04_03_tree_coastal_03', 1.5), ('F04_04_tree_coastal_04', 1.2), ('A29_pine_1', 1.0), ('A30_pine_2', 1.0)),
}
UNDER = {
    'forest': W(('A38_bush_1', 1.2), ('A39_bush_2', 1.0), ('A40_bush_3', 0.8), ('F05_01_bush_round', 1.0), ('F05_03_bush_berry', 0.6), ('F05_04_bush_juniper', 0.6),
                ('A51_fern', 1.6), ('A49_tall_grass_1', 1.2), ('A50_tall_grass_2', 1.2), ('F06_20_shrooms_brown', 0.4), ('F06_21_shrooms_toadstool', 0.3),
                ('F06_01_log_mossy', 0.3), ('F06_04_stump_sawn', 0.3), ('F06_05_stump_rotten', 0.3), ('F06_19_flowers_wild', 0.5)),
    'plains': W(('A38_bush_1', 0.8), ('F05_01_bush_round', 0.8), ('F05_02_bush_flower', 0.8), ('F06_16_flowers_buttercup', 1.2), ('F06_17_flowers_cornflower', 1.2),
                ('F06_18_flowers_poppy', 1.0), ('F06_19_flowers_wild', 1.2), ('A49_tall_grass_1', 1.5), ('A50_tall_grass_2', 1.5), ('F05_09_grass_tall_a', 0.6), ('F05_10_grass_tall_b', 0.6)),
    'alpine': W(('A58_rock_medium_1', 0.8), ('F05_04_bush_juniper', 1.0), ('E15_01_boulder_01', 0.8), ('E15_03_boulder_03', 0.8), ('A50_tall_grass_2', 0.6), ('F06_10_scree_chips', 0.6)),
    'dry': W(('A56_rock_small_1', 1.0), ('A58_rock_medium_1', 0.8), ('E15_02_boulder_02', 0.8), ('A49_tall_grass_1', 0.8), ('F05_12_dune_tuft', 0.8), ('A60_boulder_1', 0.4)),
    'coastal': W(('F05_11_sea_oats', 1.2), ('F05_12_dune_tuft', 1.2), ('F05_04_bush_juniper', 0.8), ('A56_rock_small_1', 0.8), ('F06_12_gravel_patch', 0.4)),
}
ROCK_SMALL = ['A56_rock_small_1', 'A57_rock_small_2', 'E15_01_boulder_01', 'E15_02_boulder_02', 'E15_03_boulder_03', 'E15_04_boulder_04', 'E15_05_boulder_05',
              'F06_13_boulder_mossy', 'F06_14_slab_lichen', 'F06_15_split_rock']
ROCK_MED = ['A58_rock_medium_1', 'A59_rock_medium_2', 'A60_boulder_1', 'A61_boulder_2']
CLIFF_OLD = ['A62_cliff_1', 'A63_cliff_2', 'A64_cliff_3']
FORMATIONS = ['F07_01_rock_formation_01', 'F07_02_rock_formation_02', 'F07_03_rock_formation_03', 'F07_04_rock_formation_04', 'F07_05_rock_formation_05',
              'F07_06_rock_formation_06', 'F07_07_rock_formation_07', 'F07_08_rock_formation_08']
ROCKFACE = ['E13_%02d_rock_face_%02d' % (k, k) for k in range(1, 11)]
SNOW_PEAKS = ['R02_01_snow_peak_01', 'R02_02_snow_peak_02', 'R02_03_snow_peak_03', 'R02_04_snow_peak_04']
MESAS = ['R03_01_badlands_mesa_01', 'R03_02_badlands_mesa_02', 'R03_03_badlands_mesa_03', 'R03_04_badlands_mesa_04']
SEA_CLIFFS = ['R04_01_sea_cliff_01', 'R04_02_sea_cliff_02', 'R04_03_sea_cliff_03']
ISLETS = ['R01_01_islet_01', 'R01_02_islet_02', 'R01_03_islet_03', 'R01_04_islet_04']


def pick(lst):
    names = [n for n, w in lst if n in IDS]
    wts = [w for n, w in lst if n in IDS]
    if not names:
        return None
    return rng.choices(names, wts)[0]


def pickn(lst):
    c = [n for n in lst if n in IDS]
    return rng.choice(c) if c else None


OUT = collections.defaultdict(list)


def put(plan, model, x, z, rot, group, scale=None, yo=None):
    if model is None or model not in IDS:
        return False
    it = {'model': model, 'x': round(x, 1), 'z': round(z, 1), 'rot': round(rot % 360, 1), 'group': group}
    if scale and abs(scale - 1) > 1e-3:
        it['scale'] = round(scale, 2)
    if yo:
        it['y_offset'] = round(yo, 1)
    OUT[plan].append(it)
    return True


# ------------------------------------------------------------------ forest and undergrowth
def usable(x, z, road_gap, allow_snow=False):
    if not in_map(x, z) or in_town1_zone(x, z):
        return False
    h = H(x, z)
    if h < 3.0:
        return False
    m = M(x, z)
    if m in ('C', 'P', 'S', 'M', 'I', 'X', 'E', 'K'):
        return False
    if m == 'N' and not allow_snow:
        return False
    if has_water(x, z) or in_lake(x, z):
        return False
    if town_mask(x, z) > 0.12:
        return False
    if ROADS.dist(x, z) < road_gap or RIVERS.dist(x, z) < 6:
        return False
    if occupied(x, z, 3.0):
        return False
    return True


def forest_mask(x, z, b, h, sl):
    n = fbm(x, z, 11)
    bias = {'forest': 0.38, 'plains': -0.28, 'dry': -0.85, 'alpine': 0.18, 'coastal': 0.1}.get(b, 0.0)
    f = ss(-0.25, 0.25, n + bias)
    if vnoise(x / 160, z / 160, 21) > 0.58:
        f *= 0.2
    f *= 1 - ss(0.5, 0.95, sl)
    top = 300 if b == 'alpine' else 240
    f *= 1 - ss(top - 80, top, h)
    return f


def forests():
    cnt = collections.Counter()
    CELL = 28
    for gx in range(int(X0 + 30), int(X1 - 30), CELL):
        for gz in range(int(Z0 + 30), int(Z1 - 30), CELL):
            x = gx + rng.uniform(-11, 11)
            z = gz + rng.uniform(-11, 11)
            h = H(x, z)
            if h < 3.0 or h > 330:
                continue
            b = biome(x, z)
            if b == 'jungle':
                continue
            sd = sea_dist(x, z)
            if sd < 230 and h < 16 and b not in ('alpine', 'dry'):
                b = 'coastal'
            sl = slope(x, z)
            f = forest_mask(x, z, b, h, sl)
            if b == 'plains':
                f = max(f, 0.22 * (1 - ss(0.2, 0.5, sl)))
            if b == 'dry':
                f = max(f, 0.12 * (1 - ss(0.3, 0.6, sl)))
            if f <= 0.02 or rng.random() > (f ** 0.85) * 0.9:
                continue
            if not usable(x, z, 11, allow_snow=(b == 'alpine')):
                continue
            m = pick(TREES[b])
            sc = rng.uniform(0.85, 1.25) * (1.0 + 0.12 * f)
            if put('v4_forest', m, x, z, rng.uniform(0, 360), 'Trees_' + b, scale=sc, yo=-0.4):
                cnt[b] += 1
    return cnt


def undergrowth():
    cnt = collections.Counter()
    CELL = 20
    for gx in range(int(X0 + 30), int(X1 - 30), CELL):
        for gz in range(int(Z0 + 30), int(Z1 - 30), CELL):
            x = gx + rng.uniform(-6, 6)
            z = gz + rng.uniform(-6, 6)
            h = H(x, z)
            if h < 3.0 or h > 300:
                continue
            b = biome(x, z)
            if b == 'jungle':
                continue
            sd = sea_dist(x, z)
            if sd < 120 and h < 12 and b not in ('alpine', 'dry'):
                b = 'coastal'
            sl = slope(x, z)
            f = forest_mask(x, z, b, h, sl)
            p = {'forest': 0.06 + 0.30 * f, 'plains': 0.20 + 0.20 * f, 'alpine': 0.08 + 0.20 * f, 'dry': 0.10, 'coastal': 0.20}.get(b, 0.2)
            p *= 1 - ss(0.5, 0.9, sl)
            if rng.random() > p:
                continue
            if not usable(x, z, 4.0, allow_snow=(b == 'alpine')):
                continue
            m = pick(UNDER[b])
            if put('v4_under', m, x, z, rng.uniform(0, 360), 'Under_' + b, scale=rng.uniform(0.8, 1.35)):
                cnt[b] += 1
    return cnt


# ------------------------------------------------------------------ rocks, cliffs
def rocks():
    cnt = collections.Counter()
    CELL = 36
    for gx in range(int(X0 + 30), int(X1 - 30), CELL):
        for gz in range(int(Z0 + 30), int(Z1 - 30), CELL):
            x = gx + rng.uniform(-14, 14)
            z = gz + rng.uniform(-14, 14)
            h = H(x, z)
            if h < 2.5 or h > 420 or has_water(x, z) or in_town1_zone(x, z) or town_mask(x, z) > 0.12:
                continue
            sl = slope(x, z)
            m = M(x, z)
            if m in ('C', 'P'):
                continue
            if ROADS.dist(x, z) < 5 or occupied(x, z, 3.0):
                continue
            p = ss(0.28, 0.85, sl) * 0.85
            b = biome(x, z)
            if b == 'dry':
                p = max(p, 0.07)
            if h > 120:
                p = max(p, ss(0.2, 0.6, sl) * 0.7)
            if rng.random() > p:
                continue
            r = rng.random()
            if sl > 0.8 and r < 0.35:
                mdl, sc = pickn(CLIFF_OLD), rng.uniform(1.4, 2.8)
                grp = 'Cliffs'
            elif sl > 0.55 and r < 0.2:
                mdl, sc = pickn(FORMATIONS), rng.uniform(0.9, 1.9)
                grp = 'Formations'
            elif r < 0.5:
                mdl, sc = pickn(ROCK_MED), rng.uniform(0.9, 2.2)
                grp = 'Rocks'
            else:
                mdl, sc = pickn(ROCK_SMALL), rng.uniform(0.8, 2.0)
                grp = 'Rocks'
            if put('v4_rocks', mdl, x, z, rng.uniform(0, 360), grp, scale=sc, yo=-0.8):
                cnt[grp] += 1
    return cnt


# ------------------------------------------------------------------ set pieces
def local_peaks(minh, region, radius, limit):
    """Highest points in a region, greedy with spacing."""
    cand = []
    for j in range(2, NZ - 2):
        for i in range(2, NX - 2):
            h = HG[j][i]
            if h < minh:
                continue
            x, z = X0 + i * STEP, Z0 + j * STEP
            if not region(x, z):
                continue
            cand.append((h, x, z))
    cand.sort(reverse=True)
    out = []
    for h, x, z in cand:
        if all(math.hypot(x - ox, z - oz) > radius for _, ox, oz in out):
            out.append((h, x, z))
            if len(out) >= limit:
                break
    return out


def set_pieces(plan='v4_pieces', only=None):
    cnt = collections.Counter()
    want = lambda g: only is None or g in only
    # snow peaks crowning the north-east range
    for h, x, z in (local_peaks(250, lambda x, z: x > 700 and z < -400 and not in_town1_zone(x, z), 230, 30) if want('SnowPeaks') else []):
        if town_mask(x, z) > 0.1:
            continue
        sc = rng.uniform(1.1, 1.9)
        mdl = pickn(SNOW_PEAKS)
        if put(plan, mdl, x, z, rng.uniform(0, 360), 'SnowPeaks', scale=sc, yo=-0.42 * 150 * sc):
            cnt['SnowPeaks'] += 1
    # western / northern mountain crowns (rock faces and formations)
    for h, x, z in (local_peaks(170, lambda x, z: (x < -700 or z < -2300) and not in_town1_zone(x, z), 260, 26) if want('Crowns') else []):
        if town_mask(x, z) > 0.1 or biome(x, z) == 'jungle' and abs(x + 1560) < 500 and abs(z + 400) < 500:
            continue
        sc = rng.uniform(1.0, 1.7)
        if put(plan, pickn(FORMATIONS), x, z, rng.uniform(0, 360), 'Crowns', scale=sc, yo=-6):
            cnt['Crowns'] += 1
    # badlands mesas in the dry zone
    placed = []
    for _ in range(900 if want('Mesas') else 0):
        if len(placed) >= 44:
            break
        x, z = rng.uniform(900, 2800), rng.uniform(150, 1850)
        if biome(x, z) != 'dry' or not in_map(x, z):
            continue
        h = H(x, z)
        if h < 6 or has_water(x, z) or town_mask(x, z) > 0.15 or slope(x, z) > 0.5 or occupied(x, z, 10) or ROADS.dist(x, z) < 20:
            continue
        if any(math.hypot(x - px, z - pz) < 150 for px, pz in placed):
            continue
        placed.append((x, z))
        if put(plan, pickn(MESAS), x, z, rng.uniform(0, 360), 'Mesas', scale=rng.uniform(0.9, 2.1), yo=-5):
            cnt['Mesas'] += 1
    # sea cliffs along the west coast
    placed = []
    for _ in range(4000 if want('SeaCliffs') else 0):
        if len(placed) >= 22:
            break
        z = rng.uniform(-2000, 1600)
        x = -3000
        while x < -1500 and not (H(x, z) > 4 and not has_water(x, z)):
            x += STEP
        if x >= -1500:
            continue
        if any(math.hypot(x - px, z - pz) < 170 for px, pz in placed):
            continue
        # seaward direction = -x
        placed.append((x, z))
        if put(plan, pickn(SEA_CLIFFS), x + 10, z, 90, 'SeaCliffs', scale=rng.uniform(1.1, 1.8), yo=-8):
            cnt['SeaCliffs'] += 1
    # islets on the offshore humps
    for (px, pz, pr, ptop) in (WORLD['post'][9:] if want('Islets') else []):
        if ptop > 28 and pr < 60:
            if put(plan, pickn(['F07_09_rock_formation_09', 'F07_10_rock_formation_10', 'F07_11_rock_formation_11']), px, pz, rng.uniform(0, 360), 'SeaStacks', scale=rng.uniform(0.7, 1.1), yo=-10):
                cnt['SeaStacks'] += 1
        else:
            if put(plan, pickn(ISLETS), px, pz, rng.uniform(0, 360), 'Islets', scale=max(0.9, min(2.0, pr / 38.0)), yo=-8):
                cnt['Islets'] += 1
    return cnt


# ------------------------------------------------------------------ shore and water dressing
def shore():
    cnt = collections.Counter()
    CELL = 20
    for gx in range(int(X0 + 30), int(X1 - 30), CELL):
        for gz in range(int(Z0 + 30), int(Z1 - 30), CELL):
            x = gx + rng.uniform(-8, 8)
            z = gz + rng.uniform(-8, 8)
            if not in_map(x, z) or in_town1_zone(x, z):
                continue
            h = H(x, z)
            m = M(x, z)
            sd = sea_dist(x, z)
            if m == 'S' and 0 < h < 8 and 6 < sd < 90 and not has_water(x, z) and town_mask(x, z) < 0.12 and rng.random() < 0.28:
                mdl = pick(W(('F05_11_sea_oats', 1.2), ('F05_12_dune_tuft', 1.4), ('F10_08_driftwood_pile', 0.35), ('A55_pebbles', 0.7), ('F10_09_rock_pool', 0.15), ('A56_rock_small_1', 0.4)))
                if put('v4_shore', mdl, x, z, rng.uniform(0, 360), 'Beach', scale=rng.uniform(0.9, 1.5)):
                    cnt['Beach'] += 1
                continue
            rd = RIVERS.dist(x, z)
            if 5 < rd < 22 and h > 2 and not has_water(x, z) and town_mask(x, z) < 0.12 and rng.random() < 0.3:
                mdl = pick(W(('F05_07_reed_clump', 1.2), ('F05_08_reed_stand', 1.0), ('A52_reeds', 0.8), ('F06_09_pebbles_river', 0.6), ('A58_rock_medium_1', 0.3), ('A33_willow', 0.12)))
                if put('v4_shore', mdl, x, z, rng.uniform(0, 360), 'Riverbank', scale=rng.uniform(0.9, 1.4)):
                    cnt['Riverbank'] += 1
    for L in LAKES:
        if L.get('frozen'):
            continue
        n = int(L['rx'] / 3.2)
        for k in range(n):
            a = rng.uniform(0, math.tau)
            rr = rng.uniform(1.0, 1.22)
            x, z = L['cx'] + math.cos(a) * L['rx'] * rr, L['cz'] + math.sin(a) * L['rz'] * rr
            mdl = pick(W(('F05_07_reed_clump', 1.4), ('F05_08_reed_stand', 1.2), ('A52_reeds', 0.8), ('A58_rock_medium_1', 0.4), ('F06_09_pebbles_river', 0.5)))
            if put('v4_shore', mdl, x, z, rng.uniform(0, 360), 'Lakeside', scale=rng.uniform(0.9, 1.4)):
                cnt['Lakeside'] += 1
        for k in range(int(L['rx'] / 9)):
            a = rng.uniform(0, math.tau)
            rr = rng.uniform(0.2, 0.85)
            x, z = L['cx'] + math.cos(a) * L['rx'] * rr, L['cz'] + math.sin(a) * L['rz'] * rr
            if put('v4_shore', pick(W(('F10_01_lily_pad_cluster', 1.2), ('F10_02_lily_pad_spread', 0.8))), x, z, rng.uniform(0, 360), 'LilyPads', scale=rng.uniform(0.9, 1.5), yo=0.2):
                cnt['LilyPads'] += 1
    return cnt


if __name__ == '__main__':
    n_occ = load_occupancy()
    print('occupancy footprints', n_occ, 'grid', NX, 'x', NZ)
    if os.environ.get('STAGE') == '2':
        print('pieces2', dict(set_pieces('v4_pieces2', {'SnowPeaks', 'Mesas'})))
        for plan, items in OUT.items():
            json.dump({'area': plan, 'terrain': [], 'placements': items}, open(MP + '\\\\' + plan + '.json', 'w'))
            print(plan, len(items), 'items')
        sys.exit(0)
    print('forests', dict(forests()))
    print('under', dict(undergrowth()))
    print('rocks', dict(rocks()))
    print('pieces', dict(set_pieces()))
    print('shore', dict(shore()))
    for plan, items in OUT.items():
        json.dump({'area': plan, 'terrain': [], 'placements': items}, open(MP + '\\' + plan + '.json', 'w'))
        c = collections.Counter(i['model'] for i in items)
        print(plan, len(items), 'items;', 'top:', c.most_common(5))



