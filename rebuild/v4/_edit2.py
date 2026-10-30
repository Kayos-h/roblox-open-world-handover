p = r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\v4\patch_terrain_gen_v4d.py'
t = open(p, encoding='utf-8').read()
a = "    if n3 > 0.62 and slope < 0.3 then return M.Ground end\n    return (n1 + 0.5 * n4 > 0.4) and M.LeafyGrass or M.Grass\n"
b = "    if n3 > 0.72 and slope < 0.3 then return M.Ground end\n    return (n1 + 0.5 * n4 > 0.4) and M.LeafyGrass or M.Grass\n"
assert t.count(a) == 1, t.count(a)
t = t.replace(a, b)
c = "  if n3 > 0.6 and slope < 0.3 then return M.Ground end\n  if slope > 0.45 and n2 > 0.0 then return M.Rock end\n"
d = "  if n3 > 0.7 and slope < 0.3 then return M.Ground end\n  if slope > 0.45 and n2 > 0.0 then return M.Rock end\n"
assert t.count(c) == 1, t.count(c)
t = t.replace(c, d)
open(p, 'w', encoding='utf-8').write(t)
print('ground patches made rarer')
