import json, math, collections
V4 = r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\v4'
TM = json.load(open(V4 + r'\terrain_map.json'))
X0, Z0, STEP = TM['x0'], TM['z0'], TM['step']
rows = TM['rows']
NX = len(rows[0]) // 5
def cell(i, j):
    c = rows[j][i * 5:i * 5 + 5]
    h = int(c[0:2], 36) - 100
    w = None if c[3:5] == '--' else int(c[3:5], 36) - 100
    return h, c[2], w
# water cells in the elf valley window
W = []
for j in range(len(rows)):
    z = Z0 + j * STEP
    if not (-820 <= z <= -80):
        continue
    for i in range(NX):
        x = X0 + i * STEP
        if not (-2000 <= x <= -1150):
            continue
        h, m, w = cell(i, j)
        if w is not None and w > h + 0.5:
            W.append((x, z, h, w))
print('water cells in elf window:', len(W))
# cluster by 4-neighbour flood (grid step 24)
S = {(round((x - X0) / STEP), round((z - Z0) / STEP)): (x, z, h, w) for x, z, h, w in W}
seen, clusters = set(), []
for k in S:
    if k in seen:
        continue
    q, comp = [k], []
    seen.add(k)
    while q:
        a = q.pop()
        comp.append(S[a])
        for d in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)):
            b = (a[0] + d[0], a[1] + d[1])
            if b in S and b not in seen:
                seen.add(b); q.append(b)
    clusters.append(comp)
for comp in sorted(clusters, key=len, reverse=True)[:8]:
    xs = [c[0] for c in comp]; zs = [c[1] for c in comp]
    print('  cluster cells=%d centre (%.0f,%.0f) x %.0f..%.0f z %.0f..%.0f water level %s' % (len(comp), sum(xs) / len(xs), sum(zs) / len(zs), min(xs), max(xs), min(zs), max(zs), sorted(set(c[3] for c in comp))[:4]))
# slope to the west of the valley: for rows z=-560..-300, height at x=-1900,-1850...-1700
print('west slope profile (height by x) at several z:')
for z in (-560, -500, -440, -380, -320):
    j = round((z - Z0) / STEP)
    print('  z=%d: ' % z + ' '.join('%d:%d' % (x, cell(round((x - X0) / STEP), j)[0]) for x in range(-2000, -1650, 50)))
