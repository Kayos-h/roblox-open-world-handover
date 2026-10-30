p = r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\v4\reseat_env.luau'
t = open(p, encoding='utf-8').read()
a = ("                  if fname == 'v4_pieces' then sink = math.min(math.max(gc - gmin, 0), 40)\n"
     "                  else sink = math.min(math.max(gc - gmin, 0) * 0.5, 8) end\n")
b = ("                  if fname == 'v4_pieces' then sink = math.min(math.max(gc - gmin, 0), 40)\n"
     "                  elseif math.max(size.X, size.Z) >= 30 then sink = math.min(math.max(gc - gmin, 0) * 0.85, 30)\n"
     "                  else sink = math.min(math.max(gc - gmin, 0) * 0.5, 8) end\n")
assert t.count(a) == 1, t.count(a)
t = t.replace(a, b)
open(p, 'w', encoding='utf-8').write(t)
print('big rocks (>=30) now embed up to 85 percent of the footprint drop, max 30')
