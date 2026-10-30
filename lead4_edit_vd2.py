"""lead4_edit_vd2 - batch 2 corrections: the stair uses the kit (de-z-fight) and a deeper back mass; the portal-block seams are removed by the kit as well."""
S = r"C:\Users\Nitro\.kiro\crew\workspace\town"


def edit(path, pairs):
    t = open(path, encoding='utf-8-sig').read()
    for old, new in pairs:
        assert t.count(old) == 1, (path, t.count(old), old[:80])
        t = t.replace(old, new)
    open(path, 'w', encoding='utf-8').write(t)


edit(S + r"\lead4_snip_vd.py", [
    ("    A.box((width + 5.8, 4.0, 22.0), (0, 18.0, 11.0), K['stone'])", "    A.box((width + 5.8, 4.4, 22.0), (0, 18.0, 11.0), K['stone'])"),
    ("def stair_wide_b():\n    return _grand_stair2(20.0, 36)", "def stair_wide_b():\n    return LK.wrap(lambda: _grand_stair2(20.0, 36))()"),
    ("def corner_1b():\n    return _corner(135, 11)", "def corner_1b():\n    return LK.wrap(lambda: _corner(135, 11))()"),
    ("def corner_3b():\n    return _corner(150, 13)", "def corner_3b():\n    return LK.wrap(lambda: _corner(150, 13))()"),
])
print('ok')
