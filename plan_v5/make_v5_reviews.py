"""make_v5_reviews.py - camera lists, photo runner and review briefs for the first v5 photo rounds (made offline, used after the Studio build).

Writes under town\\shots\\v5\\:
  views_v5_high.csv       high-altitude views (photo mode ON, fog off): the whole island and the Himalayas
  views_v5_tower.csv      wizard tower: orbit, porch, crown, far views, 7 interior views
  views_v5_roads.csv      mountain and lowland roads: along the Roof road, hairpins, tunnels, the rope bridge, Gale Pass, Dragonback road
  views_v5_capital.csv    capital ring wall, gates, skyline, plaza, keep, river bridges
  views_v5_elf.csv        elf valley second ring, canopy villages, waterfall, ground
  views_v5_town1.csv      Town 1 statue, avenue, street life
  views_v5_entrances.csv  an approach view for each settlement entrance (the plain arch is gone)
  photo_round_v5.ps1      runs all lists with photo_run.ps1 into shots\\v5\\<round>\\
  reviews\\BRIEF_v5.md      the brief for the independent photo reviewers
Camera y comes from the PLANNED terrain; the first Studio run clamps each camera to the live ground (the capital-wall frame of round 5 was half under water).
Run: python make_v5_reviews.py
"""
import csv
import json
import math
import os
import sys

import numpy as np
from scipy import ndimage as ndi

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import terrain_v5 as T

OUT = T.TOWN + r'\shots\v5'
os.makedirs(OUT + r'\reviews', exist_ok=True)
grid = T.load_grid()
spec = T.load_spec(grid)
world = T.load_world()
X, Z = T.grid_xz(grid)
WET = (grid['W'] > -900) & (grid['W'] > grid['H'] - 0.5)
HP = T.apply_spec(grid['H'], X, Z, spec, ~WET)
ROADS = json.load(open(T.HERE + r'\roads_v5.json'))
RT = {r['name']: r for r in ROADS['routes']}


def g(x, z):
    return float(ndi.map_coordinates(HP, [[(z - grid['z0']) / grid['step']], [(x - grid['x0']) / grid['step']]], order=1, mode='nearest')[0])


def at(name, t):
    p = [(q[0], q[1]) for q in RT[name]['pts']]
    seg = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(p[:-1], p[1:])]
    d = min(max(t, 0), 1) * sum(seg)
    for k, s in enumerate(seg):
        if d <= s or k == len(seg) - 1:
            u = d / s if s else 0
            a, b = p[k], p[k + 1]
            return a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u
        d -= s


FILES = {}


def view(file, name, pos, look):
    FILES.setdefault(file, []).append((name, '%d,%d,%d' % tuple(round(v) for v in pos), '%d,%d,%d' % tuple(round(v) for v in look)))


def ground_view(file, name, x, z, lx, lz, eye=7.0, look_up=8.0):
    view(file, name, (x, g(x, z) + eye, z), (lx, g(lx, lz) + look_up, lz))


tw = spec['plateau']['tower']
TX, TZ, FY = tw['x'], tw['z'], tw['floor_y']

# ---- high altitude (photo mode on): same cameras as round 5 plus the Himalayas
F = 'views_v5_high.csv'
for n, p, l in (('f_over_south', (0, 1700, 2300), (0, 0, -200)), ('f_over_west', (-4300, 1500, -200), (0, 0, -200)), ('f_over_north', (0, 1500, -4300), (0, 0, -1300)),
                ('f_quad_se', (1500, 2300, 900), (1500, 0, 901)), ('f_quad_nw', (-1500, 2300, -1600), (-1500, 0, -1599)),
                ('f_quad_ne', (1500, 2300, -1600), (1500, 0, -1599)), ('f_quad_sw', (-1500, 2300, 900), (-1500, 0, 901)),
                ('f_himalaya_oblique', (300, 1100, -300), (1500, 250, -1500)), ('f_himalaya_east', (3600, 900, -1000), (1500, 250, -1450)),
                ('f_plateau_down', (TX, 1300, TZ - 60), (TX, 0, TZ - 59)), ('f_skull_down', (2300, 1500, -600), (2300, 0, -599))):
    view(F, n, p, l)

# ---- wizard tower
F = 'views_v5_tower.csv'
for k in range(8):
    a = math.radians(k * 45)
    view(F, 'f_tw_orbit_%d' % k, (TX + 340 * math.sin(a), FY + 70, TZ + 340 * math.cos(a)), (TX, FY + 150, TZ))
ground_view(F, 'f_tw_porch', TX, TZ + 135, TX, TZ + 55, eye=8, look_up=16)
view(F, 'f_tw_crown', (TX + 150, FY + 250, TZ + 140), (TX, FY + 268, TZ))
view(F, 'f_tw_stair', (TX + 30, FY + 20, TZ + 180), (TX, FY + 10, TZ + 60))
view(F, 'f_tw_far_lowpass', (950, g(950, -1019) + 10, -1019), (TX, FY + 150, TZ))
view(F, 'f_tw_far_alpine', (1585, g(1585, -880) + 10, -880), (TX, FY + 150, TZ))
view(F, 'f_tw_far_capital', (440, g(440, -1585) + 40, -1585), (TX, FY + 150, TZ))
view(F, 'f_tw_plateau_wide', (TX - 330, FY + 40, TZ - 200), (TX + 40, FY + 20, TZ - 20))
# interior (eye 7 above the floor; floors at 0, 40, 72, 104, 136, 168, 200, 232 above the terrace)
view(F, 'f_tw_in_maphall_door', (TX, FY + 7, TZ + 44), (TX, FY + 4, TZ))
view(F, 'f_tw_in_map_close', (TX + 24, FY + 9, TZ + 12), (TX, FY + 3, TZ))
view(F, 'f_tw_in_maphall_shelves', (TX - 8, FY + 8, TZ - 4), (TX + 40, FY + 14, TZ + 6))
view(F, 'f_tw_in_library_gallery', (TX - 10, FY + 47, TZ + 8), (TX + 39, FY + 54, TZ + 6))
view(F, 'f_tw_in_atrium_down', (TX + 18, FY + 110, TZ), (TX, FY + 4, TZ))
view(F, 'f_tw_in_lab', (TX - 4, FY + 143, TZ + 4), (TX + 17, FY + 142, TZ + 17))
view(F, 'f_tw_in_study', (TX, FY + 175, TZ - 6), (TX, FY + 172, TZ + 20))
view(F, 'f_tw_in_observatory', (TX - 14, FY + 240, TZ + 6), (TX, FY + 244, TZ))

# ---- roads
F = 'views_v5_roads.csv'
for k, t in enumerate((0.04, 0.2, 0.36, 0.52, 0.68, 0.84)):
    x, z = at('Roof road', t)
    lx, lz = at('Roof road', min(t + 0.1, 1))
    view(F, 'f_roof_%d' % k, (x, g(x, z) + 8, z), (lx, g(lx, lz) + 6, lz))
for k, (x, z) in enumerate(RT['Roof road']['hairpin_pts'][:3]):
    view(F, 'f_roof_hairpin_%d' % k, (x + 60, g(x, z) + 40, z + 60), (x, g(x, z), z))
for k, tn in enumerate(ROADS['tunnels']):
    dx, dz = tn['x1'] - tn['x0'], tn['z1'] - tn['z0']
    L = math.hypot(dx, dz) or 1
    px_, pz_ = tn['x0'] - dx / L * 70, tn['z0'] - dz / L * 70
    view(F, 'f_tunnel_%d' % k, (px_, g(px_, pz_) + 8, pz_), (tn['x0'], g(tn['x0'], tn['z0']) + 8, tn['z0']))
for b in ROADS['bridges']:
    if b['kind'] in ('rope_suspension', 'timber_cantilever'):
        h = math.radians(b['heading'])
        for nm, off, up in (('end', -b['span'] * 0.9, 8), ('side', 0, 20), ('aerial', 0, 140)):
            if nm == 'side':
                px_, pz_ = b['x'] + 120 * math.sin(h), b['z'] - 120 * math.cos(h)
            elif nm == 'aerial':
                px_, pz_ = b['x'] + 60 * math.sin(h), b['z'] - 60 * math.cos(h)
            else:
                px_, pz_ = b['x'] + off * math.cos(h), b['z'] + off * math.sin(h)
            view(F, 'f_bridge_%s_%d_%s' % (b['kind'][:4], abs(b['x']) % 1000, nm), (px_, g(px_, pz_) + up, pz_), (b['x'], g(b['x'], b['z']) + 6, b['z']))
for nm_, tag, n in (('Gale Pass road', 'gale', 4), ('Dragonback road (lower)', 'dragon_low', 3), ('Dragonback road (terraces)', 'dragon_ter', 2), ('Highland descent', 'descent', 3), ('Ash road', 'ash', 2), ('East road', 'east', 3)):
    for k in range(n):
        t = 0.1 + 0.8 * k / max(n - 1, 1) if n > 1 else 0.5
        x, z = at(nm_, t)
        lx, lz = at(nm_, min(t + 0.1, 1))
        view(F, 'f_%s_%d' % (tag, k), (x, g(x, z) + 8, z), (lx, g(lx, lz) + 6, lz))

# ---- capital
F = 'views_v5_capital.csv'
CX, CZ = 0, -1585
for k in range(8):
    a = math.radians(k * 45)
    x, z = CX + 760 * math.sin(a), CZ + 560 * math.cos(a)
    view(F, 'f_cap_orbit_%d' % k, (x, g(x, z) + 110, z), (CX, g(CX, CZ) + 30, CZ))
ground_view(F, 'f_cap_gate_south', 0, -1040, 0, -1240, eye=10, look_up=20)
ground_view(F, 'f_cap_skyline', 0, -820, 0, -1700, eye=20, look_up=70)
ground_view(F, 'f_cap_plaza', -70, -1470, 0, -1560, eye=8, look_up=12)
ground_view(F, 'f_cap_keep', 0, -2000, 0, -2275, eye=8, look_up=40)
ground_view(F, 'f_cap_river_bridge', -300, -1000, -306, -1080, eye=10, look_up=8)
ground_view(F, 'f_cap_water_gate', -420, -1230, -330, -1327, eye=10, look_up=10)
ground_view(F, 'f_cap_wall_west', -640, -1500, -490, -1585, eye=12, look_up=24)
view(F, 'f_cap_down', (0, 1500, -1545), (0, 0, -1544))

# ---- elf valley
F = 'views_v5_elf.csv'
tx, tz = -1560, -430
for k in range(8):
    a = math.radians(k * 45 + 10)
    x, z = tx + 330 * math.cos(a), tz + 330 * math.sin(a)
    view(F, 'f_elf_ring_%d' % k, (x, g(x, z) + 12, z), (tx + 270 * math.cos(a), g(tx, tz) + 14, tz + 270 * math.sin(a)))
for k, (a, yo) in enumerate(((20, 100), (140, 120), (260, 140))):
    x, z = tx + 78 * math.cos(math.radians(a)), tz + 78 * math.sin(math.radians(a))
    view(F, 'f_elf_canopy_%d' % k, (x + 70, g(x, z) + yo + 30, z + 70), (x, g(x, z) + yo + 8, z))
view(F, 'f_elf_waterfall', (-1730, 60, -640), (-1730, 50, -745))
view(F, 'f_elf_waterfall_wide', (-1640, 80, -600), (-1740, 60, -740))
view(F, 'f_elf_city', (-1380, 60, -560), (-1560, 25, -440))
ground_view(F, 'f_elf_tree_base', -1500, -380, -1560, -430, eye=7, look_up=40)
ground_view(F, 'f_elf_path_east', -1290, -392, -1380, -410, eye=7, look_up=8)
view(F, 'f_elf_down', (tx, 1100, tz + 40), (tx, 0, tz + 41))

# ---- Town 1
F = 'views_v5_town1.csv'
ground_view(F, 'f_t1_statue', 0, 70, 0, 0, eye=8, look_up=18)
ground_view(F, 'f_t1_avenue_south', 0, -380, 0, -90, eye=8, look_up=10)
ground_view(F, 'f_t1_avenue_north', 0, -60, 0, -380, eye=8, look_up=12)
ground_view(F, 'f_t1_plaza_ring', 90, 90, -40, -30, eye=8, look_up=8)
ground_view(F, 'f_t1_street_life', -110, 40, -60, -40, eye=7, look_up=6)
ground_view(F, 'f_t1_skull_hq', 0, -230, 0, -402, eye=10, look_up=60)
view(F, 'f_t1_down', (0, 1200, -120), (0, 0, -119))

# ---- entrances: an approach view for each settlement (camera stands 130 studs out along the approach, looking at the sign)
F = 'views_v5_entrances.csv'
for nm_, (x, z, rot) in (('town1', (18, -530, 180)), ('elf', (-1290, -392, 90)), ('alpine', (1470, -902, 270)), ('rusty', (1160, 1010, 225)), ('harbour', (-385, 1400, 180)), ('desert', (1640, 1100, 270))):
    a = math.radians(rot)
    px_, pz_ = x + 130 * math.sin(a), z + 130 * math.cos(a)
    view(F, 'f_entry_%s' % nm_, (px_, g(px_, pz_) + 8, pz_), (x, g(x, z) + 9, z))
    qx, qz = x - 40 * math.sin(a), z - 40 * math.cos(a)
    view(F, 'f_entry_%s_inside' % nm_, (qx, g(qx, qz) + 8, qz), (x + 60 * math.sin(a), g(x, z) + 8, z + 60 * math.cos(a)))

total = 0
for fn, vs in FILES.items():
    with open(OUT + '\\' + fn, 'w', newline='') as f:
        w = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        w.writerow(['name', 'pos', 'look'])
        for v in vs:
            w.writerow(v)
    total += len(vs)

PS = r"""param([string]$round = 'r1', [string[]]$only = @())
# v5 photo round: high views with photo mode ON (fog off), everything else with the game atmosphere. Output shots\v5\<round>\*.jpg and log.txt
$town = 'C:\Users\Nitro\.kiro\crew\workspace\town'
$out = "$town\shots\v5\$round"
$log = "$out\log.txt"
New-Item -ItemType Directory -Force -Path $out | Out-Null
function Log($s) { ('{0} {1}' -f (Get-Date -Format 'HH:mm:ss'), $s) | Out-File $log -Append -Encoding utf8 }
$lists = @(@('views_v5_high.csv', 'on'), @('views_v5_tower.csv', 'off'), @('views_v5_roads.csv', 'off'), @('views_v5_capital.csv', 'off'), @('views_v5_elf.csv', 'off'), @('views_v5_town1.csv', 'off'), @('views_v5_entrances.csv', 'off'))
foreach ($l in $lists) {
  if ($only.Count -gt 0 -and $only -notcontains $l[0]) { continue }
  Log ('start ' + $l[0])
  & powershell -NoProfile -ExecutionPolicy Bypass -File "$town\photo_run.ps1" -mode $l[1] -csv "$town\shots\v5\$($l[0])" -dir $out | ForEach-Object { Log $_ }
}
Log 'ROUND END'
"""
open(OUT + r'\photo_round_v5.ps1', 'w').write(PS)

BRIEF = """# V5 photo review brief (first round after the v5 build)

You judge photos only. The pictures are in `C:\\Users\\Nitro\\.kiro\\crew\\workspace\\town\\shots\\v5\\<round>\\` (names `f_*`). `f_over_*`, `f_quad_*`, `f_himalaya_*`, `f_plateau_down`, `f_skull_down` were taken from high altitude with fog OFF; all other `f_*` with game fog. Ignore the small 'Back' view-cube widget (Studio overlay). Read at most 4 images per read call. Camera lists are the CSV files next to the pictures.

References (look at these first): `town\\reference\\world_concept_topdown.png` (the target composition of the whole island), `town\\reference\\castle_town_reference.png` (the target look of the capital), `town\\plan_v5\\topview_sketch_v5.jpg` (the intended top view, a rough drawing), `town\\plan_v5\\WIZARD_TOWER_BRIEF.md`.

## What to judge, area by area (score each 1-10, then SHIP / NOT YET)
1. **Whole island from above** (`f_over_*`, `f_quad_*`): does it read like the concept map? Ragged coast, colour zones, white NE massif with a pale plateau, dark forest NW, orange desert SE, dark east coast with the Skull cliff, river loops round the capital, winding roads with bridges. Is the middle still a green carpet?
2. **Himalayas and the wizard tower** (`f_himalaya_*`, `f_plateau_down`, `f_tw_*`): peaks and plateau shape, the tower as a landmark from far (`f_tw_far_*`), tower exterior (orbit, porch, crown), then interior: Map Hall with the circular map, curved bookshelves, library galleries, lab, study, observatory. Walkable? Awesome? Anything glowing or floating?
3. **Roads through the mountains** (`f_roof_*`, `f_gale_*`, `f_dragon_*`, `f_descent_*`, `f_tunnel_*`, `f_bridge_*`): do roads climb in believable hairpins, cut through ridges at tunnels, hug cliffs, cross rivers at proper bridges? Do the rope bridge and tunnel mouths look Himalayan and fit the rock? Any road that ends in nothing, floats or is buried?
4. **Capital** (`f_cap_*`): polygon ring wall with cone-roofed towers, red-brown wall-walk, gatehouse in the wall, one orange roof family, skyline towers, plaza and order hall, keep on its terrace, river loop and bridges. Compare with the castle-town reference.
5. **Elf valley** (`f_elf_*`): second house ring, canopy villages with ladders, waterfall width and mist, ground dapple, still NO glow of any kind.
6. **Town 1** (`f_t1_*`): statue with a face, avenue, street life, no gate, ground ring round the houses.
7. **Entrances** (`f_entry_*`): the plain arch must be gone. Does each settlement feel naturally entered (bend, framing trees or boulders, one sign)? Anything that still looks like a plain arch?
8. **Defects** to list: floating pieces, buried pieces, pieces in water, z-fighting, stretched textures, hard blue cut-out water, flat green carpet areas, repeated identical models in a row.

## Deliverables
Report in the same format as the round-5 reports: scores per area, `ROUND V5 SCORES:` line, a verdict `SHIP` or `NOT YET` for the whole map, and the five cheapest changes (30 minutes) that would raise the weakest scores. Give coordinates for every defect (the photo name tells the camera).
"""
open(OUT + r'\reviews\BRIEF_v5.md', 'w', encoding='utf-8').write(BRIEF)
print('camera lists written: %d views in %d files' % (total, len(FILES)))
for fn, vs in FILES.items():
    print('  %-24s %3d' % (fn, len(vs)))
