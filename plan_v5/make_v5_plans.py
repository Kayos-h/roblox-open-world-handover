"""make_v5_plans.py - DRAFT placement plans for the v5 models, written to town\\mapplan\\ in the format build_v4.ps1 reads.

Every plan is { area, note, placements: [ {model, x, z, rot, group, y_offset?, scale?, note?} ] }.
  rot: 0 = front faces +Z (south), 90 = +X (east), 180 = -Z (north), 270 = -X. Models whose long axis is X (bridges, walls) use along(heading).
  y_offset: studs above the terrain surface at (x, z) (place_v4.luau raycasts onto Terrain), used for tower floors, canopy villages, floating rocks.
Sites come from the Bible (sites_candidates.json, world_v5_terrain.json, roads_v5.json). The Town 1 zone is skipped by build_v4.ps1 unless the area name starts with 'town1'.
These are drafts on the EXPORTED terrain; the first Studio run re-seats everything on the live ground (reseat_env.luau) and checks it (verify_folders.luau).
Run: python make_v5_plans.py   -> plans, PLACEMENT_V5.md, plan_overlay_items_v5.jpg
"""
import csv
import glob
import json
import math
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as ndi
from scipy.spatial import cKDTree

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import terrain_v5 as T

TOWN, HERE = T.TOWN, T.HERE
PLAN_DIR = TOWN + r'\mapplan'
rnd = random.Random(2026)

# ------------------------------------------------------------------ manifest and library
rows = list(csv.DictReader(open(HERE + r'\V5_MANIFEST.csv', encoding='utf-8-sig')))
IDS = {}
for r_ in rows:
    IDS.setdefault(r_['row'], []).append(r_['id'])
V5 = {r_['id']: r_ for r_ in rows}
meta4 = json.load(open(TOWN + r'\library\v4_meta.json'))
old_ids = {r_['name'] for r_ in csv.DictReader(open(TOWN + r'\asset_ids.csv', encoding='utf-8-sig'))}
KNOWN = set(V5) | set(meta4) | old_ids


def ids(code):
    return IDS[code]


# ------------------------------------------------------------------ planned terrain
grid = T.load_grid()
world = T.load_world()
spec = T.load_spec(grid)
X, Z = T.grid_xz(grid)
WET = (grid['W'] > -900) & (grid['W'] > grid['H'] - 0.5)
SEA = WET & (grid['W'] <= 1.0) & (grid['H'] < -1.0)
HP = T.apply_spec(grid['H'], X, Z, spec, ~WET)
gy_, gx_ = np.gradient(HP, grid['step'])
SL = np.hypot(gx_, gy_)
MAT = grid['M']
X0, Z0, ST = grid['x0'], grid['z0'], grid['step']
NZ, NX = HP.shape
LAKES = world['lakes']
CODES = 'GLSMRTBNIDACPKH'


def cell(x, z):
    return int(round((z - Z0) / ST)), int(round((x - X0) / ST))


def inb(j, i):
    return 0 <= j < NZ and 0 <= i < NX


def hgt(x, z):
    return float(ndi.map_coordinates(HP, [[(z - Z0) / ST], [(x - X0) / ST]], order=1, mode='nearest')[0])


def in_lake(x, z, grow=1.25):
    return any(((x - l['cx']) / (l['rx'] * grow + 20)) ** 2 + ((z - l['cz']) / (l['rz'] * grow + 20)) ** 2 < 1.0 for l in LAKES)


def ok(x, z, max_slope=0.45, min_h=2.0):
    j, i = cell(x, z)
    return inb(j, i) and not WET[j, i] and HP[j, i] >= min_h and SL[j, i] <= max_slope and not in_lake(x, z)


def in_town1(x, z):
    return -318 <= x <= 318 and -545 <= z <= 311


def mat_at(x, z):
    j, i = cell(x, z)
    return CODES[MAT[j, i] - 1] if inb(j, i) and MAT[j, i] > 0 else 'E'


def face(x0, z0, x1, z1):
    return math.degrees(math.atan2(x1 - x0, z1 - z0)) % 360


def along(heading):
    return (-heading) % 360


# ------------------------------------------------------------------ what is already in the map (avoid overlaps)
def fp_of(model):
    m = meta4.get(model)
    return max(m['size'][0], m['size'][2]) if m and m.get('size') else None


def load_existing():
    """Positions of the BIG things already planned (houses, towers, big trees, rocks); small plants are cleared in Studio per footprint."""
    P_ = []
    for f in glob.glob(PLAN_DIR + r'\*.json'):
        b = os.path.basename(f)
        if b.startswith('v5_') or b == 'town1_v5.json':
            continue
        try:
            d_ = json.load(open(f, encoding='utf-8-sig'))
        except Exception:
            continue
        items_ = d_.get('placements') if isinstance(d_, dict) else None
        if isinstance(items_, list):
            for it in items_:
                if isinstance(it, dict) and 'x' in it and 'z' in it and not it.get('skip'):
                    fp = fp_of(it.get('model'))
                    if fp is not None and fp < 16:
                        continue
                    P_.append((float(it['x']), float(it['z'])))
    return np.array(P_, dtype=np.float32) if P_ else np.zeros((0, 2), np.float32)


EX = load_existing()
EXT = cKDTree(EX) if len(EX) else None
NEW = []


def free(x, z, d):
    if EXT is not None and EXT.query_ball_point([x, z], d):
        return False
    return not any((x - a) ** 2 + (z - b) ** 2 < d * d for a, b in NEW)


# ------------------------------------------------------------------ roads from the router
ROADS = json.load(open(HERE + r'\roads_v5.json'))
RT = {r_['name']: r_ for r_ in ROADS['routes']}


def rpts(name):
    return [(p[0], p[1]) for p in RT[name]['pts']]


def at(name, t, off=0.0):
    p = rpts(name)
    seg = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(p[:-1], p[1:])]
    d_ = t * sum(seg)
    for k, s in enumerate(seg):
        if d_ <= s or k == len(seg) - 1:
            u = min(max(d_ / s, 0), 1) if s else 0
            a, b = p[k], p[k + 1]
            th = math.atan2(b[1] - a[1], b[0] - a[0])
            return a[0] + (b[0] - a[0]) * u - math.sin(th) * off, a[1] + (b[1] - a[1]) * u + math.cos(th) * off, math.degrees(th)
        d_ -= s


def tangent_near(name, x, z):
    p = rpts(name)
    k = min(range(len(p) - 1), key=lambda i: (p[i][0] - x) ** 2 + (p[i][1] - z) ** 2)
    return math.degrees(math.atan2(p[k + 1][1] - p[k][1], p[k + 1][0] - p[k][0]))


# ------------------------------------------------------------------ plan container
class Plan:
    def __init__(self, area, note=''):
        self.area, self.note, self.items = area, note, []

    def add(self, model, x, z, rot=0.0, group='Misc', yo=None, scale=None, note=None):
        if model not in KNOWN:
            raise ValueError('unknown model ' + model)
        it = {'model': model, 'x': round(float(x), 1), 'z': round(float(z), 1), 'rot': round(float(rot) % 360, 1), 'group': group}
        if yo:
            it['y_offset'] = round(float(yo), 1)
        if scale:
            it['scale'] = scale
        if note:
            it['note'] = note
        v = V5.get(model)
        if v and not yo and group != 'WizardTowerInterior':
            cr = max(float(v['size_x']), float(v['size_z'])) / 2 + 4
            if cr > 9:
                it['cr'] = round(cr)      # clear small plants inside this radius before placing (Studio footprint pass)
        self.items.append(it)
        NEW.append((float(x), float(z)))
        return it

    def near(self, model, x, z, rot=0.0, group='Misc', d=16, clear=12, max_r=150, max_slope=0.45, face_to=None, **kw):
        """Place at (x, z) or the closest free, flat land spot within max_r. Returns None (and counts a miss) if there is none."""
        why = {'ground': 0, 'busy': 0}
        for rr in [0] + list(range(int(d), int(max_r) + 1, int(d))):
            for a in ([0] if rr == 0 else [k * math.tau / 8 + rr * 0.3 for k in range(8)]):
                px_, pz_ = x + rr * math.cos(a), z + rr * math.sin(a)
                if not ok(px_, pz_, max_slope):
                    why['ground'] += 1
                    continue
                if not free(px_, pz_, clear):
                    why['busy'] += 1
                    continue
                rr_ = face(px_, pz_, *face_to) if face_to else rot
                return self.add(model, px_, pz_, rr_, group, **kw)
        MISSES.append((self.area, model, round(x), round(z), why))
        return None

    def save(self):
        with open(PLAN_DIR + '\\' + self.area + '.json', 'w') as f:
            f.write('{"area":%s,"note":%s,"placements":[\n' % (json.dumps(self.area), json.dumps(self.note)))
            f.write(',\n'.join(json.dumps(i, separators=(',', ':')) for i in self.items))
            f.write('\n]}\n')


MISSES = []
PLANS = []


def scatter(plan, models, n, box, group, accept=None, min_d=40, clear=12, max_slope=0.4, tries=60000, yo=None, rot_fn=None, near_roads=None):
    """n placements, cycling through `models`, random inside box=(x0,x1,z0,z1) on ok land, at least min_d apart from each other."""
    mine = []
    t = 0
    while len(mine) < n and t < tries:
        t += 1
        x, z = rnd.uniform(box[0], box[1]), rnd.uniform(box[2], box[3])
        if near_roads is not None:
            nm_ = rnd.choice(near_roads)
            x, z, hd = at(nm_, rnd.random(), rnd.choice((-1, 1)) * rnd.uniform(18, 48))
        if in_town1(x, z) and not plan.area.startswith('town1'):
            continue
        if not ok(x, z, max_slope) or not free(x, z, clear):
            continue
        if accept and not accept(x, z):
            continue
        if any((x - a) ** 2 + (z - b) ** 2 < min_d * min_d for a, b in mine):
            continue
        mine.append((x, z))
        plan.add(models[len(mine) % len(models)], x, z, rot_fn(x, z) if rot_fn else rnd.uniform(0, 360), group, yo=yo)
    if len(mine) < n:
        MISSES.append((plan.area, models[0], 'only %d of %d' % (len(mine), n), ''))
    return mine


# ------------------------------------------------------------------ coast helpers
smooth_sea = ndi.gaussian_filter(SEA.astype(np.float32), 2.0)
sgy, sgx = np.gradient(smooth_sea)
land_edge = (~WET) & (HP > 3) & ndi.binary_dilation(SEA, iterations=2)


def coast_points(n, min_sep, cond=None):
    js, is_ = np.nonzero(land_edge)
    order = list(range(len(js)))
    rnd.shuffle(order)
    out = []
    for k in order:
        x, z = X0 + is_[k] * ST, Z0 + js[k] * ST
        if in_town1(x, z) or (cond and not cond(x, z, js[k], is_[k])):
            continue
        if any(math.hypot(x - a, z - b) < min_sep for a, b, _ in out):
            continue
        dx, dz = sgx[js[k], is_[k]], sgy[js[k], is_[k]]
        if abs(dx) + abs(dz) < 1e-6:
            continue
        out.append((x, z, face(x, z, x + dx, z + dz)))
        if len(out) >= n:
            break
    return out


def sea_spot(cx, cz, rmin, rmax, dmin, dmax, tries=400):
    for _ in range(tries):
        a, r = rnd.uniform(0, math.tau), rnd.uniform(rmin, rmax)
        x, z = cx + r * math.cos(a), cz + r * math.sin(a)
        j, i = cell(x, z)
        if inb(j, i) and SEA[j, i] and dmin <= -HP[j, i] <= dmax and free(x, z, 60):
            return x, z
    return None


# =================================================================================================== plans
def himalaya():
    P = Plan('v5_himalaya', 'Wizard tower complex (exterior and interior ring placements), Roof Plateau dressing, peaks, ice features, hidden monastery, fortress parts. Groups: WizardTower, WizardTowerInterior, Himalaya. Interior items use y_offset = floor height above the plateau ground.')
    tw = spec['plateau']['tower']
    TX, TZ = tw['x'], tw['z']
    P.add(ids('WT01')[0], TX, TZ, 0, 'WizardTower')
    P.add(ids('WT02')[0], TX, TZ, 0, 'WizardTowerInterior')
    P.add(ids('WT12')[0], TX, TZ + 52, 0, 'WizardTower')
    P.add(ids('WT11')[0], TX, TZ, 0, 'WizardTower', yo=262)
    P.add(ids('WT10')[0], TX, TZ, 0, 'WizardTowerInterior', yo=232)
    P.add(ids('WT05')[0], TX, TZ, 0, 'WizardTowerInterior', note='THE CIRCULAR MAP, Map Hall centre')
    P.add(ids('WT06')[0], TX, TZ, 0, 'WizardTowerInterior', yo=0.3)
    for k, dx in enumerate((-14, 14)):
        P.add(ids('WT09')[k], TX + dx, TZ, 0, 'WizardTowerInterior', yo=30)

    def ring_items(codes, R_, n, a0, yo, note=None):
        for k in range(n):
            a = math.radians(a0 + k * 360.0 / n)
            x, z = TX + R_ * math.cos(a), TZ + R_ * math.sin(a)
            P.add(codes[k % len(codes)], x, z, face(x, z, TX, TZ), 'WizardTowerInterior', yo=yo, note=note)

    ring_items(ids('WT03'), 41, 12, 15, 0.1)
    ring_items(ids('WT03'), 39, 12, 15, 40)
    ring_items(ids('WT04')[1:], 22, 4, 45, 40)
    ring_items(ids('WT03'), 36, 12, 15, 72)
    ring_items(ids('WT04')[1:], 22, 2, 90, 72)
    ring_items(ids('WT04')[:1], 30, 6, 30, 104)
    ring_items(ids('WT07'), 24, 4, 45, 136)
    ring_items(ids('WT08'), 20, 3, 90, 168)
    P.add(ids('WT07')[2], TX + 6, TZ, 0, 'WizardTowerInterior', yo=200)
    P.add(ids('WT09')[0], TX, TZ, 0, 'WizardTowerInterior', yo=228)
    t13 = ids('WT13')
    for mdl, dx, dz, rt in ((t13[2], 0, 100, 0), (t13[0], 98, 24, 90), (t13[1], -98, 24, 270), (t13[3], 72, 78, 0), (t13[4], -72, 84, 0), (t13[5], 26, 68, 0)):
        P.add(mdl, TX + dx, TZ + dz, rt, 'Himalaya')
    # prayer-flag strings: tarn outlet bridge, plateau east rim, low pass, monastery
    for mdl, (x, z) in zip(ids('HM07'), ((1552, -1418), (1560, -1262), (950, -1030), (2450, -1462))):
        P.near(mdl, x, z, 0, 'Himalaya', max_slope=1.2)
    # cairns on hairpins
    hp = RT['Roof road']['hairpin_pts'][:2] + RT['Dragonback road (lower)']['hairpin_pts'][:1] + RT['Dragonback road (terraces)']['hairpin_pts'][:1]
    for mdl, (x, z) in zip(ids('HM08'), hp + [(940, -1000)] * 4):
        P.near(mdl, x + 14, z + 10, rnd.uniform(0, 360), 'Himalaya', max_slope=1.2)
    # hidden monastery beyond Frost Gorge
    for mdl, (x, z, rt) in zip(ids('HM09'), ((2450, -1505, 0), (2408, -1470, 90), (2494, -1466, 270), (2450, -1448, 180))):
        P.near(mdl, x, z, rt, 'Himalaya', max_slope=0.8)
    # ice, glacier, caves, shrine, tower, mines
    for mdl, (x, z) in zip(ids('HL01'), ((1520, -1560), (1640, -1545), (1600, -1612), (1500, -1625))):
        P.near(mdl, x, z, rnd.uniform(0, 360), 'Himalaya', max_slope=1.5, clear=20)
    for mdl, (x, z) in zip(ids('HL02'), ((1760, -1880), (1300, -2010))):
        P.near(mdl, x, z, rnd.uniform(0, 360), 'Himalaya', max_slope=1.5, clear=40)
    for mdl, (x, z) in zip(ids('HL03'), ((1480, -1770), (1720, -1770), (1240, -1860))):
        P.near(mdl, x, z, rnd.uniform(0, 360), 'Himalaya', max_slope=1.5, clear=40)
    for mdl, (x, z) in zip(ids('HL04'), ((1540, -1870), (1250, -2040))):
        P.near(mdl, x, z, rnd.uniform(0, 360), 'Himalaya', max_slope=1.6, clear=30)
    P.near(ids('HL05')[0], 940, -1030, 90, 'Himalaya')
    x, z, _ = at('Roof road', 0.3, 30)
    P.near(ids('HL06')[0], x, z, face(x, z, 1380, -1320), 'Himalaya', max_slope=0.9)
    for mdl, (x, z) in zip(ids('HL07'), ((1000, -1450), (1150, -1555))):
        P.near(mdl, x, z, rnd.uniform(0, 360), 'Himalaya', max_slope=1.6)
    for mdl, pk in zip(ids('SP01'), spec['peaks']):
        P.add(mdl, pk['x'], pk['z'], rnd.uniform(0, 360), 'Himalaya', note='peak ' + pk['name'])
    # Frosthold fortress on its flank and the parts that climb it
    fx, fz = 1632, -1608
    P.add(ids('LM03')[0], fx, fz, face(fx, fz, tw['x'], tw['z']), 'Himalaya')
    for mdl, (dx, dz) in zip(ids('LM04'), ((-32, 48), (-58, 88), (-84, 128))):
        P.add(mdl, fx + dx, fz + dz, face(fx + dx, fz + dz, tw['x'], tw['z']), 'Himalaya')
    for mdl, (dx, dz) in zip(ids('LM05'), ((62, 24), (-70, -34))):
        P.add(mdl, fx + dx, fz + dz, face(fx, fz, fx + dx, fz + dz), 'Himalaya')
    P.add(ids('LM06')[0], fx - 4, fz + 40, face(fx, fz, tw['x'], tw['z']), 'Himalaya')
    for mdl, t in zip(ids('LM07'), (0.3, 0.7)):
        x, z, hd = at('Cloud stair (carved switchback stair)', t)
        P.add(mdl, x, z, along(hd), 'Himalaya')
    P.add(ids('LM08')[0], 1505, -1236, along(tangent_near('Tarn path', 1505, -1236) + 90), 'Himalaya', note='stone span over Meltwater Notch')
    return P


def road_works():
    P = Plan('v5_roads', 'Bridges, tunnel portals and lining, cliff galleries, switchback walls, watchtowers, camps, waystations, trading posts, battlefield props, abandoned houses, viaducts. Long-axis-X models use rot = -heading. Groups: Bridges, Tunnels, RoadWorks, RoadLife.')
    kinds = {}
    for b in ROADS['bridges']:
        rt = along(b['heading'])
        k = b['kind']
        if k == 'rope_suspension':
            mdl = ids('HM01')[0 if b['span'] <= 70 else (1 if b['span'] <= 100 else 2)]
        elif k == 'timber_cantilever':
            mdl = ids('HM02')[0 if b['span'] <= 32 else 1]
        elif k == 'towered_stone' and b['z'] < -500:
            mdl = ids('CP19')[0]
        elif k == 'towered_stone':
            mdl = 'F08_03_stone_bridge_double'
        else:
            mdl = 'F08_01_stone_bridge_arch'
        if (b['x'], b['z']) == (355, -883):
            mdl = ids('CP19')[1]
        kinds[mdl] = kinds.get(mdl, 0) + 1
        P.add(mdl, b['x'], b['z'], rt, 'Bridges', note='%s over %s, span %d' % (k, b['river'], b['span']))
    for ti, t_ in enumerate(sorted(ROADS['tunnels'], key=lambda q: -hgt(q['x0'], q['z0']))):
        hd = math.degrees(math.atan2(t_['z1'] - t_['z0'], t_['x1'] - t_['x0']))
        pm = ids('HM03')[[1, 2, 0][ti % 3]]
        P.add(pm, t_['x0'], t_['z0'], face(t_['x1'], t_['z1'], t_['x0'], t_['z0']), 'Tunnels', note='needs terrain carve, %d long' % t_['length'])
        P.add(pm, t_['x1'], t_['z1'], face(t_['x0'], t_['z0'], t_['x1'], t_['z1']), 'Tunnels')
        n = max(int(t_['length'] / 24) - 2, 0)
        for k in range(n):
            u = (k + 1.5) / (n + 3)
            mdl = ids('HM04')[1 if (t_['length'] >= 200 and k == n // 2) else 0]
            P.add(mdl, t_['x0'] + (t_['x1'] - t_['x0']) * u, t_['z0'] + (t_['z1'] - t_['z0']) * u, along(hd), 'Tunnels')
    # scenic Himalayan bridges in the hidden monastery pocket and on the Dragonback road (optional extras that use the other kit variants)
    for mdl, (nm_, t, off) in zip((ids('HM01')[0], ids('HM01')[1]), (('Gorge crossing', 0.9, 30), ('Highland descent', 0.1, 20))):
        x, z, hd = at(nm_, t, off)
        P.add(mdl, x, z, along(hd + 90), 'Bridges', note='scenic rope bridge over a side gully, optional')
    x, z, hd = at('Dragonback road (terraces)', 0.5, 22)
    P.add(ids('HM02')[1], x, z, along(hd + 90), 'Bridges', note='scenic timber cantilever over a stream, optional')
    gal = 0
    for rt_ in ROADS['routes']:
        for lg in rt_['ledges']:
            n = max(int(round(lg['length'] / 40)), 1)
            hd = math.degrees(math.atan2(lg['z1'] - lg['z0'], lg['x1'] - lg['x0']))
            for k in range(n):
                u = (k + 0.5) / n
                P.add(ids('HM05')[gal % 2], lg['x0'] + (lg['x1'] - lg['x0']) * u, lg['z0'] + (lg['z1'] - lg['z0']) * u, along(hd), 'RoadWorks')
                gal += 1
        for k, (x, z) in enumerate(rt_['hairpin_pts']):
            if hgt(x, z) > 120:
                hd = tangent_near(rt_['name'], x, z)
                P.add(ids('HM06')[k % 3], x, z, along(hd), 'RoadWorks')
    # watchtowers: two intact on the mountain roads, two ruined on the plains
    for k, (nm_, t, off, ruined) in enumerate((('Gale Pass road', 0.95, 40, 0), ('Roof road', 0.35, 30, 0), ('Old road', 0.85, 40, 1), ('Coast road', 0.5, 35, 1))):
        x, z, hd = at(nm_, t, off)
        P.near(ids('RD01')[k], x, z, face(x, z, *at(nm_, t)[:2]), 'RoadLife', max_slope=0.8)
    for k, (nm_, t) in enumerate((('Farm road', .5), ('Trade road', .4), ('Old road', .6), ('Greenwood road', .5), ('Ash road', .5), ('Dune road', .5))):
        x, z, hd = at(nm_, t, rnd.choice((-1, 1)) * 34)
        P.near(ids('RD02')[k], x, z, rnd.uniform(0, 360), 'RoadLife')
    for mdl, (nm_, t) in zip(ids('RD03'), (('Gale Pass road', 1.0), ('East road', .5))):
        x, z, hd = at(nm_, t, 32)
        P.near(mdl, x, z, along(hd) + 90, 'RoadLife')
    for mdl, (nm_, t) in zip(ids('RD04'), (('Trade road', .5), ('South road', .35))):
        x, z, hd = at(nm_, t, -34)
        P.near(mdl, x, z, along(hd) + 90, 'RoadLife')
    cx, cz, _ = at('Old road', 0.8, 52)
    for k, mdl in enumerate(ids('RD05')):
        P.near(mdl, cx + rnd.uniform(-45, 45), cz + rnd.uniform(-45, 45), rnd.uniform(0, 360), 'RoadLife', d=10, clear=8)
    for mdl, (nm_, t) in zip(ids('RD06'), (('Dune road', .3), ('Trade road', .2), ('Ember road', .5), ('Coast road', .6), ('Farm road', .7))):
        x, z, hd = at(nm_, t, rnd.choice((-1, 1)) * 48)
        P.near(mdl, x, z, rnd.uniform(0, 360), 'RoadLife')
    fills = sorted([(f_['length'], f_, r_['name']) for r_ in ROADS['routes'] for f_ in r_['fills']], key=lambda q: -q[0])
    for mdl, (ln, f_, nm_) in zip(ids('BR01'), fills[:2]):
        mx, mz = (f_['x0'] + f_['x1']) / 2, (f_['z0'] + f_['z1']) / 2
        P.add(mdl, mx, mz, along(math.degrees(math.atan2(f_['z1'] - f_['z0'], f_['x1'] - f_['x0']))), 'Bridges', note='viaduct on %s, fill %d high' % (nm_, f_['height']))
    return P


def entrances():
    P = Plan('v5_entrances', 'Natural entrances: one village sign and (for four of them) a boulder pair per settlement. The plain arch is removed, not replaced. Groups: Entrances.')
    S = ids('NE01')
    for mdl, (x, z, rt) in zip(S, ((18, -530, 180), (-1290, -392, 90), (1470, -902, 270), (1160, 1010, 225), (-385, 1400, 180), (1640, 1100, 270))):
        P.near(mdl, x, z, rt, 'Entrances', d=10, clear=6)
    for mdl, (x, z, rt) in zip(ids('NE02'), ((-1318, -400, 90), (1448, -914, 270), (1138, 1000, 225), (2222, -472, 200))):
        P.near(mdl, x, z, rt, 'Entrances', d=12, clear=6)
    return P


def capital():
    P = Plan('v5_capital', 'Ring wall (12 towers on an ellipse centre (0,-1585) 490 x 350), gates, plateau complex, skyline towers, order HQ, plaza, townhouses. Before placing: archive the old capital wall, gates and houses inside the ring (group CapitalHouses and the B02/C04/K08 pieces). Groups: CapitalWall, CapitalGate, CapitalPlateau, CapitalSkyline, CapitalHouses, CapitalPlaza.')
    CX, CZ, RX, RZ = 0.0, -1585.0, 490.0, 350.0
    ang = [15 + 30 * k for k in range(12)]
    V = [(CX + RX * math.cos(math.radians(a)), CZ + RZ * math.sin(math.radians(a))) for a in ang]
    gates = {'S': (0.0, -1240.0), 'N': (0.0, -1930.0)}
    wt = math.radians(132.3)
    water_gate = (CX + RX * math.cos(wt), CZ + RZ * math.sin(wt))
    sizes = [3, 1, 2, 1, 0, 1, 3, 1, 2, 1, 0, 1]
    for k, (x, z) in enumerate(V):
        P.add(ids('CP04')[sizes[k]], x, z, face(CX, CZ, x, z), 'CapitalWall')
        P.add(ids('CP02')[k % 3], x, z, face(CX, CZ, x, z), 'CapitalWall')
    for k in range(12):
        (xa, za), (xb, zb) = V[k], V[(k + 1) % 12]
        L = math.hypot(xb - xa, zb - za)
        n = max(int(round((L - 26) / 40)), 1)
        hd = math.degrees(math.atan2(zb - za, xb - xa))
        for s in range(n):
            u = (s + 0.5) / n
            x, z = xa + (xb - xa) * (0.5 * 26 / L + u * (1 - 26 / L)), za + (zb - za) * (0.5 * 26 / L + u * (1 - 26 / L))
            if abs(x - gates['S'][0]) < 78 and z > -1300:
                continue
            if abs(x - gates['N'][0]) < 40 and z < -1880:
                continue
            if math.hypot(x - water_gate[0], z - water_gate[1]) < 36:
                continue
            P.add(ids('CP01')[(k + s) % 3], x, z, along(hd), 'CapitalWall')
    P.add(ids('CP07')[0], gates['S'][0], gates['S'][1], 0, 'CapitalGate')
    for k, dx in enumerate((-48, 48)):
        P.add(ids('CP06')[k], dx, -1244, 0, 'CapitalGate')
    for k, dx in enumerate((-92, 92)):
        P.add(ids('CP03')[k], dx, -1256, 0 if dx < 0 else 0, 'CapitalGate')
    for k, dx in enumerate((-34, 34)):
        P.add(ids('CP05')[k], dx, gates['N'][1] + 6, 180, 'CapitalGate', note='north gate: open passage, turrets only')
    P.add(ids('CP08')[0], water_gate[0], water_gate[1], face(CX, CZ, *water_gate), 'CapitalGate')
    # plateau complex
    P.add(ids('CP09')[0], 0, -2275, 0, 'CapitalPlateau')
    for k, dx in enumerate((-95, 95)):
        P.add(ids('CP10')[k], dx, -2262, 0, 'CapitalPlateau')
    for k, dx in enumerate((-150, 150)):
        P.add(ids('CP11')[k], dx, -2150, 0, 'CapitalPlateau')
    for k, dx in enumerate((-120, 120)):
        P.add(ids('CP12')[k], dx, -2010, 0, 'CapitalPlateau')
    P.add(ids('CP13')[0], 0, -2030, 0, 'CapitalPlateau', note='town to terrace')
    P.add(ids('CP13')[1], 0, -2110, 0, 'CapitalPlateau', note='terrace to keep')
    for mdl, (x, z) in zip(ids('CP14'), ((0, -1700), (250, -1750), (-260, -1740), (440, -1585), (-300, -1400))):
        P.add(mdl, x, z, face(x, z, 0, -1585), 'CapitalSkyline')
    for k, (x, z) in enumerate(((190, -1570), (244, -1498), (244, -1642))):
        P.add(ids('CP15')[k], x, z, face(x, z, 0, -1560), 'CapitalPlaza', note='order compound: main hall and two annexes')
    P.add(ids('CP17')[0], 0, -1560, 0, 'CapitalPlaza', note='plaza monument')
    P.add(ids('CP17')[1], 0, -2150, 0, 'CapitalPlateau', note='royal garden feature')
    for mdl, (x, z) in zip(ids('CP18'), ((-700, -1600), (-690, -1480), (700, -1650), (690, -1530))):
        P.add(mdl, x, z, along(90), 'CapitalWall', note='quay wall on the river bank')
    # townhouses: spaced, off the avenues and the plaza, facing the plaza
    n = 0
    t = 0
    houses = []
    while n < 110 and t < 30000:
        t += 1
        a, u = rnd.uniform(0, math.tau), math.sqrt(rnd.uniform(0.02, 0.84))
        x, z = CX + RX * 0.92 * u * math.cos(a), CZ + RZ * 0.92 * u * math.sin(a)
        if math.hypot(x, z + 1560) < 100 or (abs(x) < 16 and z > -1560) or (abs(z + 1560) < 16 and abs(x) < 440):
            continue
        if abs(x - 190) < 60 and abs(z + 1570) < 50:
            continue
        if any(math.hypot(x - sx, z - sz) < 34 for sx, sz in houses):
            continue
        if not ok(x, z, 0.5, 5):
            continue
        houses.append((x, z))
        P.add(ids('CP16')[n % 12], x, z, face(x, z, 0, -1560), 'CapitalHouses')
        n += 1
    return P


def elf():
    P = Plan('v5_elf', 'Second house ring, canopy villages around the world tree, path pieces, moss and tree-side details. No glow. Groups: ElfHouses, ElfCanopy, ElfPaths.')
    tx, tz = -1560, -430
    n = 0
    for k in range(8):
        for jitter in range(12):
            a = math.radians(k * 45 + 10 + jitter * 7)
            r = 270 + (k % 3) * 24
            x, z = tx + r * math.cos(a), tz + r * math.sin(a)
            if ok(x, z, 0.4) and free(x, z, 10):
                P.add(ids('EV01')[n], x, z, face(x, z, tx, tz), 'ElfHouses', note='clear plants inside the footprint first')
                n += 1
                break
        else:
            MISSES.append(('v5_elf', ids('EV01')[k], 'no spot', ''))
    for k, (a, yo) in enumerate(((20, 100), (140, 120), (260, 140))):
        x, z = tx + 78 * math.cos(math.radians(a)), tz + 78 * math.sin(math.radians(a))
        P.add(ids('EV02')[k], x, z, face(x, z, tx, tz), 'ElfCanopy', yo=yo, note='canopy village, ladders to the ground')
    ev3 = ids('EV03')
    for mdl, (x, z, rt) in zip(ev3, ((-1500, -430, 90), (-1462, -482, 90), (-1695, -618, 60), (-1520, -560, 0), (-1470, -520, 0), (-1570, -615, 0))):
        P.near(mdl, x, z, rt, 'ElfPaths', d=8, clear=5, max_slope=0.7)
    return P


def town1():
    P = Plan('town1_v5', 'Town 1: hero statue, street life, avenue braziers and banner poles. Additive only; the old plaza prop at the centre is archived first (Town1_Removed). Groups: town1_.')
    P.add(ids('TW01')[0], 0, 0, 0, 'town1_statue', note='check the old plaza prop first')
    anchors = [(-62, -42), (62, -42), (-92, 8), (92, 8), (-48, 66), (48, 66), (0, -84), (0, 94)]
    for mdl, (x, z) in zip(ids('TW02'), anchors):
        P.near(mdl, x, z, face(x, z, 0, 0), 'town1_life', d=8, clear=5, max_slope=0.6)
    tw3 = ids('TW03')
    for mdl, (x, z) in zip(tw3, ((-14, -330), (14, -330), (-14, -200), (14, -200))):
        P.near(mdl, x, z, 0, 'town1_avenue', d=6, clear=4, max_slope=0.6)
    return P


def landmarks():
    P = Plan('v5_landmarks', 'Landmark heroes and their parts. Groups: Landmarks.')
    G = 'Landmarks'
    P.add(ids('LM01')[0], -1560, -430, 90, G, note='door in the world tree trunk')
    P.add(ids('LM02')[0], -1740, -740, 135, G, note='three-tier falls into the elf lake')
    P.add(ids('LM22')[0], -1800, -672, 90, G, note='colossal fall cliff on the west rim')
    for mdl, (x, z) in zip(ids('LM23'), ((-1760, -690), (-1730, -650), (-1790, -640))):
        P.near(mdl, x, z, 90, G, max_slope=1.5)
    for mdl, (x, z) in zip(ids('LM24'), ((-1700, -700), (-1680, -720), (-1715, -680))):
        P.near(mdl, x, z, rnd.uniform(0, 360), G, max_slope=1.0, clear=8)
    # desert temples
    P.add(ids('LM09')[0], 2160, 1248, 270, G)
    P.add(ids('LM15')[0], 1660, 1130, 0, G)
    for mdl, (dx, dz, rt) in zip(ids('LM10'), ((-100, -30, 90), (-100, 20, 90), (-100, 70, 90))):
        P.near(mdl, 2160 + dx, 1248 + dz, rt, G, max_slope=0.7)
    P.near(ids('LM11')[0], 2060, 1240, 270, G, max_slope=0.7)
    for mdl, (dx, dz, rt) in zip(ids('LM12'), ((60, 80, 0), (-60, 90, 0))):
        P.near(mdl, 2160 + dx, 1248 + dz, rt, G, max_slope=0.7)
    for mdl, (dx, dz) in zip(ids('LM13'), ((-130, -60), (-130, 60))):
        P.near(mdl, 2160 + dx, 1248 + dz, 270, G, max_slope=0.7)
    for mdl, (dx, dz) in zip(ids('LM14'), ((-170, 0), (-210, 30), (-210, -30))):
        P.near(mdl, 2160 + dx, 1248 + dz, 0, G, max_slope=0.7)
    for k, mdl in enumerate(ids('LM16')):
        a = math.radians(40 + 180 * k)
        P.near(mdl, 1660 + 150 * math.cos(a), 1130 + 150 * math.sin(a), face(1660 + 150 * math.cos(a), 1130 + 150 * math.sin(a), 1660, 1130), G, max_slope=0.6)
    P.near(ids('LM17')[0], 1660, 1130, 0, G, max_slope=0.6, clear=4)
    # crater
    P.add(ids('LM18')[0], 1368, -312, 0, G)
    for k, mdl in enumerate(ids('LM19')):
        a = math.radians(30 + k * 72)
        P.near(mdl, 1368 + 250 * math.cos(a), -312 + 250 * math.sin(a), rnd.uniform(0, 360), G, max_slope=1.2, clear=20)
    for k, mdl in enumerate(ids('LM20')):
        a = math.radians(70 + k * 120)
        P.near(mdl, 1368 + 120 * math.cos(a), -312 + 120 * math.sin(a), rnd.uniform(0, 360), G, max_slope=1.2, clear=8)
    for k, mdl in enumerate(ids('LM21')):
        a = math.radians(45 + k * 90)
        P.add(mdl, 1368 + 90 * math.cos(a), -312 + 90 * math.sin(a), rnd.uniform(0, 360), G, yo=70 + 25 * k, note='floating, optional')
    # ruins
    P.add(ids('LM25')[0], 760, 470, face(760, 470, 0, 0), G)
    for k, mdl in enumerate(ids('LM26')):
        a = math.radians(100 + k * 50)
        P.near(mdl, 760 + 100 * math.cos(a), 470 + 100 * math.sin(a), face(760 + 100 * math.cos(a), 470 + 100 * math.sin(a), 760, 470), G, max_slope=0.6)
    for mdl, (dx, dz) in zip(ids('LM27'), ((-150, -90), (140, -80))):
        P.near(mdl, 760 + dx, 470 + dz, 0, G, max_slope=0.6)
    for k, mdl in enumerate(ids('LM28')):
        P.near(mdl, 760 - 60 + k * 70, 470 + 150, rnd.uniform(0, 360), G, max_slope=0.6)
    for mdl, (dx, dz) in zip(ids('LM29'), ((170, 60), (-170, 40))):
        P.near(mdl, 760 + dx, 470 + dz, 0, G, max_slope=0.6)
    P.add(ids('LM30')[0], -760, -980, 90, G)
    for mdl, (dx, dz) in zip(ids('LM31'), ((-90, -60), (-90, 60), (60, 100))):
        P.near(mdl, -760 + dx, -980 + dz, rnd.uniform(0, 360), G, max_slope=0.8)
    return P


def regions():
    P = Plan('v5_regions', 'Scatter and cluster placements for the regional kits (trees, forest, plains, desert, Skull City, coast, floating islands, marsh). Groups: Veg*, Forest, Plains, Desert, SkullCity, Coast, Sky.')
    cen = (-1400, 1400, -700, 1600)
    allroads = [r_['name'] for r_ in ROADS['routes'] if 'stair' not in r_['name']]
    scatter(P, ids('VG01'), 90, cen, 'VegPoplar', near_roads=allroads, min_d=26, clear=10)
    scatter(P, ids('VG02'), 50, cen, 'VegOak', min_d=90, clear=25, max_slope=0.25, accept=lambda x, z: min(math.hypot(x - hx, z - hz) for hx, hz in ((0, 0), (-1248, 528))) > 200)
    for (vx, vz, vr) in ((-1248, 528, 420), (-390, 1590, 360), (1235, 1105, 300), (0, -250, 700)):
        scatter(P, ids('VG03'), 13, (vx - vr, vx + vr, vz - vr, vz + vr), 'VegFlowering', min_d=50, clear=14, accept=lambda x, z, vx=vx, vz=vz, vr=vr: math.hypot(x - vx, z - vz) < vr and (abs(vx) > 100 or vr == 700 and not in_town1(x, z)))
    # forest NW
    nw = (-2300, -900, -1900, -700)
    away = lambda x, z: math.hypot(x + 1560, z + 400) > 360
    scatter(P, ids('FR01'), 4, nw, 'Forest', min_d=220, clear=24, max_slope=0.4, accept=away)
    scatter(P, ids('FR02'), 6, nw, 'Forest', min_d=140, clear=20, max_slope=0.5, accept=away)
    scatter(P, ids('FR03'), 6, nw, 'Forest', min_d=140, clear=30, max_slope=1.3, accept=lambda x, z: away(x, z) and SL[cell(x, z)] > 0.5)
    scatter(P, ids('VG04'), 60, (-2300, -800, -1900, -600), 'VegBirch', min_d=30, clear=10, accept=away)
    # plains and marsh
    pl = (-1500, -400, 300, 1300)
    scatter(P, ids('PL01'), 4, (-1500, -1000, 350, 900), 'Plains', min_d=110, clear=14, max_slope=0.3)
    scatter(P, ids('PL02'), 3, (-1500, -1000, 350, 900), 'Plains', min_d=70, clear=20, max_slope=0.25)
    scatter(P, ids('PL03'), 2, (-1500, -1000, 350, 900), 'Plains', min_d=80, clear=14, max_slope=0.25)
    P.near(ids('PL04')[0], -1216, 600, 90, 'Plains', max_slope=0.4, d=14)
    scatter(P, ids('PL05'), 3, pl, 'Plains', min_d=300, clear=40, max_slope=0.45)
    for mdl, (x, z) in zip(ids('PL06'), ((-1100, 640), (-1330, 590))):
        P.near(mdl, x, z, 90, 'Plains', max_slope=0.6, clear=20)
    P.near(ids('VL01')[0], -1250, 470, face(-1250, 470, -1248, 560), 'Plains', max_slope=0.4, clear=20)
    mx, mz = -660, 300
    scatter(P, ids('VG05'), 30, (mx - 330, mx + 330, mz - 300, mz + 300), 'VegMarsh', min_d=26, clear=8, max_slope=0.4, accept=lambda x, z: math.hypot(x - mx, z - mz) < 330)
    scatter(P, ids('VG06'), 20, (mx - 330, mx + 330, mz - 300, mz + 300), 'VegMarsh', min_d=24, clear=6, max_slope=0.4)
    for mdl, (x, z, rt) in zip(ids('VG07'), ((mx + 140, mz + 40, 0), (mx - 150, mz - 30, 90))):
        P.near(mdl, x, z, rt, 'VegMarsh', max_slope=0.4, clear=8)
    # desert
    ox, oz = 1860, 1380
    for k, mdl in enumerate(ids('DS01')):
        a = math.radians(k * 60 + 15)
        P.near(mdl, ox + 100 * math.cos(a), oz + 100 * math.sin(a), face(ox + 100 * math.cos(a), oz + 100 * math.sin(a), ox, oz), 'Desert', max_slope=0.4, clear=14)
    for k, mdl in enumerate(ids('DS02')):
        P.near(mdl, ox + (k - 1) * 34, oz - 48, 0, 'Desert', max_slope=0.4, clear=10)
    for mdl in ids('DS03'):
        x, z, hd = at('Temple road', rnd.uniform(0.2, 0.9), 22)
        P.near(mdl, x, z, along(hd), 'Desert')
    for k, mdl in enumerate(ids('DS04')):
        a = math.radians(k * 120 + 40)
        P.near(mdl, ox + 52 * math.cos(a), oz + 52 * math.sin(a), rnd.uniform(0, 360), 'Desert', max_slope=0.4, clear=8, d=8)
    for k, mdl in enumerate(ids('DS05')):
        P.near(mdl, ox + (k * 2 - 1) * 20, oz + 8, 0, 'Desert', max_slope=0.4, clear=4, d=8)
    for cn, mdls in zip(spec['canyons'], (ids('DS06')[:2], ids('DS06')[2:])):
        pts = cn['pts']
        for k, mdl in enumerate(mdls):
            a, b = pts[min(k * 2 + 1, len(pts) - 2)], pts[min(k * 2 + 2, len(pts) - 1)]
            P.near(mdl, (a[0] + b[0]) / 2 + 60, (a[1] + b[1]) / 2 + 40, along(math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))), 'Desert', max_slope=2.0, clear=20, max_r=220)
    scatter(P, ids('DS07'), 4, (1500, 2500, 650, 1500), 'Desert', min_d=260, clear=30, max_slope=0.5)
    for mdl, (x, z) in zip(ids('DS08'), ((1700, 1180), (2200, 1300), (800, 520))):
        P.near(mdl, x, z, rnd.uniform(0, 360), 'Desert', max_slope=0.5, clear=20)
    scatter(P, ids('SD01'), 6, (1500, 2600, 650, 1700), 'Desert', min_d=300, clear=50, max_slope=0.6)
    for k, mdl in enumerate(ids('SD02')):
        a = math.radians(k * 60 + 30)
        P.near(mdl, 1660 + 290 * math.cos(a), 1130 + 290 * math.sin(a), rnd.uniform(0, 360), 'Desert', max_slope=0.5, clear=20)
    # Skull City
    sk = (1700, 2900, -1100, 100)
    in_sk = lambda x, z: math.hypot(x - 2300, z + 620) < 520
    scatter(P, ids('VC01'), 8, sk, 'SkullCity', min_d=120, clear=30, max_slope=1.2, accept=in_sk)
    for mdl, (x, z) in zip(ids('VC03'), ((2136, -576), (2424, -288), (2300, -800))):
        P.near(mdl, x, z, rnd.uniform(0, 360), 'SkullCity', max_slope=0.8, clear=12, max_r=240)
    for k, mdl in enumerate(ids('VC04')):
        P.near(mdl, 2300 + (k % 3 - 1) * 70, -450 + (k // 3) * 70 - 20, face(2300, -450, 2208, -936), 'SkullCity', max_slope=0.6, clear=18, d=12)
    for mdl, (x, z) in zip(ids('VC02'), ((2208, -936), (2760, -552))):
        P.add(mdl, x, z, face(x, z, 2300, -450), 'SkullCity')
    # coast and sea
    cp_ = coast_points(6, 900, lambda x, z, j, i: math.hypot(x + 390, z - 1590) > 500)
    for mdl, (x, z, rt) in zip(ids('CO01'), cp_):
        P.add(mdl, x, z, rt, 'Coast', note='cliff piece, check against the shoreline')
    for mdl, (x, z, rt) in zip(ids('CO02'), cp_[:3]):
        sp = sea_spot(x, z, 150, 320, 6, 45)
        if sp:
            P.add(mdl, sp[0], sp[1], rnd.uniform(0, 360), 'Coast')
    cp2 = coast_points(8, 500, lambda x, z, j, i: MAT[j, i] in (5, 6, 7))
    for mdl, (x, z, rt) in zip(ids('CO04'), cp2):
        sp = sea_spot(x, z, 60, 140, 3, 20)
        if sp:
            P.add(mdl, sp[0], sp[1], rt, 'Coast')
    for mdl in ids('CO03'):
        for _try in range(8):
            cp3 = coast_points(1, 100)
            sp = sea_spot(cp3[0][0], cp3[0][1], 60, 400, 3, 12) if cp3 else None
            if sp:
                P.add(mdl, sp[0], sp[1], rnd.uniform(0, 360), 'Coast')
                break
    for mdl in ids('CO05'):
        cp3 = coast_points(1, 100)
        if cp3:
            sp = sea_spot(cp3[0][0], cp3[0][1], 350, 600, 5, 22)
            if sp:
                P.add(mdl, sp[0], sp[1], rnd.uniform(0, 360), 'Coast')
    for mdl, (x, z) in zip(ids('HB01'), ((-640, 1700), (-140, 1700), (-390, 1480))):
        P.near(mdl, x, z, face(x, z, -390, 1650), 'Coast', max_slope=0.5, clear=14)
    for k, mdl in enumerate(ids('FL01') + ids('FL02')):
        P.add(mdl, 3050 - (k % 3) * 120 + (k // 3) * 60, -2400 + (k % 3) * 160 - (k // 3) * 70, rnd.uniform(0, 360), 'Sky', yo=150 + 25 * k, note='floating, over sea')
    # river and lake banks
    for mdl, (nm_, t) in zip(ids('RV01'), (('trunk_east', 0.0), ('trunk_west', 0.0), ('silverrun', 0.0), ('elf_river', 0.0))):
        pts = next((r_['pts'] for r_ in world['rivers'] if r_['name'] == nm_), None) or next((r_['pts'] for r_ in spec['rivers_new'] if r_['name'] == nm_), None)
        mid = pts[len(pts) // 2]
        P.near(mdl, mid[0] + 14, mid[1] + 10, rnd.uniform(0, 360), 'Rivers', max_slope=1.0, clear=8)
    return P


# =================================================================================================== run
PLANS = [himalaya(), road_works(), entrances(), capital(), elf(), town1(), landmarks(), regions()]
for p in PLANS:
    p.save()

placed = {}
for p in PLANS:
    for it in p.items:
        placed[it['model']] = placed.get(it['model'], 0) + 1
new_total = len(V5)
new_placed = sum(1 for m in V5 if m in placed)
unplaced = [m for m in V5 if m not in placed]
by_row = {}
for m in unplaced:
    by_row.setdefault(V5[m]['row'], []).append(m)

# off-land check for exterior items that should stand on dry land
SKIP_LAND = ('Coast', 'Sky', 'WizardTowerInterior', 'Bridges', 'Tunnels')
bad = []
for p in PLANS:
    for it in p.items:
        if it['group'] in SKIP_LAND or it.get('y_offset'):
            continue
        if not ok(it['x'], it['z'], 1.8, -50):
            bad.append((p.area, it['model'], it['x'], it['z']))

md = ['# Placement plans v5 (drafts, written by make_v5_plans.py)', '',
      'Built on the exported terrain plus the planned landforms. Format is the one `rebuild/v4/build_v4.ps1` reads. The new models do not exist yet, so a first run counts them as "waiting for upload" and places nothing; once a model is uploaded and listed in asset_ids.csv it is placed. Re-seat on the live ground (reseat_env.luau) and verify (verify_folders.luau) after every area.', '',
      '| Plan file (area) | Placements | Groups | Build command |', '|---|---|---|---|']
for p in PLANS:
    groups = sorted({i['group'] for i in p.items})
    small = [g for g in groups if g in ('RoadLife', 'Himalaya', 'VegMarsh', 'town1_life', 'ElfPaths', 'Entrances')]
    cmd = 'build_v4.ps1 -area %s -batch 30' % p.area + (' -nocollide ' + ','.join(small) if small else '')
    md.append('| %s | %d | %s | `%s` |' % (p.area, len(p.items), ', '.join(groups), cmd))
md += ['', 'Models placed: %d of %d new models (rows without a site yet: see below). Total placements: %d.' % (new_placed, new_total, sum(len(p.items) for p in PLANS)), '',
       '## New models with no placement yet', '']
for rcode, ms in by_row.items():
    md.append('- %s (%d): %s' % (rcode, len(ms), ', '.join(ms[:4]) + (' ...' if len(ms) > 4 else '')))
md += ['', '## Misses (no valid free spot was found; fix the site or move the rule)', '']
md += ['- ' + ' | '.join(str(v) for v in m) for m in MISSES] or ['- none']
md += ['', '## Exterior placements on wet, steep or off-grid ground (check in Studio)', '']
md += ['- %s: %s at (%s, %s)' % b for b in bad[:60]] or ['- none']
md += ['', 'Rows meant to be reworks (RW01, RW02) are not placed: they change existing models.']
open(HERE + r'\PLACEMENT_V5.md', 'w').write('\n'.join(md) + '\n')

# overlay of every placement on the top-view sketch
try:
    base = Image.open(HERE + r'\topview_sketch_v5.jpg').convert('RGB')
    d = ImageDraw.Draw(base)
    S_ = 3.0
    colours = {'v5_himalaya': (255, 80, 200), 'v5_roads': (255, 255, 0), 'v5_entrances': (0, 255, 255), 'v5_capital': (255, 120, 0), 'v5_elf': (80, 255, 80),
               'town1_v5': (255, 255, 255), 'v5_landmarks': (255, 0, 0), 'v5_regions': (120, 160, 255)}
    for p in PLANS:
        c = colours[p.area]
        for it in p.items:
            a, b = (it['x'] + 3300.0) / S_, (it['z'] + 2900.0) / S_
            d.rectangle([a - 2, b - 2, a + 2, b + 2], fill=c)
    f = ImageFont.truetype('arialbd.ttf', 22)
    d.rectangle([14, 70, 330, 70 + 28 * len(PLANS) + 12], fill=(24, 28, 36))
    for k, p in enumerate(PLANS):
        d.rectangle([24, 82 + k * 28, 40, 98 + k * 28], fill=colours[p.area])
        d.text((50, 80 + k * 28), '%s  %d' % (p.area, len(p.items)), font=f, fill=(255, 255, 255))
    base.save(HERE + r'\plan_overlay_items_v5.jpg', quality=86)
except Exception as e:
    print('overlay skipped:', e)

print('plans:', ', '.join('%s %d' % (p.area, len(p.items)) for p in PLANS))
print('new models with a placement: %d of %d; total placements %d' % (new_placed, new_total, sum(len(p.items) for p in PLANS)))
print('rows with unplaced models:', {k: len(v) for k, v in by_row.items()})
print('misses:', len(MISSES), MISSES[:12])
print('exterior placements on bad ground:', len(bad), bad[:8])
print('existing placements loaded for overlap checks:', len(EX))
