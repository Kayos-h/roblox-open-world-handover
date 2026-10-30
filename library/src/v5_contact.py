"""v5_contact - merge scratch sheets of a builder into labelled contact sheets so many models can be looked at in ONE image.
  python v5_contact.py <tag> <id,id,...|all> [before]
Reads library\\v5_work\\fix_scratch\\<tag>\\<id>.png (the 2x2 four-angle sheet, or a single 3/4 picture) and writes
library\\v5_work\\fix_scratch\\<tag>\\contact_<n>.jpg : 3 models per row, 2 rows per sheet. With 'before' every cell shows the round-1 photo
(library\\v5_round1_archive\\v4_sheets\\_t_<id>.png) on the left and the new render on the right, so you can see what changed.
Prints the sheet paths.
"""
import os
import sys
import glob
from PIL import Image, ImageDraw, ImageFont

LIB = r"C:\Users\Nitro\.kiro\crew\workspace\town\library"
tag = sys.argv[1]
want = sys.argv[2]
before = len(sys.argv) > 3 and sys.argv[3] == 'before'
D = os.path.join(LIB, 'v5_work', 'fix_scratch', tag)
ids = sorted(os.path.basename(p)[:-4] for p in glob.glob(os.path.join(D, '*.png')) if not os.path.basename(p).startswith(('_', 'contact'))) if want == 'all' else [i for i in want.split(',') if i]
ids = [i for i in ids if os.path.exists(os.path.join(D, i + '.png'))]
CW, CH, COLS, ROWS, LAB = (900 if before else 640), 640, (1 if before else 3), (2 if before else 2), 26
if before:
    CW = 1000
per = COLS * ROWS
try:
    f = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 15)
except Exception:
    f = ImageFont.load_default()
out = []
for s in range(0, len(ids), per):
    part = ids[s:s + per]
    sheet = Image.new('RGB', (COLS * CW, ROWS * (CH + LAB)), (24, 24, 28))
    d = ImageDraw.Draw(sheet)
    for k, mid in enumerate(part):
        c, r = k % COLS, k // COLS
        x0, y0 = c * CW, r * (CH + LAB)
        new = Image.open(os.path.join(D, mid + '.png')).convert('RGB')
        if before:
            old_p = os.path.join(LIB, 'v5_round1_archive', 'v4_sheets', f'_t_{mid}.png')
            if os.path.exists(old_p):
                old = Image.open(old_p).convert('RGB').resize((CH, CH), Image.LANCZOS)
                sheet.paste(old, (x0, y0 + LAB))
                d.text((x0 + 6, y0 + 4), 'ROUND 1', fill=(255, 150, 120), font=f)
            new = new.resize((CW - CH, CW - CH), Image.LANCZOS)
            sheet.paste(new, (x0 + CH, y0 + LAB))
            d.text((x0 + CH + 6, y0 + 4), mid + '  (new)', fill=(180, 230, 190), font=f)
        else:
            new = new.resize((CW, CH), Image.LANCZOS) if new.size[0] != new.size[1] else new.resize((CH, CH), Image.LANCZOS)
            sheet.paste(new, (x0, y0 + LAB))
            d.text((x0 + 6, y0 + 4), mid, fill=(235, 235, 240), font=f)
    p = os.path.join(D, f'contact_{s // per + 1}.jpg')
    sheet.save(p, 'JPEG', quality=84)
    out.append(p)
print(f'{len(ids)} models on {len(out)} contact sheets:')
for p in out:
    print(p)
