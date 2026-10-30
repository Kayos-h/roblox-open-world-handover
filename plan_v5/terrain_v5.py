"""terrain_v5.py - shared offline terrain tools for the v5 plan.

load_grid()  the exported 24-stud terrain grid (heights, material codes, water levels)
build_spec() the planned landform changes as DATA (hills, crater, canyons, Skull City floor, the Himalayan plateau with its peaks,
             ridges, gorges, tarn, falls, and the new rivers). Written to world_v5_terrain.json so Studio scripts can read it later.
apply_spec() applies the spec to any regular (X, Z) sample grid, so the road router (24-stud grid) and the top-view sketch
             (3-stud pixels) see the same planned land.
Run `python terrain_v5.py` to rebuild world_v5_terrain.json.
"""
import json
import math
import os
import random

import numpy as np

TOWN = r'C:\Users\Nitro\.kiro\crew\workspace\town'
RB = TOWN + r'\rebuild'
HERE = TOWN + r'\plan_v5'
SPEC_PATH = HERE + r'\world_v5_terrain.json'
CODES = 'GLSMRTBNIDACPKH'


def load_grid():
    tm = json.load(open(RB + r'\v4\terrain_map.json'))
    x0, z0, st = tm['x0'], tm['z0'], tm['step']
    nx = (tm['x1'] - x0) // st + 1
    nz = len(tm['rows'])
    H = np.zeros((nz, nx), np.float32)
    M = np.zeros((nz, nx), np.uint8)
    W = np.full((nz, nx), -999.0, np.float32)
    for j, row in enumerate(tm['rows']):
        for i in range(nx):
            c = row[i * 5:i * 5 + 5]
            H[j, i] = int(c[0:2], 36) - 100
            M[j, i] = CODES.index(c[2]) + 1 if c[2] in CODES else 0
            if c[3:5] != '--':
                W[j, i] = int(c[3:5], 36) - 100
    return {'x0': x0, 'z0': z0, 'step': st, 'H': H, 'M': M, 'W': W}


def load_world():
    return json.load(open(RB + r'\world.json'))


def grid_xz(grid):
    nz, nx = grid['H'].shape
    xs = grid['x0'] + grid['step'] * np.arange(nx, dtype=np.float32)
    zs = grid['z0'] + grid['step'] * np.arange(nz, dtype=np.float32)
    return np.meshgrid(xs, zs)


def sstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def slices(X, Z, cx, cz, r):
    xs, zs = X[0], Z[:, 0]
    i0 = int(np.searchsorted(xs, cx - r))
    i1 = int(np.searchsorted(xs, cx + r)) + 1
    j0 = int(np.searchsorted(zs, cz - r))
    j1 = int(np.searchsorted(zs, cz + r)) + 1
    return slice(max(j0, 0), min(j1, Z.shape[0])), slice(max(i0, 0), min(i1, X.shape[1]))


def chaikin(pts, n=2):
    pts = [tuple(p[:2]) for p in pts]
    for _ in range(n):
        out = [pts[0]]
        for a, b in zip(pts[:-1], pts[1:]):
            out.append((0.75 * a[0] + 0.25 * b[0], 0.75 * a[1] + 0.25 * b[1]))
            out.append((0.25 * a[0] + 0.75 * b[0], 0.25 * a[1] + 0.75 * b[1]))
        out.append(pts[-1])
        pts = out
    return pts


def poly_dist(X, Z, pts, margin):
    ax = [p[0] for p in pts]
    az = [p[1] for p in pts]
    sj, si = slices(X, Z, (min(ax) + max(ax)) / 2, (min(az) + max(az)) / 2, max(max(ax) - min(ax), max(az) - min(az)) / 2 + margin)
    qx, qz = X[sj, si], Z[sj, si]
    d = np.full(qx.shape, 1e9, np.float32)
    for (ax_, az_), (bx, bz) in zip(pts[:-1], pts[1:]):
        abx, abz = bx - ax_, bz - az_
        L2 = abx * abx + abz * abz
        if L2 < 1e-9:
            continue
        t = np.clip(((qx - ax_) * abx + (qz - az_) * abz) / L2, 0.0, 1.0)
        dx = qx - (ax_ + t * abx)
        dz = qz - (az_ + t * abz)
        d = np.minimum(d, np.sqrt(dx * dx + dz * dz))
    return sj, si, d


# ---------------------------------------------------------------------------------------------- the planned land (data)
def build_spec(grid, world):
    H, W = grid['H'], grid['W']
    x0, z0, st = grid['x0'], grid['z0'], grid['step']
    rnd = random.Random(11)

    def land_at(x, z, minh=6.0):
        j, i = int(round((z - z0) / st)), int(round((x - x0) / st))
        if not (0 <= j < H.shape[0] and 0 <= i < H.shape[1]):
            return False
        wet = W[j, i] > -900 and W[j, i] > H[j, i] - 0.5
        return (not wet) and H[j, i] >= minh

    pads = [(p['cx'], p['cz'], max(p.get('rx', 0), p.get('rz', 0), p.get('hx', 0), p.get('hz', 0))) for p in world['pads']]
    hills = []
    tries = 0
    while len(hills) < 11 and tries < 4000:
        tries += 1
        x, z = rnd.uniform(-1300, 1400), rnd.uniform(-900, 1500)
        if any(math.hypot(x - h['x'], z - h['z']) < 430 for h in hills):
            continue
        if abs(x) < 420 and -620 < z < 380:
            continue
        if any(math.hypot(x - a, z - b) < r + 260 for a, b, r in pads):
            continue
        if any(math.hypot(x - l['cx'], z - l['cz']) < max(l['rx'], l['rz']) + 220 for l in world['lakes']):
            continue
        if not land_at(x, z):
            continue
        hills.append({'x': round(x), 'z': round(z), 'sigma': round(rnd.uniform(230, 360)), 'amp': round(rnd.uniform(20, 42))})
    return {
        'version': 2,
        'note': 'Planned landform changes for the single terrain pass. Heights in studs; x east, z south (north is -z). Apply with apply_spec().',
        'protected': {'town1': [-318, 318, -545, 311]},
        'hills': hills,
        'crater': {'x': 1368, 'z': -312, 'radius': 240, 'depth': 46, 'rim_h': 16, 'rim_r': 275},
        'canyons': [
            {'name': 'canyon_a', 'pts': [[2350, 650], [2150, 800], [1980, 980], [1870, 1180], [1720, 1290]], 'depth': 34, 'sigma': 52},
            {'name': 'canyon_b', 'pts': [[1480, 1560], [1700, 1660], [1950, 1700], [2200, 1640]], 'depth': 34, 'sigma': 52},
        ],
        'skull_floor': {'x': 2280, 'z': -430, 'r': 330, 'level': 64, 'strength': 0.55},
        # ---- the Himalayan plateau: the room for the giant enterable wizard tower ----
        'plateau': {
            'name': 'Roof Plateau', 'x': 1380, 'z': -1400, 'rx': 280, 'rz': 190, 'level': 322, 'undulation': 5,
            'shoulder_n': 150, 'shoulder_s': 50, 'shoulder_ew': 110,
            'tower': {'name': 'wizard tower', 'x': 1380, 'z': -1320, 'shell_radius': 55, 'terrace_radius': 95, 'courtyard_radius': 140, 'floor_y': 324},
        },
        'peaks': [
            {'name': 'Spire of Dawn', 'x': 1140, 'z': -1790, 'h': 640, 'sigma': 150, 'p': 1.3},
            {'name': 'Twin Fang North', 'x': 1540, 'z': -1930, 'h': 610, 'sigma': 130, 'p': 1.3},
            {'name': 'Twin Fang South', 'x': 1700, 'z': -1860, 'h': 575, 'sigma': 110, 'p': 1.3},
            {'name': 'Wall Peak', 'x': 940, 'z': -1600, 'h': 520, 'sigma': 150, 'p': 1.3},
            {'name': 'East Horn', 'x': 1930, 'z': -1520, 'h': 540, 'sigma': 140, 'p': 1.3},
            {'name': 'Snow Saddle Peak', 'x': 1260, 'z': -2100, 'h': 560, 'sigma': 150, 'p': 1.3},
        ],
        'ridges': [
            {'name': 'Anvil Ridge', 'pts': [[1060, -1700], [1220, -1740], [1380, -1780], [1540, -1760], [1700, -1700], [1860, -1620]], 'amp': 70, 'sigma': 70},
            {'name': 'Frost Spine', 'pts': [[1000, -1500], [950, -1700], [1000, -1900]], 'amp': 60, 'sigma': 70},
        ],
        'gorges': [
            {'name': 'Frost Gorge', 'pts': [[2272, -1348], [2400, -1352], [2520, -1356], [2646, -1358]], 'depth': 40, 'sigma': 45},
            {'name': 'Meltwater Notch', 'pts': [[1530, -1300], [1505, -1235], [1480, -1190]], 'depth': 30, 'sigma': 30},
        ],
        'tarns': [{'name': 'roof_tarn', 'x': 1580, 'z': -1500, 'r': 60, 'level': 323, 'frozen': True}],
        'falls': [{'name': 'roof_falls', 'x': 1480, 'z': -1205, 'top_y': 322, 'bottom_y': 131, 'width': 26, 'ribbons': 3, 'into': 'alpine_ice_lake'}],
        'rivers_new': [
            {'name': 'trunk_east', 'w': 16, 'pts': [[380, -2350], [640, -2050], [700, -1650], [600, -1250], [220, -1080], [480, -700], [630, -200], [630, 120], [700, 600], [560, 1100], [420, 1500], [300, 1760]]},
            {'name': 'trunk_west', 'w': 16, 'pts': [[380, -2350], [140, -2100], [-640, -2000], [-700, -1600], [-600, -1250], [-220, -1080], [-500, -800], [-700, -300], [-660, 300], [-600, 800], [-450, 1300], [-400, 1700]]},
            {'name': 'forest_river', 'w': 12, 'pts': [[-1350, -1900], [-1500, -1500], [-1650, -1100], [-1700, -720]]},
            {'name': 'greenheart', 'w': 9, 'pts': [[-1150, 1150], [-1220, 800], [-1248, 560], [-950, 420], [-660, 300]]},
            {'name': 'meltwater', 'w': 12, 'pts': [[1580, -1490], [1545, -1400], [1530, -1300], [1505, -1235], [1480, -1190]]},
        ],
    }


def load_spec(grid=None, rebuild=False):
    if os.path.exists(SPEC_PATH) and not rebuild:
        return json.load(open(SPEC_PATH))
    grid = grid or load_grid()
    spec = build_spec(grid, load_world())
    json.dump(spec, open(SPEC_PATH, 'w'), indent=1)
    return spec


# ---------------------------------------------------------------------------------------------- apply the spec to a sample grid
def apply_spec(Hbase, X, Z, spec, land):
    Hp = Hbase.astype(np.float32).copy()
    lw = land.astype(np.float32)
    # 1. mountains first, so the plateau can cut into them
    for pk in spec['peaks']:
        sj, si = slices(X, Z, pk['x'], pk['z'], pk['sigma'] * 3.2)
        d = np.hypot(X[sj, si] - pk['x'], Z[sj, si] - pk['z'])
        centre = float(Hp[sj, si][np.unravel_index(np.argmin(d), d.shape)])
        Hp[sj, si] += max(pk['h'] - centre, 0.0) * np.exp(-(d / pk['sigma']) ** pk.get('p', 1.3)) * lw[sj, si]
    for rd in spec['ridges']:
        sj, si, d = poly_dist(X, Z, chaikin(rd['pts'], 2), rd['sigma'] * 3)
        wob = 0.8 + 0.2 * np.sin(X[sj, si] / 47.0 + Z[sj, si] / 61.0)
        Hp[sj, si] += rd['amp'] * np.exp(-(d / rd['sigma']) ** 2) * wob * lw[sj, si]
    # 2. central band, east and south-east
    for h in spec['hills']:
        sj, si = slices(X, Z, h['x'], h['z'], 3 * h['sigma'])
        Hp[sj, si] += h['amp'] * np.exp(-((X[sj, si] - h['x']) ** 2 + (Z[sj, si] - h['z']) ** 2) / (2 * h['sigma'] ** 2)) * lw[sj, si]
    c = spec['crater']
    sj, si = slices(X, Z, c['x'], c['z'], c['rim_r'] + 70)
    r = np.hypot(X[sj, si] - c['x'], Z[sj, si] - c['z'])
    Hp[sj, si] += (-c['depth'] * np.clip(1.0 - (r / c['radius']) ** 2, 0, 1) + c['rim_h'] * np.exp(-((r - c['rim_r']) / 45.0) ** 2)) * lw[sj, si]
    for cn in spec['canyons']:
        sj, si, d = poly_dist(X, Z, chaikin(cn['pts'], 2), 200)
        Hp[sj, si] -= cn['depth'] * np.exp(-(d / cn['sigma']) ** 2) * lw[sj, si]
    s = spec['skull_floor']
    sj, si = slices(X, Z, s['x'], s['z'], s['r'] + 10)
    r = np.hypot(X[sj, si] - s['x'], Z[sj, si] - s['z'])
    wgt = s['strength'] * (1.0 - sstep(120.0, s['r'], r)) * lw[sj, si]
    Hp[sj, si] = Hp[sj, si] * (1 - wgt) + s['level'] * wgt
    for gg in spec['gorges']:
        sj, si, d = poly_dist(X, Z, chaikin(gg['pts'], 2), gg['sigma'] * 4)
        Hp[sj, si] -= gg['depth'] * np.exp(-(d / gg['sigma']) ** 2) * lw[sj, si]
    # 3. the plateau: flat core with a gentle roll, a wide blend to the north and sides, a short cliff to the south
    p = spec['plateau']
    sj, si = slices(X, Z, p['x'], p['z'], max(p['rx'], p['rz']) + 260)
    x, z = X[sj, si], Z[sj, si]
    dx, dz = (x - p['x']) / p['rx'], (z - p['z']) / p['rz']
    d_out = (np.hypot(dx, dz) - 1.0) * 0.5 * (p['rx'] + p['rz'])
    shoulder = np.where(dz < 0, np.where(np.abs(dx) > 0.8, p['shoulder_ew'], p['shoulder_n']), p['shoulder_s']).astype(np.float32)
    w = np.where(d_out <= 0, 1.0, 1.0 - sstep(0.0, 1.0, d_out / shoulder)).astype(np.float32) * lw[sj, si]
    target = p['level'] + p['undulation'] * (np.sin(x / 90.0) * np.cos(z / 110.0) + 0.5 * np.sin(x / 37.0 + z / 53.0))
    t = p['tower']
    dt = np.hypot(x - t['x'], z - t['z'])
    target = np.where(dt < t['terrace_radius'], t['floor_y'], target)
    Hp[sj, si] = Hp[sj, si] * (1 - w) + target * w
    # 4. the Town 1 protected zone keeps its real terrain; the change feathers in over 120 studs outside it
    xa, xb, za, zb = spec['protected']['town1']
    sj, si = slices(X, Z, (xa + xb) / 2, (za + zb) / 2, max(xb - xa, zb - za) / 2 + 160)
    ox = np.maximum(np.maximum(xa - X[sj, si], X[sj, si] - xb), 0.0)
    oz = np.maximum(np.maximum(za - Z[sj, si], Z[sj, si] - zb), 0.0)
    keep = 1.0 - sstep(0.0, 120.0, np.hypot(ox, oz))
    Hp[sj, si] = Hbase[sj, si] * keep + Hp[sj, si] * (1.0 - keep)
    return Hp


if __name__ == '__main__':
    g = load_grid()
    sp = load_spec(g, rebuild=True)
    print('wrote', SPEC_PATH, '| hills', len(sp['hills']), '| peaks', len(sp['peaks']), '| rivers_new', len(sp['rivers_new']))
    X, Z = grid_xz(g)
    wat = (g['W'] > -900) & (g['W'] > g['H'] - 0.5)
    Hp = apply_spec(g['H'], X, Z, sp, ~wat)
    for nm, x, z in (('tower pad', 1380, -1320), ('plateau centre', 1380, -1400), ('plateau south edge', 1380, -1230), ('Spire of Dawn', 1140, -1790), ('fortress peak', 1632, -1608), ('alpine lodge', 1585, -880), ('Town 1', 0, 0)):
        j, i = int(round((z - g['z0']) / g['step'])), int(round((x - g['x0']) / g['step']))
        print('%-20s (%5d,%5d) now %4d -> planned %4d' % (nm, x, z, g['H'][j, i], Hp[j, i]))
