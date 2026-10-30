"""Fix worker wx3 - F08_13 gate_arch_stone (category v4_roads).
Reviewer: saturated red/blue primary panels verge on neon; mild blocky two-tone stone patches.
Fix: one uniform stone tone with thin course lines (no per-course random key), muted banner panels.
Copied from v4_wj_roads.gate_arch_stone; never edits the original.
"""
import math, random
import kitlib
from kitlib import reset, finalize, box, cyl, ball, lathe, tube, torus, poly_prism
# reuse the arch vault/ring helpers from the original roads module
from v4_wj_roads import arch_vault, arch_ring

P = kitlib.PAL
P['wx3r_stone']  = ((190, 182, 164), 'Limestone', 0.0, 0.86, 0)   # single body tone
P['wx3r_course'] = ((172, 164, 148), 'Limestone', 0.0, 0.90, 0)   # thin subtle course line, one step darker
P['wx3r_trim']   = ((214, 206, 190), 'Marble',    0.0, 0.55, 0)
P['wx3r_iron']   = ((96, 92, 88),    'Metal',     0.60, 0.50, 0)   # lightened iron (was near-black)
P['wx3r_glass']  = ((214, 180, 120), 'Glass',     0.0, 0.30, 0)    # warm, non-neon lantern glass
P['wx3r_gold']   = ((198, 160, 78),  'Metal',     1.0, 0.32, 0)
P['wx3r_ban_r']  = ((158, 120, 114), 'Fabric',    0.0, 0.90, 0)    # faded dusty rose, clearly non-primary
P['wx3r_ban_b']  = ((114, 126, 146), 'Fabric',    0.0, 0.90, 0)    # faded dusty slate-blue, clearly non-primary


def gate_arch_stone():
    """F08_13 - stone region gateway, 24 wide x 22 tall. Uniform stone, thin course lines,
    muted banner panels, warm lantern glass. Passage 14 x 14."""
    reset()
    rnd = random.Random(813)
    passage, ph = 14.0, 14.0
    pierw = 5.0
    totalw = passage + 2 * pierw
    zspring = ph - passage / 2
    for sgn in (-1, 1):
        px = sgn * (passage / 2 + pierw / 2)
        # battered pier: ONE clean solid block. (Course inlays removed - at ~0 depth they z-fought
        # the pier face and rendered as heavy black bands; a plain dressed pier reads better.)
        nc = 9
        box('pier%d' % sgn, (pierw, pierw, nc * 2.2), loc=(px, 0, 1.0 + nc * 1.1), key='wx3r_stone', bev=0.05)
        box('piercap%d' % sgn, (pierw + 0.3, pierw + 0.3, 0.8), loc=(px, 0, zspring + 0.0), key='wx3r_trim', bev=0.1)
        tube('brk%d' % sgn, [(px - sgn * pierw / 2, 0, 9.0), (px - sgn * 1.0, 0, 9.3)], 0.14, 'wx3r_iron', res=3)
        lathe('lg%d' % sgn, [(0.0, 0.0), (0.5, 0.0), (0.5, 1.2), (0.0, 1.3)], loc=(px - sgn * 1.0, 0, 8.0), key='wx3r_glass', segs=6)
    # arch over passage (uniform tone)
    arch_vault('vault', 0, zspring, passage, passage / 2, -2.5, 2.5, key='wx3r_stone')
    for side in (-1, 1):
        arch_ring('vr%d' % side, 0, zspring, passage, passage / 2, side * 2.5, 2.0, rnd, key='wx3r_stone', keystone=False)
    box('lintel', (totalw, 5.0, 1.0), loc=(0, 0, zspring + passage / 2 + 0.6), key='wx3r_trim', bev=0.08)
    # merlons - uniform tone
    nm_ = 7
    for i in range(nm_):
        x = -totalw / 2 + totalw * (i + 0.5) / nm_
        box('mer%d' % i, (totalw / nm_ - 0.8, 4.0, 1.8), loc=(x, 0, zspring + passage / 2 + 2.0), key='wx3r_stone', bev=0.06)
    box('keystone', (1.6, 5.2, 3.0), loc=(0, 0, zspring + passage / 2 - 0.5), key='wx3r_trim', bev=0.1)
    ball('keycarve', 0.6, loc=(0, -2.6, zspring + passage / 2 - 0.5), key='wx3r_gold', segs=10, rings=7, scale=(1, 0.3, 1))
    # hanging banners - muted wine / indigo
    for sgn in (-1, 1):
        bx = sgn * 4.0
        poly_prism('ban%d' % sgn, [(-1.4, 0), (1.4, 0), (1.4, -5.5), (0.8, -6.5), (-0.8, -6.5), (-1.4, -5.5)], 0.1,
                   loc=(bx, -2.7, zspring + passage / 2 - 0.5), key='wx3r_ban_r' if sgn < 0 else 'wx3r_ban_b', rot=(90, 0, 0))
        ball('bane%d' % sgn, 0.5, loc=(bx, -2.85, zspring + passage / 2 - 3.5), key='wx3r_gold', segs=8, rings=6, scale=(1, 0.3, 1))
    return finalize('gate_arch_stone', smooth_angle=30)


BATCHES = {
    'gate': ('v4_roads', [('F08_13_gate_arch_stone', gate_arch_stone, (1.0, -1.1, 0.35))]),
}
