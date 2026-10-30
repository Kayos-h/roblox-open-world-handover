"""prepare_r3 - parametrise v5_review_pack2.py by round tag and write the R3 reviewer brief (models that were never rebuilt)."""
import re

SRC = r"C:\Users\Nitro\.kiro\crew\workspace\town\library\src"
W = r"C:\Users\Nitro\.kiro\crew\workspace\town\library\v5_work"
p = SRC + r"\v5_review_pack2.py"
t = open(p, encoding='utf-8').read()
if 'TAG = sys.argv' not in t:
    t = t.replace("import os\nimport json\nimport glob\n", "import os\nimport sys\nimport json\nimport glob\n", 1)
    t = t.replace("R2 = os.path.join(LIB, 'v5_work', 'r2')",
                  "TAG = sys.argv[1] if len(sys.argv) > 1 else 'r2'\nR2 = os.path.join(LIB, 'v5_work', TAG)\nBACK = os.path.join(LIB, 'v5_work', 'r2', 'back')\nQUAD = os.path.join(R2, 'quad') if TAG == 'r2' else os.path.join(LIB, 'v4_sheets')", 1)
    t = t.replace("quad = [q['id'] for q in json.load(open(os.path.join(R2, 'quad_ids.json')))]",
                  "quad = [(q['id'] if isinstance(q, dict) else q) for q in json.load(open(os.path.join(R2, 'quad_ids.json')))]", 1)
    t = t.replace("os.path.join(R2, 'back', mid + '.png')", "os.path.join(BACK, mid + '.png')")
    t = t.replace("os.path.join(R2, 'quad', m + '.png')", "os.path.join(QUAD, m + '.png')").replace("os.path.join(R2, 'quad', mid + '.png')", "os.path.join(QUAD, mid + '.png')")
    open(p, 'w', encoding='utf-8').write(t)
b = open(W + r"\r2\REVIEWER_BRIEF_R2.md", encoding='utf-8').read()
b = b.replace('v5_work\\r2\\pack', 'v5_work\\r3\\pack').replace('v5_work\\r2\\part_', 'v5_work\\r3\\part_').replace('v5_work\\r2\\slice_', 'v5_work\\r3\\slice_')
b = b.replace('`LIB\\v5_work\\r2\\back\\<id>.png`', '`LIB\\v5_work\\r2\\back\\<id>.png` (the back views of all models are in this one folder)')
b = b.replace('review_019.jpg', 'review_015.jpg').replace('`hero_001.jpg` ... :', '`hero_001.jpg` ... (older models: a few):')
b = b.replace('# Independent reviewer brief, second review (R2)', '# Independent reviewer brief, third review (R3: models that were never rebuilt)')
open(W + r"\r3\REVIEWER_BRIEF_R3.md", 'w', encoding='utf-8').write(b)
print('pack script parametrised:', 'TAG = sys.argv' in open(p, encoding='utf-8').read())
print('brief r3 written; r3 paths:', b.count('v5_work\\r3'), '; leftover r2 pack paths:', b.count('r2\\pack'))
