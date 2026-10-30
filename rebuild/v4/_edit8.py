p = r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\v4\dress_v4.py'
t = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global t
    assert t.count(a) == n, (t.count(a), a[:70])
    t = t.replace(a, b)
# castle: the courtyard IS a 190-wide pavement slab, so the road test is switched off there (footprints still checked)
rep("def castle():\n    P = 'v4_dress_castle'\n    n = collections.Counter()\n",
    "def castle():\n    P = 'v4_dress_castle'\n    n = collections.Counter()\n    free = lambda x, z, margin=4.0, road=6.0, minh=2.0, river=3.0: _free(x, z, margin, -9e9, minh, river)\n")
rep("def free(x, z, margin=4.0, road=6.0, minh=2.0, river=3.0):", "def _free(x, z, margin=4.0, road=6.0, minh=2.0, river=3.0):")
rep("def W(*pairs):\n    return list(pairs)\n", "def free(x, z, margin=4.0, road=6.0, minh=2.0, river=3.0):\n    return _free(x, z, margin, road, minh, river)\n\n\ndef W(*pairs):\n    return list(pairs)\n")
open(p, 'w', encoding='utf-8').write(t)
print('castle recipe: road test off')
