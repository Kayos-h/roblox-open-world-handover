"""plan_overlay_v5.py - draws the world-redesign PLAN on top of the stitched north-up top-down view, and a side-by-side with the concept map.
Needs: shots/v4/topdown/topdown_full_northup.jpg (made by rebuild/v4/stitch_topdown.py) and reference/world_concept_topdown.png.
Writes plan_v5/world_plan_overlay.jpg (map + legend) and plan_v5/concept_vs_plan.jpg (concept on the left, plan on the right).
World -> pixel: the stitched picture covers x -3300..3300 and z -2900..2450 (exact at sea level; tall peaks shift a little).
Markers are proposals (sites from sites_candidates.json, good to +-30 studs); river routes are illustrative until the path search runs.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

TOWN = r'C:\Users\Nitro\.kiro\crew\workspace\town'
SRC = TOWN + r'\shots\v4\topdown\topdown_full_northup.jpg'
CONCEPT = TOWN + r'\reference\world_concept_topdown.png'
OUT = TOWN + r'\plan_v5\world_plan_overlay.jpg'
OUT2 = TOWN + r'\plan_v5\concept_vs_plan.jpg'
X0, X1, Z0, Z1 = -3300.0, 3300.0, -2900.0, 2450.0
SCALE = 0.75
LEGEND_W = 640
RES = getattr(Image, 'Resampling', Image).LANCZOS


def font(size):
    for f in ('arialbd.ttf', 'arial.ttf', 'segoeuib.ttf'):
        try:
            return ImageFont.truetype(f, size)
        except Exception:
            pass
    return ImageFont.load_default()


base = Image.open(SRC).convert('RGB')
W1, H1 = int(base.size[0] * SCALE), int(base.size[1] * SCALE)
base = base.resize((W1, H1), RES)


def px(x, z):
    return (x - X0) / (X1 - X0) * W1, (z - Z0) / (Z1 - Z0) * H1


def ctext(d, xy, text, f, fill=(255, 255, 255), stroke=0):
    box = d.textbbox((0, 0), text, font=f, stroke_width=stroke)
    d.text((xy[0] - (box[2] - box[0]) / 2 - box[0], xy[1] - (box[3] - box[1]) / 2 - box[1]), text, font=f, fill=fill,
           stroke_width=stroke, stroke_fill=(0, 0, 0))


def dashed(d, pts, color, width=5, dash=18, gap=11):
    for (ax, ay), (bx, by) in zip(pts[:-1], pts[1:]):
        L = math.hypot(bx - ax, by - ay)
        if L == 0:
            continue
        ux, uy = (bx - ax) / L, (by - ay) / L
        t = 0.0
        while t < L:
            e = min(t + dash, L)
            d.line([(ax + ux * t, ay + uy * t), (ax + ux * e, ay + uy * e)], fill=color, width=width)
            t = e + gap


# region discs: name, centre, radii, colour
REGIONS = [
    ('NW ANCIENT FOREST', (-1700, -700), (1000, 1100), (80, 210, 120)),
    ('NE FROZEN HIGHLANDS', (1600, -1500), (1100, 1000), (150, 220, 255)),
    ('NORTH CAPITAL', (0, -1650), (800, 850), (255, 205, 80)),
    ('SW GREENHEART PLAINS', (-1100, 700), (900, 700), (200, 235, 90)),
    ('SE DESERT', (1800, 1100), (1000, 800), (255, 150, 60)),
    ('SOUTH HARBOUR COAST', (-350, 1650), (700, 420), (80, 205, 205)),
    ('EAST COAST SKULL CITY', (2450, -550), (480, 560), (225, 90, 165)),
]
ov = Image.new('RGBA', base.size, (0, 0, 0, 0))
od = ImageDraw.Draw(ov)
for name, (cx, cz), (rx, rz), col in REGIONS:
    x, y = px(cx, cz)
    rxp, rzp = rx / (X1 - X0) * W1, rz / (Z1 - Z0) * H1
    od.ellipse([x - rxp, y - rzp, x + rxp, y + rzp], fill=col + (38,), outline=col + (210,), width=4)
rivers = [  # illustrative routes, solved properly by the path search later
    [(380, -2350), (640, -2050), (700, -1650), (600, -1250), (220, -1080)],
    [(380, -2350), (140, -2100), (-640, -2000), (-700, -1600), (-600, -1250), (-220, -1080)],
    [(-1350, -1900), (-1500, -1500), (-1650, -1100), (-1700, -720)],
    [(-1150, 1150), (-1220, 800), (-1248, 560), (-950, 420), (-660, 300)],
]
for r in rivers:
    dashed(od, [px(x, z) for x, z in r], (120, 205, 255, 235))
im = Image.alpha_composite(base.convert('RGBA'), ov).convert('RGB')
d = ImageDraw.Draw(im)
fr, fm, fn = font(24), font(20), font(22)
for name, (cx, cz), (rx, rz), col in REGIONS:
    x, y = px(cx, cz)
    ctext(d, (x, y - rz / (Z1 - Z0) * H1 * 0.55), name, fr, fill=(255, 255, 255), stroke=3)

EXIST = [('TOWN 1', 0, 0), ('CAPITAL', 0, -1585), ('KEEP', 0, -2275), ('ELF TREE', -1560, -430), ('ALPINE', 1585, -880), ('HARBOUR', -390, 1700), ('RUSTY', 1406, 1244)]
for name, x, z in EXIST:
    X, Y = px(x, z)
    d.ellipse([X - 6, Y - 6, X + 6, Y + 6], fill=(255, 255, 255), outline=(0, 0, 0), width=2)
    d.text((X + 11, Y - 12), name, font=fm, fill=(255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0))

PLAN = [
    (1, 0, -1650, 'Capital: ring wall + terrace keep', 'horseshoe river, skyline, orange roofs'),
    (2, 1632, -1608, 'Frost fortress (peak h 511)', 'built into the mountain, jagged spires'),
    (3, 1380, -1320, 'Abandoned magic tower', 'summit pad (1380,-1320), 200-300 studs'),
    (4, 1368, -312, 'Magical crater', 'bowl r 240, monolith ring, rim rocks'),
    (5, -1800, -672, 'Colossal waterfall + gorge', 'west rim of the elf valley, feeds the lake'),
    (6, 760, 470, 'Ancient ruined civilization', 'gate, arena, aqueducts on the plateau'),
    (7, -760, -980, 'Ruined castle', 'north-west plateau'),
    (8, 2160, 1248, 'Buried desert temple', 'half sunk in sand, stair down'),
    (9, 1660, 1130, 'Ring temple', 'circular temple + inner sanctum'),
    (10, -1000, 720, 'Greenheart farm and mill belt', 'farms, windmills, rolling grass'),
    (11, -300, 330, 'Marsh + rolling hills', 'breaks up the central green carpet'),
    (12, 2300, -700, 'Skull City (east coast)', 'skull cliff (2208,-936), dark city floor'),
    (13, -1248, 528, 'West farm village', 'farmland, spired church, mill'),
    (14, 3050, -2400, 'Floating islands', 'NE corner, as on the concept map'),
]
for n, x, z, t1, t2 in PLAN:
    X, Y = px(x, z)
    d.ellipse([X - 17, Y - 17, X + 17, Y + 17], fill=(214, 48, 49), outline=(255, 255, 255), width=3)
    ctext(d, (X, Y), str(n), fn, fill=(255, 255, 255))
map_only = im.copy()

# legend panel on the right
out = Image.new('RGB', (W1 + LEGEND_W, H1), (24, 28, 36))
out.paste(im, (0, 0))
g = ImageDraw.Draw(out)
lx = W1 + 26
g.text((lx, 22), 'WORLD PLAN v5 (proposal, north up)', font=font(30), fill=(255, 255, 255))
g.text((lx, 62), 'Follows the concept map. Nothing is built yet.', font=fm, fill=(190, 195, 205))
y = 104
for n, x, z, t1, t2 in PLAN:
    g.ellipse([lx, y + 2, lx + 34, y + 36], fill=(214, 48, 49), outline=(255, 255, 255), width=2)
    ctext(g, (lx + 17, y + 19), str(n), font(21))
    g.text((lx + 50, y), t1, font=font(23), fill=(255, 255, 255))
    g.text((lx + 50, y + 27), t2, font=font(19), fill=(170, 176, 190))
    y += 62
y += 4
g.text((lx, y), 'Region discs are loose zones, not borders:', font=fm, fill=(190, 195, 205))
y += 28
for name, c, r, col in REGIONS:
    g.rectangle([lx, y + 3, lx + 26, y + 21], fill=col, outline=(255, 255, 255))
    g.text((lx + 38, y), name.title(), font=fm, fill=(235, 238, 245))
    y += 26
dashed(g, [(lx, y + 14), (lx + 30, y + 14)], (120, 205, 255), width=5, dash=9, gap=5)
g.text((lx + 38, y + 3), 'Planned rivers (illustrative routes)', font=fm, fill=(235, 238, 245))
y += 36
for line in ('White dots are existing settlements.', 'Sites are good to +-30 studs; markers near tall peaks', 'can sit up to 50 px off (perspective).', 'NE and SW parts of the base picture are older.'):
    g.text((lx, y), line, font=font(18), fill=(150, 156, 170))
    y += 23
os.makedirs(os.path.dirname(OUT), exist_ok=True)
out.save(OUT, quality=90, optimize=True)
print('wrote', OUT, out.size, os.path.getsize(OUT) // 1024, 'KB')

# side by side: concept (left) and the plan on the current map (right), same height
cp = Image.open(CONCEPT).convert('RGB')
Hs = 1128
cp = cp.resize((int(cp.size[0] * Hs / cp.size[1]), Hs), RES)
pl = map_only.resize((int(map_only.size[0] * Hs / map_only.size[1]), Hs), RES)
gap = 24
sb = Image.new('RGB', (cp.size[0] + gap + pl.size[0], Hs + 56), (24, 28, 36))
sb.paste(cp, (0, 56))
sb.paste(pl, (cp.size[0] + gap, 56))
sd = ImageDraw.Draw(sb)
sd.text((16, 12), 'CONCEPT MAP (your picture, the target)', font=font(30), fill=(255, 255, 255))
sd.text((cp.size[0] + gap + 16, 12), 'PLAN ON THE CURRENT MAP (stitched top-down, north up)', font=font(30), fill=(255, 255, 255))
sb.save(OUT2, quality=88, optimize=True)
print('wrote', OUT2, sb.size, os.path.getsize(OUT2) // 1024, 'KB')
