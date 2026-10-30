import json, math, collections
RB = r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\v4'
TM = json.load(open(RB + r'\terrain_map.json'))
X0, Z0, STEP = TM['x0'], TM['z0'], TM['step']
rows = TM['rows']
cx, cz = 0, -402
cnt = collections.Counter()
far = collections.defaultdict(int)
for j, row in enumerate(rows):
    z = Z0 + j * STEP
    if abs(z - cz) > 160:
        continue
    for i in range(len(row) // 5):
        x = X0 + i * STEP
        d = math.hypot(x - cx, z - cz)
        if d > 160:
            continue
        ch = row[i * 5 + 2]
        cnt[(int(d // 24) * 24, ch)] += 1
for r in range(0, 160, 24):
    print('r %3d-%3d: %s' % (r, r + 24, dict((c, n) for (rr, c), n in sorted(cnt.items()) if rr == r)))
