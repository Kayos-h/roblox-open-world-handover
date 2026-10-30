p = r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\v4\reseat_env.luau'
t = open(p, encoding='utf-8').read()
a = "              local big = math.max(size.X, size.Z) >= 14\n"
b = "              local big = math.max(size.X, size.Z) >= 14 and (fname == 'v4_rocks' or fname == 'v4_pieces')\n"
assert t.count(a) == 1, t.count(a)
t = t.replace(a, b)
open(p, 'w', encoding='utf-8').write(t)
print('reseat: slope burying and footprint-over-water now only for rocks and pieces')
