"""topview_sketch_v5.py - a ROUGH SKETCH of how the redesigned island should look from above (north up).
Built from the exported terrain grid (24-stud cells) plus the planned changes in world_v5_terrain.json (hills, crater, canyons, Skull City
floor, the Himalayan peaks and plateau, gorges, the new rivers), the routed roads in roads_v5.json (bridges, tunnels, hairpins), and glyphs
for the settlements and landmarks. It is an intent drawing made from data, not a render of the game. Re-run after the plan files change.
Writes plan_v5/topview_sketch_v5.jpg
"""
import json
import math
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage as ndi

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import terrain_v5 as T

OUT = T.HERE + r'\topview_sketch_v5.jpg'
X0, X1, Z0, Z1 = -3300.0, 3300.0, -2900.0, 2450.0
S = 3.0                                    # studs per pixel
W = int(round((X1 - X0) / S))
H = int(round((Z1 - Z0) / S))
rnd = random.Random(11)
rng = np.random.default_rng(11)

grid = T.load_grid()
WORLD = T.load_world()
SPEC = T.load_spec(grid)
ROADS = json.load(open(T.HERE + r'\roads_v5.json'))
gx0, gz0, STEP = grid['x0'], grid['z0'], grid['step']
Hg, Mg, Wg = grid['H'], grid['M'], grid['W']
NZ, NX = Hg.shape


def px(x, z):
    return ((x - X0) / S, (z - Z0) / S)


sstep = T.sstep

# ------------------------------------------------------------------ terrain at 3 studs per pixel
xs = (X0 + (np.arange(W) + 0.5) * S).astype(np.float32)
zs = (Z0 + (np.arange(H) + 0.5) * S).astype(np.float32)
XX, ZZ = np.meshgrid(xs, zs)
fi = (XX - gx0) / STEP
fj = (ZZ - gz0) / STEP
Hh = ndi.map_coordinates(Hg, [fj, fi], order=1, mode='nearest').astype(np.float32)
ii = np.clip(np.rint(fi).astype(np.int32), 0, NX - 1)
jj = np.clip(np.rint(fj).astype(np.int32), 0, NZ - 1)
Mh = Mg[jj, ii]
Wh = Wg[jj, ii]
del fi, fj, ii, jj
has_w = Wh > -900
water = has_w & (Wh > Hh - 0.5)
sea = water & (Wh <= 1.0) & (Hh < -1.0)
lake = water & ~sea
land = ~water
lakes = WORLD['lakes']

# planned landforms (shared with the road router): the drawing and the routes see the same land
Hp = T.apply_spec(Hh, XX, ZZ, SPEC, land)

# ------------------------------------------------------------------ hillshade
gy, gx = np.gradient(Hp, S)
slope = np.hypot(gx, gy)
zf = 2.4
alt = math.radians(40.0)
Lx = Lz = -0.707 * math.cos(alt)
Ly = math.sin(alt)
nx_, nz_ = -gx * zf, -gy * zf
shade = (nx_ * Lx + nz_ * Lz + Ly) / (np.sqrt(nx_ * nx_ + nz_ * nz_ + 1.0) * math.sin(alt))
shade = np.clip(shade, 0.0, 1.6).astype(np.float32)
del gx, gy, nx_, nz_


def noise(sigma):
    a = ndi.gaussian_filter(rng.standard_normal((H, W)).astype(np.float32), sigma)
    return a / (a.std() + 1e-6)


lf, mf, hf = noise(22), noise(6), noise(2.2)

# ------------------------------------------------------------------ colours
PAL = np.array([
    (120, 140, 90), (122, 170, 76), (84, 134, 64), (226, 206, 150), (112, 92, 66), (128, 124, 120), (110, 108, 112), (70, 66, 72),
    (240, 244, 250), (196, 226, 242), (150, 124, 86), (208, 146, 88), (160, 150, 140), (168, 160, 150), (222, 200, 160), (234, 228, 214)], np.float32)
img = PAL[Mh]
green = np.isin(Mh, (1, 2))
central = np.exp(-((XX / 1500.0) ** 2 + ((ZZ - 450.0) / 1300.0) ** 2))
t_forest = sstep(0.1, 0.9, 0.5 + 0.38 * lf - 0.42 * central + 0.10 * mf)
forest_col = np.array((46, 98, 48), np.float32)
meadow_col = np.array((148, 186, 84), np.float32)
gcol = (meadow_col + (forest_col - meadow_col) * t_forest[..., None]) * (1.0 + 0.10 * hf)[..., None]
a_alt = (0.55 * sstep(150.0, 300.0, Hp))[..., None]
gcol = gcol * (1 - a_alt) + np.array((118, 118, 108), np.float32) * a_alt
img[green] = gcol[green]
del gcol, t_forest
dry = land & (XX > 700) & (ZZ > 250) & np.isin(Mh, (0, 3, 4, 10, 11, 14, 15))
sand_a, sand_b = np.array((226, 186, 118), np.float32), np.array((196, 118, 66), np.float32)
dcol = sand_a + (sand_b - sand_a) * sstep(-0.4, 1.2, lf + 0.5 * mf)[..., None]
img[dry] = dcol[dry]
del dcol
mesa = land & (XX > 700) & (ZZ > 250) & (slope > 0.45)
img[mesa] = np.array((172, 92, 56), np.float32)
dsk = np.hypot(XX - 2300.0, ZZ + 620.0) + 150.0 * lf
skull = land & (dsk < 520.0)
img[skull] = np.array((54, 50, 58), np.float32) * (1.0 + 0.25 * mf[skull])[..., None]
# the Himalayas: bare rock and snow above the tree line, snow cap on the high peaks
hi = land & (Hp > 300) & (XX > 800) & (ZZ < -900)
img[hi] = np.array((132, 128, 126), np.float32) * (1.0 + 0.12 * hf[hi])[..., None]
snow = land & (Hp > 430) & (XX > 800) & (ZZ < -900)
img[snow] = np.array((238, 242, 248), np.float32)
pl = SPEC['plateau']
on_plateau = land & (((XX - pl['x']) / pl['rx']) ** 2 + ((ZZ - pl['z']) / pl['rz']) ** 2 < 1.0)
img[on_plateau] = np.array((214, 218, 226), np.float32) * (1.0 + 0.05 * hf[on_plateau])[..., None]
img = img * (0.52 + 0.58 * np.minimum(shade, 1.45))[..., None]
img[lake] = np.array((110, 160, 80), np.float32) * (0.52 + 0.58 * np.minimum(shade[lake], 1.45))[..., None]
depth = np.clip(-Hh, 0, 120)
stops_d = [0, 10, 28, 60, 120]
stops_c = np.array([(86, 206, 204), (52, 164, 196), (28, 108, 170), (14, 62, 128), (8, 36, 96)], np.float32)
sea_rgb = np.stack([np.interp(depth, stops_d, stops_c[:, k]) for k in range(3)], axis=-1).astype(np.float32)
img[sea] = sea_rgb[sea] * (1.0 + 0.04 * mf[sea])[..., None]
del sea_rgb, depth
coast = ndi.binary_dilation(sea, iterations=3) & ~sea
img[coast] = img[coast] * 0.35 + 255.0 * 0.65
base = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
del img

# ------------------------------------------------------------------ vector layers
ov = Image.new('RGBA', base.size, (0, 0, 0, 0))
od = ImageDraw.Draw(ov)


def quad(cx, cz, w, h, th):
    return [px(cx + dx * math.cos(th) - dz * math.sin(th), cz + dx * math.sin(th) + dz * math.cos(th)) for dx, dz in ((-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2))]


def on_land(x, z, max_slope=0.4):
    j, i = int((z - Z0) / S), int((x - X0) / S)
    return 0 <= j < H and 0 <= i < W and bool(land[j, i]) and Hh[j, i] > 3 and slope[j, i] < max_slope


def fields(cx, cz, rad, n, cols, size=(70, 190)):
    for _ in range(n):
        a, rr = rnd.uniform(0, math.tau), rad * math.sqrt(rnd.random())
        x, z = cx + rr * math.cos(a), cz + rr * math.sin(a)
        if not on_land(x, z, 0.35):
            continue
        od.polygon(quad(x, z, rnd.uniform(*size), rnd.uniform(*size), rnd.uniform(-0.5, 0.5)), fill=rnd.choice(cols) + (235,))


FARM = [(212, 196, 98), (176, 196, 84), (138, 170, 70), (196, 160, 96), (110, 150, 66), (226, 214, 130)]
MARSH = [(74, 128, 98), (60, 110, 86), (96, 150, 110)]
fields(-1248, 528, 430, 150, FARM)
fields(-1000, 720, 560, 190, FARM)
fields(500, 650, 420, 70, FARM)
fields(-500, -300, 350, 50, FARM)
fields(-660, 300, 320, 70, MARSH, size=(40, 110))
ov_img = Image.alpha_composite(base.convert('RGBA'), ov)
d = ImageDraw.Draw(ov_img)


def blob(cx, cz, rx, rz, seed, grow=1.12):
    r2 = random.Random(seed)
    ph = [r2.uniform(0, math.tau) for _ in range(3)]
    pts = []
    for k in range(72):
        t = math.tau * k / 72
        f = 1.0 + 0.16 * math.sin(2 * t + ph[0]) + 0.10 * math.sin(3 * t + ph[1]) + 0.06 * math.sin(5 * t + ph[2])
        pts.append(px(cx + rx * grow * f * math.cos(t), cz + rz * grow * f * math.sin(t)))
    return pts


for k, l in enumerate(lakes):
    frozen = bool(l.get('frozen')) or 'ice' in l['name']
    d.polygon(blob(l['cx'], l['cz'], l['rx'], l['rz'], 100 + k), fill=(196, 226, 242) if frozen else (62, 134, 196), outline=(96, 150, 78))
for tn in SPEC['tarns']:
    d.polygon(blob(tn['x'], tn['z'], tn['r'], tn['r'] * 0.8, 500), fill=(204, 232, 246), outline=(120, 150, 170))
for rv in WORLD['rivers']:
    pts = [px(p[0], p[1]) for p in rv['pts']]
    if len(pts) >= 2:
        d.line(pts, fill=(64, 140, 204), width=max(2, int(rv['w'] / S * 1.3)), joint='curve')
for rv in SPEC['rivers_new']:
    sm = [px(*p) for p in T.chaikin(rv['pts'], 3)]
    d.line(sm, fill=(52, 128, 196), width=max(3, int(rv['w'] / S * 1.6)), joint='curve')
fl = SPEC['falls'][0]
d.line([px(fl['x'], fl['z'] - 40), px(fl['x'], fl['z'] + 60)], fill=(245, 250, 255), width=7)

# roads from the router: tan ribbons with a dark edge; carved stairs thin and pale
for rt in ROADS['routes']:
    sm = [px(p[0], p[1]) for p in T.chaikin([(p[0], p[1]) for p in rt['pts']], 1)]
    stair = 'stair' in rt['name']
    d.line(sm, fill=(150, 118, 80), width=(4 if stair else 7), joint='curve')
for rt in ROADS['routes']:
    sm = [px(p[0], p[1]) for p in T.chaikin([(p[0], p[1]) for p in rt['pts']], 1)]
    stair = 'stair' in rt['name']
    d.line(sm, fill=(238, 224, 196) if stair else (226, 200, 152), width=(2 if stair else 4), joint='curve')
# tunnels: dark gap in the road with portal ticks
for t in ROADS['tunnels']:
    d.line([px(t['x0'], t['z0']), px(t['x1'], t['z1'])], fill=(46, 32, 26), width=9)
    for qx, qz in ((t['x0'], t['z0']), (t['x1'], t['z1'])):
        a, b = px(qx, qz)
        d.rectangle([a - 4, b - 4, a + 4, b + 4], fill=(250, 244, 230), outline=(46, 32, 26))
# bridges: stone white, towered lilac, rope and timber brown with flags
BR_COL = {'stone_arch': (240, 236, 228), 'towered_stone': (190, 160, 190), 'rope_suspension': (122, 82, 50), 'timber_cantilever': (146, 104, 64), 'stone_viaduct': (232, 226, 214)}
for b in ROADS['bridges']:
    th = math.radians(b['heading'])
    d.polygon(quad(b['x'], b['z'], b['span'] + 10, 14, th), fill=BR_COL.get(b['kind'], (255, 255, 255)), outline=(30, 30, 36))
    if b['kind'] == 'rope_suspension':
        for k in range(-3, 4):
            ax, az = px(b['x'] + math.cos(th) * k * b['span'] / 7.0, b['z'] + math.sin(th) * k * b['span'] / 7.0)
            d.rectangle([ax - 2, az - 6, ax + 2, az - 2], fill=[(220, 60, 50), (240, 200, 60), (60, 120, 200), (250, 250, 250), (60, 160, 90)][k % 5])
ov_img.convert('RGB').save(T.HERE + r'\wizard_map_src.png')       # terrain, water and roads without the glyphs: source of the tower's circular map


def houses(cx, cz, rx, rz, n, cols, size=(14, 30), edge=None):
    done = 0
    guard = 0
    while done < n and guard < n * 20:
        guard += 1
        a, rr = rnd.uniform(0, math.tau), math.sqrt(rnd.random())
        x, z = cx + rx * rr * math.cos(a), cz + rz * rr * math.sin(a)
        if not on_land(x, z, 0.6):
            continue
        d.polygon(quad(x, z, rnd.uniform(*size), rnd.uniform(*size), rnd.choice((0, 0.15, -0.15, 0.4, -0.4))), fill=rnd.choice(cols), outline=edge)
        done += 1


def ring(cx, cz, r, color, width=3, rz=None):
    rz = rz or r
    d.ellipse([px(cx - r, cz - rz), px(cx + r, cz + rz)], outline=color, width=width)


def disc(cx, cz, r, color, outline=None, rz=None):
    rz = rz or r
    d.ellipse([px(cx - r, cz - rz), px(cx + r, cz + rz)], fill=color, outline=outline)


ORANGE = [(198, 88, 52), (214, 104, 58), (178, 72, 46), (206, 96, 56), (140, 62, 48)]
# capital: castle plateau, ring wall, orange town, plaza
disc(0, -2200, 300, (128, 122, 132), (90, 86, 96), rz=215)
disc(0, -2230, 70, (170, 160, 176), (90, 86, 96), rz=55)
for k in range(8):
    a = k * math.tau / 8
    disc(70 * math.cos(a), -2230 + 55 * math.sin(a), 10, (120, 44, 52))
houses(0, -1585, 455, 320, 560, ORANGE, size=(16, 34))
ring(0, -1585, 490, (150, 142, 158), width=6, rz=350)
for k in range(12):
    a = math.radians(15 + 30 * k)
    disc(490 * math.cos(a), -1585 + 350 * math.sin(a), 16, (120, 44, 52), (230, 226, 230))
disc(0, -1560, 80, (232, 214, 188), (150, 142, 158), rz=62)
# Town 1: dark cluster, skull HQ, avenue
houses(0, 0, 280, 300, 200, [(78, 76, 86), (104, 90, 80), (60, 58, 68), (126, 112, 98)], size=(12, 26))
disc(0, -402, 40, (232, 228, 220), (60, 58, 68))
d.line([px(0, -360), px(0, -80)], fill=(226, 200, 152), width=4)
# elf valley: canopy, giant tree, houses, waterfall
disc(-1560, -400, 330, (30, 84, 44), (20, 60, 34), rz=320)
disc(-1560, -430, 112, (70, 138, 70), (30, 84, 44))
houses(-1560, -420, 300, 290, 46, [(150, 112, 74), (132, 98, 66), (170, 136, 92)], size=(16, 30))
d.line([px(-1780, -790), px(-1700, -700)], fill=(240, 248, 252), width=5)
# alpine village and the fortress on its peak
houses(1585, -880, 200, 150, 34, [(238, 240, 246), (226, 230, 238)], size=(14, 26), edge=(90, 90, 100))
d.polygon(quad(1632, -1608, 90, 70, 0.3), fill=(96, 96, 108), outline=(40, 40, 50))
for ox, oz in ((-45, -35), (45, -35), (-45, 35), (45, 35)):
    disc(1632 + ox, -1608 + oz, 12, (150, 150, 160))
# THE WIZARD TOWER on the Roof Plateau: terrace, shell, inner ring, star, buttresses
tw = pl['tower']
disc(tw['x'], tw['z'], tw['courtyard_radius'], (200, 204, 214), (150, 150, 168))
disc(tw['x'], tw['z'], tw['terrace_radius'], (226, 226, 236), (110, 100, 140))
disc(tw['x'], tw['z'], tw['shell_radius'], (96, 86, 134), (250, 250, 255))
disc(tw['x'], tw['z'], 32, (64, 54, 104), (200, 190, 230))
for k in range(8):
    a = k * math.tau / 8
    disc(tw['x'] + 62 * math.cos(a), tw['z'] + 62 * math.sin(a), 9, (170, 160, 190), (60, 52, 90))
star = []
for k in range(10):
    rr = 20 if k % 2 == 0 else 8
    a = -math.pi / 2 + k * math.pi / 5
    star.append(px(tw['x'] + rr * math.cos(a), tw['z'] + rr * math.sin(a)))
d.polygon(star, fill=(255, 236, 160))
# hidden monastery in the pocket beyond the Frost Gorge, prayer-flag line, harbour, desert, west village, Skull City, crater, ruins
houses(2450, -1480, 80, 60, 9, [(150, 70, 60), (176, 96, 70), (230, 226, 218)], size=(14, 22))
d.line([px(2400, -1420), px(2500, -1440)], fill=(230, 80, 60), width=2)
d.line([px(2400, -1428), px(2500, -1448)], fill=(250, 210, 70), width=2)
d.line([px(-625, 1808), px(-155, 1808)], fill=(196, 196, 202), width=10)
houses(-390, 1590, 280, 190, 130, [(238, 238, 240), (92, 128, 176), (190, 90, 70), (226, 210, 180)], size=(14, 28))
for k in range(9):
    disc(-560 + k * 52, 1880 + 40 * math.sin(k * 1.7), 14, (250, 250, 250), (90, 90, 100), rz=7)
houses(1235, 1105, 230, 200, 60, [(210, 168, 110), (190, 140, 92), (226, 190, 130)], size=(14, 26))
ring(1660, 1130, 110, (206, 190, 160), width=5)
ring(1660, 1130, 70, (206, 190, 160), width=4)
d.polygon(quad(2160, 1248, 110, 90, 0.2), fill=(190, 170, 130), outline=(120, 100, 70))
disc(1860, 1380, 45, (62, 134, 196), (80, 140, 80))
houses(-1248, 528, 160, 140, 36, [(236, 226, 206), (206, 120, 84), (190, 100, 70)], size=(12, 22))
d.polygon([px(-1248, 470), px(-1236, 505), px(-1260, 505)], fill=(70, 60, 60))
houses(2300, -450, 250, 230, 46, [(30, 28, 34), (70, 64, 74), (46, 42, 50)], size=(14, 30))
disc(2208, -936, 70, (214, 208, 200), (40, 36, 40))
disc(2185, -950, 14, (30, 26, 30))
disc(2231, -950, 14, (30, 26, 30))
for _ in range(26):
    x, z = 2300 + rnd.uniform(-480, 480), -620 + rnd.uniform(-520, 520)
    if not on_land(x, z, 5):
        continue
    pts = [px(x, z)]
    for _k in range(7):
        x += rnd.uniform(-60, 60)
        z += rnd.uniform(-60, 60)
        pts.append(px(x, z))
    d.line(pts, fill=(255, 150, 60), width=3, joint='curve')
    d.line(pts, fill=(255, 70, 34), width=1, joint='curve')
ring(1368, -312, 240, (40, 40, 46), width=4)
for k in range(12):
    a = k * math.tau / 12
    disc(1368 + 262 * math.cos(a), -312 + 262 * math.sin(a), 7, (210, 206, 200))
ring(760, 470, 80, (176, 172, 164), width=4)
d.polygon(quad(-760, -980, 90, 70, 0.1), fill=(150, 146, 140), outline=(70, 66, 60))
for fx, fz, fr in ((3050, -2400, 90), (2930, -2220, 50), (3150, -2230, 40)):
    disc(fx + 14, fz + 24, fr, (20, 60, 110))
    disc(fx, fz, fr, (146, 176, 112), (80, 100, 70))
    disc(fx, fz, fr * 0.45, (96, 134, 86))
# peaks: small white-capped marks with a dark foot
for pk in SPEC['peaks']:
    a, b = px(pk['x'], pk['z'])
    d.polygon([(a, b - 14), (a - 12, b + 8), (a + 12, b + 8)], fill=(250, 252, 255), outline=(70, 74, 90))

# labels
fL = ImageFont.truetype('arialbd.ttf', 30)
fS = ImageFont.truetype('arialbd.ttf', 22)
LABELS = [('THE ELDEN TREE', -1700, -1150, fL), ('FROSTHOLD', 1500, -2150, fL), ('CASTLE TOWN', 0, -1000, fL), ('SKULL CITY', 2520, -120, fL),
          ('SANDS OF ELYSIUM', 1950, 1480, fL), ('WEST VILLAGE', -1560, 770, fL), ('TOWN 1', 0, 330, fL), ('HARBOUR', -390, 2120, fL),
          ('THE CRATER', 1368, -90, fL), ('GREENHEART PLAINS', -1000, 1050, fL), ('ELF VALLEY', -1560, -20, fL),
          ('WIZARD TOWER', 1020, -1400, fS), ('ROOF PLATEAU', 1380, -1560, fS), ('GALE PASS', 640, -1070, fS), ('FROST GORGE', 2600, -1180, fS),
          ('HIDDEN MONASTERY', 2450, -1610, fS), ('ROOF FALLS', 1640, -1180, fS)]
for t, x, z, f in LABELS:
    X, Y = px(x, z)
    box = d.textbbox((0, 0), t, font=f, stroke_width=4)
    d.text((X - (box[2] - box[0]) / 2, Y - (box[3] - box[1]) / 2), t, font=f, fill=(255, 255, 255), stroke_width=4, stroke_fill=(20, 24, 30))
# clouds on the edges
cl = Image.new('L', ov_img.size, 0)
cd = ImageDraw.Draw(cl)
for cx, cz, rx, rz in ((-3050, -1800, 420, 160), (-3150, 200, 300, 140), (3150, -1400, 380, 150), (3100, 300, 300, 140), (2000, 2250, 420, 150), (-1000, 2300, 380, 130), (300, -2800, 350, 120)):
    for _ in range(14):
        ox, oz = rnd.uniform(-rx, rx), rnd.uniform(-rz, rz)
        rr = rnd.uniform(60, 130)
        cd.ellipse([px(cx + ox - rr, cz + oz - rr * 0.6), px(cx + ox + rr, cz + oz + rr * 0.6)], fill=255)
cl = cl.filter(ImageFilter.GaussianBlur(20)).point(lambda v: int(v * 0.6))
final = ov_img.convert('RGB')
final.paste((255, 255, 255), mask=cl)
fd = ImageDraw.Draw(final)
fd.rectangle([0, 0, 1180, 58], fill=(24, 28, 36))
fd.text((14, 10), 'ROUGH SKETCH of the intended top view (from terrain data, not a game render)', font=ImageFont.truetype('arialbd.ttf', 28), fill=(255, 255, 255))
# legend
lx, ly = 18, H - 168
fd.rectangle([lx - 8, ly - 8, lx + 520, ly + 150], fill=(24, 28, 36))
items = [((226, 200, 152), 'road'), ((240, 236, 228), 'stone bridge'), ((190, 160, 190), 'towered bridge'), ((122, 82, 50), 'rope / timber bridge (Himalayan)'), ((46, 32, 26), 'tunnel'), ((96, 86, 134), 'wizard tower on the Roof Plateau')]
for k, (c, t) in enumerate(items):
    fd.rectangle([lx, ly + k * 24, lx + 40, ly + k * 24 + 14], fill=c, outline=(255, 255, 255))
    fd.text((lx + 52, ly + k * 24 - 4), t, font=ImageFont.truetype('arialbd.ttf', 20), fill=(255, 255, 255))
final.save(OUT, quality=88, optimize=True)
print('wrote', OUT, final.size, os.path.getsize(OUT) // 1024, 'KB')
for name, x, z in (('west sea', -3200, 0), ('wizard tower', 1380, -1320), ('plateau edge', 1380, -1560), ('Spire of Dawn', 1140, -1790), ('elf tree', -1560, -430),
                   ('desert', 2160, 1300), ('skull zone', 2300, -600), ('harbour bay', -390, 1950), ('alpine lake', 1490, -1080), ('rope bridge', 2448, -1358)):
    print('%-14s (%5d,%5d) rgb %s' % (name, x, z, final.getpixel((int((x - X0) / S), int((z - Z0) / S)))))
a = np.asarray(final).astype(np.float32)
g = a.mean(axis=2)
print('mean %.0f std %.0f | near-black %.2f%% | near-white %.2f%%' % (g.mean(), g.std(), 100 * (g < 20).mean(), 100 * (g > 240).mean()))
