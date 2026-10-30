p = r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\v4\reseat_env.luau'
t = open(p, encoding='utf-8').read()
a = "                if big then sink = math.min(math.max(gc - gmin, 0) * 0.5, 8) end\n"
b = ("                if big then\n"
     "                  if fname == 'v4_pieces' then sink = math.min(math.max(gc - gmin, 0), 40)\n"
     "                  else sink = math.min(math.max(gc - gmin, 0) * 0.5, 8) end\n"
     "                end\n")
assert t.count(a) == 1, t.count(a)
t = t.replace(a, b)
open(p, 'w', encoding='utf-8').write(t)
print('pieces now sit on the lowest footprint ground')
