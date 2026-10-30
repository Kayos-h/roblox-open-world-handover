"""road_paint_data.py - samples for the paint-widening of roads and trails (material only; heights untouched).
Main roads: 24 studs wide (half 12) Limestone; ring roads and trails: 12 studs wide (half 6) Ground. Town 1 zone and town pads are skipped.
"""
import json, math
RB = r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild'
W = json.load(open(RB + r'\world.json'))
T1 = W['keep']['town1']  # x0,x1,z0,z1


def resample(pts, step):
    out = []
    carry = 0.0
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        seg = math.hypot(b[0] - a[0], b[1] - a[1])
        if seg == 0:
            continue
        d = carry
        while d <= seg:
            t = d / seg
            ya = a[2] if len(a) > 2 else None
            yb = b[2] if len(b) > 2 else None
            y = (ya + (yb - ya) * t) if (ya is not None and yb is not None) else None
            out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, y))
            d += step
        carry = d - seg
    return out


def in_t1(x, z):
    return T1[0] - 20 <= x <= T1[1] + 20 and T1[2] - 20 <= z <= T1[3] + 20


samples = []
stats = {}
MAIN = ('north', 'east', 'west', 'south', 'southeast')
for r in W['roads']:
    if r['name'] in MAIN:
        half, mat = 12, 'Limestone'
    elif r['name'] in ('ring_east', 'ring_west'):
        half, mat = 6, 'Ground'
    else:
        continue
    n = 0
    for (x, z, y) in resample(r['pts'], 7.0):
        if in_t1(x, z):
            continue
        samples.append([round(x, 1), round(z, 1), None if y is None else round(y, 1), half, mat])
        n += 1
    stats[r['name']] = n
for s in W['streets']:
    if str(s['name']).startswith('trail_'):
        n = 0
        for (x, z, y) in resample(s['pts'], 6.0):
            if in_t1(x, z):
                continue
            samples.append([round(x, 1), round(z, 1), None if y is None else round(y, 1), 6, 'Ground'])
            n += 1
        stats[s['name']] = n
json.dump({'samples': samples}, open(RB + r'\v4\road_paint.json', 'w'), separators=(',', ':'))
print('samples', len(samples), 'bytes', len(json.dumps(samples)))
print(stats)
