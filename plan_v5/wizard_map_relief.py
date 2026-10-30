"""wizard_map_relief.py - source data for the tower's CIRCULAR MAP (WT05), made from the planned island.

Reads wizard_map_src.png (written by topview_sketch_v5.py: terrain, water, rivers, roads, bridges) and the planned heights
(terrain_v5.apply_spec). Writes, next to this file:
  wizard_map_relief.obj   a 100 x 100 grid cut to a disc (about 15k triangles), 44 studs across, relief up to 3.4 studs, sea sunk below the land
  wizard_map_color.png    2048 x 2048 colour map (UV 0..1 across the whole square, disc inside it)
  wizard_map_preview.jpg  a picture of the intended map: disc on a dark table with a brass ring
Axes in the OBJ: x east, y north, z up (Blender), units are studs.
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import terrain_v5 as T

HERE = T.HERE
grid = T.load_grid()
spec = T.load_spec(grid)
X, Z = T.grid_xz(grid)
water = (grid['W'] > -900) & (grid['W'] > grid['H'] - 0.5)
Hp = T.apply_spec(grid['H'], X, Z, spec, ~water)

# the square that holds the island: 6600 studs wide, centred on the map's vertical middle
SIDE = 6600.0
CX, CZ = 0.0, (-2900.0 + 2450.0) / 2.0
x_min, z_min = CX - SIDE / 2, CZ - SIDE / 2
N = 100
DIAM = 44.0

# colour map: pad the sketch image to the square and make the sea fill the margin
src = Image.open(HERE + r'\wizard_map_src.png').convert('RGB')
S = 3.0
sq = int(round(SIDE / S))
canvas = Image.new('RGB', (sq, sq), src.getpixel((4, 4)))
off_x = int(round((-3300.0 - x_min) / S))
off_y = int(round((-2900.0 - z_min) / S))
canvas.paste(src, (off_x, off_y))
col = canvas.resize((2048, 2048), getattr(Image, 'Resampling', Image).LANCZOS)
col.save(HERE + r'\wizard_map_color.png')

# relief
us = np.linspace(0, 1, N + 1)
wx = x_min + us * SIDE
wz = z_min + us * SIDE
WX, WZ = np.meshgrid(wx, wz)
h = ndi.map_coordinates(Hp, [(WZ - grid['z0']) / grid['step'], (WX - grid['x0']) / grid['step']], order=1, mode='nearest')
inside_grid = (WX >= X[0, 0]) & (WX <= X[0, -1]) & (WZ >= Z[0, 0]) & (WZ <= Z[-1, 0])
h = np.where(inside_grid, h, -30.0)
land_rel = 0.14 + 3.2 * np.sqrt(np.clip(h, 0, 700) / 700.0)
sea_rel = -0.25 - 0.9 * np.clip(-h / 120.0, 0, 1)
rel = np.where(h > 0, land_rel, sea_rel)
rel = ndi.gaussian_filter(rel, 0.6)
rr = np.hypot(WX - CX, WZ - CZ) / (SIDE / 2)
verts, uvs = [], []
for j in range(N + 1):
    for i in range(N + 1):
        u, v = us[i], us[j]
        verts.append(((u - 0.5) * DIAM, -(v - 0.5) * DIAM, float(rel[j, i])))
        uvs.append((u, 1.0 - v))
faces = []
for j in range(N):
    for i in range(N):
        if rr[j, i] > 1.0 and rr[j + 1, i] > 1.0 and rr[j, i + 1] > 1.0 and rr[j + 1, i + 1] > 1.0:
            continue
        a = j * (N + 1) + i + 1
        b = a + 1
        c = a + (N + 1)
        d_ = c + 1
        faces.append((a, c, b))
        faces.append((b, c, d_))
with open(HERE + r'\wizard_map_relief.obj', 'w') as f:
    f.write('# circular island relief for the wizard tower map table (WT05); studs; x east, y north, z up\n')
    for v in verts:
        f.write('v %.3f %.3f %.3f\n' % v)
    for t in uvs:
        f.write('vt %.5f %.5f\n' % t)
    f.write('o island_relief\n')
    for a, b, c in faces:
        f.write('f %d/%d %d/%d %d/%d\n' % (a, a, b, b, c, c))
print('wizard_map_relief.obj: %d vertices, %d triangles; z range %.2f .. %.2f' % (len(verts), len(faces), rel.min(), rel.max()))

# preview picture of the intended table
P = 1400
prev = Image.new('RGB', (P, P), (28, 30, 38))
pd = ImageDraw.Draw(prev)
pd.ellipse([40, 40, P - 40, P - 40], fill=(86, 80, 90), outline=(200, 164, 84), width=14)
inner = col.resize((P - 220, P - 220), getattr(Image, 'Resampling', Image).LANCZOS)
mask = Image.new('L', inner.size, 0)
ImageDraw.Draw(mask).ellipse([0, 0, inner.size[0] - 1, inner.size[1] - 1], fill=255)
prev.paste(inner, (110, 110), mask)
pd.ellipse([110, 110, P - 110, P - 110], outline=(200, 164, 84), width=10)
pd.ellipse([70, 70, P - 70, P - 70], outline=(150, 120, 60), width=4)
for k in range(72):
    a = math.tau * k / 72
    r0, r1 = (P / 2 - 62), (P / 2 - 48 if k % 6 else P / 2 - 40)
    pd.line([(P / 2 + r0 * math.cos(a), P / 2 + r0 * math.sin(a)), (P / 2 + r1 * math.cos(a), P / 2 + r1 * math.sin(a))], fill=(230, 200, 120), width=3)
pd.text((P / 2 - 8, 52), 'N', fill=(255, 236, 160))
prev.save(HERE + r'\wizard_map_preview.jpg', quality=88)
print('wrote wizard_map_color.png and wizard_map_preview.jpg')
