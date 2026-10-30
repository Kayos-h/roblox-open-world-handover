"""lead_kit_dz2 - de-z-fight v2: instead of translating a whole box (opposite coplanar ends cancelled each other out), push only the conflicting FACE of the smaller box outward by 0.04."""
p = r"C:\Users\Nitro\.kiro\crew\workspace\town\library\src\v5_leadkit.py"
t = open(p, encoding='utf-8').read()
a = t.index("def _dezfight(")
b = t.index("def _patched(")
new = '''def _dezfight(A, delta=0.04, min_area=0.02, min_overlap=0.08):
    """Find coplanar, same-direction faces of DIFFERENT islands (boxes) that overlap, and push the conflicting face of the smaller island outward along its normal."""
    isl_vol = []
    items = []
    for bm in A.bms.values():
        if not len(bm.faces):
            continue
        bm.normal_update()
        for isl in _islands(bm):
            vs = {v for f in isl for v in f.verts}
            xs = [v.co.x for v in vs]
            ys = [v.co.y for v in vs]
            zs = [v.co.z for v in vs]
            iid = len(isl_vol)
            isl_vol.append((max(xs) - min(xs) + 1e-3) * (max(ys) - min(ys) + 1e-3) * (max(zs) - min(zs) + 1e-3))
            for f in isl:
                items.append((f, iid))
    byn = {}
    for f, iid in items:
        n = f.normal
        if n.z < -0.9 or f.calc_area() < min_area:
            continue
        byn.setdefault((round(n.x, 2), round(n.y, 2), round(n.z, 2)), []).append((n.dot(f.calc_center_median()), f, iid, n.copy()))
    push = {}
    for lst in byn.values():
        lst.sort(key=lambda r: r[0])
        i0 = 0
        while i0 < len(lst):
            i1 = i0 + 1
            while i1 < len(lst) and lst[i1][0] - lst[i0][0] <= 0.015:
                i1 += 1
            cl = lst[i0:i1]
            i0 = i1
            if len({r[2] for r in cl}) < 2:
                continue
            n = cl[0][3]
            a_ = Vector((0, 0, 1)) if abs(n.z) < 0.9 else Vector((1, 0, 0))
            u = n.cross(a_).normalized()
            w = n.cross(u).normalized()
            bx = []
            for _, f, iid, _n in cl:
                us = [vt.co.dot(u) for vt in f.verts]
                ws = [vt.co.dot(w) for vt in f.verts]
                bx.append((min(us), max(us), min(ws), max(ws), iid, f))
            bx.sort(key=lambda b: b[0])
            for i in range(len(bx)):
                for j in range(i + 1, len(bx)):
                    if bx[j][0] >= bx[i][1] - min_overlap:
                        break
                    if bx[i][4] == bx[j][4] or min(bx[i][3], bx[j][3]) - max(bx[i][2], bx[j][2]) <= min_overlap:
                        continue
                    small = bx[i] if isl_vol[bx[i][4]] < isl_vol[bx[j][4]] else bx[j]
                    push[small[5]] = n
    for f, n in push.items():
        for v in f.verts:
            v.co += n * delta
    print('SCRATCH_DZ pushed', len(push), 'faces of', len(isl_vol), 'islands')
    return len(push)


'''
t = t[:a] + new + t[b:]
open(p, 'w', encoding='utf-8').write(t)
print('kit dezfight v2 installed')
