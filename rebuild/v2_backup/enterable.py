import json, math, sys
import world as W

R = json.load(open(r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\reserved.json'))
OUT = r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild'

RUSTY = {'wall': [168, 136, 104], 'wall_mat': 'Sandstone', 'trim': [138, 118, 98], 'trim_mat': 'Limestone',
         'roof': [132, 64, 36], 'roof_mat': 'CorrodedMetal', 'ridge': [96, 48, 30], 'floor': [96, 84, 74], 'floor_mat': 'Slate',
         'chancel': [120, 96, 80], 'beam': [70, 48, 32], 'gold': [170, 120, 60],
         'glass': [[205, 140, 60], [150, 60, 50], [90, 130, 80], [200, 170, 90]], 'broken': 0.3, 'boards': [104, 76, 52]}
CAPITAL = {'wall': [236, 232, 222], 'wall_mat': 'Marble', 'trim': [214, 206, 190], 'trim_mat': 'Marble',
           'roof': [62, 82, 128], 'roof_mat': 'Slate', 'ridge': [200, 170, 80], 'floor': [200, 190, 175], 'floor_mat': 'Marble',
           'chancel': [150, 40, 45], 'beam': [92, 62, 40], 'gold': [222, 184, 74],
           'glass': [[70, 110, 200], [190, 50, 60], [230, 190, 70], [90, 160, 120]]}
TAVERN = {'low': [122, 116, 108], 'low_mat': 'Cobblestone', 'up': [226, 214, 188], 'up_mat': 'SmoothPlastic', 'trim': [84, 54, 34],
          'roof': [112, 52, 44], 'roof_mat': 'Slate', 'ridge': [80, 40, 34], 'floor': [140, 100, 66], 'floor_mat': 'WoodPlanks',
          'base': [110, 104, 96], 'base_mat': 'Cobblestone', 'stone': [118, 112, 104], 'glass': [230, 190, 120]}
LODGE = {'low': [132, 126, 118], 'low_mat': 'Cobblestone', 'up': [128, 84, 50], 'up_mat': 'Wood', 'trim': [78, 50, 30],
         'roof': [86, 58, 40], 'roof_mat': 'WoodPlanks', 'ridge': [70, 46, 32], 'floor': [146, 104, 68], 'floor_mat': 'WoodPlanks',
         'base': [120, 116, 108], 'base_mat': 'Cobblestone', 'stone': [126, 120, 112], 'glass': [240, 200, 130], 'snow': True}
ELF = {'base': [205, 208, 200], 'base_mat': 'Marble', 'floor': [196, 226, 214], 'floor_mat': 'Marble', 'col': [236, 238, 230],
       'col_mat': 'Marble', 'trim': [214, 204, 172], 'glow': [140, 255, 220]}

SPEC = {
    'rusty_church': {'kind': 'church', 'style': RUSTY, 'half_w': 30, 'half_l': 62, 'wall_h': 44, 'roof_rise': 30, 'tower_w': 26, 'tower_h': 104, 'spire_h': 52},
    'capital_cathedral': {'kind': 'church', 'style': CAPITAL, 'half_w': 28, 'half_l': 58, 'wall_h': 46, 'roof_rise': 30, 'tower_w': 24, 'tower_h': 112, 'spire_h': 58},
    'harbour_tavern': {'kind': 'hall', 'style': TAVERN, 'half_w': 15, 'half_l': 20, 'wall_h': 14, 'roof_rise': 10, 'bar': True},
    'alpine_lodge': {'kind': 'hall', 'style': LODGE, 'half_w': 15, 'half_l': 22, 'wall_h': 15, 'roof_rise': 13},
    'elf_temple': {'kind': 'shrine', 'style': ELF, 'radius': 18, 'col_h': 18, 'crown': 11},
}


def to_world(cx, cz, rot, lx, lz):
    t = math.radians(rot)
    return cx + lx * math.cos(t) + lz * math.sin(t), cz - lx * math.sin(t) + lz * math.cos(t)


def footprint_ground(cx, cz, rot, hw, hl):
    ys = []
    for lx in (-hw, 0, hw):
        for lz in (-hl, 0, hl):
            x, z = to_world(cx, cz, rot, lx, lz)
            ys.append(W.ground_no_noise(x, z))
    return min(ys), max(ys)


def shell_data(name):
    cx, cz, hl, hw, rot, y = R[name]
    s = dict(SPEC[name])
    ext_l = s.get('half_l', 20) + (s.get('tower_w', 0) + 30 if s['kind'] == 'church' else 4)
    lo, hi = footprint_ground(cx, cz, rot, s.get('half_w', s.get('radius', 20)) + 8, ext_l)
    s.update({'name': name, 'cx': cx, 'cz': cz, 'rot': rot, 'y': round(hi + 0.2, 2), 'plinth': round(hi - lo + 3, 2)})
    return s


def interior(name, s):
    """Furniture placements (world coords) with y_offset to stand on the building floor."""
    cx, cz, rot = s['cx'], s['cz'], s['rot']
    floor = s['y'] + 1.6 if s['kind'] != 'hall' else s['y'] + 1.4
    items = []

    def put(model, lx, lz, lrot=0, up=0.0, group='Interior', scale=None):
        x, z = to_world(cx, cz, rot, lx, lz)
        g = W.ground_no_noise(x, z)
        it = {'model': model, 'x': round(x, 2), 'z': round(z, 2), 'rot': round((rot + lrot) % 360, 1), 'group': f'{name}_{group}',
              'y_offset': round(floor + up - g + 0.25, 2)}
        if scale:
            it['scale'] = scale
        items.append(it)

    if s['kind'] == 'church':
        W2, Lh, H = s['half_w'], s['half_l'], s['wall_h']
        zB = -Lh
        put('K14_red_carpet', 0, 8, 0, 0.02)
        for z in [zB + 18 + 7 * k for k in range(int((2 * Lh - 34) / 7))]:
            for x in (-11, 11):
                put('D05_pew', x, z, 180)
        bays = int((Lh * 2 - 20) / 20)
        bl = (Lh * 2 - 20) / bays
        for b in range(1, bays):
            for x in (-W2 + 9, W2 - 9):
                put('D10_church_pillar', x, zB + 10 + bl * b, 0, 0, scale=1.45)
        put('D06_altar', 0, zB - 8, 0, 3.0, 'Sanctuary')
        put('D08_pipe_organ', 0, zB - W2 * 0.85 + 6, 0, 3.0, 'Sanctuary')
        put('D07_pulpit', -W2 + 10, zB + 14, 30, 0, 'Sanctuary')
        for (x, z) in ((-9, zB - 4), (9, zB - 4), (-14, zB - 14), (14, zB - 14)):
            put('D09_candle_stand', x, z, 0, 3.0, 'Sanctuary')
        put('A23_candle_cluster', -3, zB - 8, 0, 3.0 + 9.0, 'Sanctuary')
        put('A23_candle_cluster', 3, zB - 8, 0, 3.0 + 9.0, 'Sanctuary')
        for z in (zB + 25, 0, Lh - 25):
            put('K13_chandelier', 0, z, 0, H - 15)
        put('D02_church_bell', 0, Lh + s['tower_w'] / 2 + 1.5, 0, s['tower_h'] - 22, 'Belfry')
        if name == 'rusty_church':
            for (x, z) in ((W2 - 5, Lh - 6), (-W2 + 5, Lh - 10), (W2 - 6, zB + 30)):
                put('D32_broken_barrel', x, z, 40)
            put('D33_broken_fence', -W2 + 4, 10, 90)
        else:
            for (x, z) in ((-W2 + 4, -10), (W2 - 4, -10), (-W2 + 4, 20), (W2 - 4, 20)):
                put('K22_candelabra', x, z, 0)
            put('K16_tapestry_1', -W2 + 1.8, -30, 90, 14)
            put('K17_tapestry_2', W2 - 1.8, -30, 270, 14)
    elif s['kind'] == 'hall':
        W2, Lh = s['half_w'], s['half_l']
        for (x, z) in ((-W2 * 0.5, Lh * 0.45), (W2 * 0.5, Lh * 0.45), (-W2 * 0.5, Lh * 0.05), (W2 * 0.5, Lh * 0.05)):
            put('A84_table', x, z, 90)
            for dx in (-3.2, 3.2):
                put('A85_chair' if name == 'alpine_lodge' else 'A86_stool', x + dx, z, 90 if dx < 0 else 270)
            put('A23_candle_cluster', x, z, 0, 3.0)
        if s.get('bar'):
            for k in range(4):
                put('A71_barrel', -W2 + 2.2, -Lh * 0.45 - 4 + k * 3.2, 0)
            for k in range(-2, 3):
                put('A86_stool', -W2 * 0.2 + k * 3.2, -Lh * 0.45 + 2.6, 180)
            put('G30_ship_bell', W2 - 3, -Lh + 4, 270)
            put('G19_anchor', W2 - 2, Lh * 0.75, 270)
            put('A75_crate_stack', W2 - 5, -Lh + 5, 0)
        else:
            put('A90_firewood_stack', W2 * 0.55, -Lh + 4, 0)
            put('A90_firewood_stack', -W2 * 0.55, -Lh + 4, 0)
            put('E22_sled', W2 - 3, Lh * 0.7, 270)
            put('A71_barrel', -W2 + 2.5, Lh * 0.75, 0)
            put('A72_barrel_open', -W2 + 2.5, Lh * 0.6, 0)
        for z in (-Lh * 0.5, 0, Lh * 0.5):
            put('A19_hanging_lantern', 0, z, 0, s['wall_h'] - 6)
    else:
        put('F34_crystal_cluster', 0, 0, 0, 1.0)
        for k in range(5):
            a = math.radians(k * 72 + 36)
            put('F33_elf_bench', math.cos(a) * 11, math.sin(a) * 11, (math.degrees(math.atan2(-math.cos(a), -math.sin(a)))) % 360, 0)
        for k in range(10):
            a = math.radians(k * 36 + 18)
            put('F25_glow_flower_1' if k % 2 else 'F26_glow_flower_2', math.cos(a) * 15.5, math.sin(a) * 15.5, k * 37, 0)
    return items


if __name__ == '__main__':
    names = sys.argv[1].split(',') if len(sys.argv) > 1 else list(R.keys())
    tpl = open(rf'{OUT}\builders.luau', encoding='utf-8').read()
    allitems = []
    for n in names:
        s = shell_data(n)
        code = tpl.replace('__DATA__', json.dumps(s))
        json.dump({'code': code}, open(rf'{OUT}\_build_{n}.json', 'w'))
        allitems += interior(n, s)
        print(n, s['cx'], s['cz'], s['rot'], 'y', s['y'], 'plinth', s['plinth'])
    json.dump({'area': 'v2_interiors', 'terrain': [], 'placements': allitems},
              open(r'C:\Users\Nitro\.kiro\crew\workspace\town\mapplan\v2_interiors.json', 'w'), indent=0)
    print('interior items', len(allitems))
