import json, math
V4 = r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\v4'
TM = json.load(open(V4 + r'\terrain_map.json'))
X0, Z0, STEP = TM['x0'], TM['z0'], TM['step']
rows = TM['rows']
def H(x, z):
    fi, fj = (x - X0) / STEP, (z - Z0) / STEP
    i0, j0 = int(math.floor(fi)), int(math.floor(fj))
    ti, tj = fi - i0, fj - j0
    def g(i, j):
        c = rows[j][i * 5:i * 5 + 5]
        return int(c[0:2], 36) - 100
    a = g(i0, j0) * (1 - ti) + g(i0 + 1, j0) * ti
    b = g(i0, j0 + 1) * (1 - ti) + g(i0 + 1, j0 + 1) * ti
    return a * (1 - tj) + b * tj
# steepest descent paths from candidate start points on the north-west rim of the elf valley toward the elf lake (-1660,-640)
best = []
for sx in range(-1840, -1640, 20):
    for sz in range(-860, -700, 20):
        x, z = float(sx), float(sz)
        h0 = H(x, z)
        if h0 < 70 or h0 > 150:
            continue
        pts = [(x, z, h0)]
        for _ in range(60):
            # move to the lowest of 8 neighbours at 8 studs
            bh, bp = H(x, z), None
            for k in range(16):
                a = math.tau * k / 16
                nx, nz = x + math.cos(a) * 8, z + math.sin(a) * 8
                nh = H(nx, nz)
                if nh < bh - 0.2:
                    bh, bp = nh, (nx, nz)
            if bp is None:
                break
            x, z = bp
            pts.append((x, z, bh))
            if bh < 16:
                break
        drop = pts[0][2] - pts[-1][2]
        run = math.hypot(pts[0][0] - pts[-1][0], pts[0][1] - pts[-1][1])
        # average slope and steepest 3-sample section
        slopes = [(pts[i][2] - pts[i + 1][2]) / 8.0 for i in range(len(pts) - 1)]
        steep = sum(1 for s in slopes if s > 0.9)
        dist_lake = math.hypot(pts[-1][0] + 1660, pts[-1][1] + 640)
        if drop > 45 and run > 30:
            best.append((steep / max(1, len(slopes)), drop, run, dist_lake, pts))
best.sort(key=lambda t: (-t[0], t[3]))
for frac, drop, run, dl, pts in best[:5]:
    print('steep fraction %.2f drop %.0f run %.0f end %.0f from lake centre; start (%.0f,%.0f,%.0f) end (%.0f,%.0f,%.0f), %d pts' % (frac, drop, run, dl, pts[0][0], pts[0][1], pts[0][2], pts[-1][0], pts[-1][1], pts[-1][2], len(pts)))
json.dump([[round(a, 1), round(b, 1), round(c, 1)] for a, b, c in best[0][4]], open(V4 + r'\waterfall_path.json', 'w'))
print('chosen path points:', [(round(a), round(b), round(c)) for a, b, c in best[0][4]][::4])
