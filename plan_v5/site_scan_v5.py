"""site_scan_v5.py - offline terrain analysis for the world redesign (no Studio, no Blender).
Reads rebuild/v4/terrain_map.json (24-stud grid exported from Studio after the last terrain generation; heights are current,
some later paint changes are not in it) and rebuild/world.json. Writes plan_v5/terrain_stats.json and plan_v5/sites_candidates.json
and prints a short report.
Cell format in terrain_map.json: 5 chars = height (2 chars base36, minus 100), material letter, water level (2 chars base36 minus 100, or '--').
Materials: G grass, L leafy grass, S sand, M mud, R rock, T slate, B basalt, N snow, I ice, D ground, A sandstone, C cobble/brick, P pavement, K limestone, H salt.
"""
import json
import math
import os

import numpy as np
from scipy import ndimage as ndi

RB = r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild'
OUT = r'C:\Users\Nitro\.kiro\crew\workspace\town\plan_v5'
os.makedirs(OUT, exist_ok=True)
TM = json.load(open(RB + r'\v4\terrain_map.json'))
W = json.load(open(RB + r'\world.json'))
X0, Z0, STEP = TM['x0'], TM['z0'], TM['step']
NX = (TM['x1'] - X0) // STEP + 1
rows = TM['rows']
NZ = len(rows)
H = np.zeros((NZ, NX), np.float32)
Mt = np.empty((NZ, NX), dtype='<U1')
WL = np.full((NZ, NX), np.nan, np.float32)
for j, row in enumerate(rows):
    for i in range(NX):
        c = row[i * 5:i * 5 + 5]
        H[j, i] = int(c[0:2], 36) - 100
        Mt[j, i] = c[2]
        if c[3:5] != '--':
            WL[j, i] = int(c[3:5], 36) - 100
xs = X0 + STEP * np.arange(NX)
zs = Z0 + STEP * np.arange(NZ)
XX, ZZ = np.meshgrid(xs, zs)
water = (~np.isnan(WL)) & (WL > H - 0.5)
land = (H >= 3) & ~water
gz, gx = np.gradient(H, STEP)
slope = np.hypot(gx, gz)
relief7 = ndi.maximum_filter(H, size=7) - ndi.minimum_filter(H, size=7)      # 168-stud window
relief13 = ndi.maximum_filter(H, size=13) - ndi.minimum_filter(H, size=13)   # 312-stud window
print('grid %dx%d cells of %d studs, land cells %d (%.0f%% of grid)' % (NX, NZ, STEP, land.sum(), 100.0 * land.sum() / land.size))

CENTERS = {
    'NW forest / elf valley': (-1560, -400),
    'NE frozen highlands': (1500, -1250),
    'SE desert / badlands': (1700, 1150),
    'North: capital + castle': (0, -1800),
    'Centre: Town 1': (0, 0),
    'SW plains': (-1100, 800),
    'South: harbour': (-300, 1700),
    'East coast': (2500, -150),
}
names = list(CENTERS)
d2 = np.stack([(XX - CENTERS[n][0]) ** 2 + (ZZ - CENTERS[n][1]) ** 2 for n in names], axis=-1)
reg = np.argmin(d2, axis=-1)

GROUPS = {'green': 'GL', 'dirt/mud': 'DM', 'rock': 'RTB', 'sand/desert': 'SAH', 'snow/ice': 'NI', 'paved': 'PCK'}
stats = {}
land_total = int(land.sum())
print('\nREGION STATS (land only; Voronoi regions around the centres listed in CENTERS)')
print('%-26s %6s %5s %5s %5s | %5s %5s | flat%% varied%% | green rock sand snow' % ('region', 'land%', 'hP50', 'hP90', 'hMax', 'slP50', 'slP90'))
for k, n in enumerate(names):
    m = land & (reg == k)
    cnt = int(m.sum())
    if cnt == 0:
        continue
    h = H[m]
    s = slope[m]
    r7 = relief7[m]
    gl = np.isin(Mt[m], list('GL'))
    flat_green = float(np.mean(gl & (r7 <= 12)))
    sh = {g: float(np.mean(np.isin(Mt[m], list(v)))) for g, v in GROUPS.items()}
    stats[n] = {'land_share': cnt / land_total, 'h_p50': float(np.percentile(h, 50)), 'h_p90': float(np.percentile(h, 90)), 'h_max': float(h.max()),
                'slope_p50': float(np.percentile(s, 50)), 'slope_p90': float(np.percentile(s, 90)),
                'flat_share': float(np.mean(r7 <= 12)), 'varied_share': float(np.mean(r7 >= 60)), 'flat_green_share': flat_green, 'materials': sh}
    print('%-26s %5.1f%% %5.0f %5.0f %5.0f | %5.2f %5.2f | %4.0f%% %5.0f%% | %3.0f%% %3.0f%% %3.0f%% %3.0f%%  flat-green %3.0f%%' % (
        n, 100.0 * cnt / land_total, stats[n]['h_p50'], stats[n]['h_p90'], stats[n]['h_max'], stats[n]['slope_p50'], stats[n]['slope_p90'],
        100 * stats[n]['flat_share'], 100 * stats[n]['varied_share'], 100 * sh['green'], 100 * sh['rock'], 100 * sh['sand/desert'], 100 * sh['snow/ice'], 100 * flat_green))

# ---------------------------------------------------------------- candidate sites
pads = {p['name']: p for p in W['pads']}
pad_centres = [(p['cx'], p['cz']) for p in W['pads']] + [(0, 0)]


def far_from_pads(x, z, d):
    return all(math.hypot(x - px, z - pz) >= d for px, pz in pad_centres)


def pick(mask, score, k, min_sep):
    idx = np.argwhere(mask)
    if len(idx) == 0:
        return []
    order = sorted(idx.tolist(), key=lambda t: -float(score[t[0], t[1]]))
    out = []
    for j, i in order:
        x, z = float(xs[i]), float(zs[j])
        if all(math.hypot(x - o['x'], z - o['z']) >= min_sep for o in out):
            out.append({'x': int(x), 'z': int(z), 'h': round(float(H[j, i]), 1), 'slope': round(float(slope[j, i]), 3),
                        'relief168': round(float(relief7[j, i]), 1), 'relief312': round(float(relief13[j, i]), 1), 'mat': str(Mt[j, i])})
        if len(out) >= k:
            break
    return out


sites = {}
ne = names.index('NE frozen highlands')
tower = (1380, -1320)
near_tower = np.hypot(XX - tower[0], ZZ - tower[1]) < 350
sites['fortress_peak_candidates'] = pick(land & (reg == ne) & ~near_tower, H, 3, 450)
flatok = land & (relief13 <= 22) & (slope < 0.12) & (H >= 25) & (H <= 170)
far = np.vectorize(lambda x, z: far_from_pads(x, z, 520))(XX, ZZ)
sites['crater_candidates'] = pick(flatok & far & (np.abs(XX) < 2200), -(relief13 + 40 * slope), 3, 600)
se = names.index('SE desert / badlands')
desert = land & (reg == se) & np.isin(Mt, list('SAHD')) & (relief13 <= 26) & (np.hypot(XX - 1235, ZZ - 1105) > 380)
sites['desert_flat_candidates'] = pick(desert, -relief13, 3, 500)
maxf9 = ndi.maximum_filter(H, size=9)
drop = maxf9 - H
nwne = (reg == names.index('NW forest / elf valley')) | (reg == ne)
sites['cliff_base_candidates'] = pick(land & nwne & (drop >= 120) & (H < 90), drop, 4, 500)
sites['peaks_overall'] = pick(land, H, 8, 500)
# --- concept-map additions (30 Oct, "follow the top view"): skull zone on the east coast, farm village in the west
sea_mask = (~np.isnan(WL)) & (WL <= 1) & (H < -1)
sea_dist = ndi.distance_transform_edt(~sea_mask) * STEP
east_box = land & (XX >= 2100) & (XX <= 3150) & (ZZ >= -1300) & (ZZ <= -100)
sites['skull_cliff_candidates'] = pick(east_box & (sea_dist < 700), relief7, 3, 400)
sites['skull_city_floor_candidates'] = pick(east_box & (H >= 5) & (H <= 160), -(relief13 + 30 * slope), 3, 400)
wv = land & (np.hypot(XX + 1630, ZZ - 385) < 450) & (H >= 3) & (H <= 140)
sites['west_village_candidates'] = pick(wv, -(relief13 + 30 * slope), 3, 300)
sites['existing_pads'] = {n: {'x': p['cx'], 'z': p['cz'], 'y': p['ground'].get('y', p['ground'].get('y0'))} for n, p in pads.items()}
sites['lakes'] = [{'name': l['name'], 'x': l['cx'], 'z': l['cz'], 'rx': l['rx'], 'rz': l['rz'], 'level': l['level']} for l in W['lakes']]
sites['rivers'] = [{'name': r['name'], 'points': len(r.get('pts', [])), 'width': r.get('w')} for r in W['rivers']]

print('\nCANDIDATE SITES (24-stud grid, +-30 studs)')
for key in ('fortress_peak_candidates', 'crater_candidates', 'desert_flat_candidates', 'cliff_base_candidates', 'peaks_overall',
            'skull_cliff_candidates', 'skull_city_floor_candidates', 'west_village_candidates'):
    print(key)
    for s in sites[key]:
        print('   (%5d,%5d) h %5.0f slope %.2f relief168 %3.0f relief312 %3.0f mat %s' % (s['x'], s['z'], s['h'], s['slope'], s['relief168'], s['relief312'], s['mat']))
print('lakes:', [(l['name'], l['x'], l['z'], l['level']) for l in sites['lakes']])
print('land bbox x %d..%d z %d..%d' % (xs[np.where(land.any(axis=0))[0][[0, -1]]][0], xs[np.where(land.any(axis=0))[0][[0, -1]]][1],
                                      zs[np.where(land.any(axis=1))[0][[0, -1]]][0], zs[np.where(land.any(axis=1))[0][[0, -1]]][1]))

json.dump(stats, open(OUT + r'\terrain_stats.json', 'w'), indent=1)
json.dump(sites, open(OUT + r'\sites_candidates.json', 'w'), indent=1)
print('\nwrote terrain_stats.json and sites_candidates.json')
