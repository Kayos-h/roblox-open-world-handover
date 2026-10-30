"""lead4_edits_vh - kit: prune can target thin islands; fx_vh: DS08_02 pylons thicker and standing on the body."""
S = r"C:\Users\Nitro\.kiro\crew\workspace\town"


def edit(path, pairs):
    t = open(path, encoding='utf-8-sig').read()
    for old, new in pairs:
        assert t.count(old) == 1, (path, t.count(old), old[:80])
        t = t.replace(old, new)
    open(path, 'w', encoding='utf-8').write(t)


edit(S + r"\library\src\v5_leadkit.py", [("""            if size > rule.get('max_size', 2.0):
                continue
""", """            if size > rule.get('max_size', 2.0):
                continue
            if rule.get('thin') is not None and min(max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs)) > rule['thin']:
                continue
""")])
edit(S + r"\library\src\v5_fx_vh.py", [("A.frustum((3.0, 3.0), (1.4, 1.4), 12.0, (sg * (W / 2 - 3.0), -D / 2 + 2.5, bodyh - 2.0), P['sandd'])",
                                       "A.frustum((5.0, 5.0), (2.6, 2.6), 11.0, (sg * (W / 2 - 4.5), -D / 2 + 4.5, bodyh - 2.0), P['sandd'])")])
print('ok')
