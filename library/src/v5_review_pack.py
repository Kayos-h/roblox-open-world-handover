"""v5_review_pack - labelled contact sheets of EVERY v5 model for the independent reviewers.
Output (library\\v5_work\\review_pack): review_001.jpg ... (12 models each, 4 x 3, grouped by build queue so families sit together), hero_001.jpg ...
(four-angle views of the big landmark pieces, 2 per sheet) and INDEX.md. Caption = id, triangles, size in studs (x y z).
"""
import os
import csv
import json
import glob
from PIL import Image, ImageDraw, ImageFont

LIB = r"C:\Users\Nitro\.kiro\crew\workspace\town\library"
MAN = r"C:\Users\Nitro\.kiro\crew\workspace\town\plan_v5\V5_MANIFEST.csv"
OUT = os.path.join(LIB, 'v5_work', 'review_pack')
SHEETS = os.path.join(LIB, 'v4_sheets')
COLS, ROWS, CELL, LABEL_H = 4, 3, 360, 34
PER = COLS * ROWS
os.makedirs(OUT, exist_ok=True)
for f in glob.glob(os.path.join(OUT, '*.jpg')):
    os.remove(f)


def font(sz):
    for p in (r'C:\Windows\Fonts\segoeui.ttf', r'C:\Windows\Fonts\arial.ttf'):
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


order, meta = [], {}
for w in 'abcdefghij':
    f = os.path.join(LIB, f'v4_meta_v{w}.json')
    if os.path.exists(f):
        d = json.load(open(f))
        man = [r['id'] for r in csv.DictReader(open(MAN, encoding='utf-8-sig'))]
        order += [i for i in man if i in d]
        meta.update(d)
f1, f2 = font(15), font(12)
idx = ['# v5 review pack index', '', f'{len(order)} built models, {PER} per sheet (4 columns x 3 rows, left to right, top to bottom). Caption = saved id, triangles, size in studs (x y z).', '']
missing = []
n_sheets = (len(order) + PER - 1) // PER
for s in range(n_sheets):
    part = order[s * PER:(s + 1) * PER]
    sheet = Image.new('RGB', (COLS * CELL, ROWS * (CELL + LABEL_H)), (24, 24, 28))
    d = ImageDraw.Draw(sheet)
    idx.append(f'## review_{s + 1:03d}.jpg')
    for i, mid in enumerate(part):
        c, r = i % COLS, i // COLS
        x0, y0 = c * CELL, r * (CELL + LABEL_H)
        p = os.path.join(SHEETS, f'_t_{mid}.png')
        if os.path.exists(p):
            try:
                sheet.paste(Image.open(p).convert('RGB').resize((CELL, CELL), Image.LANCZOS), (x0, y0))
            except Exception:
                missing.append(mid)
        else:
            missing.append(mid)
            d.text((x0 + 10, y0 + CELL // 2), 'NO PHOTO', fill=(255, 120, 120), font=f1)
        e = meta[mid]
        size = ' x '.join(str(round(v)) for v in (e.get('size') or []))
        tri = e.get('tris', '?')
        tri = f'{tri / 1000:.1f}k' if isinstance(tri, (int, float)) and tri >= 1000 else str(tri)
        d.rectangle([x0, y0 + CELL, x0 + CELL - 1, y0 + CELL + LABEL_H - 1], fill=(40, 40, 48))
        d.text((x0 + 6, y0 + CELL + 2), mid[:46], fill=(235, 235, 240), font=f1)
        d.text((x0 + 6, y0 + CELL + 19), f'{tri} tris   {size}', fill=(170, 200, 230), font=f2)
        idx.append(f'- {i + 1:>2}. {mid}  ({tri} tris, {size})')
    sheet.save(os.path.join(OUT, f'review_{s + 1:03d}.jpg'), 'JPEG', quality=86)
    idx.append('')
quads = [m for m in order if os.path.exists(os.path.join(SHEETS, m + '.png'))]
hs = 0
idx.append('## Hero four-angle sheets (hero_NNN.jpg, 2 models each)')
for k in range(0, len(quads), 2):
    pair = quads[k:k + 2]
    sheet = Image.new('RGB', (2 * 920, 920 + LABEL_H), (24, 24, 28))
    d = ImageDraw.Draw(sheet)
    for i, mid in enumerate(pair):
        sheet.paste(Image.open(os.path.join(SHEETS, mid + '.png')).convert('RGB').resize((920, 920), Image.LANCZOS), (i * 920, 0))
        d.rectangle([i * 920, 920, i * 920 + 919, 920 + LABEL_H - 1], fill=(40, 40, 48))
        d.text((i * 920 + 8, 920 + 8), f"{mid}  ({meta[mid].get('tris')} tris, {' x '.join(str(round(v)) for v in meta[mid].get('size', []))})", fill=(235, 235, 240), font=f1)
        idx.append(f'- hero_{hs + 1:03d}.jpg: {mid}')
    hs += 1
    sheet.save(os.path.join(OUT, f'hero_{hs:03d}.jpg'), 'JPEG', quality=86)
if missing:
    idx += ['', '## Models without a photo', ''] + [f'- {m}' for m in missing]
open(os.path.join(OUT, 'INDEX.md'), 'w', encoding='utf-8').write('\n'.join(idx))
print(f'review pack: {len(order)} models on {n_sheets} sheets, {hs} hero sheets ({len(quads)} four-angle models); no photo for {len(missing)}; out {OUT}')
