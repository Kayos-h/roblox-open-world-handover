"""World designer v4 (island about 1.25x, more relief, rivers, cliffs, islets, trails).
Imports the v3 designer (world.py), mutates its tables in place, then writes rebuild/world.json (v4) + rebuild/v4/world_extra.json.
The v3 world.json is backed up once to rebuild/v4/world_v3.json. Replayable: python world_v4.py
Coordinates: X east, Z south (north = -Z), Y up, sea level 0. Town 1 interior is protected through world['keep']['town1'].
"""
import sys, os, json, math, random, shutil, heapq

RB = r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild'
V4 = RB + r'\v4'
os.makedirs(V4, exist_ok=True)
sys.path.insert(0, RB)
import world as W

if os.path.exists(RB + r'\world.json') and not os.path.exists(V4 + r'\world_v3.json'):
    shutil.copy(RB + r'\world.json', V4 + r'\world_v3.json')

rng = random.Random(30102026)
smooth = W.smoothstep

# ------------------------------------------------------------------ coast
W.COAST.update({'ax': 3240, 'az_n': 3500, 'az_s': 2200, 'p': 2.6, 'west_start': 0.93, 'deep': 26})

# the frozen lake sat on a raised terrace (31 studs above the village shelf): lower it into a bowl next to the village
for p in W.PADS:
    if p['name'] == 'alpine_lake':
        p['ground'] = {'type': 'flat', 'y': 131.0}
for L in W.LAKES:
    if L['name'] == 'alpine_ice_lake':
        L['level'] = 131.0
_lp = W.ROADS['lake_path']['pts']
W.ROADS['lake_path']['pts'] = [(1560, -960, 120.0), (1530, -1000, 123.0), (1470, -1004, 126.0), (1430, -985, 129.0), (1420, -1010, 131.0)]


def coast_start(x, z):
    ws = W.COAST.get('west_start')
    if ws is None:
        return W.COAST['start']
    return W.COAST['start'] + (ws - W.COAST['start']) * smooth(900, 1700, -x)


def base_h2(x, z):
    h = 6.0
    for kind, cx, cz, r, hh in W.FEATURES:
        d = math.hypot(x - cx, z - cz)
        if kind == 'g':
            if d < r * 3:
                h += hh * math.exp(-(d / r) ** 2)
        elif kind == 'M':
            if d < r * 3:
                h += hh * math.exp(-(d / r) ** 2) * 0.85
        else:
            h += hh * (1 - smooth(r * 0.72, r, d))
    c = smooth(coast_start(x, z), W.COAST['end'], W.coast_d(x, z))
    return h + (W.COAST['floor'] - h) * c


W.base_h = base_h2
G = W.ground_no_noise

# ------------------------------------------------------------------ hand-placed features
NEW = [
    # north: castle backdrop and forested flanks
    ('M', 0, -2900, 280, 115), ('M', -620, -2700, 330, 150), ('M', 640, -2650, 340, 170),
    ('M', -1250, -2350, 330, 170), ('M', -1750, -2000, 330, 190), ('M', 1250, -2250, 330, 200),
    ('g', -300, -2550, 200, 40), ('g', 330, -2480, 200, 36),
    # north-east snow range and the tower ridge next to the capital
    ('M', 1000, -1700, 230, 100), ('M', 2000, -2050, 340, 270), ('M', 2450, -1750, 330, 285),
    ('M', 2350, -1050, 320, 250), ('M', 2700, -600, 240, 150), ('M', 1800, -2450, 320, 240),
    ('M', 2550, -2200, 300, 240), ('M', 1300, -2050, 300, 205), ('g', 2150, -300, 250, 40),
    # west: forested hills and a cliff coast
    ('M', -2500, -300, 270, 160), ('M', -2450, -1150, 280, 170), ('M', -2500, 650, 270, 140),
    ('M', -1850, 800, 280, 120), ('M', -2200, 1250, 250, 110), ('M', -1700, -1650, 300, 170),
    ('m', -2650, -700, 130, 60), ('m', -2700, 200, 140, 70), ('m', -2600, 1000, 120, 55), ('m', -2300, 1500, 100, 45),
    # south-west
    ('g', -1800, 1400, 250, 45), ('g', -600, 1750, 200, 30),
    # south-east badlands
    ('m', 2300, 700, 130, 80), ('m', 2450, 1250, 150, 95), ('m', 2150, 1550, 100, 60), ('m', 2000, 380, 110, 62),
    ('m', 1900, 1150, 90, 46), ('m', 2650, 250, 90, 55), ('m', 1300, 1750, 90, 40),
    ('g', 2500, -150, 260, 40),
]
W.FEATURES.extend(NEW)

# ------------------------------------------------------------------ exclusion zones for random hills
EXC = []
for p in W.PADS:
    r = (math.hypot(p['hx'], p['hz']) if p['shape'] == 'rect' else max(p['rx'], p['rz'])) + p['e'] + 60
    EXC.append((p['cx'], p['cz'], r))
for L in W.LAKES:
    EXC.append((L['cx'], L['cz'], max(L['rx'], L['rz']) * 1.8 + 140))


def seg_dist(px, pz, ax, az, bx, bz):
    vx, vz = bx - ax, bz - az
    L2 = vx * vx + vz * vz
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((px - ax) * vx + (pz - az) * vz) / L2))
    return math.hypot(px - (ax + vx * t), pz - (az + vz * t))


def near_line(x, z, pts, d):
    for i in range(len(pts) - 1):
        if seg_dist(x, z, pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1]) < d:
            return True
    return False


ROAD_LINES = [[(q[0], q[1]) for q in r['pts']] for r in W.ROADS.values()]


def excluded(x, z):
    for cx, cz, r in EXC:
        if math.hypot(x - cx, z - cz) < r:
            return True
    for line in ROAD_LINES:
        if near_line(x, z, line, 150):
            return True
    return False


HILLS = []
for ix in range(-12, 13):
    for iz in range(-13, 9):
        x = ix * 300 + rng.uniform(-110, 110)
        z = iz * 300 + rng.uniform(-110, 110) - 150
        cd = W.coast_d(x, z)
        if cd > 0.80 or excluded(x, z):
            continue
        r = rng.uniform(150, 290)
        h = rng.uniform(12, 46) * (1.0 if cd < 0.6 else 0.7)
        HILLS.append(('g', round(x), round(z), round(r), round(h)))
W.FEATURES.extend(HILLS)

# gentle meadow undulation in the lowlands (small, so the middle of the island rolls instead of lying flat)
MEADOW = []
for ix in range(-12, 13):
    for iz in range(-13, 9):
        x = ix * 215 + rng.uniform(-80, 80)
        z = iz * 215 + rng.uniform(-80, 80) - 100
        if W.coast_d(x, z) > 0.74:
            continue
        bad = False
        for p in W.PADS:
            if W.pad_mask(p, x, z) > 0.0:
                bad = True
                break
        if bad:
            continue
        if any(math.hypot(x - L['cx'], z - L['cz']) < max(L['rx'], L['rz']) * 1.8 + 80 for L in W.LAKES):
            continue
        if any(near_line(x, z, line, 70) for line in ROAD_LINES):
            continue
        MEADOW.append(('g', round(x), round(z), round(rng.uniform(100, 200)), round(rng.uniform(5, 17))))
W.FEATURES.extend(MEADOW)

# ------------------------------------------------------------------ islets and sea stacks (POST: x, z, r, top)
NEWPOST = []
cx0, cz0 = 0.0, -300.0
for bearing in (8, 22, 38, 55, 75, 100, 118, 135, 150, 170, 200, 225, 245, 262, 280, 298, 318, 335, 350):
    a = math.radians(bearing)
    ux, uz = math.sin(a), -math.cos(a)
    t = 1500.0
    while t < 4200 and W.coast_d(cx0 + ux * t, cz0 + uz * t) < 1.03 + rng.uniform(0.0, 0.06):
        t += 20
    x, z = cx0 + ux * t, cz0 + uz * t
    if abs(x + 390) < 750 and z > 1600:
        continue
    NEWPOST.append((round(x), round(z), round(rng.uniform(45, 110)), round(rng.uniform(5, 22))))
for k in range(9):  # west coast sea stacks
    zz = rng.uniform(-1900, 1500)
    t = 2200.0
    while t < 3600 and W.coast_d(-t, zz) < 0.955 + rng.uniform(0.0, 0.03):
        t += 15
    NEWPOST.append((round(-t), round(zz), round(rng.uniform(22, 44)), round(rng.uniform(32, 70))))
W.POST.extend(NEWPOST)

# ------------------------------------------------------------------ biomes
W.BIOMES[:] = [
    ('jungle', -1560, -400, 560), ('forest', -1050, -1500, 480), ('forest', -1450, 900, 360), ('forest', 600, -1200, 260),
    ('dry', 1235, 1105, 640), ('dry', 1650, 1350, 420), ('dry', 2050, 900, 800), ('dry', 1500, 1750, 500),
    ('alpine', 1420, -1180, 700), ('alpine', 2000, -1500, 1000), ('alpine', 1200, -1950, 600),
    ('plains', 0, 0, 640), ('plains', 0, -1600, 800), ('plains', -390, 1620, 420), ('plains', 700, 300, 300), ('plains', -700, 350, 300),
]

# ------------------------------------------------------------------ rivers: trace downhill from seeds
LAKES_CENTERS = [(L['cx'], L['cz'], max(L['rx'], L['rz']) * 1.3, L['level']) for L in W.LAKES if not L.get('frozen')]


def pad_hit(x, z, thr=0.02):
    for p in W.PADS:
        if W.pad_mask(p, x, z) > thr:
            return True
    return False


def trace(x, z, step=50, maxn=130):
    pts = [(x, z)]
    dx = dz = 0.0
    best_h = G(x, z)
    stuck = 0
    for n in range(maxn):
        best = None
        for k in range(32):
            a = 2 * math.pi * k / 32
            ux, uz = math.cos(a), math.sin(a)
            nx, nz = x + ux * step, z + uz * step
            h = G(nx, nz)
            c = h - 14 * (ux * dx + uz * dz)
            if pad_hit(nx, nz):
                c += 150
            for (qx, qz) in pts[-14:-1]:
                if (nx - qx) ** 2 + (nz - qz) ** 2 < (step * 0.9) ** 2:
                    c += 200
            if best is None or c < best[0]:
                best = (c, ux, uz, nx, nz, h)
        _, ux, uz, x, z, h = best
        dx, dz = 0.65 * dx + 0.35 * ux, 0.65 * dz + 0.35 * uz
        m = math.hypot(dx, dz) or 1.0
        dx, dz = dx / m, dz / m
        pts.append((x, z))
        if h < best_h - 0.5:
            best_h = h
            stuck = 0
        else:
            stuck += 1
        if h < 1.0 or W.coast_d(x, z) > 0.86:
            return pts, 'sea', None
        for (lx, lz, lr, lv) in LAKES_CENTERS:
            if math.hypot(x - lx, z - lz) < lr:
                return pts, 'lake', lv
        if stuck > 25:
            return pts, 'stuck', None
    return pts, 'long', None


def chaikin(pts, n=2):
    for _ in range(n):
        out = [pts[0]]
        for i in range(len(pts) - 1):
            a, b = pts[i], pts[i + 1]
            out.append((0.75 * a[0] + 0.25 * b[0], 0.75 * a[1] + 0.25 * b[1]))
            out.append((0.25 * a[0] + 0.75 * b[0], 0.25 * a[1] + 0.75 * b[1]))
        out.append(pts[-1])
        pts = out
    return pts


def resample(pts, step):
    out = [pts[0]]
    carry = 0.0  # distance travelled since the last emitted point
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        seg = math.hypot(b[0] - a[0], b[1] - a[1])
        if seg == 0:
            continue
        d = step - carry
        while d <= seg:
            t = d / seg
            out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
            d += step
        carry = seg - (d - step)
    if math.hypot(out[-1][0] - pts[-1][0], out[-1][1] - pts[-1][1]) > 1:
        out.append(pts[-1])
    return out


def levels(pts, margin=4.0, floor=-2.5, end_level=None):
    out = []
    lv = G(pts[0][0], pts[0][1]) - 3.0
    for (x, z) in pts:
        lv = min(lv, G(x, z) - 2.2 - margin)
        out.append(max(lv, floor))
    if end_level is not None:
        out[-1] = min(out[-1], end_level)
    return out


SEEDS = [
    ('ne_a', 2300, -1700), ('ne_b', 1900, -2000), ('n_ridge', -1000, -2500), ('nw_a', -1700, -1800),
    ('w_a', -2400, -900), ('w_b', -2300, 700), ('se_a', 2300, 600), ('sw_a', -1300, 1100),
    ('n_b', 700, -2400), ('mid_hills', 1000, -700), ('w_hills', -900, 300), ('e_hills', 2100, -300),
]
RIVERS_NEW = []
RIVER_LINES = []
for name, sx, sz in SEEDS:
    raw, how, lake_lv = trace(sx, sz)
    print('river', name, how, len(raw), 'pts', 'from', (round(raw[0][0]), round(raw[0][1])), 'to', (round(raw[-1][0]), round(raw[-1][1])))
    if how not in ('sea', 'lake') or len(raw) < 14:
        continue
    pts = resample(chaikin(raw, 2), 60)
    lv = levels(pts, end_level=(lake_lv if how == 'lake' else None))
    half = len(pts) // 2
    up = [[round(p[0], 1), round(p[1], 1), round(l, 2)] for p, l in zip(pts[:half + 1], lv[:half + 1])]
    dn = [[round(p[0], 1), round(p[1], 1), round(l, 2)] for p, l in zip(pts[half:], lv[half:])]
    RIVERS_NEW.append({'name': name + '_up', 'w': 7, 'depth': 3, 'pts': up})
    RIVERS_NEW.append({'name': name + '_dn', 'w': 13, 'depth': 5, 'pts': dn})
    RIVER_LINES.append((name, pts))

# the v3 rivers, recomputed on the new terrain (same routes)
SILVER = [(1860, -700), (1930, -610), (1975, -500), (1940, -380), (1820, -260), (1620, -160), (1380, -90), (1120, -30), (900, 40), (720, 100)]
silver_pts = [(p[0], p[1]) for p in resample(chaikin(SILVER, 1), 60)]
sl = levels(silver_pts, margin=3.0, floor=-3.0, end_level=-3.0)
RIVERS = [r for r in W.RIVERS if r['name'] in ('t1_west', 't1_east')]
RIVERS.append({'name': 'silverrun', 'w': 9, 'depth': 5, 'pts': [[round(p[0], 1), round(p[1], 1), round(l, 2)] for p, l in zip(silver_pts, sl)]})
RIVERS.extend([r for r in W.RIVERS if r['name'] == 'elf_river'])
RIVERS.extend(RIVERS_NEW)
RIVER_LINES.append(('silverrun', silver_pts))
W.RIVERS[:] = RIVERS

# ------------------------------------------------------------------ extra lakes (level below the whole rim)
EXTRA_LAKES = [('nw_tarn', -1350, -1900, 70, 55), ('sw_pond', -1150, 1150, 70, 50), ('east_pond', 1900, 500, 60, 45), ('north_pool', 380, -2350, 75, 55)]
for name, cx, cz, rx, rz in EXTRA_LAKES:
    rim = []
    for k in range(16):
        a = 2 * math.pi * k / 16
        rim.append(G(cx + math.cos(a) * rx * 1.5, cz + math.sin(a) * rz * 1.5))
    lvl = min(min(rim), G(cx, cz)) - 5.0
    W.LAKES.append({'name': name, 'cx': cx, 'cz': cz, 'rx': rx, 'rz': rz, 'level': round(lvl, 2), 'depth': 6})

# ------------------------------------------------------------------ trails (cheapest slope-aware path on a grid), written as streets
STEP = 40
X0, X1, Z0, Z1 = -3200, 3200, -3400, 2400
NX, NZ = (X1 - X0) // STEP + 1, (Z1 - Z0) // STEP + 1
HG = [[G(X0 + i * STEP, Z0 + j * STEP) for j in range(NZ)] for i in range(NX)]
WATERMASK = [[False] * NZ for _ in range(NX)]
for _, line in RIVER_LINES:
    for (x, z) in line:
        i, j = int(round((x - X0) / STEP)), int(round((z - Z0) / STEP))
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                if 0 <= i + di < NX and 0 <= j + dj < NZ:
                    WATERMASK[i + di][j + dj] = True


def route(a, b):
    si, sj = int(round((a[0] - X0) / STEP)), int(round((a[1] - Z0) / STEP))
    ei, ej = int(round((b[0] - X0) / STEP)), int(round((b[1] - Z0) / STEP))
    dist = {(si, sj): 0.0}
    prev = {}
    pq = [(0.0, si, sj)]
    while pq:
        d, i, j = heapq.heappop(pq)
        if (i, j) == (ei, ej):
            break
        if d > dist.get((i, j), 1e18):
            continue
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                if di == 0 and dj == 0:
                    continue
                ni, nj = i + di, j + dj
                if not (0 <= ni < NX and 0 <= nj < NZ):
                    continue
                h2 = HG[ni][nj]
                x, z = X0 + ni * STEP, Z0 + nj * STEP
                if h2 < 2.5 or W.coast_d(x, z) > 0.83:
                    continue
                ln = STEP * (1.414 if di and dj else 1.0)
                slope = abs(h2 - HG[i][j]) / ln
                c = ln * (1 + 14 * slope * slope)
                if WATERMASK[ni][nj]:
                    c += 1500
                nd = d + c
                if nd < dist.get((ni, nj), 1e18):
                    dist[(ni, nj)] = nd
                    prev[(ni, nj)] = (i, j)
                    heapq.heappush(pq, (nd, ni, nj))
    if (ei, ej) not in dist:
        return None
    path = [(ei, ej)]
    while path[-1] != (si, sj):
        path.append(prev[path[-1]])
    path.reverse()
    return [(X0 + i * STEP, Z0 + j * STEP) for i, j in path]


TRAIL_DEFS = [
    ('trail_lake_w', [(-650, -120), (-640, 230), (-760, 340), (-1000, 700), (-1300, 1000)]),
    ('trail_lake_e', [(650, -110), (640, 40), (900, 420), (1100, 700)]),
    ('trail_summit', [(560, -1560), (700, -1620), (820, -1660), (900, -1690)]),
    ('trail_elf_coast', [(-1880, -440), (-2200, -420), (-2500, -380)]),
    ('trail_nw', [(-500, -1580), (-1000, -1700), (-1500, -1500), (-1900, -1300), (-1700, -760)]),
    ('trail_harbour_w', [(-640, 1700), (-1000, 1500), (-1300, 1400), (-1900, 1000), (-2300, 600)]),
    ('trail_rusty_e', [(1700, 1250), (2200, 1150), (2500, 700), (2400, 200), (2300, -200)]),
    ('trail_castle_n', [(0, -2420), (60, -2650), (60, -2780)]),
    ('trail_alpine_n', [(1700, -1000), (1950, -1350), (2200, -1750)]),
    ('trail_south_farm', [(-150, 520), (-300, 700), (-200, 1000), (200, 1200), (500, 1500)]),
    ('trail_nw_coast', [(-1000, -2200), (-1600, -2300), (-2100, -2000)]),
    ('trail_ne_pass', [(1000, -1300), (1250, -1900), (1700, -2300)]),
]
TRAILS = []
for name, wps in TRAIL_DEFS:
    full = []
    ok = True
    for a, b in zip(wps[:-1], wps[1:]):
        seg = route(a, b)
        if seg is None:
            ok = False
            break
        full.extend(seg if not full else seg[1:])
    if not ok:
        print('trail', name, 'no route')
        continue
    pts = resample(chaikin(full, 2), 36)
    ys = [G(p[0], p[1]) for p in pts]
    sm = [sum(ys[max(0, i - 2):i + 3]) / len(ys[max(0, i - 2):i + 3]) for i in range(len(ys))]
    TRAILS.append({'name': name, 'w': 2.6, 'mat': 'Ground', 'bank': 8,
                   'pts': [[round(p[0], 1), round(p[1], 1), round(y, 2)] for p, y in zip(pts, sm)]})
    print('trail', name, len(pts), 'pts')

# ------------------------------------------------------------------ assemble and write
streets = []
sp = RB + r'\streets.json'
if os.path.exists(sp):
    streets = json.load(open(sp))
# the old elf village paths are replaced by the v4 elf paths (rebuild\v4\elf_plan.py writes elf_streets.json)
_old = len(streets)
streets = [s for s in streets if not str(s.get('name', '')).startswith('v3_elf')]
print('old elf streets removed:', _old - len(streets))
_ep = V4 + r'\elf_streets.json'
ELF_STREETS = json.load(open(_ep)) if os.path.exists(_ep) else []
print('v4 elf streets added:', len(ELF_STREETS))
world = {
    'features': [list(f) for f in W.FEATURES],
    'coast': W.COAST,
    'post': [list(p) for p in W.POST],
    'pads': W.PADS,
    'roads': W.build_roads(),
    'rivers': W.RIVERS,
    'lakes': W.LAKES,
    'biomes': [list(b) for b in W.BIOMES],
    'keep': {'town1': [-318, 318, -545, 311]},
    't1': W.T1,
    'streets': streets + TRAILS + ELF_STREETS,
    'relief': {'base': 10, 'slope': 0.12},
    'default_biome': 'forest',
}
json.dump(world, open(RB + r'\world.json', 'w'), separators=(',', ':'))
json.dump(world, open(V4 + r'\world_v4.json', 'w'), separators=(',', ':'))
extra = {
    'rivers': [{'name': n, 'pts': [[round(x), round(z)] for x, z in pts]} for n, pts in RIVER_LINES],
    'trails': [{'name': t['name'], 'pts': [[p[0], p[1]] for p in t['pts']]} for t in TRAILS],
    'islets': [list(p) for p in NEWPOST],
    'hills': [list(h) for h in HILLS],
    'lakes': [l for l in W.LAKES],
}
json.dump(extra, open(V4 + r'\world_extra.json', 'w'), separators=(',', ':'))
print('features', len(world['features']), 'hills', len(HILLS), 'meadow', len(MEADOW), 'post', len(world['post']), 'rivers', len(world['rivers']),
      'lakes', len(world['lakes']), 'streets', len(world['streets']), 'json bytes', len(json.dumps(world)))

# stats: tallest points and heights at the settlements
mx = (0, 0, 0)
over = {300: 0, 400: 0, 500: 0}
for x in range(-3200, 3201, 50):
    for z in range(-3400, 2401, 50):
        h = G(x, z)
        if h > mx[0]:
            mx = (h, x, z)
        for k in over:
            if h > k:
                over[k] += 1
print('tallest', [round(mx[0]), mx[1], mx[2]], 'samples above 300/400/500:', over)
for nm, (x, z) in {'capital': (0, -1578), 'capital_east_edge': (700, -1578), 'capital_west_edge': (-700, -1578), 'castle': (0, -2200),
                   'castle_back': (0, -2550), 'alpine_shelf': (1640, -850), 'ice_lake': (1490, -1075), 'summit_pad': (1380, -1320),
                   'tower_ridge': (900, -1690), 'elf_tree': (-1560, -430), 'elf_edge_w': (-1900, -430), 'rusty': (1235, 1105),
                   'harbour_north': (-390, 1500), 'town1_ring_e': (500, -100)}.items():
    print('  ground', nm, (x, z), round(G(x, z), 1))

# coarse height map for a sanity check: '.' sea, digit = height/40 (0..9), 'T' pad core
for z in range(-3300, 2400, 150):
    row = ''
    for x in range(-3000, 3001, 100):
        h = G(x, z)
        row += '.' if h < 1.0 else str(min(9, int(h / 40)))
    print('%6d %s' % (z, row))
