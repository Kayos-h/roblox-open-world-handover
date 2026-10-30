"""thumbs_sheet - labelled contact sheet of library photos: python thumbs_sheet.py <out.jpg> <id,id,...|@file.json> [cols] [cell]
Cell = front photo (library\\v4_sheets\\_t_<id>.png). If a back view exists (v5_work\\r4\\back, r3 back in r2\\back, or lead_back\\) it is shown next to it."""
import os
import sys
import json
from PIL import Image, ImageDraw, ImageFont

LIB = r"C:\Users\Nitro\.kiro\crew\workspace\town\library"
out, want = sys.argv[1], sys.argv[2]
cols = int(sys.argv[3]) if len(sys.argv) > 3 else 3
cell = int(sys.argv[4]) if len(sys.argv) > 4 else 330
ids = json.load(open(want[1:])) if want.startswith('@') else [i for i in want.split(',') if i]
backs = [os.path.join(LIB, 'v5_work', 'lead_back'), os.path.join(LIB, 'v5_work', 'r4', 'back'), os.path.join(LIB, 'v5_work', 'r2', 'back')]
f = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 15)
rows = (len(ids) + cols - 1) // cols
W = cols * (2 * cell + 8)
sheet = Image.new('RGB', (W, rows * (cell + 26)), (24, 24, 28))
d = ImageDraw.Draw(sheet)
for k, mid in enumerate(ids):
    c, r = k % cols, k // cols
    x0, y0 = c * (2 * cell + 8), r * (cell + 26)
    d.text((x0 + 4, y0 + 4), mid[:44], fill=(235, 235, 240), font=f)
    p = os.path.join(LIB, 'v4_sheets', f'_t_{mid}.png')
    if os.path.exists(p):
        sheet.paste(Image.open(p).convert('RGB').resize((cell, cell), Image.LANCZOS), (x0, y0 + 26))
    for b in backs:
        q = os.path.join(b, f'{mid}.png')
        if os.path.exists(q):
            sheet.paste(Image.open(q).convert('RGB').resize((cell, cell), Image.LANCZOS), (x0 + cell, y0 + 26))
            break
sheet.save(out, 'JPEG', quality=82)
print(out, len(ids), 'models', sheet.size)
