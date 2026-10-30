"""Layout helpers for the Phase 1 rebuild. Placement plan format = mapplan contract
(model, x, z, rot, group, scale, y_offset). rot = direction the model FRONT faces:
0 = +Z (south), 90 = +X (east), 180 = -Z, 270 = -X.
"""
import json, math, random
import world as W

CAT = {m['id']: m for m in json.load(open(r'C:\Users\Nitro\.kiro\crew\workspace\town\mapplan\catalog.json', encoding='utf-8-sig'))}


def norm(dx, dz):
    L = math.hypot(dx, dz)
    return (dx / L, dz / L) if L > 1e-9 else (0.0, 1.0)


def face_rot(fx, fz):
    """rot (degrees) so the model front faces direction (fx, fz)."""
    return math.degrees(math.atan2(fx, fz)) % 360


def obb(cx, cz, hw, hd, rot):
    """Rectangle with half sizes hw (local X) and hd (local Z), rotated by rot."""
    t = math.radians(rot)
    ux = (math.cos(t), -math.sin(t))   # local X axis in world (x, z)
    uz = (math.sin(t), math.cos(t))    # local Z axis (front)
    return (cx, cz, hw, hd, ux, uz)


def obb_overlap(a, b, pad=0.0):
    ax, az, ahw, ahd, aux, auz = a
    bx, bz, bhw, bhd, bux, buz = b
    dx, dz = bx - ax, bz - az
    for (nx, nz) in (aux, auz, bux, buz):
        ra = (ahw * abs(aux[0] * nx + aux[1] * nz) + ahd * abs(auz[0] * nx + auz[1] * nz))
        rb = (bhw * abs(bux[0] * nx + bux[1] * nz) + bhd * abs(buz[0] * nx + buz[1] * nz))
        if abs(dx * nx + dz * nz) > ra + rb + pad:
            return False
    return True


class Polyline:
    def __init__(self, pts):
        self.p = [tuple(q[:2]) for q in pts]
        self.cum = [0.0]
        for i in range(1, len(self.p)):
            self.cum.append(self.cum[-1] + math.hypot(self.p[i][0] - self.p[i - 1][0], self.p[i][1] - self.p[i - 1][1]))
        self.L = self.cum[-1]

    def at(self, s):
        s = max(0.0, min(self.L, s))
        for i in range(1, len(self.p)):
            if s <= self.cum[i] or i == len(self.p) - 1:
                a, b = self.p[i - 1], self.p[i]
                seg = self.cum[i] - self.cum[i - 1]
                t = 0 if seg <= 0 else (s - self.cum[i - 1]) / seg
                d = norm(b[0] - a[0], b[1] - a[1])
                return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t), d
        return self.p[-1], (0.0, 1.0)


def catmull(pts, step=24):
    """Smooth a control polyline (x, z) into a dense curve."""
    if len(pts) < 3:
        out = []
        a, b = pts[0], pts[-1]
        n = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) / step))
        for k in range(n + 1):
            t = k / n
            out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
        return out
    out = []
    P = pts
    for i in range(len(P) - 1):
        p0 = P[max(0, i - 1)]; p1 = P[i]; p2 = P[i + 1]; p3 = P[min(len(P) - 1, i + 2)]
        n = max(1, int(math.hypot(p2[0] - p1[0], p2[1] - p1[1]) / step))
        for k in range(n):
            t = k / n; t2, t3 = t * t, t * t * t
            q = []
            for a in range(2):
                q.append(0.5 * ((2 * p1[a]) + (-p0[a] + p2[a]) * t + (2 * p0[a] - 5 * p1[a] + 4 * p2[a] - p3[a]) * t2 + (-p0[a] + 3 * p1[a] - 3 * p2[a] + p3[a]) * t3))
            out.append(tuple(q))
    out.append(tuple(P[-1]))
    return out


class Plan:
    def __init__(self, area, seed=1):
        self.area = area
        self.items = []
        self.blocks = []      # OBBs that nothing may overlap (buildings)
        self.sblocks = []     # street corridors and plazas (buildings and nature keep off)
        self.soft = []        # OBBs for small things (props, trees) to keep apart
        self.streets = []
        self.rng = random.Random(seed)
        self.missing = []

    # ----------------------------------------------------------- streets
    def street(self, pts, w, mat='Cobblestone', smooth=True, y=None, bank=18, block=True, step=20):
        dense = catmull(pts, step) if smooth else [tuple(p) for p in pts]
        out = []
        for i, (x, z) in enumerate(dense):
            yy = y[i] if isinstance(y, list) else (y if y is not None else W.ground_no_noise(x, z))
            out.append([round(x, 1), round(z, 1), round(yy, 2)])
        self.streets.append({'name': f'{self.area}_{len(self.streets)}', 'w': w, 'mat': mat, 'bank': bank, 'pts': out})
        if block:
            for i in range(len(dense) - 1):
                a, b = dense[i], dense[i + 1]
                L = math.hypot(b[0] - a[0], b[1] - a[1])
                if L < 0.1:
                    continue
                d = norm(b[0] - a[0], b[1] - a[1])
                self.sblocks.append(obb((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, L / 2 + w * 0.3, w + 0.5, face_rot(-d[1], d[0])))
        return Polyline(dense)

    def plaza(self, cx, cz, rx, rz, mat='Pavement', y=None):
        """Paved oval plaza as a fat street segment."""
        if rx >= rz:
            pts = [(cx - (rx - rz), cz), (cx + (rx - rz) + 0.01, cz)]
            w = rz
        else:
            pts = [(cx, cz - (rz - rx)), (cx, cz + (rz - rx) + 0.01)]
            w = rx
        return self.street(pts, w, mat, smooth=False, y=y, bank=10, block=False)

    # ----------------------------------------------------------- placement
    def size(self, model):
        m = CAT.get(model)
        if not m:
            raise KeyError(model)
        return m['size_x'], m['size_z'], m['height']

    def fits(self, box, pad=0.0, soft=False, streets=True):
        for b in self.blocks:
            if obb_overlap(box, b, pad):
                return False
        if streets:
            for b in self.sblocks:
                if obb_overlap(box, b, pad):
                    return False
        if soft:
            for b in self.soft:
                if obb_overlap(box, b, pad):
                    return False
        return True

    def put(self, model, x, z, rot=0.0, group='Misc', check=True, block=True, soft=False, pad=1.0,
            scale=None, yo=None, shrink=1.0, force=False, streets=True):
        sx, sz, h = self.size(model)
        s = scale or 1.0
        box = obb(x, z, sx * s / 2 * shrink, sz * s / 2 * shrink, rot)
        if check and not force and not self.fits(box, pad, soft=True, streets=streets):
            return False
        it = {'model': model, 'x': round(x, 2), 'z': round(z, 2), 'rot': round(rot % 360, 1), 'group': group}
        if scale and abs(scale - 1) > 1e-3:
            it['scale'] = round(scale, 3)
        if yo:
            it['y_offset'] = round(yo, 2)
        self.items.append(it)
        if block:
            self.blocks.append(box)
        else:
            self.soft.append(box)
        return True

    def frontage(self, line, side, models, group, half_w, setback=3.0, gap=(2.0, 5.0), s0=0.0, s1=None,
                 weights=None, max_items=999, props=None, on_place=None):
        """Buildings along one side of a street, fronts facing it. side=+1 right, -1 left."""
        s1 = line.L if s1 is None else s1
        s = s0
        placed = 0
        last = []
        tries = 0
        while s < s1 and placed < max_items and tries < 400:
            tries += 1
            choices = [m for m in models if m not in last[-2:]] or models
            if weights:
                wts = [weights.get(m, 1.0) for m in choices]
                m = self.rng.choices(choices, wts)[0]
            else:
                m = self.rng.choice(choices)
            sx, sz, h = self.size(m)
            sc = s + sx / 2
            if sc + sx / 2 > s1:
                s += 4
                continue
            (px, pz), d = line.at(sc)
            R = (-d[1], d[0])
            nrm = (R[0] * side, R[1] * side)
            off = half_w + setback + sz / 2
            cx, cz = px + nrm[0] * off, pz + nrm[1] * off
            rot = face_rot(-nrm[0], -nrm[1])
            if self.put(m, cx, cz, rot, group, pad=0.8):
                placed += 1
                last.append(m)
                if on_place:
                    on_place(m, cx, cz, rot, nrm, d)
                s += sx + self.rng.uniform(*gap)
            else:
                s += 5
        return placed

    def lamps(self, line, model, group, half_w, spacing=40.0, offset=1.8, s0=10.0, s1=None, alternate=True, side=1):
        s1 = line.L if s1 is None else s1
        s = s0
        k = 0
        n = 0
        while s <= s1:
            (px, pz), d = line.at(s)
            R = (-d[1], d[0])
            sd = side * (1 if (k % 2 == 0 or not alternate) else -1)
            nx, nz = R[0] * sd, R[1] * sd
            x, z = px + nx * (half_w + offset), pz + nz * (half_w + offset)
            if self.put(model, x, z, face_rot(-nx, -nz), group, block=False, check=True, pad=0.0, force=False, streets=False):
                n += 1
            k += 1
            s += spacing
        return n

    def scatter(self, inside, models, n, group, min_gap=2.0, scale=(0.9, 1.15), weights=None, block=False,
                tries=None, rot=None, bbox=None):
        """Random placement inside region test inside(x, z); bbox = (x0, x1, z0, z1)."""
        x0, x1, z0, z1 = bbox
        tries = tries or n * 25
        placed = 0
        for _ in range(tries):
            if placed >= n:
                break
            x = self.rng.uniform(x0, x1); z = self.rng.uniform(z0, z1)
            if not inside(x, z):
                continue
            m = self.rng.choices(models, [weights.get(q, 1) for q in models])[0] if weights else self.rng.choice(models)
            sc = self.rng.uniform(*scale) if scale else None
            r = self.rng.uniform(0, 360) if rot is None else rot
            if self.put(m, x, z, r, group, block=block, pad=min_gap, scale=sc):
                placed += 1
        return placed

    def cluster(self, x, z, models, group, n=4, radius=6.0, scale=None):
        k = 0
        for _ in range(n * 6):
            if k >= n:
                break
            a = self.rng.uniform(0, math.tau); r = self.rng.uniform(0, radius)
            m = self.rng.choice(models)
            if self.put(m, x + math.cos(a) * r, z + math.sin(a) * r, self.rng.uniform(0, 360), group, block=False, pad=0.3,
                        scale=(self.rng.uniform(*scale) if scale else None), streets=False):
                k += 1
        return k

    def line_of(self, model, p0, p1, group, step=None, rot_extra=0.0, block=True, pad=0.3, along='x', streets=True):
        """Repeat a model along a straight line (walls, fences, hedges). Model long axis = local X."""
        sx, sz, h = self.size(model)
        step = step or sx
        L = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
        d = norm(p1[0] - p0[0], p1[1] - p0[1])
        n = max(1, int(math.ceil(L / (step * 0.97))))
        st = L / n
        rot = (math.degrees(math.atan2(-d[1], d[0])) + rot_extra) % 360
        k = 0
        for i in range(n):
            s = st * (i + 0.5)
            x, z = p0[0] + d[0] * s, p0[1] + d[1] * s
            if self.put(model, x, z, rot, group, block=block, pad=pad, check=False):
                k += 1
        return k

    def save(self, path):
        json.dump({'area': self.area, 'terrain': [], 'placements': self.items}, open(path, 'w'), indent=0)
