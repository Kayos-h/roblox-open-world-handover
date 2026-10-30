"""lead4_edit_vc2 - corrections after the first look at batch 1 (vc)."""
S = r"C:\Users\Nitro\.kiro\crew\workspace\town"


def edit(path, pairs):
    t = open(path, encoding='utf-8-sig').read()
    for old, new in pairs:
        assert t.count(old) == 1, (path, t.count(old), old[:80])
        t = t.replace(old, new)
    open(path, 'w', encoding='utf-8').write(t)


# lintel wider than the posts: their end faces are no longer coplanar (black strips)
edit(S + r"\library\src\v5_fx_vc.py", [("A.box((23.0, 2.9, 8.4), (-R + R * math.cos(ar), R * math.sin(ar), 15.8), VC['stone2'], (0, 0, a), bev=0.1)",
                                        "A.box((23.6, 2.9, 8.4), (-R + R * math.cos(ar), R * math.sin(ar), 15.8), VC['stone2'], (0, 0, a), bev=0.1)")])
p = S + r"\lead4_snip_vc.py"
edit(p, [
    ("        x2 = min(half, x + 3.0)\n        for y in (-3.45, 3.45):\n            A.beam((x, y, zd(x) - 0.95), (x2, y, zd(x2) - 0.95), 0.95, 0.85, VC['timber'])\n            A.beam((x, y * 1.04, zd(x) + 1.95), (x2, y * 1.04, zd(x2) + 1.95), 0.55, 0.5, VC['timber'])",
     "        x2 = min(half, x + 5.8)\n        for y in (-3.45, 3.45):\n            A.beam((x, y, zd(x) - 0.95), (x2, y, zd(x2) - 0.95), 0.95, 0.85, VC['timber'])\n            A.beam((x, y, zd(x) + 1.95), (x2, y, zd(x2) + 1.95), 0.55, 0.5, VC['timber'])"),
    ("            A.box((0.6, 0.6, 2.2), (xx, y * 1.04, zd(xx) + 0.9), VC['timber'], bev=0.04)", "            A.box((0.6, 0.6, 2.2), (xx, y, zd(xx) + 0.9), VC['timber'], bev=0.04)"),
    ("    for xx in range(int(-half), int(half) + 1, 6):", "    for xx in range(int(-half), int(half) + 1, 8):"),
    ("recolor=[LK.ramp([VC['stone'], VC['stone2']], RAMP_A, trange=(0.0, 24.0), wobble=0.07)])()", "recolor=[LK.ramp(STONE3, RAMP_A, trange=(0.0, 24.0), wobble=0.07)])()"),
    ("recolor=[LK.ramp([VC['stone'], VC['stone2']], RAMP_B, trange=(0.0, 24.0), wobble=0.07)])()", "recolor=[LK.ramp(STONE3, RAMP_B, trange=(0.0, 24.0), wobble=0.07)])()"),
    ("""    return LK.wrap(ORIG.shrine_1, recolor=[LK.ramp(STONE3, RAMP_A, trange=(0.0, 12.0), wobble=0.08),
                                           LK.ramp([VC['f_blue']], [VC['f_red']]), LK.ramp([VC['f_green']], [VC['f_yellow']])])()""",
     """    return LK.wrap(ORIG.shrine_1, post=_flags1_post, prune=[dict(keys=[VC['f_blue'], VC['f_white'], VC['f_red'], VC['f_green'], VC['f_yellow']], max_size=3.0)],
                   recolor=[LK.ramp(STONE3, RAMP_A, zlim=(-1.0, 11.5), trange=(0.0, 11.0), wobble=0.08)])()"""),
    ("def ne02_03():\n    return _boulders(3)", "def ne02_03():\n    return LK.wrap(lambda: _boulders(3), recolor=[LK.ramp([P['rock_d']], [PBR['rock_b'], PBR['rock_c']], trange=(0.0, 14.0), wobble=0.1)])()"),
    ("def _hall3_back(A):", "def _flags1_post(A):\n    for k, key in enumerate((VC['f_red'], VC['f_yellow'], VC['f_blue'])):\n        A.box((1.5, 0.12, 0.7), (0.85, 0.0, 13.5 - k * 0.85), key, bev=0.02)\n\n\ndef _hall3_back(A):"),
])
print('vc snippet corrected')
