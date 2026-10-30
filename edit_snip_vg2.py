"""edit_snip_vg2 - LM06_01: no coplanar tier faces (they render as black seams), larger readable opening."""
p = r"C:\Users\Nitro\.kiro\crew\workspace\town\lead_snip_vg.py"
t = open(p, encoding='utf-8-sig').read()


def sub(old, new):
    global t
    assert t.count(old) == 1, (t.count(old), old[:70])
    t = t.replace(old, new)


sub("    ow, oh = 9.0, 18.0\n    pw = W / 2.0 - ow\n    fy = -25.5", "    ow, oh = 11.0, 22.0\n    pw = W / 2.0 - ow\n    fy = -25.5")
sub("A.box((w, dep, th + 0.6), (sg * (ow + w / 2.0), fy + dep / 2.0, zb + th / 2.0), cols[t], bev=0.6)",
    "A.box((w, dep, th + 0.6), (sg * (ow + w / 2.0), fy + 0.15 * t + dep / 2.0, zb + th / 2.0), cols[t], bev=0.6)")
sub("for t, (zb, ht, wx, dep) in enumerate(((oh, 10.5, 2.0, 49.0), (oh + 9.0, 11.5, 3.0, 47.0), (oh + 19.5, 11.5, 4.0, 42.0))):",
    "for t, (zb, ht, wx, dep) in enumerate(((oh, 9.0, 2.0, 49.0), (oh + 8.0, 9.5, 3.0, 47.0), (oh + 16.0, 12.0, 4.0, 42.0))):")
sub("A.box((2 * ow + 2 * wx, dep, ht + 0.6), (0, fy + dep / 2.0 + 0.2 * t, zb + ht / 2.0), cols[t + 1], bev=0.6)",
    "A.box((2 * ow + 2 * wx, dep, ht + 0.6), (0, fy + 0.2 * t + 0.07 + dep / 2.0, zb + ht / 2.0), cols[t + 1], bev=0.6)")
open(p, 'w', encoding='utf-8').write(t)
print('ok')
