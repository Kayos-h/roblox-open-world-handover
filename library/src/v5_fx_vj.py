"""v5_fx_vj - FIX ROUND builder for assignment A6 (worker vj). Owner: builder A6.
Replaces round-1 vj RW01_01 badlands mesa (MAJOR: crude offset slab stack -> coherent banded mesa with aligned connected courses + closed cap + talus).
Keeps the RW01_01 footprint so the export replaces the old mesh in place. Reuses vj palette via ORIG. New keys only under vj_f_.
No glow. Front -Y, pivot bottom centre. 75.7 x 70.3 x 79.9.
"""
import math
import random
import kitlib
from kitlib import reset, finalize
import v4util
import v5kit
from v5kit import Acc, polar, tang, mk, ids, band, strata
import v5gen as G
from v5gen import house, round_tower, wall_seg, column, cliff, spire, rock_arch, tree
import v5_vj as ORIG          # round-1 module: reuse its M palette + BANDS; never edit it

M = ORIG.M

P = G.reg('vj_f', {
    'red':    ((176, 92, 60),  'Sandstone', 0.0, 0.92),
    'red_d':  ((150, 70, 48),  'Sandstone', 0.0, 0.93),
    'sand':   ((214, 184, 140),'Sandstone', 0.0, 0.9),
    'cream':  ((226, 208, 170),'Sandstone', 0.0, 0.88),
    'orange': ((200, 120, 70), 'Sandstone', 0.0, 0.92),
    'cap':    ((234, 214, 174),'Limestone', 0.0, 0.85),
    'base':   ((120, 84, 60),  'Ground', 0.0, 1.0),
    'moss':   ((110, 126, 70), 'Grass', 0.0, 1.0),
})
# graded bottom->top bands: one clear gradient, not random coloured slabs
BANDS = [P['red_d'], P['red'], P['orange'], P['sand'], P['cream']]


def _fin(A, name):
    A.to_scene()
    return finalize(name, 28)


def mesa_closed():
    """RW01_01 - a coherent tapering mesa: aligned horizontal courses of one connected faceted mass, graded colour, closed flat cap, talus skirt.
    Not a pile of offset slabs - each course is a single wide faceted prism sharing the one below, so the silhouette reads as a solid butte."""
    reset()
    A = Acc()
    rnd = random.Random(11000)
    # dirt apron at the foot
    A.mound(0, 0, 78.0, 72.0, 7.0, 26, [P['base'], P['red_d']], rnd, 0.0, 0.3, 0.6, 0.1)
    # the mesa body: tall connected courses, each a many-sided prism (16-gon) that tapers gently.
    # Using one prism per course (shared footprint, small inset) reads as a monolithic butte, not loose slabs.
    nb = 11
    z = 5.0
    r0 = 36.0
    for k in range(nb):
        t = k / (nb - 1.0)
        r = r0 * (1.0 - 0.18 * t)                       # gentle, steady taper (clear structure)
        h = (73.0 - 5.0) / nb
        key = BANDS[min(len(BANDS) - 1, int(t * len(BANDS)))]
        # a 16-gon prism course; jitter the radius slightly per vertex for a faceted (not CAD) edge
        pts = []
        for i in range(16):
            a = math.radians(360.0 * i / 16)
            rr = r * (1.0 + rnd.uniform(-0.04, 0.03)) * (0.93 if r0 < 0 else 1.0)
            pts.append((math.cos(a) * rr * 1.05, math.sin(a) * rr * 0.97))   # slightly oval footprint
        A.prism(pts, h * 1.04, (0, 0, z), key)
        # a thin recessed stratum line between courses (reads as sedimentary banding, connected)
        if k < nb - 1:
            for i in range(16):
                a = math.radians(360.0 * i / 16)
                A.box((2.2, 1.0, 0.5), (math.cos(a) * r * 1.02, math.sin(a) * r * 0.95, z + h), M['red2'] if k % 2 else P['red_d'], (0, 0, math.degrees(a) + 90), bev=0)
        z += h
    # closed flat cap (solid plate, no open lip)
    rc = r0 * 0.82 * 1.02
    capts = [(math.cos(math.radians(360.0 * i / 16)) * rc * 1.05, math.sin(math.radians(360.0 * i / 16)) * rc * 0.97) for i in range(16)]
    A.prism(capts, 2.4, (0, 0, z), P['cap'])
    A.prism([(p[0] * 0.9, p[1] * 0.9) for p in capts], 1.2, (0, 0, z + 2.4), P['sand'])
    # erosion gullies: shallow recessed channels on the lower front face (kept inside the taper so they never protrude)
    for gx in (-12.0, 4.0, 15.0):
        A.box((2.2, 2.0, 30.0), (gx, -24.0, 22.0), M['red2'], bev=0)
    # talus skirt of fallen rubble at the base, touching the ground (ties the butte to the terrain)
    for k in range(20):
        a = rnd.uniform(0, 360)
        x, y, _ = polar(rnd.uniform(30, 40), a)
        A.chunk((rnd.uniform(5, 11), rnd.uniform(4, 9), rnd.uniform(5, 16)), (x, y * 0.92, rnd.uniform(4, 16)), BANDS[k % len(BANDS)], (0, 0, a), 0.16, rnd, (0.8, 0.8))
    for k in range(10):
        A.ball(rnd.uniform(1.4, 2.4), (rnd.uniform(-18, 18), rnd.uniform(-16, 16), z + 3.0), P['moss'], segs=6, rings=4, scale=(1.5, 1.2, 0.35))
    ob = _fin(A, 'badlands_mesa_closed')
    return v5kit.fit(ob, w=75.7, d=70.3, h=79.9)


def natural_gate():
    """RW01_02 (round 3, lead) - natural entrance gateposts: two rough posts of stacked sandstone blocks in graded warm colours (no plain grey), tapering and leaning a little, rope band,
    moss crowns, base stones that touch the posts; NO lintel (no freestanding arch). A timber signpost with a plank and a cream plaque stands between them. 24 x 7 x 20."""
    reset()
    A = Acc()
    rnd = random.Random(11002)
    for sg in (-1, 1):
        for k in range(4):
            w = 5.4 - k * 0.55
            d = 4.8 - k * 0.45
            A.chunk((w, d, 5.4), (sg * (9.5 - 0.2 * k) + rnd.uniform(-0.25, 0.25), rnd.uniform(-0.3, 0.3), 2.6 + k * 4.5), BANDS[k], (0, 0, rnd.uniform(-8, 8)), 0.07, rnd, (0.95, 0.95))
        A.box((5.6, 5.0, 0.5), (sg * 9.3, 0, 6.2), M['rope'], bev=0.04)
        A.ball(1.5, (sg * 8.7, 0, 20.0), P['moss'], segs=7, rings=4, scale=(1.4, 1.2, 0.5))
        for k in range(2):
            A.chunk((rnd.uniform(3.0, 4.2), rnd.uniform(2.6, 3.6), rnd.uniform(1.8, 2.6)), (sg * (9.5 + (1 if k else -1) * 3.2), rnd.uniform(-1.2, 1.2), 1.0), BANDS[k], (0, 0, rnd.uniform(0, 90)), 0.1, rnd)
    A.cyl(0.4, 9.0, (0, 1.6, 0.0), M['plank'], verts=6)
    A.box((6.0, 0.5, 2.8), (0, 1.35, 6.4), M['plank'], bev=0.05)
    A.box((5.0, 0.12, 1.9), (0, 1.0, 6.4), P['cream'], bev=0)
    A.box((6.4, 0.5, 0.4), (0, 1.35, 8.1), M['plank'], bev=0)
    ob = _fin(A, 'natural_entrance_gateposts')
    return v5kit.fit(ob, w=24.3, d=7.0, h=19.8)


def rw01_01():
    return LK.wrap(mesa_closed, prune=[dict(keys=None, max_size=32.0, thin=4.2, max_z=18.0)])()


BATCHES = {
    'reworks': ('v5_rework', mk(list(zip(ids('RW01'), [mesa_closed]))[:1], 0.1)),
}


# --- lead3 registration ---
BATCHES['lead3'] = ('v5_rework', [('RW01_02_rework_existing_02', natural_gate)])


# --- lead4 registration ---
import v5_leadkit as LK
BATCHES['lead4_vj'] = ('v5_rework', mk([('RW01_01_rework_existing_01', rw01_01)], 0.1))
