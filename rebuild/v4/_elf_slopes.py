import json, math
V4 = r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\v4'
TM = json.load(open(V4 + r'\terrain_map.json'))
X0, Z0, STEP = TM['x0'], TM['z0'], TM['step']
rows = TM['rows']
def h(x, z):
    i, j = round((x - X0) / STEP), round((z - Z0) / STEP)
    c = rows[j][i * 5:i * 5 + 5]
    return int(c[0:2], 36) - 100
print('height grid (rows = z, cols = x):')
xs = list(range(-1840, -1480, 40))
print('        ' + ' '.join('%5d' % x for x in xs))
for z in range(-900, -560, 24):
    print('z=%5d ' % z + ' '.join('%5d' % h(x, z) for x in xs))
# steepest north-facing slope within the valley's north rim: find cells where height rises >= 18 over 24 studs going north (z decreasing)
best = []
for x in range(-1800, -1500, 24):
    for z in range(-860, -640, 24):
        d = h(x, z - 24) - h(x, z)
        if d >= 14:
            best.append((d, x, z, h(x, z), h(x, z - 24)))
best.sort(reverse=True)
print('steep north-facing cells (rise per 24 studs):', best[:10])
