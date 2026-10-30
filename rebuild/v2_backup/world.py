"""World designer v3 (65% map). Writes world.json for terrain_gen.luau and layout scripts.
H = 6 + features (g gaussian, m mesa, M ridged mountain) -> coast falloff -> post promontories -> pads -> roads/rivers
Town 1 interior terrain is resampled in Luau from _G.T1SNAP (old Town 1 terrain, compressed 0.7).
X east, Z south, Y up, sea 0.
"""
import json, math, os

OUT = r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\world.json'

def smoothstep(a, b, x):
    if b == a:
        return 1.0 if x >= b else 0.0
    t = min(1.0, max(0.0, (x - a) / (b - a)))
    return t * t * (3 - 2 * t)

# ---------------------------------------------------------------- features
# ('g', x, z, r, h) gaussian | ('m', x, z, r, h) mesa | ('M', x, z, r, h) ridged mountain (gaussian x ridged noise)
FEATURES = [
    # tower mountain massif (NE) + side peaks
    ('M', 1380, -1300, 500, 330), ('M', 1760, -1480, 300, 200), ('M', 1050, -1520, 300, 190), ('M', 1500, -1650, 280, 160),
    # four mountains around the elf valley (W)
    ('M', -1990, -830, 290, 270), ('M', -1120, -860, 270, 235), ('M', -2010, 70, 290, 250), ('M', -1150, 80, 260, 215),
    # northern ridge west of the capital
    ('M', -880, -1660, 380, 210), ('M', -1420, -1380, 300, 170), ('M', -380, -2050, 260, 120),
    # capital surroundings rise gently
    ('g', 0, -1650, 650, 26),
    # south-west coastal hills
    ('M', -1450, 980, 330, 120), ('g', -1000, 1350, 260, 40),
    # rolling hills
    ('g', 600, -700, 260, 40), ('g', -500, 620, 280, 30), ('g', 300, 950, 220, 24), ('g', -900, 300, 220, 28),
    ('g', 1000, -200, 220, 28), ('g', -330, -950, 200, 30), ('g', 520, -1150, 230, 34), ('g', 120, 1450, 240, 26),
    ('g', 1700, 300, 260, 34), ('g', 2000, -300, 200, 26),
    # dry badlands mesas (SE)
    ('m', 1700, 780, 140, 72), ('m', 1720, 1480, 170, 88), ('m', 830, 1460, 110, 52), ('m', 1480, 560, 100, 46),
    ('m', 1500, 1650, 90, 40), ('m', 1000, 1650, 80, 36),
    # harbour bay
    ('g', -390, 2080, 330, -75),
]

COAST = {'ax': 2200, 'az_n': 2480, 'az_s': 2000, 'start': 0.84, 'end': 1.0, 'floor': -30, 'p': 3.0}
POST = [(-700, 1862, 95, 22), (-70, 1872, 90, 20), (250, 2060, 45, 14), (-1100, 1980, 55, 16), (2080, -900, 70, 40),
        (2140, -400, 45, 22), (-2150, -1000, 60, 28), (-2060, 700, 50, 18), (900, -2330, 55, 30)]

def coast_d(x, z):
    az = COAST['az_n'] if z < 0 else COAST['az_s']
    p = COAST.get('p', 4)
    return ((abs(x) / COAST['ax']) ** p + (abs(z) / az) ** p) ** (1 / p)

def base_h(x, z):
    """Noise-free regional height (mountains use their mean ridged factor 0.85)."""
    h = 6.0
    for f in FEATURES:
        kind, cx, cz, r, hh = f
        d = math.hypot(x - cx, z - cz)
        if kind == 'g':
            if d < r * 3:
                h += hh * math.exp(-(d / r) ** 2)
        elif kind == 'M':
            if d < r * 3:
                h += hh * math.exp(-(d / r) ** 2) * 0.85
        else:
            h += hh * (1 - smoothstep(r * 0.72, r, d))
    c = smoothstep(COAST['start'], COAST['end'], coast_d(x, z))
    h = h + (COAST['floor'] - h) * c
    return h

# ---------------------------------------------------------------- pads
T1 = {'x': 304, 'z0': -538, 'z1': 304}       # Town 1 snapshot region (inside the compressed walls)
PADS = [
    {'name': 'town1ring', 'shape': 'rect', 'cx': 0, 'cz': -117, 'hx': 330, 'hz': 445, 'e': 210,
     'ground': {'type': 'flat', 'y': 2.0}, 'noise': 0.0},
    {'name': 'capital_city', 'shape': 'rect', 'cx': 0, 'cz': -1578, 'hx': 545, 'hz': 370, 'e': 150,
     'ground': {'type': 'ramp', 'p0': [0, -1240], 'dir': [0, -1], 'y0': 18.0, 'slope': 0.06, 'lo': 18.0, 'hi': 60.0}, 'noise': 0.0},
    {'name': 'capital_castle', 'shape': 'ell', 'cx': 0, 'cz': -2200, 'rx': 300, 'rz': 215, 'e': 70,
     'ground': {'type': 'flat', 'y': 92.0}, 'noise': 0.0, 'cliff': True},
    {'name': 'elf', 'shape': 'ell', 'cx': -1560, 'cz': -400, 'rx': 330, 'rz': 320, 'e': 170,
     'ground': {'type': 'flat', 'y': 12.0}, 'noise': 2.5},
    {'name': 'elf_tree', 'shape': 'ell', 'cx': -1560, 'cz': -430, 'rx': 112, 'rz': 112, 'e': 45,
     'ground': {'type': 'flat', 'y': 14.0}, 'noise': 0.0},
    {'name': 'harbour', 'shape': 'ell', 'cx': -390, 'cz': 1590, 'rx': 300, 'rz': 215, 'e': 140,
     'ground': {'type': 'ramp', 'p0': [-390, 1400], 'dir': [0, 1], 'y0': 20.0, 'slope': -0.0385, 'lo': 5.0, 'hi': 20.0}, 'noise': 0.0},
    {'name': 'harbour_quay', 'shape': 'rect', 'cx': -390, 'cz': 1808, 'hx': 235, 'hz': 18, 'e': 8,
     'ground': {'type': 'flat', 'y': 4.5}, 'noise': 0.0},
    {'name': 'rusty', 'shape': 'ell', 'cx': 1235, 'cz': 1105, 'rx': 245, 'rz': 220, 'e': 150,
     'ground': {'type': 'flat', 'y': 14.0}, 'noise': 1.2},
    {'name': 'rusty_church', 'shape': 'ell', 'cx': 1400, 'cz': 1250, 'rx': 120, 'rz': 120, 'e': 45,
     'ground': {'type': 'flat', 'y': 14.0}, 'noise': 0.0},
    {'name': 'alpine_lake', 'shape': 'ell', 'cx': 1490, 'cz': -1075, 'rx': 225, 'rz': 150, 'e': 70,
     'ground': {'type': 'flat', 'y': 151.0}, 'noise': 0.6},
    {'name': 'alpine_shelf', 'shape': 'rect', 'cx': 1640, 'cz': -850, 'hx': 220, 'hz': 175, 'e': 75,
     'ground': {'type': 'flat', 'y': 120.0}, 'noise': 0.8},
    {'name': 'tower_summit', 'shape': 'ell', 'cx': 1380, 'cz': -1320, 'rx': 95, 'rz': 95, 'e': 70,
     'ground': {'type': 'flat', 'y': 318.0}, 'noise': 0.0},
    {'name': 'plateau_e', 'shape': 'ell', 'cx': 760, 'cz': 470, 'rx': 190, 'rz': 140, 'e': 40,
     'ground': {'type': 'flat', 'y': 46.0}, 'noise': 1.5, 'cliff': True},
    {'name': 'plateau_nw', 'shape': 'ell', 'cx': -760, 'cz': -980, 'rx': 165, 'rz': 125, 'e': 45,
     'ground': {'type': 'flat', 'y': 62.0}, 'noise': 1.5, 'cliff': True},
]

def pad_mask(p, x, z):
    if p['shape'] == 'rect':
        dx = abs(x - p['cx']) - p['hx']; dz = abs(z - p['cz']) - p['hz']
        out = math.hypot(max(dx, 0), max(dz, 0))
        if dx <= 0 and dz <= 0:
            out = 0.0
    else:
        nx = (x - p['cx']) / p['rx']; nz = (z - p['cz']) / p['rz']
        r = math.hypot(nx, nz)
        out = max(0.0, (r - 1) * min(p['rx'], p['rz']))
    return 1 - smoothstep(0, p['e'], out)

def pad_ground(p, x, z):
    g = p['ground']
    if g['type'] == 'flat':
        return g['y']
    t = (x - g['p0'][0]) * g['dir'][0] + (z - g['p0'][1]) * g['dir'][1]
    return min(g['hi'], max(g['lo'], g['y0'] + g['slope'] * t))

def ground_no_noise(x, z):
    if abs(x) <= T1['x'] and T1['z0'] <= z <= T1['z1']:
        return 2.0
    h = base_h(x, z)
    for p in PADS:
        m = pad_mask(p, x, z)
        if m > 0:
            h = h + (pad_ground(p, x, z) - h) * m
    return h

# ---------------------------------------------------------------- roads
ROADS = {
    'north': {'w': 10, 'mat': 'Cobblestone', 'pts': [(0, -546, 2.0), (0, -620), (22, -760), (-15, -930), (12, -1100), (0, -1200), (0, -1226, 18.0)]},
    'east': {'w': 9, 'mat': 'Cobblestone', 'pts': [(316, -50, 2.0), (420, -55), (650, -110), (900, -200), (1150, -330), (1380, -470), (1500, -560),
                                                    (1780, -585, 74.0), (1880, -622, 86.0), (1840, -662, 96.0), (1700, -648, 108.0), (1610, -662, 116.0), (1585, -700, 120.0)]},
    'west': {'w': 9, 'mat': 'Cobblestone', 'pts': [(-316, -50, 2.0), (-420, -60), (-650, -120), (-900, -220), (-1100, -320), (-1230, -398), (-1292, -404)]},
    'south': {'w': 9, 'mat': 'Cobblestone', 'pts': [(0, 316, 2.0), (8, 420), (-30, 650), (-140, 900), (-260, 1150), (-360, 1330), (-390, 1392)]},
    'southeast': {'w': 8, 'mat': 'Cobblestone', 'pts': [(6, 480), (250, 560), (520, 690), (780, 830), (950, 930), (1030, 968), (1062, 985)]},
    'ring_east': {'w': 6, 'mat': 'Ground', 'pts': [(1380, 920), (1520, 600), (1640, 250), (1660, -100), (1600, -380), (1505, -552)]},
    'ring_west': {'w': 6, 'mat': 'Ground', 'pts': [(-1560, -95), (-1560, 120), (-1420, 450), (-1110, 800), (-760, 1150), (-500, 1380), (-440, 1400)]},
    'lake_path': {'w': 5, 'mat': 'Cobblestone', 'pts': [(1560, -960, 120.0), (1530, -1000, 128.0), (1470, -1004, 138.0), (1430, -985, 145.0), (1420, -1010, 151.0)]},
}

def build_roads():
    out = []
    for name, r in ROADS.items():
        pts = []
        for p in r['pts']:
            if len(p) == 3:
                pts.append([p[0], p[1], p[2], 1])
            else:
                pts.append([p[0], p[1], ground_no_noise(p[0], p[1]), 0])
        for _ in range(3):
            for i in range(1, len(pts) - 1):
                if not pts[i][3]:
                    pts[i][2] = (pts[i - 1][2] + 2 * pts[i][2] + pts[i + 1][2]) / 4
        dense = []
        P = [(q[0], q[1], q[2]) for q in pts]
        for i in range(len(P) - 1):
            p0 = P[max(0, i - 1)]; p1 = P[i]; p2 = P[i + 1]; p3 = P[min(len(P) - 1, i + 2)]
            seg = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
            n = max(1, int(seg / 24))
            for k in range(n):
                t = k / n; t2, t3 = t * t, t * t * t
                pt = []
                for a in range(3):
                    pt.append(0.5 * ((2 * p1[a]) + (-p0[a] + p2[a]) * t + (2 * p0[a] - 5 * p1[a] + 4 * p2[a] - p3[a]) * t2 + (-p0[a] + 3 * p1[a] - 3 * p2[a] + p3[a]) * t3))
                dense.append([round(pt[0], 1), round(pt[1], 1), round(pt[2], 2)])
        dense.append([P[-1][0], P[-1][1], round(P[-1][2], 2)])
        out.append({'name': name, 'w': r['w'], 'mat': r['mat'], 'pts': dense})
    return out

# ---------------------------------------------------------------- water
def stepped(pts, start_level, final_level=None, drop_min=2.5):
    """Give each river point a water level that never rises and stays below the ground."""
    out = []
    lv = start_level
    for i, (x, z) in enumerate(pts):
        g = ground_no_noise(x, z)
        lv = min(lv, g - 2.2)
        if final_level is not None and i == len(pts) - 1:
            lv = min(lv, final_level)
        out.append([x, z, round(lv, 2)])
    return out

RIVERS = [
    {'name': 't1_west', 'w': 11, 'depth': 6, 'pts': [[-298, 190, -3], [-380, 200, -3], [-480, 230, -3], [-560, 262, -3]]},
    {'name': 't1_east', 'w': 10, 'depth': 6, 'pts': [[298, 160, -3], [380, 155, -3], [460, 140, -3], [530, 128, -3]]},
    {'name': 'silverrun', 'w': 9, 'depth': 5, 'pts': stepped([(1860, -700), (1930, -610), (1975, -500), (1940, -380), (1820, -260), (1620, -160), (1380, -90), (1120, -30), (900, 40), (720, 100)], 118.0, -3.0)},
    {'name': 'elf_river', 'w': 9, 'depth': 4, 'pts': [[-1690, -560, 12], [-1780, -500, 12], [-1880, -440, 12], [-1980, -410, 8], [-2060, -395, 4], [-2140, -385, 1], [-2240, -380, 0]]},
]
LAKES = [
    {'name': 'west_lake', 'cx': -660, 'cz': 300, 'rx': 120, 'rz': 90, 'level': -3.0, 'depth': 9},
    {'name': 'east_lake', 'cx': 630, 'cz': 120, 'rx': 115, 'rz': 85, 'level': -3.0, 'depth': 9},
    {'name': 'elf_lake', 'cx': -1660, 'cz': -640, 'rx': 80, 'rz': 62, 'level': 12.0, 'depth': 7},
    {'name': 'elf_pond', 'cx': -1440, 'cz': -250, 'rx': 40, 'rz': 32, 'level': 12.0, 'depth': 5},
    {'name': 'alpine_ice_lake', 'cx': 1490, 'cz': -1080, 'rx': 170, 'rz': 108, 'level': 151.0, 'depth': 4, 'frozen': True},
    {'name': 'alpine_pond', 'cx': 1800, 'cz': -760, 'rx': 30, 'rz': 22, 'level': 118.5, 'depth': 4},
]

BIOMES = [
    ('jungle', -1560, -400, 560), ('forest', -1050, -1500, 480), ('forest', -1450, 900, 360), ('forest', 600, -1200, 260),
    ('dry', 1235, 1105, 640), ('dry', 1650, 1350, 420), ('alpine', 1420, -1180, 700),
]

world = {
    'features': [list(f) for f in FEATURES],
    'coast': COAST,
    'post': [list(p) for p in POST],
    'pads': PADS,
    'roads': build_roads(),
    'rivers': RIVERS,
    'lakes': LAKES,
    'biomes': [list(b) for b in BIOMES],
    'keep': {},
    't1': T1,
}

if __name__ == '__main__':
    sp = r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\streets.json'
    if os.path.exists(sp):
        world['streets'] = json.load(open(sp))
    json.dump(world, open(OUT, 'w'), separators=(',', ':'))
    for r in world['roads']:
        ys = [p[2] for p in r['pts']]
        L = sum(math.hypot(r['pts'][i + 1][0] - r['pts'][i][0], r['pts'][i + 1][1] - r['pts'][i][1]) for i in range(len(r['pts']) - 1))
        grades = [abs(r['pts'][i + 1][2] - r['pts'][i][2]) / max(1, math.hypot(r['pts'][i + 1][0] - r['pts'][i][0], r['pts'][i + 1][1] - r['pts'][i][1])) for i in range(len(r['pts']) - 1)]
        print(f"{r['name']}: L {L:.0f}, y {min(ys):.1f}..{max(ys):.1f}, max grade {max(grades)*100:.1f}%")
    print('silverrun levels', [p[2] for p in RIVERS[2]['pts']])
    for (x, z, label) in [(0, -1240, 'capital gate'), (0, -1918, 'capital top'), (0, -2200, 'castle'), (-1560, -400, 'elf'), (-390, 1400, 'harbour N'),
                          (1235, 1105, 'rusty'), (1640, -850, 'alpine'), (1490, -1075, 'ice lake'), (1380, -1320, 'summit'), (1500, -560, 'alpine road foot'),
                          (-1230, -398, 'elf east pass'), (-1560, 120, 'elf south pass')]:
        print(f'{label}: {ground_no_noise(x, z):.1f}  base {base_h(x, z):.1f}')
    print('size', len(json.dumps(world)))
