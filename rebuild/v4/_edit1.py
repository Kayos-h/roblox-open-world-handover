import re
p = r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\v4\patch_terrain_gen_v4d.py'
t = open(p, encoding='utf-8').read()
old = '''    "    h = -(dd <= 30 and dd * 0.5 or 15 + (dd - 30))\\n"'''
new = '''    "    h = -(dd <= 10 and dd or (dd <= 40 and 10 + (dd - 10) * 0.5 or 25 + (dd - 40)))\\n"'''
assert t.count(old) == 1, t.count(old)
t = t.replace(old, new)
open(p, 'w', encoding='utf-8').write(t)
print('shelf profile updated')
