"""palette_diff - compare the merged palette now with the copy archived before this pass: new keys, changed keys, emissive keys."""
import json
import os

LIB = r"C:\Users\Nitro\.kiro\crew\workspace\town\library"
old = json.load(open(os.path.join(LIB, 'v5_fix3_archive', 'meta', 'palette.json')))
new = json.load(open(os.path.join(LIB, 'palette.json')))
add = [k for k in new if k not in old]
chg = [k for k in new if k in old and new[k] != old[k]]
gone = [k for k in old if k not in new]
emi = [k for k, v in new.items() if v.get('glow')]
print('keys: before', len(old), 'now', len(new), '| new', len(add), '| changed value', len(chg), '| removed', len(gone), '| emissive', len(emi))
print('new keys:', ', '.join(sorted(add)))
for k in chg:
    print('CHANGED', k, old[k], '->', new[k])
