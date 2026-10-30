"""route_v5.py - offline road routing for the v5 plan.

Finds a road network that joins every region (capital, Town 1, harbour, west village, elf valley, ruins, desert temples, alpine,
Skull City, the crater and the Himalayan plateau with the wizard tower), runs it through the mountains by passes, hairpins and
tunnels where a ridge is in the way, and lists every river crossing as a bridge with a type.

Method: least-cost path on the 24-stud terrain grid after the planned landform changes (terrain_v5.apply_spec).
  step cost = length * (1 + 40 * grade^2 + 3 * slope^2) * surface factor + river-band cost   (40 * grade^2 makes the optimum grade about 0.16)
  sea, lakes, ice lake and cliffs are blocked; existing roads and already-routed roads are cheaper, so roads merge into trunks.
Output: roads_v5.json (routes with graded profile, bridges, tunnels) and ROADS_V5.md.  Run: python route_v5.py
"""
import json
import math
import os
import sys

import numpy as np
from scipy import ndimage as ndi
from scipy import sparse
from scipy.sparse.csgraph import dijkstra

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import terrain_v5 as T

HERE = T.HERE
grid = T.load_grid()
world = T.load_world()
spec = T.load_spec(grid)
H0, MAT, WL = grid['H'], grid['M'], grid['W']
X0, Z0, ST = grid['x0'], grid['z0'], grid['step']
NZ, NX = H0.shape
X, Z = T.grid_xz(grid)
water = (WL > -900) & (WL > H0 - 0.5)
sea = water & (WL <= 1.0) & (H0 < -1.0)
H = T.apply_spec(H0, X, Z, spec, ~water)
gy, gx = np.gradient(H, ST)
SLOPE = np.hypot(gx, gy)

# ------------------------------------------------------------------ blocked cells and cell costs
blocked = sea | (SLOPE > 1.6)
for l in world['lakes']:
    blocked |= (((X - l['cx']) / (l['rx'] * 1.2 + 24)) ** 2 + ((Z - l['cz']) / (l['rz'] * 1.2 + 24)) ** 2) < 1.0
for t in spec['tarns']:
    blocked |= np.hypot(X - t['x'], Z - t['z']) < t['r'] + 30
SURF = np.array([1.0, 1.0, 1.15, 1.1, 1.5, 1.15, 1.15, 1.3, 1.25, 2.5, 1.0, 1.1, 0.9, 0.85, 1.0, 1.2], np.float32)
mult = SURF[MAT].copy()
add = np.zeros((NZ, NX), np.float32)
rivers = [dict(name=r['name'], w=r['w'], pts=[(p[0], p[1]) for p in r['pts']], new=False) for r in world['rivers']]
rivers += [dict(name=r['name'], w=r['w'], pts=[(p[0], p[1]) for p in r['pts']], new=True) for r in spec['rivers_new']]
for r in rivers:
    sj, si, d = T.poly_dist(X, Z, T.chaikin(r['pts'], 1), 80)
    add[sj, si] += np.where(d < r['w'] / 2 + 16, 70.0, 0.0)
disc = np.ones((NZ, NX), np.float32)
for rd in world['roads']:
    sj, si, d = T.poly_dist(X, Z, [(p[0], p[1]) for p in rd['pts']], 60)
    disc[sj, si] = np.where(d < 14, np.minimum(disc[sj, si], 0.5), disc[sj, si])
IDX = np.arange(NZ * NX).reshape(NZ, NX)
DIRS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def build_graph(use_disc=True):
    rows, cols, vals = [], [], []
    for dj, di in DIRS:
        j0, i0 = slice(max(0, -dj), NZ - max(0, dj)), slice(max(0, -di), NX - max(0, di))
        j1, i1 = slice(max(0, dj), NZ - max(0, -dj)), slice(max(0, di), NX - max(0, -di))
        L = ST * math.hypot(dj, di)
        gr = np.abs(H[j1, i1] - H[j0, i0]) / L
        c = L * (1.0 + 40.0 * gr * gr + 400.0 * np.maximum(gr - 0.17, 0.0) ** 2 + 3.0 * SLOPE[j1, i1] ** 2) * mult[j1, i1] + add[j1, i1]
        if use_disc:
            c = c * disc[j1, i1]
        ok = ~blocked[j1, i1] & ~blocked[j0, i0]
        rows.append(IDX[j0, i0][ok])
        cols.append(IDX[j1, i1][ok])
        vals.append(c[ok])
    return sparse.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(NZ * NX, NZ * NX))


def snap(x, z):
    j0, i0 = int(round((z - Z0) / ST)), int(round((x - X0) / ST))
    best = None
    for rr in range(0, 7):
        for dj in range(-rr, rr + 1):
            for di in range(-rr, rr + 1):
                j, i = j0 + dj, i0 + di
                if 0 <= j < NZ and 0 <= i < NX and not blocked[j, i]:
                    d = dj * dj + di * di
                    if best is None or d < best[0]:
                        best = (d, j, i)
        if best:
            return best[1], best[2]
    raise ValueError('cannot snap %s,%s' % (x, z))


NODES = {
    'town1': (0, 0), 'town1_n': (0, -546), 'capital_s': (0, -1237), 'harbour': (-420, 1560), 'west_village': (-1248, 528),
    'elf_e': (-1300, -406), 'ruins_e': (760, 470), 'rusty': (1235, 1105), 'ring_temple': (1660, 1130), 'buried_temple': (2160, 1248),
    'ruined_castle': (-760, -980), 'alpine': (1585, -880), 'low_pass': (950, -1019), 'wizard_tower': (1380, -1250),
    'tarn_shore': (1560, -1420), 'dragon_a': (1800, -1290), 'dragon_b': (2100, -1260), 'gorge_s': (2450, -1250),
    'hidden_monastery': (2450, -1480), 'skull_city': (2250, -450), 'crater_rim': (1130, -300),
}
EDGES = [
    ('town1_n', 'capital_s', 'North road'), ('town1', 'harbour', 'South road'), ('town1', 'west_village', 'Farm road'),
    ('west_village', 'elf_e', 'Greenwood road'), ('town1', 'alpine', 'East road'),
    ('capital_s', 'low_pass', 'Gale Pass road'), ('alpine', 'low_pass', 'Lake shore road'), ('low_pass', 'wizard_tower', 'Roof road'),
    ('wizard_tower', 'tarn_shore', 'Tarn path'), ('tarn_shore', 'dragon_a', 'Cloud stair (carved switchback stair)', 'd'), ('alpine', 'dragon_a', 'Dragonback road (lower)', 'f'),
    ('dragon_a', 'dragon_b', 'Dragonback road (terraces)', 'f'),
    ('dragon_b', 'gorge_s', 'Dragonback road (east)', 'f'), ('gorge_s', 'hidden_monastery', 'Gorge crossing', 'd'), ('gorge_s', 'skull_city', 'Highland descent', 'f'),
    ('alpine', 'skull_city', 'Ash road'),
    ('town1', 'crater_rim', 'Crater spur'), ('town1', 'ruins_e', 'Old road'), ('ruins_e', 'rusty', 'Dune road'),
    ('rusty', 'ring_temple', 'Temple road'), ('ring_temple', 'buried_temple', 'Buried road'), ('elf_e', 'ruined_castle', 'Ruin road'),
    ('ruined_castle', 'capital_s', 'West gate road'), ('harbour', 'west_village', 'Coast road'), ('skull_city', 'crater_rim', 'Ember road'),
    ('rusty', 'harbour', 'Trade road'),
]


def bilinear(arr, xs, zs):
    return ndi.map_coordinates(arr, [(zs - Z0) / ST, (xs - X0) / ST], order=1, mode='nearest')


def resample(pts, ds):
    p = np.array(pts, np.float64)
    seg = np.hypot(np.diff(p[:, 0]), np.diff(p[:, 1]))
    s = np.concatenate([[0], np.cumsum(seg)])
    n = max(int(s[-1] / ds), 1)
    u = np.linspace(0, s[-1], n + 1)
    return np.interp(u, s, p[:, 0]), np.interp(u, s, p[:, 1]), u


def seg_hit(p1, p2, q1, q2):
    r = (p2[0] - p1[0], p2[1] - p1[1])
    s = (q2[0] - q1[0], q2[1] - q1[1])
    den = r[0] * s[1] - r[1] * s[0]
    if abs(den) < 1e-9:
        return None
    t = ((q1[0] - p1[0]) * s[1] - (q1[1] - p1[1]) * s[0]) / den
    u = ((q1[0] - p1[0]) * r[1] - (q1[1] - p1[1]) * r[0]) / den
    return t if (0 <= t <= 1 and 0 <= u <= 1) else None


def analyse(name, a, b, cells):
    pts = [(X0 + i * ST, Z0 + j * ST) for j, i in cells]
    pts[0], pts[-1] = NODES[a], NODES[b]
    px, pz, s = resample(T.chaikin(pts, 3), 24.0)
    h = bilinear(H, px, pz)
    n = len(px)
    ds = 24.0
    r = ndi.uniform_filter1d(h, 5, mode='nearest')
    gmax = 0.16
    for _ in range(3):
        for i in range(1, n):
            r[i] = min(max(r[i], r[i - 1] - gmax * ds), r[i - 1] + gmax * ds)
        for i in range(n - 2, -1, -1):
            r[i] = min(max(r[i], r[i + 1] - gmax * ds), r[i + 1] + gmax * ds)
    cut = h - r
    # hairpins: heading change above 110 degrees inside 150 studs
    hd = np.unwrap(np.arctan2(np.diff(pz), np.diff(px)))
    k = 6
    hairpins, last = 0, -99
    hp_pts = []
    for i in range(0, len(hd) - k):
        if abs(hd[i + k] - hd[i]) > math.radians(110) and i - last > k:
            hairpins += 1
            hp_pts.append([round(float(px[i + k // 2])), round(float(pz[i + k // 2]))])
            last = i
    tunnels, fills = [], []
    i = 0
    while i < n:
        if cut[i] > 22:
            j = i
            while j + 1 < n and cut[j + 1] > 22:
                j += 1
            if j - i + 1 >= 3:
                tunnels.append(dict(x0=round(float(px[i])), z0=round(float(pz[i])), x1=round(float(px[j])), z1=round(float(pz[j])), length=round((j - i + 1) * ds), depth=round(float(cut[i:j + 1].max()))))
            i = j + 1
        else:
            i += 1
    i = 0
    while i < n:
        if -cut[i] > 14:
            j = i
            while j + 1 < n and -cut[j + 1] > 14:
                j += 1
            if j - i + 1 >= 2:
                fills.append(dict(x0=round(float(px[i])), z0=round(float(pz[i])), x1=round(float(px[j])), z1=round(float(pz[j])), length=round((j - i + 1) * ds), height=round(float((-cut[i:j + 1]).max()))))
            i = j + 1
        else:
            i += 1
    # designed tunnel: the highest crest on a mountain road, when the ground rises 40+ studs above the road ends of a 192-stud window
    if h.max() >= 200 and not tunnels and n > 12:
        ip = int(np.argmax(h[4:n - 4])) + 4
        i0_, i1_ = max(ip - 4, 0), min(ip + 4, n - 1)
        base_ = min(h[i0_], h[i1_])
        if h[ip] - base_ >= 40:
            line = np.interp(np.arange(i0_, i1_ + 1), [i0_, i1_], [h[i0_], h[i1_]])
            tunnels.append(dict(x0=round(float(px[i0_])), z0=round(float(pz[i0_])), x1=round(float(px[i1_])), z1=round(float(pz[i1_])), length=round((i1_ - i0_) * ds), depth=round(float((h[i0_:i1_ + 1] - line).max())), designed=True))
    # cliff galleries: the road sits on a steep side slope for 96+ studs
    sl = bilinear(SLOPE, px, pz)
    ledges = []
    i = 0
    while i < n:
        if sl[i] >= 0.7:
            j = i
            while j + 1 < n and sl[j + 1] >= 0.7:
                j += 1
            if j - i + 1 >= 4:
                ledges.append(dict(x0=round(float(px[i])), z0=round(float(pz[i])), x1=round(float(px[j])), z1=round(float(pz[j])), length=round((j - i + 1) * ds)))
            i = j + 1
        else:
            i += 1
    # a long cliff gallery on a high mountain road is bored as a tunnel instead (designed): the road goes THROUGH the rock rib
    if h.max() >= 250 and not tunnels:
        for lg in ledges:
            if lg['length'] >= 120:
                tunnels.append(dict(x0=lg['x0'], z0=lg['z0'], x1=lg['x1'], z1=lg['z1'], length=lg['length'], depth=24, designed=True))
                ledges = [q for q in ledges if q is not lg]
                break
    bridges = []
    dense_x, dense_z, _ = resample(list(zip(px, pz)), 8.0)
    for rv in rivers:
        rp = T.chaikin(rv['pts'], 2)
        for q1, q2 in zip(rp[:-1], rp[1:]):
            for k2 in range(len(dense_x) - 1):
                t = seg_hit((dense_x[k2], dense_z[k2]), (dense_x[k2 + 1], dense_z[k2 + 1]), q1, q2)
                if t is not None:
                    x = dense_x[k2] + t * (dense_x[k2 + 1] - dense_x[k2])
                    z = dense_z[k2] + t * (dense_z[k2 + 1] - dense_z[k2])
                    hz = float(bilinear(H, np.array([x]), np.array([z]))[0])
                    ring = [bilinear(H, np.array([x + 90 * math.cos(a)]), np.array([z + 90 * math.sin(a)]))[0] for a in np.linspace(0, 6.28, 8, endpoint=False)]
                    relief = float(max(ring) - hz)
                    span = int(math.ceil((rv['w'] + 16) / 4.0) * 4)
                    gorge = None
                    for gg in spec['gorges']:
                        gp = T.chaikin(gg['pts'], 1)
                        dmin = min(math.hypot(x - qx, z - qz) for qx, qz in gp)
                        if dmin < gg['sigma'] * 1.3:
                            gorge = gg
                    if gorge is not None:
                        span = int(round(2.6 * gorge['sigma'] / 4.0) * 4)
                    near_capital = math.hypot(x, z + 1585) < 700 or math.hypot(x + 420, z - 1560) < 500
                    if max(hz, max(ring)) >= 150 and (gorge is not None or relief >= 25 or rv['name'].startswith(('ne_', 'meltwater'))):
                        kind = 'rope_suspension' if span >= 44 else 'timber_cantilever'
                    elif near_capital:
                        kind = 'towered_stone'
                    elif span >= 56:
                        kind = 'stone_viaduct'
                    else:
                        kind = 'stone_arch'
                    bridges.append(dict(x=round(float(x)), z=round(float(z)), river=rv['name'], span=span, kind=kind, ground=round(hz), heading=round(math.degrees(math.atan2(dense_z[k2 + 1] - dense_z[k2], dense_x[k2 + 1] - dense_x[k2])))))
    clean, seen = [], []
    for b2 in bridges:
        if not any(b2['river'] == q['river'] and math.hypot(b2['x'] - q['x'], b2['z'] - q['z']) < 50 for q in seen):
            seen.append(b2)
            clean.append(b2)
    g4 = [abs(h[i + 4] - h[i]) / (4 * ds) for i in range(0, n - 4)] or [0.0]
    return dict(name=name, a=a, b=b, length=round(float(s[-1])), top=round(float(h.max())), maxgrade=round(float(max(g4)), 2),
                climb=round(float(np.maximum(np.diff(r), 0).sum())), hairpins=hairpins, hairpin_pts=hp_pts, tunnels=tunnels, fills=fills, ledges=ledges, bridges=clean,
                pts=[[round(float(px[i])), round(float(pz[i])), round(float(h[i])), round(float(r[i]))] for i in range(0, n, 2)])


routes = []
for edge in EDGES:
    a, b, name = edge[:3]
    flags = edge[3] if len(edge) > 3 else ''
    if 'd' in flags:
        (xa, za), (xb, zb) = NODES[a], NODES[b]
        m = max(int(math.hypot(xb - xa, zb - za) / ST), 2)
        cells = [(int(round((za + (zb - za) * k / m - Z0) / ST)), int(round((xa + (xb - xa) * k / m - X0) / ST))) for k in range(m + 1)]
    else:
        G = build_graph(use_disc='f' not in flags)
        sj, si = snap(*NODES[a])
        tj, ti = snap(*NODES[b])
        dist, pred = dijkstra(G, directed=True, indices=int(IDX[sj, si]), return_predecessors=True)
        k = int(IDX[tj, ti])
        if not np.isfinite(dist[k]):
            print('NO ROUTE', name)
            continue
        cells = []
        while k >= 0:
            cells.append((k // NX, k % NX))
            k = pred[k]
        cells.reverse()
    routes.append(analyse(name, a, b, cells))
    for j, i in cells:
        disc[max(0, j - 1):j + 2, max(0, i - 1):i + 2] = np.minimum(disc[max(0, j - 1):j + 2, max(0, i - 1):i + 2], 0.55)

all_b, all_t = [], []
for rt in routes:
    for b2 in rt['bridges']:
        if not any(b2['river'] == q['river'] and math.hypot(b2['x'] - q['x'], b2['z'] - q['z']) < 60 for q in all_b):
            all_b.append(dict(b2, road=rt['name']))
    for t2 in rt['tunnels']:
        if not any(math.hypot(t2['x0'] - q['x0'], t2['z0'] - q['z0']) < 80 for q in all_t):
            all_t.append(dict(t2, road=rt['name']))
json.dump(dict(nodes=NODES, routes=routes, bridges=all_b, tunnels=all_t), open(HERE + r'\roads_v5.json', 'w'))

kinds = {}
for b2 in all_b:
    kinds[b2['kind']] = kinds.get(b2['kind'], 0) + 1
lines = ['# Roads v5: route table (offline search on the planned terrain)', '',
         'Least-cost routes on the 24-stud grid after the planned landform changes. Grade-limited profile (max 0.16) gives the cuts (tunnel when the cut is deeper than 22 studs for 72+ studs) and the fills (viaduct when the road stands 14+ studs above the ground for 48+ studs).', '',
         '| Road | From - to | Length | Top | Steepest 96 studs | Climb | Hairpins | Bridges | Tunnels | Cliff galleries | Viaduct fills |', '|---|---|---|---|---|---|---|---|---|---|---|']
for rt in routes:
    lines.append('| %s | %s - %s | %d | %d | %.2f | %d | %d | %d | %d | %d | %d |' % (rt['name'], rt['a'], rt['b'], rt['length'], rt['top'], rt['maxgrade'], rt['climb'], rt['hairpins'], len(rt['bridges']), len(rt['tunnels']), len(rt['ledges']), len(rt['fills'])))
lines += ['', 'Total new and reused road length: %d studs. Unique bridges: %d (%s). Tunnels: %d.' % (sum(r['length'] for r in routes), len(all_b), ', '.join('%s %d' % kv for kv in sorted(kinds.items())), len(all_t)), '', '## Bridges', '', '| Road | River | Kind | Span | Ground y | At (x, z) |', '|---|---|---|---|---|---|']
for b2 in sorted(all_b, key=lambda q: q['kind']):
    lines.append('| %s | %s | %s | %d | %d | (%d, %d) |' % (b2['road'], b2['river'], b2['kind'], b2['span'], b2['ground'], b2['x'], b2['z']))
lines += ['', '## Tunnels', '', '| Road | From | To | Length | Depth |', '|---|---|---|---|---|']
for t2 in all_t:
    lines.append('| %s | (%d, %d) | (%d, %d) | %d | %d |' % (t2['road'], t2['x0'], t2['z0'], t2['x1'], t2['z1'], t2['length'], t2['depth']))
open(HERE + r'\ROADS_V5.md', 'w').write('\n'.join(lines) + '\n')
print('\n'.join(lines))
