"""lead_compare - before / after sheets for the models fixed in this pass.  Cell = BEFORE front photo | AFTER front photo | AFTER back view, with a one-line note.
Writes library\\v5_work\\lead\\fixed_01.jpg ... (8 models per sheet)."""
import os
import json
from PIL import Image, ImageDraw, ImageFont

LIB = r"C:\Users\Nitro\.kiro\crew\workspace\town\library"
W = os.path.join(LIB, 'v5_work')
OUT = os.path.join(W, 'lead')
ids = json.load(open(os.path.join(OUT, 'fixed_ids.json')))
NOTE = {
    'LM06_01': 'solid tiered rock gate with a passable tunnel and timber frame (was stacked slabs)',
    'LM07_01': 'solid banded rock tower, stair wedges bolted to the face (was a hollow box with a black void)',
    'LM07_02': 'mirror variant of 01: solid tower, stair bolted to the face',
    'LM23_01': 'chunky stacked rock wall in warm bands (was striped slabs with square patches)',
    'LM24_02': 'boulder cluster with a table stone, warm colours (was plain grey boxes)',
    'LM24_03': 'leaning rock spires over a boulder ring, different shape from 02',
    'FR02_04': 'shrine ruin: warm stone columns, lintel, stone urn (was grey with a bright gold tip)',
    'CP15_01': 'gold star badge replaced by a bronze ring with a small tower glyph',
    'CP17_01': 'gold star finial replaced by a dull bronze urn and orb',
    'CP18_02': 'curved quay as plain ashlar masonry with short bollards (was ship-like)',
    'EV03_01': 'solid root-and-stone stair, closed underside, light step edges, rails',
    'LM02_01': 'bark ribs now sit on the trunk; no hanging roots or loose rubble',
    'TW02_03': 'market stall with awning, crates, barrel and sacks (was plain boxes)',
    'TW02_07': "smith's hanging sign with an anvil emblem in light warm colours (was a dark blob)",
    'TW03_02': 'brazier filled with coals and ash, dull iron and bronze (was an empty bowl with a gold rim)',
    'TW03_04': 'swallowtail banner as one cloth shape with a plain diamond (was reading as letters)',
    'LM16_02': 'all columns intact under a full entablature, fewer stripes, drums on the plinth',
    'VC04_04': 'closed gable roof (was an open frame with rafters)',
    'VC04_06': 'lean-to roof as one solid wedge seated on the walls (was a floating plank)',
    'CO04_01': 'wide natural arch with a clear opening, built at full size',
    'RD06_05': 'ruin with a roof slope resting on the back wall and posts (was jumbled tiles)',
    'RV01_02': 'solid stacked bank rock (was a crumpled slab with shards)',
    'LM19_04': 'lighter, warmer lower rock bands (was near-black)',
    'LM19_05': 'lighter, warmer lower rock bands (was near-black)',
    'LM20_02': 'full-size arcane ruin: stone circle, trilithons, rune altar, tall rune pillars',
    'LM21_04': 'solid banded root under a grass cap (was a stack of wafers)',
    'HM03_02': 'warm banded rock, no icicle stripes, thicker snow caps',
    'HM08_03': 'roof carried by four posts, tie beams and a hub block (was floating)',
    'WT13_05': 'stepped plateau terrace with a cairn on top (was tiny rubble piles)',
    'WT13_06': 'stone lantern with dark openings, no yellow glow',
    'RW01_02': 'banded sandstone gateposts with moss, sign between them (was plain grey boxes)',
}
f = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 15)
fs = ImageFont.truetype(r'C:\Windows\Fonts\segoeui.ttf', 13)
CELL, GAP, HEAD = 300, 6, 46
COLS, ROWS = 2, 4
PER = COLS * ROWS
cw = 3 * CELL + 2 * GAP
sheets = []
for s in range(0, len(ids), PER):
    part = ids[s:s + PER]
    rows = (len(part) + COLS - 1) // COLS
    sheet = Image.new('RGB', (COLS * (cw + 14), rows * (CELL + HEAD + 8)), (24, 24, 28))
    d = ImageDraw.Draw(sheet)
    for k, mid in enumerate(part):
        c, r = k % COLS, k // COLS
        x0, y0 = c * (cw + 14), r * (CELL + HEAD + 8)
        short = mid[:7]
        d.text((x0 + 4, y0 + 2), mid[:60], fill=(240, 240, 244), font=f)
        d.text((x0 + 4, y0 + 22), NOTE.get(short, ''), fill=(170, 200, 180), font=fs)
        srcs = [os.path.join(LIB, 'v5_fix3_archive', 'v4_sheets', f'_t_{mid}.png'), os.path.join(LIB, 'v4_sheets', f'_t_{mid}.png'), os.path.join(W, 'lead_back', f'{mid}.png')]
        for j, (p, lab) in enumerate(zip(srcs, ('BEFORE', 'AFTER front', 'AFTER back'))):
            xx = x0 + j * (CELL + GAP)
            if os.path.exists(p):
                sheet.paste(Image.open(p).convert('RGB').resize((CELL, CELL), Image.LANCZOS), (xx, y0 + HEAD))
            d.rectangle([xx, y0 + HEAD, xx + 92, y0 + HEAD + 18], fill=(0, 0, 0))
            d.text((xx + 4, y0 + HEAD + 1), lab, fill=(255, 190, 150) if j == 0 else (190, 240, 200), font=fs)
    p = os.path.join(OUT, f'fixed_{s // PER + 1:02d}.jpg')
    sheet.save(p, 'JPEG', quality=84)
    sheets.append(p)
print(len(ids), 'models on', len(sheets), 'sheets')
for p in sheets:
    print(p)
