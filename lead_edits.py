"""lead_edits - exact text edits inside existing functions of the vh, vi_b and vi_a fix modules (round 3, lead).  Every old string must occur exactly once."""
S = r"C:\Users\Nitro\.kiro\crew\workspace\town\library\src"


def edit(fn, pairs):
    p = S + '\\' + fn
    t = open(p, encoding='utf-8-sig').read()
    for old, new in pairs:
        assert t.count(old) == 1, (fn, t.count(old), old[:90])
        t = t.replace(old, new)
    open(p, 'w', encoding='utf-8').write(t)
    print('edited', fn, len(pairs))


# ---------------------------------------------------------------- vh: skull city buildings 04 (collapsed) and 06 (lean-to), ring temple 02
edit('v5_fx_vh.py', [
    # VC04_06: lean-to roof as one solid wedge seated on the ceiling slab (the tilted plate overhung the back wall and floated)
    ("A.box((W + 1.2, D + 1.2, 1.0), (0, -0.5, ztop + 2.2), tile, (12, 0, 0), bev=0.08)",
     "A.prism([(-D / 2 - 0.6, 0.0), (D / 2 + 0.6, 0.0), (D / 2 + 0.6, 4.4), (-D / 2 - 0.6, 1.2)], W + 1.2, (-(W + 1.2) / 2.0, 0, ztop + 0.7), tile, (90, 0, 90))"),
    ("A.box((W + 1.0, 0.8, 0.6), (0, D / 2 + 0.2, ztop + 3.6), P['dband'], bev=0.06)",
     "A.box((W + 1.4, 0.8, 0.6), (0, D / 2 + 0.4, ztop + 0.7 + 4.4), P['dband'], bev=0.06)"),
    # VC04_04: closed gable roof instead of an open frame with rafters
    ("A.box((W * 0.5, D + 1.0, 0.8), (-W * 0.24, 0, ztop + 2.4), tile, (0, -16, 0), bev=0.08)",
     "A.gable(W + 1.4, D + 1.4, 5.0, (0, 0, ztop + 0.7), tile, (0, 0, 90))"),
    ("A.beam((W * 0.1 + k * 2.0, -D / 2 + 1.0, ztop), (W * 0.1 + k * 2.0, D / 2 - 1.0, ztop + rnd.uniform(1.5, 3.5)), 0.5, 0.5, P['wood'])",
     "pass"),
    ("A.box((2.4, th, mh), (cx + off, cy, ztop + mh / 2.0), wk2, bev=0.1)", "pass"),
    ("A.box((th, 2.4, mh), (cx, cy + off, ztop + mh / 2.0), wk2, bev=0.1)", "pass"),
    # LM16_02: all columns intact under a full entablature, fewer stripes, fallen drums on the plinth top
    ("broken = (i == 1 and k in (1, 4))", "broken = False"),
    ("A.sweep([(R0 + 1.9, wall_top + 0.5), (R0 + 4.9, wall_top + 0.5), (R0 + 4.9, wall_top + 2.6), (R0 + 1.9, wall_top + 2.6)], a0, a0 + 34, 8, P['sandl'])",
     "A.sweep([(R0 + 1.9, wall_top + 0.5), (R0 + 4.9, wall_top + 0.5), (R0 + 4.9, wall_top + 2.6), (R0 + 1.9, wall_top + 2.6)], a0, a1, 22, P['sandl'])"),
    ("for t, key in ((0.25, P['clay']), (0.5, P['sandd']), (0.75, P['clay'])):", "for t, key in ((0.5, P['sandd']),):"),
    ("x, y, _ = polar(R0 + rnd.uniform(4.6, 5.6), aw)", "x, y, _ = polar(R0 + rnd.uniform(3.4, 4.6), aw)"),
    ("A.cyl(1.5, 3.2, (x, y, 1.9), P['sand'], verts=10, rot=(0, 90, aw))", "A.cyl(1.5, 3.2, (x, y, 4.5), P['sand'], verts=10, rot=(0, 90, aw))"),
    ("(x, y, 2.2), (P['sandd'], P['stone'])[k % 2]", "(x, y, 3.9), (P['sandd'], P['stone'])[k % 2]"),
])

# ---------------------------------------------------------------- vi_b: sea arch 01, ruined house 05, bank rock 02
edit('v5_fx_vi_b.py', [
    ("span = 40.0 if i == 0 else 52.0", "span = 56.0 if i == 0 else 52.0"),
    ("h = 48.0 if i == 0 else 40.0", "h = 64.0 if i == 0 else 40.0"),
    ("thick = 11.0 if i == 0 else 8.5", "thick = 12.0 if i == 0 else 8.5"),
    ("G.rock_arch(A, rnd, span, h, thick, ARCH, 0, 0, 0, 14.0, 14 if i == 0 else 18, P['moss'])",
     "G.rock_arch(A, rnd, span, h, thick, ARCH, 0, 0, 0, 26.0 if i == 0 else 14.0, 18, P['moss'])"),
    ("A.box((w * 0.9, 3.0, 0.5), (0, d / 4 + k * 0.1, 10.5 - k * 1.3), R.V['cone'], (34 + k * 2, 0, 0), bev=0.05)",
     "A.box((w + 0.4, 8.2, 0.55), (0, d / 4 + 0.6 + k * 0.0, 8.2), R.V['cone'], (31, 0, 0), bev=0.05) if k == 0 else None"),
    ("A.gable(w * 0.5, 5.0, 2.6, (w * 0.2, d / 4, 10.0), R.V['cap'], (0, 0, 90))",
     "[A.box((0.7, 0.7, 6.0), (sx_ * (w / 2 - 0.4), 0.0, 3.5), P['timber_dk'], bev=0.05) for sx_ in (-1, 1)] + [A.beam((-w / 2 + 0.4, 0.0, 6.2), (w / 2 - 0.4, 0.0, 6.2), 0.7, 0.7, P['timber_dk'])]"),
    ("boulder(-2, 0, 18, 18.5, 9.5, 0.5)",
     "A.chunk((20.0, 15.0, 8.5), (-2.0, 0.0, 4.25), band(keys, 0.45, rnd), (0, 0, 8), 0.07, rnd, (0.78, 0.78))\n"
     "        A.chunk((13.0, 11.0, 6.5), (7.5, -3.0, 3.25), band(keys, 0.25, rnd), (0, 0, -14), 0.08, rnd, (0.8, 0.8))\n"
     "        A.chunk((10.0, 9.0, 5.0), (-10.0, 4.0, 2.5), band(keys, 0.1, rnd), (0, 0, 24), 0.08, rnd, (0.8, 0.8))\n"
     "        A.chunk((9.0, 8.0, 3.4), (-3.0, 0.5, 9.0), band(keys, 0.85, rnd), (0, 0, 35), 0.07, rnd, (0.75, 0.75))\n"
     "        humps.extend([(-3.0, 0.5, 10.2), (7.5, -3.0, 6.4), (-10.0, 4.0, 4.8)])"),
    ("boulder(9, -5, 8, 8, 4.0, 0.25)", "pass"),
    ("A.chunk((5.0, 4.5, 3.0), (6, 6, 1.5), band(keys, 0.3, rnd), (0, 0, 30), 0.14, rnd)", "pass"),
])

# ---------------------------------------------------------------- vi_a: crater rim rocks (lighter low bands)
edit('v5_fx_vi_a.py', [
    ("A.mound(0, 0, 54.0, 44.0, 36.0, 44, ROCK, rnd, 0.0, 0.34, 0.74, 0.14)", "A.mound(0, 0, 54.0, 44.0, 36.0, 44, ROCKL, rnd, 0.0, 0.34, 0.74, 0.14)"),
    ("_ground_rubble(A, rnd, 13, 27.0, 20.0, ROCK, 1.6, 4.2)", "_ground_rubble(A, rnd, 13, 27.0, 20.0, ROCKL, 1.6, 4.2)"),
])
