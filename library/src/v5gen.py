"""v5gen - family generators for the v5 modules (houses, towers, walls, rocks, trees, ruins). All draw into an Acc.
K arguments are dicts of palette keys (strings); callers register their own <worker>_ keys and pass them in.
Front faces -Y. Ground is z = z0. Nothing here emits light. Sizes are in studs.
"""
import math
import random
import kitlib
from v5kit import Acc, polar, tang, band, strata


def reg(prefix, table):
    """Register palette entries {name: ((r,g,b), 'RobloxMaterial', metallic, roughness)} as <prefix>_<name>; returns {name: key}."""
    out = {}
    for n, (rgb, m, met, rough) in table.items():
        kitlib.PAL[f'{prefix}_{n}'] = (rgb, m, met, rough, 0)
        out[n] = f'{prefix}_{n}'
    return out


# ------------------------------------------------------------------ roofs
def roof_lines(A, w, d, h, loc, key, n=5, rot_z=90.0, thick=0.18):
    """Shingle/tile course lines on a gable roof built with A.gable(w, d, h, loc, ..., (0, 0, rot_z)) (w = eave width, d = ridge length)."""
    c, s = math.cos(math.radians(rot_z)), math.sin(math.radians(rot_z))
    for k in range(1, n + 1):
        t = k / (n + 1.0)
        for sg in (-1, 1):
            x = sg * (w / 2.0) * (1 - t)
            z = h * t + 0.07
            p0 = (loc[0] + x * c - (-d / 2.0 - 0.15) * s, loc[1] + x * s + (-d / 2.0 - 0.15) * c, loc[2] + z)
            p1 = (loc[0] + x * c - (d / 2.0 + 0.15) * s, loc[1] + x * s + (d / 2.0 + 0.15) * c, loc[2] + z)
            A.beam(p0, p1, 0.42, thick, key)


# ------------------------------------------------------------------ houses
def _window(A, x, y, z, face, K, w=2.0, h=2.6, shutters=True, frame=None):
    """Window on a wall face. face = outward angle in degrees (270 = front/-Y, 90 = back, 0 = +X, 180 = -X)."""
    tx, ty = tang(face)
    ca, sa = math.cos(math.radians(face)), math.sin(math.radians(face))
    fr = frame or K['timber']
    P = lambda off, out, zz: (x + tx * off + ca * out, y + ty * off + sa * out, zz)
    A.box((0.3, w, h), P(0, 0.1, z), K['glass'], (0, 0, face), bev=0)
    A.box((0.45, w + 0.7, 0.4), P(0, 0.2, z + h / 2 + 0.2), fr, (0, 0, face), bev=0)
    A.box((0.6, w + 0.9, 0.35), P(0, 0.3, z - h / 2 - 0.15), K['stone'], (0, 0, face), bev=0)
    for sg in (-1, 1):
        A.box((0.45, 0.36, h), P(sg * (w / 2 + 0.2), 0.2, z), fr, (0, 0, face), bev=0)
    A.box((0.42, w, 0.16), P(0, 0.3, z), fr, (0, 0, face), bev=0)
    A.box((0.42, 0.16, h), P(0, 0.3, z), fr, (0, 0, face), bev=0)
    if shutters:
        for sg in (-1, 1):
            A.box((0.18, w * 0.5, h + 0.2), P(sg * (w / 2 + 0.2 + w * 0.25 + 0.1), 0.35, z), K['shutter'], (0, 0, face), bev=0)


def house(A, rnd, w, d, n=2, K=None, cx=0.0, cy=0.0, z0=0.0, hs=6.2, jetty=0.9, pitch=0.7, ridge_x=True, chimney=True, door=True,
          shutters=True, hip=False, dormers=0, arcade=False, balcony=False, sign=False, belfry=False, wall_key=None):
    """Half-timbered house: stone plinth, n storeys with timber frame + bracing + windows, jettied upper floors, tiled roof with course lines."""
    pl = 1.1
    A.box((w + 0.9, d + 0.9, pl), (cx, cy, z0 + pl / 2), K['stone'], bev=0.12)
    z = z0 + pl
    wk = wall_key or K['wall']
    dd = d
    for s in range(n):
        j = jetty if s > 0 else 0.0
        dd = d + 2 * j
        arc = arcade and s == 0
        if arc:                                                                              # open arcade on the ground floor: columns + back wall
            A.box((w, 0.9, hs), (cx, cy + d / 2 - 0.45, z + hs / 2), wk)
            A.box((0.9, d, hs), (cx - w / 2 + 0.45, cy, z + hs / 2), wk)
            A.box((0.9, d, hs), (cx + w / 2 - 0.45, cy, z + hs / 2), wk)
            nc = max(3, int(w / 4.2))
            for i in range(nc + 1):
                x = cx - w / 2 + 0.6 + i * (w - 1.2) / nc
                A.cyl(0.55, hs - 0.7, (x, cy - d / 2 + 0.7, z), K['stone'], verts=10)
                A.box((1.5, 1.5, 0.5), (x, cy - d / 2 + 0.7, z + hs - 0.45), K['stone'])
                A.box((1.5, 1.5, 0.4), (x, cy - d / 2 + 0.7, z + 0.2), K['stone'])
            A.box((w, 1.3, 0.9), (cx, cy - d / 2 + 0.7, z + hs - 0.2), K['timber'])
        else:
            A.box((w, dd, hs), (cx, cy, z + hs / 2), wk)
        for sx in (-1, 1):
            for sy in (-1, 1):
                A.box((0.75, 0.75, hs + 0.2), (cx + sx * w / 2, cy + sy * dd / 2, z + hs / 2), K['timber'], bev=0.08)
        for sy in (-1, 1):
            yy = cy + sy * (dd / 2 + 0.03)
            A.box((w + 0.6, 0.6, 0.6), (cx, yy, z + 0.3), K['timber'], bev=0.06)
            A.box((w + 0.6, 0.6, 0.6), (cx, yy, z + hs - 0.3), K['timber'], bev=0.06)
            if not arc:
                A.box((w, 0.5, 0.42), (cx, yy, z + hs * 0.5), K['timber'], bev=0.05)
                for sx in (-1, 1):
                    A.beam((cx + sx * w / 2, yy, z + 0.5), (cx + sx * (w / 2 - 2.8), yy, z + hs * 0.5 - 0.2), 0.4, 0.4, K['timber'])
                    A.beam((cx + sx * w / 2, yy, z + hs - 0.5), (cx + sx * (w / 2 - 2.8), yy, z + hs * 0.5 + 0.2), 0.4, 0.4, K['timber'])
                for xs in range(int(-w / 2 + 3), int(w / 2 - 2), 3):
                    A.box((0.4, 0.45, hs - 1.2), (cx + xs, yy, z + hs / 2), K['timber'], bev=0)
        for sx in (-1, 1):
            xx = cx + sx * (w / 2 + 0.03)
            A.box((0.6, dd + 0.6, 0.6), (xx, cy, z + 0.3), K['timber'], bev=0.06)
            A.box((0.6, dd + 0.6, 0.6), (xx, cy, z + hs - 0.3), K['timber'], bev=0.06)
            A.box((0.5, dd, 0.42), (xx, cy, z + hs * 0.5), K['timber'], bev=0.05)
        wz = z + hs * 0.56
        if not arc:
            nwf = max(1, int((w - 3.0) / 4.4))
            for sy, face in ((-1, 270), (1, 90)):
                for i in range(nwf):
                    x = cx + (i - (nwf - 1) / 2.0) * 4.4
                    if sy < 0 and s == 0 and door and abs(x - cx) < 2.6:
                        continue
                    _window(A, x, cy + sy * (dd / 2 + 0.05), wz, face, K, 2.0, 2.6, shutters)
            nws = max(1, int((dd - 3.0) / 4.6))
            for sx, face in ((-1, 180), (1, 0)):
                for i in range(nws):
                    _window(A, cx + sx * (w / 2 + 0.05), cy + (i - (nws - 1) / 2.0) * 4.6, wz, face, K, 2.0, 2.6, shutters)
        if s > 0 and jetty > 0.3:                                                            # brackets under the jetty
            for xs in range(int(-w / 2 + 2), int(w / 2 - 1), 4):
                for sy in (-1, 1):
                    A.beam((cx + xs, cy + sy * (d / 2 - 0.1), z - 1.5), (cx + xs, cy + sy * (dd / 2 + 0.05), z), 0.35, 0.5, K['timber'], up=(1, 0, 0))
        if s == 0 and door:                                                                   # front door, step and hood
            yf = cy - dd / 2
            A.box((2.5, 0.4, 4.2), (cx, yf - 0.05, z + 2.1), K['door'], bev=0.04)
            for sg in (-1, 1):
                A.box((0.55, 0.7, 4.6), (cx + sg * 1.5, yf - 0.1, z + 2.3), K['timber'], bev=0.05)
            A.box((3.9, 0.8, 0.6), (cx, yf - 0.1, z + 4.6), K['timber'], bev=0.05)
            A.box((4.6, 1.8, 0.35), (cx, yf - 0.9, z + 5.2), K['roof'], (-12, 0, 0), bev=0)
            A.box((4.0, 1.8, 0.5), (cx, yf - 1.2, z - pl + 0.35 + pl - 0.25), K['stone'], bev=0.08)
            A.box((3.2, 1.0, 0.5), (cx, yf - 2.1, z - pl + 0.25 + pl - 0.45), K['stone'], bev=0.08)
        z += hs
    if balcony:
        yb = cy - dd / 2 - 1.1
        A.box((w * 0.5, 2.2, 0.4), (cx, yb, z - hs + 0.2), K['timber'])
        for xs in range(-3, 4):
            A.box((0.25, 0.25, 1.4), (cx + xs * (w * 0.5 / 6.0), yb - 0.95, z - hs + 1.1), K['timber'], bev=0)
        A.box((w * 0.5, 0.3, 0.3), (cx, yb - 0.95, z - hs + 1.85), K['timber'], bev=0)
    ov = 1.2
    Ev = (dd + 2 * ov) if ridge_x else (w + 2 * ov)
    Lr = (w + 2 * ov) if ridge_x else (dd + 2 * ov)
    h = (Ev / 2.0) * pitch
    if hip:
        top = (max(Lr - Ev, 0.8), 0.7)
        A.frustum((Lr, Ev) if ridge_x else (Ev, Lr), top if ridge_x else (top[1], top[0]), h, (cx, cy, z), K['roof'], bev=None) if False else \
            A.frustum((Lr, Ev) if ridge_x else (Ev, Lr), top if ridge_x else (top[1], top[0]), h, (cx, cy, z), K['roof'])
    else:
        if ridge_x:
            A.gable(Ev, Lr, h, (cx, cy, z), K['roof'], (0, 0, 90))
        else:
            A.gable(Ev, Lr, h, (cx, cy, z), K['roof'], (0, 0, 0))
        A.box((Lr + 0.3, 0.6, 0.45), (cx, cy, z + h + 0.05), K['cap'], (0, 0, 0 if ridge_x else 90), bev=0.06)
        for t in (0.22, 0.42, 0.62, 0.82):                                                   # tile course lines on both slopes
            for sg in (-1, 1):
                if ridge_x:
                    p0 = (cx - Lr / 2, cy + sg * (Ev / 2) * (1 - t), z + h * t + 0.05)
                    p1 = (cx + Lr / 2, cy + sg * (Ev / 2) * (1 - t), z + h * t + 0.05)
                    A.beam(p0, p1, 0.35, 0.16, K['roof2'], up=(0, sg * h, Ev / 2))
                else:
                    p0 = (cx + sg * (Ev / 2) * (1 - t), cy - Lr / 2, z + h * t + 0.05)
                    p1 = (cx + sg * (Ev / 2) * (1 - t), cy + Lr / 2, z + h * t + 0.05)
                    A.beam(p0, p1, 0.35, 0.16, K['roof2'], up=(sg * h, 0, Ev / 2))
        for sg in (-1, 1):                                                                   # barge boards on the gable ends
            for sd in (-1, 1):
                if ridge_x:
                    A.beam((cx + sg * Lr / 2, cy + sd * Ev / 2, z), (cx + sg * Lr / 2, cy, z + h), 0.3, 0.5, K['timber'], up=(1, 0, 0))
                else:
                    A.beam((cx + sd * Ev / 2, cy + sg * Lr / 2, z), (cx, cy + sg * Lr / 2, z + h), 0.3, 0.5, K['timber'], up=(0, 1, 0))
    if chimney:
        cxx, cyy = (cx + w * 0.28, cy) if ridge_x else (cx, cy + dd * 0.28)
        A.box((1.9, 1.9, h + 2.8), (cxx, cyy, z + (h + 2.8) / 2 - 0.2), K['stone'], bev=0.1)
        A.box((2.5, 2.5, 0.45), (cxx, cyy, z + h + 2.4), K['cap'], bev=0.08)
        A.box((1.0, 1.0, 0.7), (cxx, cyy, z + h + 2.85), K['stone'], bev=0.05)
    for i in range(dormers):
        xd = cx + (i - (dormers - 1) / 2.0) * 6.0
        yd = cy - (Ev / 2.0) * 0.45
        A.box((2.6, 2.0, 2.6), (xd, yd, z + h * 0.45 + 1.0), K['wall'])
        A.gable(3.4, 2.8, 1.5, (xd, yd - 0.3, z + h * 0.45 + 2.3), K['roof'], (0, 0, 90))
        A.box((0.3, 1.2, 1.5), (xd, yd - 1.05, z + h * 0.45 + 1.1), K['glass'], bev=0)
    if sign:                                                                                  # hanging inn / shop sign
        A.beam((cx + w / 2 - 1.5, cy - dd / 2 - 0.1, z - hs * 0.6), (cx + w / 2 - 1.5, cy - dd / 2 - 3.0, z - hs * 0.6), 0.25, 0.25, K['iron'])
        A.box((0.25, 2.2, 1.7), (cx + w / 2 - 1.5, cy - dd / 2 - 2.9, z - hs * 0.6 - 1.1), K['sign'], bev=0)
    if belfry:
        A.box((4.0, 4.0, 4.5), (cx, cy, z + h + 2.0), K['wall'])
        for sg in (-1, 1):
            A.box((0.8, 0.8, 4.5), (cx + sg * 1.6, cy - 1.6, z + h + 2.0), K['timber'])
            A.box((0.8, 0.8, 4.5), (cx + sg * 1.6, cy + 1.6, z + h + 2.0), K['timber'])
        A.cyl(3.4, 4.5, (cx, cy, z + h + 4.2), K['roof'], verts=4, r2=0.0, start=45)
        A.ball(0.8, (cx, cy, z + h + 3.2), K['gold'], segs=8, rings=5)
    return z + h


# ------------------------------------------------------------------ round towers
def round_tower(A, rnd, r, h, K, cx=0.0, cy=0.0, z0=0.0, top='cone', slits=3, bands=2, door=False, flag=False, verts=24, ruin=False, roof_k=1.7):
    """Stone round tower: battered plinth, wall with string courses and slit windows, corbelled top with merlons or a tiled cone roof."""
    A.cyl(r + 1.3, 2.8, (cx, cy, z0), K['stone'], verts=verts, r2=r + 0.3)
    hb = h - 2.8
    A.cyl(r, hb, (cx, cy, z0 + 2.8), K['wall'], verts=verts, r2=r - 0.35)
    for k in range(bands):
        zb = z0 + 2.8 + hb * (k + 1) / (bands + 1)
        A.sweep([(r - 0.6, -0.35), (r + 0.4, -0.35), (r + 0.4, 0.35), (r - 0.6, 0.35)], 0, 360, verts, K['trim'], loc=(cx, cy, zb))
    nsl = 5
    for row, fz in enumerate((0.3, 0.55, 0.78)[:slits]):
        for i in range(nsl):
            a = 270 + i * 360.0 / nsl + (row % 2) * 36.0
            x, y, _ = polar(r + 0.05, a)
            zz = z0 + 2.8 + hb * fz
            A.box((0.5, 0.75, 2.5), (cx + x, cy + y, zz), K['dark'], (0, 0, a), bev=0)
            A.box((0.6, 1.5, 0.4), (cx + x * 1.01, cy + y * 1.01, zz + 1.4), K['trim'], (0, 0, a), bev=0)
            A.box((0.6, 1.5, 0.4), (cx + x * 1.01, cy + y * 1.01, zz - 1.4), K['trim'], (0, 0, a), bev=0)
    zt = z0 + h
    if door:
        x, y, _ = polar(r + 0.1, 270)
        A.box((0.5, 3.0, 4.6), (cx + x, cy + y, z0 + 3.5), K['door'], (0, 0, 270), bev=0.05)
        for sg in (-1, 1):
            A.box((0.8, 0.7, 5.2), (cx + x - 0.1, cy + y + sg * 0.0 + 0.0 - 0.0, z0 + 3.5), K['trim'], (0, 0, 270), bev=0) if False else None
        A.box((1.0, 4.0, 0.7), (cx + x, cy + y - 0.1, z0 + 6.2), K['trim'], (0, 0, 270), bev=0.05)
    if ruin:
        for k in range(10):
            a = rnd.uniform(0, 360)
            x, y, _ = polar(r - 0.8, a)
            A.chunk((2.6, 2.2, rnd.uniform(1.0, 4.0)), (cx + x, cy + y, zt + 0.5), K['wall'], (0, 0, a), 0.15, rnd)
        for k in range(10):
            x, y, _ = polar(r + rnd.uniform(1.0, 4.5), rnd.uniform(0, 360))
            A.chunk((rnd.uniform(1.0, 2.4),) * 2 + (rnd.uniform(0.7, 1.6),), (cx + x, cy + y, z0 + 0.6), K['stone'], (0, 0, rnd.uniform(0, 90)), 0.2, rnd)
        return zt
    for k in range(verts):                                                                    # corbel table under the top
        a = 360.0 * k / verts
        x, y, _ = polar(r + 0.55, a)
        A.box((0.8, 0.9, 0.9), (cx + x, cy + y, zt - 0.7), K['trim'], (0, 0, a), bev=0)
    A.sweep([(r - 0.2, zt - 0.35), (r + 1.3, zt - 0.35), (r + 1.3, zt + 0.25), (r - 0.2, zt + 0.25)], 0, 360, verts, K['trim'], loc=(cx, cy, 0))
    if top == 'crenel':
        A.sweep([(r - 0.1, zt + 0.25), (r + 1.3, zt + 0.25), (r + 1.3, zt + 1.0), (r - 0.1, zt + 1.0)], 0, 360, verts, K['deck'], loc=(cx, cy, 0))
        nm = max(10, int(2 * math.pi * (r + 0.6) / 3.2))
        for k in range(nm):
            a = 360.0 * k / nm
            x, y, _ = polar(r + 0.75, a)
            A.box((r * 0.36 + 0.6, 1.1, 1.7), (cx + x, cy + y, zt + 1.85), K['trim'], (0, 0, a + 90.0), bev=0.07)
    elif top == 'cone':
        rr = r + 1.5
        hr = rr * roof_k
        A.cyl(rr, hr, (cx, cy, zt + 0.25), K['roof'], verts=verts, r2=0.0)
        for k in range(1, 6):
            t = k / 6.0
            A.sweep([(rr * (1 - t) - 0.25, -0.17), (rr * (1 - t) + 0.28, -0.17), (rr * (1 - t) + 0.28, 0.17), (rr * (1 - t) - 0.25, 0.17)], 0, 360, verts, K['roof2'], loc=(cx, cy, zt + 0.25 + hr * t))
        A.revolve([(0.5, 0.0), (0.5, 1.2), (0.9, 1.5), (0.0, 2.4)], (cx, cy, zt + 0.25 + hr), K['gold'], segs=8)
        if flag:
            A.cyl(0.12, 4.2, (cx, cy, zt + hr + 2.4), K['timber'], verts=6)
            A.box((3.0, 0.1, 1.7), (cx + 1.6, cy, zt + hr + 5.4), K['flag'], bev=0)
    elif top == 'flat':
        A.cyl(r + 0.8, 0.9, (cx, cy, zt + 0.25), K['deck'], verts=verts)
    return zt


# ------------------------------------------------------------------ walls
def wall_seg(A, rnd, L, h, t, K, cx=0.0, cy=0.0, z0=0.0, walk=8.0, slits=False, buttress=False, battlement=True):
    """Curtain wall segment along X: battered stone body, wall-walk deck, crenellated outer (-Y) edge, white-capped inner parapet."""
    A.box((L + 0.6, t + 1.6, 1.8), (cx, cy, z0 + 0.9), K['stone'])
    A.frustum((L, t), (L, t - 1.6), h - 1.8, (cx, cy, z0 + 1.8), K['wall'])
    for k in range(3):                                                                        # coursed bands on both faces
        zz = z0 + 1.8 + (h - 1.8) * (k + 1) / 4.0
        for sg in (-1, 1):
            A.box((L + 0.2, 0.35, 0.4), (cx, cy + sg * (t / 2 - 0.55 * (k + 1) / 4.0 + 0.05), zz), K['trim'], bev=0)
    A.box((L, walk, 0.7), (cx, cy + (t - walk) / 2 - 0.0, z0 + h + 0.15), K['deck'])
    A.box((L + 0.3, 1.0, 1.7), (cx, cy + t / 2 - 0.5, z0 + h + 1.15), K['wall'])
    A.box((L + 0.5, 1.3, 0.4), (cx, cy + t / 2 - 0.5, z0 + h + 2.15), K['cap'], bev=0.06)
    if battlement:
        n = int(L / 4.0)
        for k in range(n):
            x = cx - L / 2 + 2.0 + k * 4.0
            A.box((2.4, 1.2, 2.2), (x, cy - t / 2 + 0.6, z0 + h + 1.55), K['wall'], bev=0.08)
            A.box((2.7, 1.5, 0.4), (x, cy - t / 2 + 0.6, z0 + h + 2.8), K['cap'], bev=0.06)
    if slits:
        for k in range(4):
            x = cx - L / 2 + 5.0 + k * 10.0
            A.box((0.7, 0.6, 3.4), (x, cy - t / 2 + 0.05, z0 + h * 0.55), K['dark'], bev=0)
            A.box((1.6, 0.5, 0.5), (x, cy - t / 2 + 0.02, z0 + h * 0.55 + 1.9), K['trim'], bev=0)
    if buttress:
        for k in range(4):
            x = cx - L / 2 + 5.0 + k * 10.0
            A.box((2.4, 3.2, h * 0.8), (x, cy + t / 2 + 1.0, z0 + h * 0.4), K['stone'], (0, 0, 0), bev=0.1)
            A.box((3.0, 3.8, 0.5), (x, cy + t / 2 + 1.0, z0 + h * 0.8 + 0.2), K['trim'], bev=0.06)


def column(A, x, y, z, r, h, K, broken=0.0, rnd=None, flutes=10):
    """Classical column: base, shaft drums with flutes, capital. broken in 0..1 cuts the top and drops a drum beside it."""
    hb = h * (1.0 - broken * 0.55)
    A.cyl(r * 1.45, 0.55, (x, y, z), K['stone'], verts=12)
    A.cyl(r * 1.2, 0.35, (x, y, z + 0.55), K['stone'], verts=12)
    nd = max(2, int(hb / 3.0))
    for i in range(nd):
        zz = z + 0.9 + (hb - 1.9) * i / nd
        A.cyl(r * (1.0 - 0.04 * i / nd), (hb - 1.9) / nd + 0.03, (x, y, zz), K['wall'] if i % 2 else K['stone'], verts=flutes, r2=r * (1.0 - 0.04 * (i + 1) / nd))
    if broken < 0.3:
        A.cyl(r * 1.25, 0.5, (x, y, z + hb - 1.0), K['trim'], verts=12)
        A.box((r * 2.9, r * 2.9, 0.8), (x, y, z + hb - 0.4), K['trim'], bev=0.08)
    elif rnd is not None:
        A.chunk((r * 1.7, r * 1.5, 0.9), (x, y, z + hb), K['wall'], (0, 0, rnd.uniform(0, 90)), 0.2, rnd)
        a = rnd.uniform(0, 360)
        A.cyl(r * 0.95, 2.4, (x + math.cos(math.radians(a)) * r * 2.8, y + math.sin(math.radians(a)) * r * 2.8, z + r * 0.95), K['wall'], verts=10, rot=(0, 90, a))


# ------------------------------------------------------------------ rocks
def cliff(A, rnd, w, d, h, keys, cx=0.0, cy=0.0, z0=0.0, cols=None, cap=None, ledges=True, lean=0.0, mode='strata'):
    """Stratified cliff face: columns of angular chunks of varying depth, ledges and a cap. Face toward -Y.
    mode 'strata' = repeating horizontal bands (same band at the same height in every column), 'grade' = one gradient from keys[0] (bottom) to keys[-1] (top).
    The old (column + layer) % n choice made a checkerboard of square patches; it is gone."""
    cols = cols or max(3, int(w / 7.0))
    cw = w / cols
    for c in range(cols):
        x = cx - w / 2 + cw * (c + 0.5)
        hc = h * rnd.uniform(0.78, 1.0)
        z = z0
        k = 0
        while z < z0 + hc - 0.5:
            sh = min(rnd.uniform(3.0, 5.2), z0 + hc - z)
            dep = d * rnd.uniform(0.7, 1.0) * (1.0 - 0.18 * (z - z0) / h)
            key = strata(keys, int((z - z0) / 4.2)) if mode == 'strata' else band(keys, (z - z0) / max(h, 1e-6), rnd)
            A.chunk((cw * rnd.uniform(1.0, 1.25), dep, sh * 1.08), (x + rnd.uniform(-0.5, 0.5), cy + (d - dep) / 2.0 * 0.3 + rnd.uniform(-0.6, 0.6) + lean * (z - z0) / h * d, z + sh / 2.0),
                    key, (0, 0, rnd.uniform(-6, 6)), 0.11, rnd, (0.96, 0.95))
            z += sh * 0.93
            k += 1
        if cap:
            A.chunk((cw * 1.1, d * 0.8, 1.6), (x, cy, z0 + hc + 0.5), cap, (0, 0, rnd.uniform(-8, 8)), 0.14, rnd)
    if ledges:
        for k in range(2):
            A.chunk((w * rnd.uniform(0.18, 0.3), d * 0.35, 1.0), (cx + rnd.uniform(-w * 0.35, w * 0.35), cy - d * 0.5, z0 + h * rnd.uniform(0.25, 0.7)), keys[1 % len(keys)], (0, 0, 0), 0.12, rnd)


def spire(A, rnd, r, h, keys, cx=0.0, cy=0.0, z0=0.0, tiers=7, lean=0.0, cap=None):
    """Tapering tower of angular chunks (rock spire / hoodoo / sea stack)."""
    z = z0
    for k in range(tiers):
        t = k / max(1, tiers - 1)
        rr = r * (1.0 - 0.72 * t) * rnd.uniform(0.9, 1.1)
        sh = h / tiers * rnd.uniform(0.95, 1.25)
        A.chunk((rr * 2.0, rr * 1.8, sh * 1.1), (cx + lean * t * h * 0.3 + rnd.uniform(-rr * 0.12, rr * 0.12), cy + rnd.uniform(-rr * 0.12, rr * 0.12), z + sh / 2),
                keys[k % len(keys)], (0, 0, rnd.uniform(0, 90)), 0.12, rnd, (0.88, 0.88))
        z += sh * 0.9
    if cap:
        A.chunk((r * 0.9, r * 0.9, h * 0.07), (cx + lean * h * 0.3, cy, z + h * 0.02), cap, (0, 0, rnd.uniform(0, 90)), 0.1, rnd, (0.7, 0.7))
    return z


def rock_arch(A, rnd, span, h, thick, keys, cx=0.0, cy=0.0, z0=0.0, depth=None, n=11, cap=None):
    """Natural rock arch: chunks following a half ellipse, thicker at the feet. Passage runs along Y (front -Y)."""
    depth = depth or thick * 1.6
    for k in range(n + 1):
        t = k / n
        a = math.pi * t
        x = cx + math.cos(a) * span / 2.0
        z = z0 + math.sin(a) * h * 0.82
        sz = thick * (1.25 - 0.45 * math.sin(a))
        A.chunk((sz * 1.15, depth * rnd.uniform(0.85, 1.0), sz * 1.2), (x, cy + rnd.uniform(-0.4, 0.4), z + sz * 0.3), band(keys, math.sin(a), rnd, 0.1),
                (0, math.degrees(a) - 90.0, 0), 0.12, rnd)
    for sg in (-1, 1):
        A.mound(cx + sg * span / 2.0, cy, thick * 2.4, depth * 1.1, h * 0.38, 7, keys, rnd, z0, 0.45, 0.8, 0.13)
    if cap:
        A.chunk((span * 0.5, depth * 0.8, 1.3), (cx, cy, z0 + h * 0.86), cap, (0, 0, 0), 0.1, rnd)


# ------------------------------------------------------------------ trees
def tree(A, rnd, h, crown, K, kind='oak', cx=0.0, cy=0.0, z0=0.0, lean=0.0, dead=False):
    """Low-poly tree. kind: oak (broad), poplar (narrow), beech, birch, conifer, cypress, cherry (flowering), broken (snapped crown)."""
    tr = h * (0.045 if kind in ('oak', 'broken', 'cypress') else 0.03)
    th = h * (0.5 if kind in ('oak', 'beech', 'cherry', 'broken') else 0.35 if kind in ('birch', 'cypress') else 0.12)
    A.cyl(tr * 1.9, h * 0.06, (cx, cy, z0), K['bark'], verts=8, r2=tr * 1.1)                                       # root flare
    for k in range(4):
        a = 90 * k + rnd.uniform(-15, 15)
        x, y, _ = polar(tr * 1.5, a)
        A.beam((cx + x * 1.9, cy + y * 1.9, z0 + 0.1), (cx + x * 0.5, cy + y * 0.5, z0 + h * 0.1), tr * 0.8, tr * 0.8, K['bark'])
    top = z0 + th + (h - th) * (0.55 if kind in ('conifer', 'poplar') else 0.0)
    A.cyl(tr * 1.1, top - z0 - h * 0.05, (cx + lean * 0.1, cy, z0 + h * 0.05), K['bark'], verts=8, r2=tr * 0.55)
    leaf, leaf2 = K['leaf'], K['leaf2']
    if kind == 'conifer':
        n = 7
        for k in range(n):
            t = k / n
            rr = crown * (1.0 - 0.85 * t)
            zz = z0 + h * 0.14 + h * 0.84 * t
            A.cyl(rr, h * 0.2, (cx, cy, zz), leaf if k % 2 else leaf2, verts=9, r2=rr * 0.25)
        return
    if kind in ('poplar', 'cypress', 'birch'):
        n = 11 if kind != 'cypress' else 8
        for k in range(n):
            t = (k + 0.5) / n
            zz = z0 + th + (h - th) * t
            rr = crown * (math.sin(math.pi * (0.15 + 0.8 * t)) * 0.9 + 0.1)
            for j in range(2):
                a = rnd.uniform(0, 360)
                x, y, _ = polar(rr * 0.35, a)
                A.ball(rr * rnd.uniform(0.62, 0.9), (cx + x + lean * t, cy + y, zz + rnd.uniform(-0.6, 0.6)), leaf if (k + j) % 2 else leaf2, segs=9, rings=6, scale=(1, 1, 1.25))
        return
    nb = 9
    for k in range(nb):
        a = 360.0 * k / nb + rnd.uniform(-18, 18)
        x, y, _ = polar(crown * (0.45 + 0.25 * (k % 3)), a)
        zb = z0 + th * rnd.uniform(0.6, 1.0)
        ztop = z0 + h * rnd.uniform(0.62, 0.92)
        A.beam((cx, cy, zb), (cx + x, cy + y, ztop), tr * 0.5, tr * 0.45, K['bark'])
        for j in range(3):                                                                    # three foliage clumps per limb
            f = rnd.uniform(0.55, 1.0)
            key = K['bloom'] if (kind == 'cherry' and (k + j) % 2 == 0) else (leaf if (k + j) % 2 else leaf2)
            A.ball(crown * rnd.uniform(0.34, 0.5), (cx + x * f + rnd.uniform(-1, 1), cy + y * f + rnd.uniform(-1, 1), ztop - (1 - f) * h * 0.1 + j * crown * 0.22),
                   key, segs=9, rings=6, scale=(1, 1, 0.8))
    A.ball(crown * 0.62, (cx + lean, cy, z0 + h * 0.84), leaf2 if kind != 'cherry' else K['bloom'], segs=10, rings=6, scale=(1, 1, 0.85))
    A.ball(crown * 0.45, (cx + lean, cy, z0 + h * 0.96), leaf if kind != 'cherry' else K['bloom'], segs=9, rings=6, scale=(1, 1, 0.85))
    if kind == 'broken':
        A.chunk((tr * 2.4, tr * 2.4, h * 0.2), (cx, cy, z0 + th + h * 0.1), K['bark'], (0, 0, 20), 0.2, rnd, (0.5, 0.5))
