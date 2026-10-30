"""v5_tower_label - number the pieces on the tower plan sections so a reviewer can name a piece, and append a legend (number, model id, level).
  python v5_tower_label.py <tower_check folder, e.g. fixed2>
Reads metrics.json (written by v5_tower_assembly.py) and plan_L0..L3 pngs; writes plan_L?_labelled.png next to them. Orthographic scales: L0 112, L1 112, L2 100, L3 92.
"""
import os
import sys
import json
from PIL import Image, ImageDraw, ImageFont

D = os.path.join(r"C:\Users\Nitro\.kiro\crew\workspace\town\library\v5_work\tower_check", sys.argv[1])
rows = json.load(open(os.path.join(D, 'metrics.json')))
SCALE = {0: 112, 1: 112, 2: 100, 3: 92}
NAMES = {0: 'plan_L0_map_hall', 1: 'plan_L1_gallery', 2: 'plan_L2_gallery', 3: 'plan_L3_vault'}
try:
    f = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 15)
    f2 = ImageFont.truetype(r'C:\Windows\Fonts\segoeui.ttf', 14)
except Exception:
    f = f2 = ImageFont.load_default()
for lv, name in NAMES.items():
    p = os.path.join(D, name + '.png')
    if not os.path.exists(p):
        continue
    im = Image.open(p).convert('RGB')
    W, H = im.size
    pieces = [r for r in rows if r['lvl'] == lv]
    canvas = Image.new('RGB', (W + 330, H), (24, 24, 28))
    canvas.paste(im, (0, 0))
    d = ImageDraw.Draw(canvas)
    for k, r in enumerate(pieces, 1):
        px = (r['x'] / SCALE[lv] + 0.5) * W
        py = (0.5 - r['y'] / SCALE[lv]) * H
        d.ellipse([px - 11, py - 11, px + 11, py + 11], fill=(255, 220, 40), outline=(0, 0, 0))
        d.text((px - (5 if k < 10 else 9), py - 8), str(k), fill=(0, 0, 0), font=f)
        d.text((W + 10, 8 + (k - 1) * 20), f'{k:>2}  {r["id"][:38]}', fill=(235, 235, 240), font=f2)
    canvas.save(os.path.join(D, name + '_labelled.png'))
print('labelled plans written to', D)
