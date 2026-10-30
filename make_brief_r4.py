"""make_brief_r4 - build the r4 reviewer brief from the r3 brief with every folder path switched to r4 (back views of r4 models are in r4\\back)."""
src = r"C:\Users\Nitro\.kiro\crew\workspace\town\library\v5_work\r3\REVIEWER_BRIEF_R3.md"
dst = r"C:\Users\Nitro\.kiro\crew\workspace\town\library\v5_work\r4\REVIEWER_BRIEF_R4.md"
b = open(src, encoding='utf-8').read()
b = b.replace('v5_work\\r3\\', 'v5_work\\r4\\')
b = b.replace('v5_work\\r2\\back\\<id>.png` (the back views of all models are in this one folder)', 'v5_work\\r4\\back\\<id>.png`')
b = b.replace('review_015.jpg', 'review_008.jpg')
b = b.replace('third review (R3: models that were never rebuilt)', 'fourth review (R4: models rebuilt in the second fix round)')
b = b.replace('`hero_001.jpg` ... (older models: a few):', '`hero_001.jpg` ... :')
open(dst, 'w', encoding='utf-8').write(b)
import re
print('r4 paths:', len(re.findall(r'v5_work\\r4', b)), '| r3 paths left:', len(re.findall(r'v5_work\\r3', b)), '| r2 paths left:', len(re.findall(r'v5_work\\r2', b)))
print([l for l in b.splitlines() if l.startswith('#')][:2])
