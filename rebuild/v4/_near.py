import json, math
W = json.load(open(r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\world.json'))
def near(pts, x, z, d):
    best = 1e9
    for i in range(len(pts) - 1):
        ax, az, bx, bz = pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1]
        vx, vz = bx - ax, bz - az
        L2 = vx * vx + vz * vz
        t = 0 if L2 == 0 else max(0, min(1, ((x - ax) * vx + (z - az) * vz) / L2))
        best = min(best, math.hypot(x - (ax + vx * t), z - (az + vz * t)))
    return best
for (x, z) in [(3002, -1698), (3040, -1650), (2850, 1520)]:
    print('point', x, z)
    for kind in ('rivers', 'roads', 'streets'):
        for r in W[kind]:
            d = near(r['pts'], x, z, 400)
            if d < 400:
                print('   ', kind, r['name'], 'dist %.0f' % d, 'w', r.get('w'), 'end', r['pts'][-1])
    for L in W['lakes']:
        d = math.hypot(x - L['cx'], z - L['cz'])
        if d < 600:
            print('    lake', L['name'], 'dist %.0f' % d)
    for p in W['post']:
        d = math.hypot(x - p[0], z - p[1])
        if d < 400:
            print('    post', p, 'dist %.0f' % d)
