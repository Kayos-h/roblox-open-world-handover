"""lead4_edit_b7 - batch 7: WT13_01 loses the raised joint bars (they read as a grate), RW01_01 prunes the thin base fragments more widely."""
S = r"C:\Users\Nitro\.kiro\crew\workspace\town"


def edit(path, pairs):
    t = open(path, encoding='utf-8-sig').read()
    for old, new in pairs:
        assert t.count(old) == 1, (path, t.count(old), old[:80])
        t = t.replace(old, new)
    open(path, 'w', encoding='utf-8').write(t)


edit(S + r"\lead4_snip_va.py", [("    return LK.wrap(terrace_wall_straight, recolor=[LK.ramp([P['joint']], [P['stone_d']])])()",
                                 "    return LK.wrap(terrace_wall_straight, prune=[dict(keys=[P['joint']], max_size=30.0)])()")])
edit(S + r"\lead4_snip_vj.py", [("prune=[dict(keys=None, max_size=14.0, thin=3.6, max_z=14.0)]", "prune=[dict(keys=None, max_size=32.0, thin=4.2, max_z=18.0)]")])
print('ok')
