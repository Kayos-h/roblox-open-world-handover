import sys, json, math
V4 = r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\v4'
TOWN = r'C:\Users\Nitro\.kiro\crew\workspace\town'
sys.path.insert(0, V4)
import env_plan as E
E.load_occupancy()
CX, CZ = -1560.0, -430.0
import collections
why = collections.Counter()
samples = 0
for k in range(0, 360, 6):
    for r in (96, 110, 125, 140):
        a = math.radians(k)
        x, z = CX + math.cos(a) * r, CZ + math.sin(a) * r * 0.92
        samples += 1
        if not E.in_map(x, z): why['not in map'] += 1; continue
        if E.H(x, z) <= 3: why['too low'] += 1; continue
        if E.has_water(x, z): why['water'] += 1; continue
        if E.in_lake(x, z, 1.15): why['lake'] += 1; continue
        if E.ROADS.dist(x, z) <= 7: why['road<=7'] += 1; continue
        if E.occupied(x, z, 10.0): why['occupied(10)'] += 1; continue
        if E.slope(x, z) >= 0.28: why['slope'] += 1; continue
        why['FREE'] += 1
print('samples', samples, dict(why))
# what is the footprint at the tree: the world tree models have huge bounding boxes
big = []
for k, lst in E.OCC.items():
    for (x, z, hx, hz) in lst:
        if hx > 60 or hz > 60:
            big.append((round(x), round(z), round(hx), round(hz)))
print('huge footprints:', sorted(set(big))[:12])
