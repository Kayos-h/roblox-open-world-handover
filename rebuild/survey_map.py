import json, re
raw = open(r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\survey_raw.txt', encoding='utf-8-sig').read()
j = json.loads(raw)
rows = j['returnValue'].split(';')
grid = [r.split(',') for r in rows]
xs = list(range(-3500, 3501, 100)); zs = list(range(-3500, 3501, 100))
def ch(v):
    if v == 'n': return ' '
    if v.endswith('w'): return '~'
    h = int(v)
    if h < 0: return '_'
    for lim, c in ((5, '.'), (15, ','), (30, '-'), (60, '='), (100, '+'), (160, '*'), (250, '#'), (400, '%')):
        if h < lim: return c
    return '@'
print('    ' + ''.join(str((x // 1000) % 10) if x % 1000 == 0 else ' ' for x in xs))
for z, r in zip(zs, grid):
    print(f'{z:6d} ' + ''.join(ch(v) for v in r))
# mountain stats
pk = max(((int(v), xs[i], zs[k]) for k, r in enumerate(grid) for i, v in enumerate(r) if v not in ('n',) and not v.endswith('w')))
print('peak', pk)
for z in range(-2900, -800, 100):
    k = zs.index(z)
    print(z, ' '.join(f'{grid[k][xs.index(x)]:>4}' for x in range(1500, 3501, 100)))
