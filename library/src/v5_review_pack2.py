"""v5_review_pack2 - blind review pack for the second review: the 198 rebuilt models plus 24 untouched anchor models, shuffled, 12 per sheet.
Each cell: the library thumbnail (3/4 front) and the back view side by side; caption = id, triangles, size. Nothing on a sheet says whether a model was rebuilt.
Four-angle sheets (hero_NNN.jpg, 2 per sheet) exist for the big or complex rebuilt models. Output: library\\v5_work\\r2\\pack\\ (review_NNN.jpg, hero_NNN.jpg, INDEX.md).
"""
import os
import sys
import json
import glob
from PIL import Image, ImageDraw, ImageFont

LIB = r"C:\Users\Nitro\.kiro\crew\workspace\town\library"
TAG = sys.argv[1] if len(sys.argv) > 1 else 'r2'
R2 = os.path.join(LIB, 'v5_work', TAG)
BACK = os.path.join(R2, 'back') if TAG == 'r4' else os.path.join(LIB, 'v5_work', 'r2', 'back')
QUAD = os.path.join(R2, 'quad') if TAG in ('r2', 'r4') else os.path.join(LIB, 'v4_sheets')
OUT = os.path.join(R2, 'pack')
os.makedirs(OUT, exist_ok=True)
for f in glob.glob(os.path.join(OUT, '*.jpg')):
    os.remove(f)
pack = json.load(open(os.path.join(R2, 'pack_ids.json')))
quad = [(q['id'] if isinstance(q, dict) else q) for q in json.load(open(os.path.join(R2, 'quad_ids.json')))]
meta = {}
for f in glob.glob(os.path.join(LIB, 'v4_meta_v[a-j].json')):
    meta.update(json.load(open(f)))
COLS, ROWS, S, LAB = 3, 4, 300, 38
PER = COLS * ROWS


def font(sz, bold=False):
    for p in ((r'C:\Windows\Fonts\segoeuib.ttf' if bold else r'C:\Windows\Fonts\segoeui.ttf'), r'C:\Windows\Fonts\arial.ttf'):
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


f1, f2 = font(14, True), font(12)
ids = [p['id'] for p in pack]
idx = ['# Review pack 2 index', '', f'{len(ids)} models, {PER} per sheet (3 columns x 4 rows). Each cell: front 3/4 view (left) and back 3/4 view (right). Caption: id, triangles, size in studs (x y z).', '']
missing = []
for s in range(0, len(ids), PER):
    part = ids[s:s + PER]
    W, H = COLS * (2 * S + 6) + 6, ROWS * (S + LAB + 6) + 6
    sh = Image.new('RGB', (W, H), (24, 24, 28))
    d = ImageDraw.Draw(sh)
    n = s // PER + 1
    idx.append(f'## review_{n:03d}.jpg')
    for k, mid in enumerate(part):
        c, r = k % COLS, k // COLS
        x0, y0 = 6 + c * (2 * S + 6), 6 + r * (S + LAB + 6)
        for j, p in enumerate((os.path.join(LIB, 'v4_sheets', f'_t_{mid}.png'), os.path.join(BACK, mid + '.png'))):
            if os.path.exists(p):
                sh.paste(Image.open(p).convert('RGB').resize((S, S), Image.LANCZOS), (x0 + j * S, y0))
            else:
                missing.append((mid, 'front' if j == 0 else 'back'))
                d.text((x0 + j * S + 10, y0 + S // 2), 'NO PICTURE', fill=(255, 120, 120), font=f1)
        e = meta[mid]
        tri = e.get('tris', '?')
        tri = f'{tri / 1000:.1f}k' if isinstance(tri, (int, float)) and tri >= 1000 else str(tri)
        d.rectangle([x0, y0 + S, x0 + 2 * S - 1, y0 + S + LAB - 1], fill=(40, 40, 48))
        d.text((x0 + 6, y0 + S + 2), mid[:52], fill=(235, 235, 240), font=f1)
        d.text((x0 + 6, y0 + S + 20), f"{tri} tris   {' x '.join(str(round(v)) for v in e.get('size', []))}   (front | back)", fill=(170, 200, 230), font=f2)
        idx.append(f'- {k + 1:>2}. {mid}' + ('   [four-angle sheet: yes]' if mid in quad else ''))
    sh.save(os.path.join(OUT, f'review_{n:03d}.jpg'), 'JPEG', quality=86)
    idx.append('')
n_hero = 0
idx.append('## Four-angle sheets (3/4 front, 3/4 back, close-up, front elevation)')
have = [m for m in quad if os.path.exists(os.path.join(QUAD, m + '.png'))]
for k in range(0, len(have), 2):
    pair = have[k:k + 2]
    sh = Image.new('RGB', (2 * 920, 920 + 34), (24, 24, 28))
    d = ImageDraw.Draw(sh)
    n_hero += 1
    for i, mid in enumerate(pair):
        sh.paste(Image.open(os.path.join(QUAD, mid + '.png')).convert('RGB').resize((920, 920), Image.LANCZOS), (i * 920, 0))
        d.rectangle([i * 920, 920, i * 920 + 919, 920 + 33], fill=(40, 40, 48))
        d.text((i * 920 + 8, 927), mid, fill=(235, 235, 240), font=f1)
        idx.append(f'- hero_{n_hero:03d}.jpg: {mid}')
    sh.save(os.path.join(OUT, f'hero_{n_hero:03d}.jpg'), 'JPEG', quality=84)
open(os.path.join(OUT, 'INDEX.md'), 'w', encoding='utf-8').write('\n'.join(idx))
print(f'pack: {len(ids)} models on {(len(ids) + PER - 1) // PER} sheets; four-angle sheets for {len(have)} of {len(quad)} models on {n_hero} pages; missing pictures {len(missing)} {missing[:5]}')
