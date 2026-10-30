p = r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\v4\dress_v4.py'
t = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global t
    assert t.count(a) == n, (t.count(a), a[:60])
    t = t.replace(a, b)
rep("        r = rng.uniform(103, 124)\n", "        r = rng.uniform(112, 134)\n")
rep("        if not free(x, z, 3.0, 6.0, minh=-5):\n            continue\n        r2 = rng.random()",
    "        if not free(x, z, 3.0, 6.0, minh=-5) or E.M(x, z) not in ('G', 'L', 'D', 'R'):\n            continue\n        r2 = rng.random()")
open(p, 'w', encoding='utf-8').write(t)
print('town1 apron ring pushed to the disc edge, grass/rock cells only')
