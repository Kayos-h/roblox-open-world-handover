"""make_v5_briefs.py - Blender style guide, per-row briefs, worker plan, worker prompts and the module template for the v5 models.

Reads V5_MANIFEST.csv (the single source of truth). Writes:
  library\\V5_STYLE_GUIDE.md                 shared rules for every v5 model (also copied to plan_v5)
  plan_v5\\V5_BRIEFS.md                      one brief per manifest row, P1 first in build order
  plan_v5\\v5_worker_plan.json / .md         workers, batches, categories, estimated hours, run commands
  plan_v5\\worker_prompts\\<worker>.md        the task text for each Blender worker (use with spawn_run when Blender is allowed)
  plan_v5\\MODEL_REVIEW_BRIEF.md             rubric for the independent model reviewers
  library\\src\\v5_template.py                module template that follows the v4worker contract
Run: python make_v5_briefs.py
"""
import collections
import csv
import json
import math
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = r'C:\Users\Nitro\.kiro\crew\workspace\town\library'
rows = list(csv.DictReader(open(HERE + r'\V5_MANIFEST.csv', encoding='utf-8-sig')))
G = collections.OrderedDict()
for r in rows:
    G.setdefault(r['row'], []).append(r)

PALETTES = {
    'capital': 'plaster (232,214,188), timber (112,80,60), roofs orange-red (198,88,52) (214,104,58) (178,72,46) with (140,62,48) accents, stone grey-lilac (150,142,158), cone roofs maroon (120,44,52), wall-walk deck (150,88,70), parapet cap (232,226,230)',
    'wizard': 'granite (176,172,180), limestone band (226,214,190), whitewash (238,234,226), ochre trim (196,150,76), red-brown timber (112,60,48), indigo slate roof (52,60,96), copper-green (92,150,128), brass (200,164,84), parchment (226,208,170), book spines in 12 muted colours',
    'himalaya': 'weathered grey stone (128,124,120), dark slate (84,86,96), snow (240,244,250), ice (196,226,242), weathered timber (112,92,70), rope (176,150,104), cloth flags in this order: blue (60,120,200), white (250,250,250), red (200,60,50), green (60,160,90), yellow (240,200,60)',
    'elf': 'living wood (140,104,70), pale bark (176,150,112), moss (86,130,70), leaf greens (70,120,60) (104,150,80), warm stone (150,140,120), shingle teal-green (80,120,100); lantern light only, no glow',
    'forest': 'bark (96,74,56), moss (86,130,70), fern green (70,120,60), ancient stone (130,126,118), root brown (110,80,58)',
    'desert': 'sandstone (214,150,90), red mesa (172,92,56), pale sand (226,200,150), adobe (200,150,106), clay (176,112,76), bleached bone (224,216,196), dark timber (92,70,52)',
    'skull': 'basalt (54,50,58), ash grey (96,92,100), cracked-lava rock (70,56,60), bone (224,216,196), rust iron (122,62,36); no glow (lava veins are terrain paint)',
    'coast': 'sea rock (110,108,110), wet stone (84,88,92), barnacle white (210,206,196), harbour white (238,238,240), harbour blue (92,128,176), brick red (190,90,70)',
    'roads': 'weathered timber (112,92,70), canvas (214,200,170), stone (140,134,126), rust (122,62,36), tar black (40,38,37), faded banner red (170,70,60)',
    'plains': 'whitewash (236,226,206), terracotta roof (206,120,84), thatch (190,160,100), timber (112,80,60), field stone (150,142,128), hay (214,190,110)',
    'town1': 'dark stone (78,76,86), warm brick (126,112,98), iron (40,38,37), banner crimson (150,40,48), bone (224,216,196)',
    'entrance': 'carve each sign in the palette of its settlement: Town 1 dark stone and iron; elf living wood; alpine log and snow; rusty salvage plate on sandstone; harbour whitewashed board with rope; desert painted clay on timber',
    'arcane': 'floating rock (118,116,122), moss, pale runes carved (no glow), ancient stone (130,126,118)',
    'trees': 'poplar and beech leaf greens (90,140,70) (120,160,80); old oak dark (52,92,50) with bark (80,62,48); blossom white (244,232,236) and pink (232,176,196); birch bark (232,228,220)',
}

CAT = {}
for c in ('WT',):
    CAT[c] = 'v5_wizard'
for c in ('HM', 'HL', 'SP'):
    CAT[c] = 'v5_himalaya'
for c in ('CP',):
    CAT[c] = 'v5_capital'
for c in ('EV', 'RW'):
    CAT[c] = 'v5_elf'
for c in ('TW',):
    CAT[c] = 'v5_town1'
for c in ('NE',):
    CAT[c] = 'v5_entrances'
for c in ('LM',):
    CAT[c] = 'v5_landmarks'
for c in ('CO', 'HB', 'FL'):
    CAT[c] = 'v5_coast'
for c in ('RD', 'BR', 'RV'):
    CAT[c] = 'v5_roads'
for c in ('FR', 'VG'):
    CAT[c] = 'v5_forest'
for c in ('PL', 'VL'):
    CAT[c] = 'v5_plains'
for c in ('DS', 'SD'):
    CAT[c] = 'v5_desert'
for c in ('VC',):
    CAT[c] = 'v5_skull'


def palette_for(code):
    p = code[:2]
    n = int(''.join(ch for ch in code if ch.isdigit()) or 0)
    if p == 'LM':
        if n in (1, 2, 22, 23, 24):
            return 'forest'
        if n in range(3, 9):
            return 'himalaya'
        if n in range(9, 18):
            return 'desert'
        if n in (18, 19, 20, 21):
            return 'arcane'
        return 'plains'
    return {'CP': 'capital', 'WT': 'wizard', 'HM': 'himalaya', 'HL': 'himalaya', 'SP': 'himalaya', 'EV': 'elf', 'RW': 'elf', 'FR': 'forest', 'DS': 'desert', 'SD': 'desert',
            'VC': 'skull', 'CO': 'coast', 'HB': 'coast', 'FL': 'arcane', 'RD': 'roads', 'BR': 'roads', 'RV': 'roads', 'PL': 'plains', 'VL': 'plains', 'TW': 'town1', 'NE': 'entrance', 'VG': 'trees'}[p]


LONG_X = {'HM01', 'HM02', 'HM05', 'HM06', 'BR01', 'CP19', 'CP01', 'CP12', 'CP18', 'LM08', 'LM04', 'LM26', 'LM27', 'VG07', 'DS06', 'HM07', 'LM10'}
TUNNEL = {'HM03', 'HM04'}
INTERIOR = {'WT02', 'WT03', 'WT04', 'WT05', 'WT06', 'WT07', 'WT08', 'WT09', 'WT10'}


def orientation(code):
    if code in LONG_X:
        return 'Long axis along X (like the library bridges). Pivot = centre of the footprint, bottom at z=0. Add markers `end_a`, `end_b` and `deck` (deck centreline height) with v4util.marker where the row is a bridge or walkway.'
    if code in TUNNEL:
        return 'The passage runs along Y; the opening faces -Y (front). Clear passage 14 wide x 16 high. Pivot = centre of the opening at ground.'
    if code in INTERIOR:
        return 'Interior prop: front faces -Y, pivot = centre of the footprint at the floor (z=0). Placed with Studio y_offset = floor height. Keep the back flat so it can sit against a curved wall.'
    if code.startswith('WT') or code in ('CP07', 'CP09', 'CP15'):
        return 'Building: entrance side faces -Y, pivot = centre of the footprint at ground (z=0). Enterable where the row says so: walls at least 4 studs thick, door openings 8 x 12, nothing narrower than 7 studs on a walking route.'
    return 'Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.'


EXTRA = {
    'CP01': '8-stud wide wall-walk with a red-brown deck, white-capped inner parapet, crenellated outer edge. Variants: a) plain, b) arrow slits, c) buttressed. 40 studs long, ends square so segments butt against towers and corners.',
    'CP02': 'Polygon joints at 135, 90 and 150 degrees with a round tower seat (socket radius 11). Wall-walk continues through the corner.',
    'CP03': 'Stone stair from ground up to the wall-walk (height 20) with a railing, built against the inner face; ends flush with a wall segment.',
    'CP04': 'Round towers 16, 22, 28 and 34 studs wide: slit windows, a string course, maroon cone roof (120,44,52) with a small finial. Open bottom, no floor.',
    'CP06': 'Twin towers that flank the main gatehouse: machicolated top, banner mounts, slit windows, cone roof.',
    'CP07': 'Gatehouse built into the ring wall: passage 18 wide x 22 high, raised portcullis as a separate mesh, two machicolated bays, banner mounts, crenellated top, walkable passage with a clear collision gap. Replaces the old C04/K08/B02_07 gates.',
    'CP08': 'River gate where the capital river passes under the wall: water passage 20 wide, iron grille as a separate mesh, quay steps either side.',
    'CP09': 'Keep on the castle terrace: stepped massing with a central tower, four corner and four mid turrets with cone roofs, buttresses, arched windows, balconies, portcullis gate at the base. Must NOT look like the old B02_01 keep.',
    'CP10': 'Wings that flank the keep, same family and palette as the keep, lower roofline, covered walkway to the keep.',
    'CP12': 'Retaining wall for the castle terrace: buttressed stone, 40 studs long, parapet on top, drain spouts.',
    'CP13': 'Grand stair with landings and a balustrade, rise at most 1.2, run at least 2.2, 30 studs wide.',
    'CP14': 'Five different skyline towers, each a clear silhouette from 800 studs: clock tower (faces on four sides), bell tower (open belfry), observatory (dome with slit), beacon tower (open brazier cage, no glow), water tower (tank on stone legs). 110 tall.',
    'CP15': 'Order headquarters: wide hall with two wings and a banner tower, own name, own heraldry, no Black Clover shapes. Three variants: main hall and two annexes that sit beside it.',
    'CP19': 'Towered stone bridge for the capital river: two gate towers, cobbled deck 14 wide, parapets, long axis X.',
    'EV01': 'Eight house types: tall tower house, bridge house, library, healer hut, archery lodge, bathhouse, council hall, weavers hall. Wood and stone, warm lantern hooks, NO glow, ladder or stairs to the ground on anything raised.',
    'EV02': 'Canopy clusters 90-140 studs up: 3-4 platforms, rope bridges, small huts, ladders to the ground (markers ladder_bottom / ladder_top). Natural, no glow.',
    'EV03': 'Root stairs, carved steps, stone-and-root bridge, garden arch, path posts, plaza paving ring: small pieces that stitch the valley together.',
    'RW02': 'REWORK of D05_02 world tree roots: 8-10 rounded buttress roots, soft taper, bright bark tinted like the trunk, moss patches. Keep the old footprint so the export replaces the old mesh in place.',
    'NE01': 'One carved sign per settlement (post or stone), 10 x 18 x 4. Town 1: stone slab with a carved jaw motif and iron bracket. Elf: living-wood board on a root post. Alpine: log post with a snow cap and a small bell. Rusty: salvage plate on sandstone. Harbour: whitewashed board with an anchor and rope. Desert village: painted clay slab on a beam. No arch, no gate.',
    'NE02': 'Boulder pairs that frame a road: mossy, frosted, sandstone, basalt. 30 wide so the road passes between them.',
    'HM01': 'Himalayan rope-and-plank suspension bridges in three spans (60, 90, 116 studs): stone anchor towers at both ends, plank deck 7 wide, two hand ropes, prayer flags on the ropes. The 116 crosses Frost Gorge.',
    'HM03': 'Rock-cut road tunnel mouths: plain, snow-capped, timber-framed. A rectangular timber frame set in a 40-stud-wide rock face that blends into terrain. Not a freestanding arch.',
    'HM04': 'Tunnel lining segments, 24 studs: straight and a 30-degree bend. Rock walls, timber ribs every 8 studs, lantern brackets (warm, unlit).',
    'LM03': 'Frosthold fortress built into a snowy mountain flank (own name and design): terraced ramparts, cliff towers, gate tunnel, no copied shapes.',
    'LM09': 'Buried temple, half under sand: stepped entrance down, colonnade, guardian statues nearby. Sandstone, no glow.',
    'LM15': 'Ring temple: a great stone ring with an inner sanctum, 220 across, worn by wind.',
    'LM18': 'Crater monolith ring: 12 tall carved stones around a bowl, pale runes carved not glowing.',
    'LM22': 'Colossal waterfall cliff for the elf valley west rim, 240 wide: three tiers with ledges and pools; the water is added in Studio.',
    'LM25': 'Gate of the ancient civilization, half collapsed: massive pillars and a broken lintel.',
    'LM30': 'Ruined castle with a broken keep, 140 wide, open to the sky.',
    'VC02': 'Giant skull carved into a dark cliff, the Skull City landmark (own design, not a copy of any film skull): hollow eye caves, jaw as a gate, 200 wide. Two sites: the main cliff and a smaller one on the east coast.',
    'CO01': 'Coastal cliff pieces to replace the archived grey box cliffs: layered rock, ledges, sea-cut notches, 110 wide.',
    'CO02': 'Sea stacks, three silhouettes, 90 tall.',
    'VG01': 'Poplar and beech, narrow crown, 3 silhouettes.',
    'VG02': 'Dark old oaks with a broken crown, 2 silhouettes.',
    'VG03': 'Flowering trees, 2 species (white blossom, pink blossom).',
}
for c in ('WT01', 'WT02', 'WT03', 'WT04', 'WT05', 'WT06', 'WT07', 'WT08', 'WT09', 'WT10', 'WT11', 'WT12', 'WT13'):
    EXTRA[c] = 'READ plan_v5/WIZARD_TOWER_BRIEF.md first and follow it exactly (sections 2 and 3 for this row). ' + EXTRA.get(c, '')
EXTRA['WT05'] += ' Source data is ready: plan_v5/wizard_map_relief.obj (about 16k triangles, 44 studs across) and plan_v5/wizard_map_color.png; import them, then build the table, brass rings and landmark tokens around them.'
EXTRA['WT02'] += ' Export tower_collision.json (boxes in tower-local coordinates) next to the model.'

# worker plan: (worker, title, [(batch, category, [row codes])])
W = [
    ('va', 'Wizard tower exterior (do first, most review rounds)', [('tower_shell', 'v5_wizard', ['WT01']), ('tower_porch', 'v5_wizard', ['WT12', 'WT11']), ('tower_terrace', 'v5_wizard', ['WT13'])]),
    ('vb', 'Wizard tower interior and the circular map', [('interior_shell', 'v5_wizard', ['WT02']), ('map_table', 'v5_wizard', ['WT05', 'WT06']), ('shelves', 'v5_wizard', ['WT03', 'WT04']), ('furniture', 'v5_wizard', ['WT07', 'WT08', 'WT09', 'WT10'])]),
    ('vc', 'Himalayan road kit and natural entrances', [('bridges', 'v5_himalaya', ['HM01']), ('tunnels', 'v5_himalaya', ['HM03', 'HM04']), ('signs', 'v5_entrances', ['NE01']), ('road_extras', 'v5_himalaya', ['HM02', 'HM05', 'HM06', 'HM07', 'HM08', 'HM09']), ('boulders', 'v5_entrances', ['NE02'])]),
    ('vd', 'Capital', [('walls_towers', 'v5_capital', ['CP01', 'CP02', 'CP03', 'CP04', 'CP05', 'CP06']), ('gates_keep', 'v5_capital', ['CP07', 'CP08', 'CP09', 'CP10']), ('terrace_skyline', 'v5_capital', ['CP12', 'CP13', 'CP14', 'CP15', 'CP19']), ('town_extras', 'v5_capital', ['CP11', 'CP16', 'CP17', 'CP18'])]),
    ('ve', 'Elf valley and Town 1', [('elf_houses', 'v5_elf', ['EV01']), ('canopy_roots', 'v5_elf', ['EV02', 'RW02']), ('elf_paths', 'v5_elf', ['EV03', 'LM01', 'LM02']), ('town1', 'v5_town1', ['TW01', 'TW02', 'TW03'])]),
    ('vf', 'Landmark heroes, trees and coast', [('heroes_a', 'v5_landmarks', ['LM03', 'LM22', 'LM25', 'LM30']), ('heroes_b', 'v5_landmarks', ['LM09', 'LM15', 'LM18']), ('skull', 'v5_skull', ['VC02']), ('trees', 'v5_forest', ['VG01', 'VG02', 'VG03']), ('coast', 'v5_coast', ['CO01', 'CO02'])]),
    ('vg', 'Highlands, forest and marsh extras', [('highland_set', 'v5_himalaya', ['HL01', 'HL02', 'HL03', 'HL04', 'HL05', 'HL06', 'HL07', 'SP01']), ('fortress_parts', 'v5_landmarks', ['LM04', 'LM05', 'LM06', 'LM07', 'LM08']), ('forest_set', 'v5_forest', ['FR01', 'FR02', 'FR03', 'VG04', 'LM23', 'LM24']), ('marsh_set', 'v5_forest', ['VG05', 'VG06', 'VG07'])]),
    ('vh', 'Desert and Skull City', [('desert_village', 'v5_desert', ['DS01', 'DS02', 'DS03', 'DS04', 'DS05']), ('desert_land', 'v5_desert', ['DS06', 'DS07', 'DS08', 'SD01', 'SD02']), ('temple_parts', 'v5_landmarks', ['LM10', 'LM11', 'LM12', 'LM13', 'LM14', 'LM16', 'LM17']), ('skull_set', 'v5_skull', ['VC01', 'VC03', 'VC04'])]),
    ('vi', 'Plains, ruins, coast extras, roads and sky', [('plains_set', 'v5_plains', ['PL01', 'PL02', 'PL03', 'PL04', 'PL05', 'PL06', 'VL01']), ('ruins_crater', 'v5_landmarks', ['LM19', 'LM20', 'LM21', 'LM26', 'LM27', 'LM28', 'LM29', 'LM31']), ('coast_set', 'v5_coast', ['CO03', 'CO04', 'CO05', 'HB01']), ('road_life', 'v5_roads', ['RD01', 'RD02', 'RD03', 'RD04', 'RD05', 'RD06', 'BR01', 'RV01']), ('sky', 'v5_coast', ['FL01', 'FL02'])]),
]


def minutes(code):
    r = G[code][0]
    return 2.0 + 0.17 * float(r['tri_budget']) / 1000.0


plan = []
assigned = set()
for w, title, batches in W:
    wb = []
    tot = 0.0
    for bname, cat, codes in batches:
        ids = []
        mins = 0.0
        for c in codes:
            assigned.add(c)
            for r in G[c]:
                ids.append(r['id'])
                mins += minutes(c)
        tot += mins
        wb.append({'batch': bname, 'category': cat, 'rows': codes, 'ids': ids, 'models': len(ids), 'est_minutes': round(mins)})
    plan.append({'worker': w, 'title': title, 'module': 'v5_%s' % w, 'models': sum(b['models'] for b in wb), 'est_hours': round(tot / 60.0, 1), 'batches': wb})
missing = [c for c in G if c not in assigned and not c.startswith('RW01')]
total_h = sum(p['est_hours'] for p in plan)
json.dump({'workers': plan, 'unassigned_rows': missing, 'note': 'est_hours is worker-hours of building and fixing; two Blender processes run at once (v4run.ps1 slots), reviews and fix rounds add about 40 percent'}, open(HERE + r'\v5_worker_plan.json', 'w'), indent=1)

md = ['# V5 worker plan', '', 'Nine worker queues. Blender is parked; nothing here has run. When it is allowed: `v4run.ps1 -Module <module> -Worker <worker> -Batch <batch>` per batch (two Blender processes at a time), then `python v4_merge.py`, then `upload_v5.ps1`.', '',
      '| Worker | Module (create in library/src) | Models | Est. worker-hours | Content |', '|---|---|---|---|---|']
for p in plan:
    md.append('| %s | %s.py | %d | %.1f | %s |' % (p['worker'], p['module'], p['models'], p['est_hours'], p['title']))
md += ['', 'Total models in the queues: %d; worker-hours %.1f (about %.1f hours of wall time with 3 active workers plus 40%% for reviews and fixes). Rows not in any queue: %s.' % (sum(p['models'] for p in plan), total_h, total_h * 1.4 / 3, ', '.join(missing) or 'none (RW01 reworks are done by hand on the old models)'), '']
for p in plan:
    md += ['## %s: %s' % (p['worker'], p['title']), '', '| Batch | Category folder | Rows | Models | Est. minutes |', '|---|---|---|---|---|']
    for b in p['batches']:
        md.append('| %s | %s | %s | %d | %d |' % (b['batch'], b['category'], ', '.join(b['rows']), b['models'], b['est_minutes']))
    md += ['', '```', ] + ['powershell -File library\\src\\v4run.ps1 -Module %s -Worker %s -Batch %s' % (p['module'], p['worker'], b['batch']) for b in p['batches']] + ['```', '']
open(HERE + r'\v5_worker_plan.md', 'w').write('\n'.join(md) + '\n')

# per-row briefs, P1 first, in worker order
order = []
for p in plan:
    for b in p['batches']:
        for c in b['rows']:
            order.append((c, p['worker'], b['batch'], b['category']))
pos_ = {t[0]: i for i, t in enumerate(order)}
order.sort(key=lambda t: (G[t[0]][0]['priority'], pos_[t[0]]))
out = ['# V5 briefs: one entry per manifest row (P1 first)', '',
       'Read `library/V5_STYLE_GUIDE.md` first. Every model: original design, no emissive or glowing parts, 1 Blender unit = 1 stud, each MeshPart at most 20k triangles, size within +-10% of the manifest, ids exactly as listed. Rows marked REWORK change an existing model.', '']
for c, w, batch, cat in order:
    rs = G[c]
    r = rs[0]
    base = r['id']
    size = '%s x %s x %s' % (r['size_x'], r['size_y'], r['size_z'])
    out += ['### %s ×%d · %s · %s · %s · up to %s triangles each' % (c, len(rs), r['priority'], r['region'], size, format(int(float(r['tri_budget'])), ',')), '',
            '- Ids: ' + ', '.join(x['id'] for x in rs),
            '- What: ' + (r['note'] or 'see the Bible'),
            '- Extra: ' + EXTRA.get(c, 'none beyond the style guide'),
            '- Palette (%s): %s' % (palette_for(c), PALETTES[palette_for(c)]),
            '- Orientation: ' + orientation(c),
            '- Queue: worker %s, batch %s, folder %s' % (w, batch, cat), '']
open(HERE + r'\V5_BRIEFS.md', 'w', encoding='utf-8').write('\n'.join(out) + '\n')

STYLE = """# V5 Blender style guide (all new models)

Written 30 Oct 2026. Applies to every row in `plan_v5/V5_MANIFEST.md`. Plan and reasons: `plan_v5/WORLD_BIBLE_v5.md`. Per-row text: `plan_v5/V5_BRIEFS.md`.

## 1. Hard rules
- **Original designs only.** No Black Clover names, emblems, title art or recognisable character shapes. No marketplace models.
- **No glow.** Every palette key has emission 0. Warm light comes from Roblox lights placed in Studio. Lava veins and runes are terrain paint or carved relief.
- **Units and axes:** 1 Blender unit = 1 stud. Z is up. The front (the side you walk up to) faces -Y. Pivot is the centre of the footprint at z = 0. Long-axis models (bridges, walls) run along X.
- **Size:** within +-10% of the manifest size. **Triangles:** each MeshPart at most 20k, the whole model at most the manifest budget (the wizard tower rows are the only ones allowed above 60k).
- **Watertight and clean:** no floating pieces, no flipped normals, no hidden interior junk, no pieces thinner than 0.3 studs. Walls of enterable buildings at least 4 studs thick. Doors, portcullises, banners and gates that should move are separate meshes with their pivot at the hinge.
- **Materials:** at most 8 palette keys per model. Keys are `<worker>_<name>` (for example `vd_roof_orange`) registered as `PAL['vd_name'] = ((r,g,b), 'RobloxMaterial', metallic, roughness, 0)`. Roblox materials to prefer: Cobblestone, Slate, Limestone, Brick, WoodPlanks, Wood, Fabric, Metal, CorrodedMetal, Sand, Snow, Ice, Grass, Ground.
- **Colour per place:** use the palette in the row brief. One dominant roof family per settlement. Vary value, not hue, inside a family.

## 2. What makes a model look good in this game
- **Silhouette first.** It must read at 500 studs on a 256 px render. Break straight edges: roof overhangs, buttresses, chimneys, finials, uneven heights.
- **Three scales of detail:** big forms (the massing), medium (windows, beams, stairs, balconies), small (trim, nails, hanging lamps). Skip the medium level and it looks like a box.
- **Believable structure:** things carry loads; stairs go somewhere; every raised floor has a way up (stairs or ladder with `ladder_bottom` / `ladder_top` markers).
- **Weathering by shape and colour,** not noise: stains by value, moss on the north side, chipped corners, uneven stone courses.
- **Natural places stay natural:** forest and elf pieces are wood, stone and moss with curved forms; no neon, no metal pipes.
- **No arches at entrances.** The plain arch is gone; entrances are roads, trees, boulders and a sign. Real gatehouses in walls (capital, fortress) are fine.

## 3. Interiors (wizard tower and any enterable building)
- Clear height 28 per floor in the tower (10 minimum elsewhere), door openings 8 x 12, nothing narrower than 7 studs on a walking route, stairs: rise at most 1.2, run at least 2.2, landings 10 deep, handrails both sides.
- Build interiors so they can be walked on: floors are flat boxes or flat meshes, no tiny bumps. Export a `<model>_collision.json` (boxes) for large interiors; visible meshes of props do not collide.

## 4. Worker procedure (same as v4)
1. Copy `library/src/v5_template.py` to `library/src/v5_<worker>.py`; write one builder function per model and a `BATCHES` dict (batch name -> (category folder, [(id, builder), ...])).
2. Run through `v4run.ps1 -Module v5_<worker> -Worker v<x> -Batch <batch>` (headless, factory startup, two Blender processes at most, calls over 60 s lose the reply, so keep batches to 12 models or fewer).
3. Look at the contact sheets in `library/v4_sheets/`, fix, re-run only the failing ids with `--only`.
4. When a batch is clean, ask an independent reviewer (see `MODEL_REVIEW_BRIEF.md`). Fix what it lists.
5. `python library/src/v4_merge.py` folds the metadata into `v4_meta.json` and the palettes into `palette.json`. Then `upload_v5.ps1`.
6. Never print or paste the Open Cloud key. The user closes Blender before the upload.

## 5. Naming
Ids are exactly the ids in the manifest (for example `CP01_02_ring_wall_straight_02`). Category folders: v5_wizard, v5_himalaya, v5_capital, v5_elf, v5_town1, v5_entrances, v5_landmarks, v5_coast, v5_roads, v5_forest, v5_plains, v5_desert, v5_skull.
"""
open(LIB + r'\V5_STYLE_GUIDE.md', 'w', encoding='utf-8').write(STYLE)
shutil.copy2(LIB + r'\V5_STYLE_GUIDE.md', HERE + r'\V5_STYLE_GUIDE.md')

TEMPLATE = '''"""v5 worker module TEMPLATE. Copy to library/src/v5_<worker>.py and implement the builders.
Contract (same as v4, see v4worker.py): run through v4run.ps1 -Module v5_<worker> -Worker v<x> -Batch <batch>.
  BATCHES = {'batch': ('category_folder', [(manifest_id, builder_fn), ...])}
  builder_fn() takes no argument, calls reset(), builds with kitlib primitives, returns finalize('name', smooth_angle=25).
Units: 1 Blender unit = 1 stud, Z up, front faces -Y, pivot = centre of footprint at z=0. Palette keys start with the worker prefix, emission 0.
Read library/V5_STYLE_GUIDE.md and plan_v5/V5_BRIEFS.md for the rows you build. Use v4_wa_ice.py / v4_we_castle.py as examples.
"""
import math, random
import kitlib
from kitlib import (reset, finalize, box, cyl, ball, lathe, tube, torus, poly_prism)
from arch import F, faces, lbox, lbeam, beam3, slab, lslab, nm
from nature import blob, rock
import v4util

PAL = kitlib.PAL
PAL['vx_stone'] = ((150, 142, 158), 'Slate', 0.00, 0.90, 0)     # key: ((r,g,b), RobloxMaterial, metallic, roughness, emission)
PAL['vx_roof'] = ((198, 88, 52), 'Brick', 0.00, 0.85, 0)


def example_block():
    """ZZ_V5_TEMPLATE - a small house shape to prove the pipeline end to end. Delete when real builders exist."""
    reset()
    box(nm('body'), (10, 8, 6), loc=(0, 0, 3), key='vx_stone', bev=0.2)
    box(nm('roof'), (11, 9, 1.2), loc=(0, 0, 6.6), key='vx_roof', bev=0.2)
    return finalize('v5_template_block', smooth_angle=25)


BATCHES = {
    'selftest': ('v4_test', [('ZZ_V5_TEMPLATE', example_block)]),
}
'''
open(LIB + r'\src\v5_template.py', 'w', encoding='utf-8').write(TEMPLATE)

# worker prompts
os.makedirs(HERE + r'\worker_prompts', exist_ok=True)
for p in plan:
    t = ['# Worker %s: %s' % (p['worker'], p['title']), '',
         'You are a Blender model builder for Kayos-h\'s Roblox map (v5 redesign). Blender 5.2 is at C:\\Program Files\\Blender Foundation\\Blender 5.2; build headless only through `library/src/v4run.ps1` (never the live Blender MCP tools). Work in `C:\\Users\\Nitro\\.kiro\\crew\\workspace\\town`.',
         '', 'Read first: `library/V5_STYLE_GUIDE.md`, `plan_v5/V5_BRIEFS.md` (your rows), `plan_v5/WORLD_BIBLE_v5.md` section 8, ' + ('`plan_v5/WIZARD_TOWER_BRIEF.md` (follow it exactly), ' if p['worker'] in ('va', 'vb') else '') + 'and the examples `library/src/v4_wa_ice.py`, `library/src/v4worker.py`.', '',
         'Module to write: `library/src/%s.py` (copy `v5_template.py`). Worker id `%s`; palette keys start with `%s_`.' % (p['module'], p['worker'], p['worker']), '', 'Your batches, in order:', '']
    for b in p['batches']:
        t.append('- **%s** (folder `%s`, %d models, about %d min): %s' % (b['batch'], b['category'], b['models'], b['est_minutes'], ', '.join(b['ids'][:6]) + (' ...' if len(b['ids']) > 6 else '')))
    t += ['', 'For each batch: write the builders, run `powershell -File library\\src\\v4run.ps1 -Module %s -Worker %s -Batch <batch>`, read the contact sheets, fix and re-run failing ids with `-Only`, then report ids built, triangle counts, size check and anything you could not do. Chunks of 12 models or fewer. Do not run `v4_merge.py` or the upload; the parent does.' % (p['module'], p['worker']), '',
          'Stop conditions: a batch is clean when every model passes the checks in the style guide section 1 and the contact sheet shows a clear silhouette. Maximum three fix rounds per model; list what is still weak.', '',
          'Rules: original designs only; no glow; no marketplace models; never print the Open Cloud key; do not touch other workers\' files.']
    open(HERE + r'\worker_prompts\%s.md' % p['worker'], 'w', encoding='utf-8').write('\n'.join(t) + '\n')

REVIEW = """# Model review brief (independent reviewer for Blender batches)

You see contact sheets (4 views per model) from `library/v4_sheets/` and the metadata lines below each. Judge only what you see. Do not read the builder code.

For every model give: id, score 1-10 on SILHOUETTE (reads at 500 studs), FORM (three scales of detail), MATERIALS (palette fits the place, no grey default), SCALE and PROPORTION (matches the manifest size, a 5-stud player fits doors), CONSTRUCTION (believable structure, ladders or stairs on raised floors, no floating bits), ORIGINALITY (does not copy a known franchise design), then a verdict `KEEP`, `FIX` (with the exact change) or `REBUILD`.

Rules that fail a model automatically: any glow or neon look, a freestanding plain entrance arch, floating geometry, inverted or missing faces, tri count over the budget, enterable building with walls thinner than 4 studs or openings narrower than 8 studs.

Extra for the wizard tower rows (WT01-WT13): also score EXTERIOR PRESENCE (does it look like the landmark of the island from far away), INTERIOR (walkable, headroom, stairs), BOOKSHELVES (floor-to-ceiling, packed books, curved to the wall), CIRCULAR MAP (reads as a relief map of an island, rings and landmark tokens, brass and stone). The tower needs 8 or more in every category. A single category under 8 means `FIX`.

End with `BATCH SCORE:` (mean), the list of ids to fix first, and at most five cheap changes that would raise the weakest scores.
"""
open(HERE + r'\MODEL_REVIEW_BRIEF.md', 'w', encoding='utf-8').write(REVIEW)

print('briefs: %d rows, %d models; workers %d; worker-hours %.1f; unassigned rows: %s' % (len(G), len(rows), len(plan), total_h, missing))
for p in plan:
    print('  %s %-58s %3d models %5.1f h' % (p['worker'], p['title'], p['models'], p['est_hours']))
