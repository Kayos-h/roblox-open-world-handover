"""stitch_topdown.py - ONE north-up top-down picture of the whole island from four straight-down photos.

Why a rotation: tour.ps1 takes every photo with CFrame.lookAt(pos, look): camera 2300 studs up, aimed 1 stud south of
straight down, vertical field of view 70 degrees. The camera's up vector is then +Z, so SOUTH is at the top and WEST on
the right of each photo. Each photo is rotated 180 degrees first, then cut into its quadrant of one shared canvas
(world studs, x east, z south). Seams are blended with a smoothstep over +-FEATHER studs. The scale is exact only at
sea level (mountains show the normal perspective shift).
Nothing here judges the picture: it only moves pixels and prints mean/std per tile as a blank check.
Re-run after a new shoot: edit the four photo paths in TILES and run `python stitch_topdown.py`.
"""
import math
import os
import time

from PIL import Image, ImageDraw, ImageFont, ImageStat

TOWN = r'C:\Users\Nitro\.kiro\crew\workspace\town'
SHOTS = TOWN + r'\shots\v4'
# name: (photo path, camera x, camera z)
TILES = {
    'NW': (SHOTS + r'\r5\f_quad_nw.jpg', -1500.0, -1600.0),
    'NE': (SHOTS + r'\r4\q_ne_down.jpg', 1500.0, -1600.0),
    'SW': (SHOTS + r'\r4\q_sw_down.jpg', -1500.0, 900.0),
    'SE': (SHOTS + r'\r5\f_quad_se.jpg', 1500.0, 900.0),
}
ALT = 2300.0                # camera height in studs
FOV = 70.0                  # vertical field of view in degrees (tour.ps1 sets FieldOfView = 70)
X0, X1 = -3300.0, 3300.0    # canvas edges in world studs (x east)
Z0, Z1 = -2900.0, 2450.0    # (z south)
XM, ZM = 0.0, -350.0        # seam lines between the quadrants
FEATHER = 250.0             # studs: half-width of the blend across a seam
UPSCALE = 2
OUT_DIR = SHOTS + r'\topdown'
OUT = OUT_DIR + r'\topdown_full_northup.jpg'
RES = getattr(Image, 'Resampling', Image).LANCZOS


def sstep(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)


def stats(img):
    st = ImageStat.Stat(img.convert('L'))
    return st.mean[0], st.stddev[0]


def font(size):
    for f in ('arialbd.ttf', 'arial.ttf', 'segoeuib.ttf'):
        try:
            return ImageFont.truetype(f, size)
        except Exception:
            pass
    return ImageFont.load_default()


photos = {}
mt = {}
for name, (path, cx, cz) in TILES.items():
    im = Image.open(path).convert('RGB')
    photos[name] = im
    mt[name] = os.path.getmtime(path)
    m, sd = stats(im)
    print('%s: %s size %dx%d taken %s mean %.0f std %.0f' % (
        name, os.path.basename(path), im.size[0], im.size[1], time.strftime('%d %b %H:%M', time.localtime(mt[name])), m, sd))

pw, ph = photos['NW'].size
assert all(p.size == (pw, ph) for p in photos.values()), 'photos differ in size'
s = ph / (2.0 * ALT * math.tan(math.radians(FOV / 2.0)))   # pixels per stud at sea level
W = int(round((X1 - X0) * s))
H = int(round((Z1 - Z0) * s))
print('scale %.4f px/stud (%.2f studs/px), canvas %dx%d, output %dx%d' % (s, 1.0 / s, W, H, W * UPSCALE, H * UPSCALE))

# canvas columns/rows where each tile has non-zero weight
xm_lo, xm_hi = (XM - FEATHER - X0) * s, (XM + FEATHER - X0) * s
zm_lo, zm_hi = (ZM - FEATHER - Z0) * s, (ZM + FEATHER - Z0) * s
canvas = {}
for name, (path, cx, cz) in TILES.items():
    rot = photos[name].rotate(180)                      # south-up/west-right -> north-up/east-right
    ou = pw / 2.0 + s * (X0 - cx)
    ov = ph / 2.0 + s * (Z0 - cz)
    box = (int(round(ou)), int(round(ov)), int(round(ou)) + W, int(round(ov)) + H)
    canvas[name] = rot.crop(box)
    i0, i1 = (0.0, xm_hi) if name in ('NW', 'SW') else (xm_lo, float(W))
    j0, j1 = (0.0, zm_hi) if name in ('NW', 'NE') else (zm_lo, float(H))
    miss = max(0.0, -(ou + i0), (ou + i1) - pw, -(ov + j0), (ov + j1) - ph)
    print('%s: crop box %s, uses photo x %.0f..%.0f y %.0f..%.0f -> %s' % (
        name, box, ou + i0, ou + i1, ov + j0, ov + j1, 'OK' if miss <= 0.5 else 'WARNING outside photo by %.0f px' % miss))

mask_x = Image.new('L', (W, H), 0)
dx = ImageDraw.Draw(mask_x)
for i in range(W):
    x = X0 + (i + 0.5) / s
    dx.line([(i, 0), (i, H - 1)], fill=int(round(255 * sstep((x - (XM - FEATHER)) / (2 * FEATHER)))))
mask_z = Image.new('L', (W, H), 0)
dz = ImageDraw.Draw(mask_z)
for j in range(H):
    z = Z0 + (j + 0.5) / s
    dz.line([(0, j), (W - 1, j)], fill=int(round(255 * sstep((z - (ZM - FEATHER)) / (2 * FEATHER)))))

top = Image.composite(canvas['NE'], canvas['NW'], mask_x)      # east -> NE
bottom = Image.composite(canvas['SE'], canvas['SW'], mask_x)   # east -> SE
final = Image.composite(bottom, top, mask_z)                   # south -> bottom row
final = final.resize((W * UPSCALE, H * UPSCALE), RES)
Wc, Hc = final.size

# caption band and compass
newest = max(mt.values())
older = [n for n in ('NW', 'NE', 'SW', 'SE') if newest - mt[n] > 20 * 60]
line1 = 'North up. Whole island stitched from four straight-down photos taken 2300 studs up.'
line2 = 'Photo times: ' + ', '.join('%s %s' % (n, time.strftime('%H:%M', time.localtime(mt[n]))) for n in ('NW', 'NE', 'SW', 'SE')) + '.'
if older:
    line2 += ' ' + ' and '.join(older) + ' are older, so sea colour, foam and coast edges there may differ. Seams are blended.'
else:
    line2 += ' Seams are blended.'
overlay = Image.new('RGBA', final.size, (0, 0, 0, 0))
ImageDraw.Draw(overlay).rectangle([0, Hc - 84, Wc, Hc], fill=(0, 0, 0, 150))
final = Image.alpha_composite(final.convert('RGBA'), overlay).convert('RGB')
d = ImageDraw.Draw(final)
f1, f2 = font(26), font(34)
d.text((18, Hc - 78), line1, fill=(255, 255, 255), font=f1)
d.text((18, Hc - 42), line2, fill=(255, 255, 255), font=f1)
ax, ay = Wc - 90, 40
d.polygon([(ax, ay), (ax + 20, ay + 62), (ax, ay + 48), (ax - 20, ay + 62)], fill=(255, 255, 255), outline=(0, 0, 0))
d.text((ax - 12, ay + 70), 'N', fill=(255, 255, 255), font=f2, stroke_width=3, stroke_fill=(0, 0, 0))

os.makedirs(OUT_DIR, exist_ok=True)
final.save(OUT, quality=90, optimize=True)

# numeric blank check only
m, sd = stats(final)
for k, (fx, fy) in {'NW': (0.0, 0.0), 'NE': (0.5, 0.0), 'SW': (0.0, 0.5), 'SE': (0.5, 0.5)}.items():
    c = final.crop((int(Wc * (fx + 0.1)), int(Hc * (fy + 0.05)), int(Wc * (fx + 0.4)), int(Hc * (fy + 0.4))))
    cm, cs = stats(c)
    print('final %s part: mean %.0f std %.0f' % (k, cm, cs))
print('final: %dx%d, mean %.0f std %.0f, %d KB -> %s' % (Wc, Hc, m, sd, os.path.getsize(OUT) // 1024, OUT))
print(line2)
