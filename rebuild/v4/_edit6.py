p = r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\v4\dress_v4.py'
t = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global t
    assert t.count(a) == n, (t.count(a), a[:60])
    t = t.replace(a, b)
rep("g = group_prefix + 'Trees'", "g = 'Trees' + group_prefix")
rep("'CastleTrees'", "'TreesCastle'", 2)
rep("'CapitalTrees'", "'TreesCapital'")
rep("'HarbourTrees'", "'TreesHarbour'")
rep("if put(P, choose(W(('A83_bench_stone', 1), ('K33_ornate_bench', 1))), cx, cz, ang + 90 * (ang in (90, 270)), 'CastleProps', scale=1.0):",
    "if put(P, choose(W(('A83_bench_stone', 1), ('K33_ornate_bench', 1))), cx, cz, ang, 'CastleProps', scale=1.0):")
open(p, 'w', encoding='utf-8').write(t)
print('dress_v4.py fixed')
