"""lead_kit_dbg - temporary debug line in the kit: report how many islands the de-z-fight step moved."""
p = r"C:\Users\Nitro\.kiro\crew\workspace\town\library\src\v5_leadkit.py"
t = open(p, encoding='utf-8').read()
old = "    return len(shifts)\n"
new = "    print('SCRATCH_DZ shifted', len(shifts), 'of', len(isl_data), 'islands; plane clusters:', sum(1 for l in byn.values() for _ in [0]), 'normal groups')\n    return len(shifts)\n"
assert t.count(old) == 1
open(p, 'w', encoding='utf-8').write(t.replace(old, new))
print('debug line added')
