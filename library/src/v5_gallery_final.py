"""v5_gallery - photo galleries of ALL 404 v5 models, grouped by the reviewers' verdict, plus one PDF with everything.
Reads: library\\v5_work\\review_defects_v5.json (verdict, defects, fix), the manifest (order), v4_meta_v*.json (sizes), v4_sheets\\_t_<id>.png (the photos).
Writes library\\v5_work\\gallery\\: A_defective_NN.jpg (REDO first, then MAJOR), B_small_flaws_NN.jpg (MINOR), C_good_NN.jpg (OK), INDEX.md and ALL_MODELS_v5.pdf
(legend page + all gallery sheets + the four-angle sheets of the 27 landmark pieces). 12 photos per sheet, 4 columns x 3 rows, photo at native 420 px.
Under each photo: verdict colour bar, id, triangles and size, and the reviewer's note. It prints no judgement of its own.
"""
import os
import csv
import json
import glob
from PIL import Image, ImageDraw, ImageFont

LIB = r"C:\Users\Nitro\.kiro\crew\workspace\town\library"
MAN = r"C:\Users\Nitro\.kiro\crew\workspace\town\plan_v5\V5_MANIFEST.csv"
OUT = os.path.join(LIB, 'v5_work', 'gallery_final')
THUMBS = os.path.join(LIB, 'v4_sheets')
HERO = sorted(glob.glob(os.path.join(LIB, 'v5_work', 'r3', 'pack', 'hero_*.jpg'))) + sorted(glob.glob(os.path.join(LIB, 'v5_work', 'r4', 'pack', 'hero_*.jpg')))
os.makedirs(OUT, exist_ok=True)
for f in glob.glob(os.path.join(OUT, '*.jpg')) + glob.glob(os.path.join(OUT, '*.pdf')):
    os.remove(f)

CELL, BAR, NOTE, GAP, HEAD, COLS, ROWS = 420, 44, 54, 6, 46, 4, 3
PER = COLS * ROWS
COL = {'FIXED': (46, 112, 196), 'UNREVIEWED': (96, 104, 120), 'REDO': (176, 28, 44), 'MAJOR': (206, 86, 38), 'MINOR': (190, 150, 24), 'OK': (44, 134, 70)}
BG, INK, DIM = (24, 24, 28), (240, 240, 244), (170, 182, 196)


def font(sz, bold=False):
    for p in ((r'C:\Windows\Fonts\segoeuib.ttf' if bold else r'C:\Windows\Fonts\segoeui.ttf'), r'C:\Windows\Fonts\arial.ttf'):
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


F_ID, F_SM, F_NOTE, F_HEAD, F_BIG = font(14, True), font(12), font(12), font(20, True), font(30, True)
_probe = ImageDraw.Draw(Image.new('RGB', (4, 4)))


def wrap(text, fnt, maxw, maxlines):
    lines, cur = [], ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if _probe.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if len(lines) > maxlines:
        lines = lines[:maxlines]
        last = lines[-1]
        while last and _probe.textlength(last + '…', font=fnt) > maxw:
            last = last[:-1]
        lines[-1] = last.rstrip() + '…'
    return lines


order = [r['id'] for r in csv.DictReader(open(MAN, encoding='utf-8-sig'))]
pos = {i: k for k, i in enumerate(order)}
def _load(p):
    return {e['id']: e for e in json.load(open(os.path.join(LIB, 'v5_work', p)))}


_r1, _r2, _r3, _r4 = _load('review_defects_v5.json'), _load(r'r2\review_defects_r2.json'), _load(r'r3\review_defects_r3.json'), _load(r'r4\review_defects_r4.json')
_fix2 = {e['id'] for e in json.load(open(os.path.join(LIB, 'v5_work', r'r2\fix2_ids.json')))}
rev = {}
for _i in order:
    if _i in _r4:
        _e = dict(_r4[_i])
    elif _i in _fix2:
        _e = dict(verdict='UNREVIEWED', defects=['rebuilt in fix round 2; this version has no independent review'], fix='')
    elif _i in _r3:
        _e = dict(_r3[_i])
    elif _i in _r2:
        _e = dict(_r2[_i])
    else:
        _e = dict(_r1[_i])
    _e['id'] = _i
    _d = _e.get('defects') or []
    _e['defects'] = [_d] if isinstance(_d, str) else list(_d)
    _e['fix'] = _e.get('fix') or ''
    rev[_i] = _e
_fixed = json.load(open(os.path.join(LIB, 'v5_work', 'lead', 'fixed_ids.json'))) + json.load(open(os.path.join(LIB, 'v5_work', 'lead2', 'worklist.json')))
_NOTE = json.load(open(os.path.join(LIB, 'v5_work', 'lead2', 'notes_all.json')))
for _i in _fixed:
    rev[_i] = dict(id=_i, verdict='FIXED', defects=[_NOTE.get(_i[:7], 'rebuilt in this pass')], fix='')
size = {}
TRIS = {}
for f in glob.glob(os.path.join(LIB, 'v4_meta_v[a-j].json')):
    for k, v in json.load(open(f)).items():
        size[k] = v.get('size') or []
        TRIS[k] = v.get('tris')
assert set(rev) == set(order), 'review and manifest disagree'

groups = [
    ('F', 'F_fixed_now', 'FIXED BY THE LEAD (two passes, 118 models): rebuilt and checked by the lead, waiting for YOUR review', [i for i in order if rev[i]['verdict'] == 'FIXED']),
    ('A', 'A_defective', 'DEFECTIVE: REDO (rebuild) first, then MAJOR (must fix)', sorted([i for i in order if rev[i]['verdict'] in ('REDO', 'MAJOR')], key=lambda i: (rev[i]['verdict'] != 'REDO', pos[i]))),
    ('B', 'B_small_flaws', 'SMALL FLAWS: MINOR (fixing optional)', [i for i in order if rev[i]['verdict'] == 'MINOR']),
    ('C', 'C_good', 'GOOD: OK (reviewers saw no reason to fix)', [i for i in order if rev[i]['verdict'] == 'OK']),
    ('D', 'D_not_reviewed', 'NOT REVIEWED: rebuilt in fix round 2, no independent verdict on this version', [i for i in order if rev[i]['verdict'] == 'UNREVIEWED']),
]
W = COLS * (CELL + GAP) + GAP
H = HEAD + ROWS * (CELL + BAR + NOTE + GAP) + GAP
pages, index, made = [], ['# v5 photo galleries (all models)', ''], 0
for letter, stem, title, idl in groups:
    n_sheets = (len(idl) + PER - 1) // PER
    index += [f'## {title} ({len(idl)} models, {n_sheets} sheets)', '']
    for s in range(n_sheets):
        part = idl[s * PER:(s + 1) * PER]
        sheet = Image.new('RGB', (W, H), BG)
        d = ImageDraw.Draw(sheet)
        d.text((GAP + 6, 10), f'{title}   |   sheet {s + 1} of {n_sheets}   |   models {s * PER + 1} to {s * PER + len(part)} of {len(idl)}', fill=INK, font=F_HEAD)
        names = []
        for k, mid in enumerate(part):
            c, r = k % COLS, k // COLS
            x0, y0 = GAP + c * (CELL + GAP), HEAD + GAP + r * (CELL + BAR + NOTE + GAP)
            sheet.paste(Image.open(os.path.join(THUMBS, f'_t_{mid}.png')).convert('RGB').resize((CELL, CELL), Image.LANCZOS), (x0, y0))
            e = rev[mid]
            col = COL[e['verdict']]
            d.rectangle([x0, y0 + CELL, x0 + CELL - 1, y0 + CELL + BAR - 1], fill=col)
            d.text((x0 + 8, y0 + CELL + 4), e['verdict'], fill=(255, 255, 255), font=F_ID)
            tag = _probe.textlength(e['verdict'], font=F_ID) + 18
            idtxt = mid
            while _probe.textlength(idtxt, font=F_ID) > CELL - tag - 8 and len(idtxt) > 8:
                idtxt = idtxt[:-1]
            d.text((x0 + tag, y0 + CELL + 4), idtxt, fill=(255, 255, 255), font=F_ID)
            tri = TRIS.get(mid)
            tri = f'{tri:,} tris' if isinstance(tri, int) else '? tris'
            sz = ' x '.join(str(round(v)) for v in size.get(mid, []))
            d.text((x0 + 8, y0 + CELL + 24), f'{tri}   |   {sz} studs (x, y, height)', fill=(255, 255, 255), font=F_SM)
            d.rectangle([x0, y0 + CELL + BAR, x0 + CELL - 1, y0 + CELL + BAR + NOTE - 1], fill=(40, 40, 48))
            defects = '; '.join(e['defects']).strip()
            if e['verdict'] == 'OK' and not defects:
                lines, ncol = ['no flaws noted by the reviewer'], (120, 160, 130)
            elif e['verdict'] == 'OK':
                lines, ncol = wrap('note: ' + defects + (' (fix suggested)' if e['fix'].strip() else ''), F_NOTE, CELL - 14, 3), DIM
            else:
                lines, ncol = wrap(defects, F_NOTE, CELL - 14, 3), INK
            for li, ln in enumerate(lines):
                d.text((x0 + 7, y0 + CELL + BAR + 4 + li * 16), ln, fill=ncol, font=F_NOTE)
            names.append(mid)
            made += 1
        fn = f'{stem}_{s + 1:02d}.jpg'
        sheet.save(os.path.join(OUT, fn), 'JPEG', quality=82, subsampling=1)
        pages.append(sheet)
        index.append(f'- `{fn}`: ' + ', '.join(names))
    index.append('')

leg = Image.new('RGB', (W, 900), BG)
d = ImageDraw.Draw(leg)
d.text((40, 36), 'v5 Blender models: photos of all 404 (final state after fix round 2)', fill=INK, font=F_BIG)
d.text((40, 90), 'One 3/4 photo per model, grouped by the LATEST independent verdict (front and back views). Under each photo: verdict, id, triangles, size, reviewer note.', fill=DIM, font=F_HEAD)
y = 160
for letter, stem, title, idl in groups:
    n_sheets = (len(idl) + PER - 1) // PER
    d.text((40, y), f'{title}', fill=INK, font=F_HEAD)
    d.text((40, y + 28), f'{len(idl)} models on {n_sheets} pages ({stem}_01 to {stem}_{n_sheets:02d})', fill=DIM, font=F_NOTE)
    y += 78
for v, lab in (('FIXED', 'rebuilt in this pass, for your review'), ('UNREVIEWED', 'rebuilt in round 2, no verdict yet'), ('REDO', 'rebuild from scratch'), ('MAJOR', 'clearly wrong, must be fixed'), ('MINOR', 'small flaw, fixing optional'), ('OK', 'normal and usable')):
    d.rectangle([40, y, 150, y + 30], fill=COL[v])
    d.text((52, y + 4), v, fill=(255, 255, 255), font=F_ID)
    d.text((170, y + 6), lab, fill=INK, font=F_NOTE)
    y += 42
d.text((40, y + 14), 'After the groups: four-angle pages (front, back, close-up, elevation) of the big pieces: first the never-rebuilt ones, then the round-2 ones.', fill=DIM, font=F_NOTE)
d.text((40, y + 40), 'OK models can still carry a small reviewer note. A different reviewer can rate the same model one step differently (see the report).', fill=DIM, font=F_NOTE)
d.text((40, y + 66), 'Grey ground and sky are only the photo studio. Roblox colours the pieces from a palette.', fill=DIM, font=F_NOTE)
pdf_pages = [leg] + pages + [Image.open(h).convert('RGB') for h in HERO]
pdf_pages[0].save(os.path.join(OUT, 'ALL_MODELS_v5.pdf'), 'PDF', save_all=True, append_images=pdf_pages[1:], resolution=150.0, quality=80)
open(os.path.join(OUT, 'INDEX.md'), 'w', encoding='utf-8').write('\n'.join(index))
print(f'photos placed: {made} of {len(order)}; sheets: {len(pages)}; pdf pages: {len(pdf_pages)}; groups: ' + ', '.join(f'{g[1]} {len(g[3])}' for g in groups))
print('pdf MB:', round(os.path.getsize(os.path.join(OUT, 'ALL_MODELS_v5.pdf')) / 1e6, 1), ' jpg MB:', round(sum(os.path.getsize(f) for f in glob.glob(os.path.join(OUT, '*.jpg'))) / 1e6, 1))
