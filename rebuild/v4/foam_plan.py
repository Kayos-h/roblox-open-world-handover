"""foam_plan.py - shoreline contour (sea level 0) from the exported terrain map -> rebuild/v4/foam_segments.json
Marching squares on the 24-stud height grid; only segments next to cells whose water level is 0 (the sea, not lakes or rivers).
Segments are refined inside Studio against the real terrain by foam_build.luau.
"""
import json, math, random
RB = r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\v4'
TM = json.load(open(RB + r'\terrain_map.json'))
X0, Z0, STEP = TM['x0'], TM['z0'], TM['step']
rows = TM['rows']
NZ = len(rows)
NX = len(rows[0]) // 5
H = [[0.0] * NX for _ in range(NZ)]
WL = [[None] * NX for _ in range(NZ)]
for j, row in enumerate(rows):
    for i in range(NX):
        c = row[i * 5:i * 5 + 5]
        H[j][i] = int(c[0:2], 36) - 100
        w = c[3:5]
        WL[j][i] = None if w == '--' else int(w, 36) - 100


def sea_near(i, j):
    for dj in (-1, 0, 1, 2):
        for di in (-1, 0, 1, 2):
            ii, jj = i + di, j + dj
            if 0 <= ii < NX and 0 <= jj < NZ and WL[jj][ii] == 0:
                return True
    return False


LEVEL = -0.4
segs = []


def lerp_pt(i0, j0, i1, j1):
    h0, h1 = H[j0][i0] - LEVEL, H[j1][i1] - LEVEL
    t = h0 / (h0 - h1) if h0 != h1 else 0.5
    return (X0 + (i0 + (i1 - i0) * t) * STEP, Z0 + (j0 + (j1 - j0) * t) * STEP)


for j in range(NZ - 1):
    for i in range(NX - 1):
        c = [H[j][i], H[j][i + 1], H[j + 1][i + 1], H[j + 1][i]]
        s = [v > LEVEL for v in c]
        n = sum(s)
        if n == 0 or n == 4:
            continue
        if not sea_near(i, j):
            continue
        # edges: 0:(i,j)-(i+1,j) 1:(i+1,j)-(i+1,j+1) 2:(i+1,j+1)-(i,j+1) 3:(i,j+1)-(i,j)
        corners = [(i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1)]
        pts = []
        for e in range(4):
            a, b = e, (e + 1) % 4
            if s[a] != s[b]:
                pts.append(lerp_pt(corners[a][0], corners[a][1], corners[b][0], corners[b][1]))
        if len(pts) == 2:
            segs.append((pts[0], pts[1]))
        elif len(pts) == 4:
            segs.append((pts[0], pts[1]))
            segs.append((pts[2], pts[3]))

# keep segments that are long enough, merge very short ones by skipping
out = []
for (a, b) in segs:
    L = math.hypot(b[0] - a[0], b[1] - a[1])
    if L < 3:
        continue
    out.append([round(a[0], 1), round(a[1], 1), round(b[0], 1), round(b[1], 1)])
# island interior ponds near Town 1 are excluded because their water level is not 0
total = sum(math.hypot(s[2] - s[0], s[3] - s[1]) for s in out)
json.dump({'segments': out}, open(RB + r'\foam_segments.json', 'w'))
print('shoreline segments:', len(out), 'total length %.0f studs' % total)
