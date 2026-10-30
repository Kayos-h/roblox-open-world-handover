"""lead4_edits_vc - exact text edits in v5_fx_vc.py: HM04_02 lintel no longer coplanar with the portal posts (those overlapping faces rendered as black squares)."""
S = r"C:\Users\Nitro\.kiro\crew\workspace\town\library\src"
p = S + r"\v5_fx_vc.py"
t = open(p, encoding='utf-8-sig').read()
old = "A.box((23.0, 2.8, 8.4), (-R + R * math.cos(ar), R * math.sin(ar), 15.8), VC['stone2'], (0, 0, a), bev=0.1)"
new = "A.box((23.0, 2.9, 8.4), (-R + R * math.cos(ar), R * math.sin(ar), 15.8), VC['stone2'], (0, 0, a), bev=0.1)"
assert t.count(old) == 1, t.count(old)
t = t.replace(old, new)
open(p, 'w', encoding='utf-8').write(t)
print('fx_vc edited')
