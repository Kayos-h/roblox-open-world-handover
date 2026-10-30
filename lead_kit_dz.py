"""lead_kit_dz - add an automatic de-z-fight step to v5_leadkit.py: coplanar overlapping faces of different boxes (they render as black seams) are separated by sliding the smaller box 0.04 outward."""
p = r"C:\Users\Nitro\.kiro\crew\workspace\town\library\src\v5_leadkit.py"
t = open(p, encoding='utf-8').read()
func = '''
def _dezfight(A, delta=0.04, min_area=0.02, min_overlap=0.08):
    """Find coplanar, same-direction faces of DIFFERENT islands (boxes) that overlap, and slide the smaller island outward along the face normal."""
    isl_data = []
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
            vol = (max(xs) - min(xs) + 1e-3) * (max(ys) - min(ys) + 1e-3) * (max(zs) - min(zs) + 1e-3)
            iid = len(isl_data)
            isl_data.append((vs, vol))
            for f in isl:
                items.append((f, iid))
    byn = {}
    for f, iid in items:
        n = f.normal
        if n.z < -0.9 or f.calc_area() < min_area:
            continue
        byn.setdefault((round(n.x, 2), round(n.y, 2), round(n.z, 2)), []).append((n.dot(f.calc_center_median()), f, iid, n.copy()))
    shifts = {}
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
            a = Vector((0, 0, 1)) if abs(n.z) < 0.9 else Vector((1, 0, 0))
            u = n.cross(a).normalized()
            w = n.cross(u).normalized()
            bx = []
            for _, f, iid, _n in cl:
                us = [vt.co.dot(u) for vt in f.verts]
                ws = [vt.co.dot(w) for vt in f.verts]
                bx.append((min(us), max(us), min(ws), max(ws), iid))
            bx.sort(key=lambda b: b[0])
            for i in range(len(bx)):
                for j in range(i + 1, len(bx)):
                    if bx[j][0] >= bx[i][1] - min_overlap:
                        break
                    if bx[i][4] == bx[j][4] or min(bx[i][3], bx[j][3]) - max(bx[i][2], bx[j][2]) <= min_overlap:
                        continue
                    small = bx[i][4] if isl_data[bx[i][4]][1] < isl_data[bx[j][4]][1] else bx[j][4]
                    shifts.setdefault(small, {})[(round(n.x, 2), round(n.y, 2), round(n.z, 2))] = n
    for iid, ns in shifts.items():
        mv = Vector((0, 0, 0))
        for n in ns.values():
            mv += n * delta
        for v in isl_data[iid][0]:
            v.co += mv
    return len(shifts)

'''
marker = "def _patched(self, keep_normals=()):"
assert t.count(marker) == 1
t = t.replace(marker, func + "\n" + marker)
old = """    for bm in self.bms.values():
        if len(bm.faces):
            bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    for rule in cfg.get('recolor') or []:"""
new = """    for bm in self.bms.values():
        if len(bm.faces):
            bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    if cfg.get('dezfight', True):
        _dezfight(self)
    for rule in cfg.get('recolor') or []:"""
assert t.count(old) == 1
t = t.replace(old, new)
old2 = "def wrap(fn, deform=None, post=None, prune=None, recolor=None):\n    cfg = dict(deform=deform, post=post, prune=prune, recolor=recolor)"
new2 = "def wrap(fn, deform=None, post=None, prune=None, recolor=None, dezfight=True):\n    cfg = dict(deform=deform, post=post, prune=prune, recolor=recolor, dezfight=dezfight)"
assert t.count(old2) == 1
t = t.replace(old2, new2)
t = t.replace("Order inside the hook: deform -> prune -> post -> normals -> recolor", "Order inside the hook: deform -> prune -> post -> normals -> de-z-fight -> recolor")
open(p, 'w', encoding='utf-8').write(t)
print('kit updated')
