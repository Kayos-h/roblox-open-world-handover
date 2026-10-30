s = open('enterable.py', encoding='utf-8').read()
s = s.replace("""    'elf_temple': {'kind': 'shrine', 'style': ELF, 'radius': 18, 'col_h': 18, 'crown': 11},
}""", """    'elf_temple': {'kind': 'shrine', 'style': ELF, 'radius': 18, 'col_h': 18, 'crown': 11},
    'elf_house_1': {'kind': 'elfhouse', 'style': ELFHOUSE, 'radius': 14, 'wall_h': 12},
    'elf_house_2': {'kind': 'elfhouse', 'style': ELFHOUSE, 'radius': 14, 'wall_h': 12},
}""")
s = s.replace("""SPEC = {""", """ELFHOUSE = {'base': [200, 204, 196], 'base_mat': 'Marble', 'floor': [168, 132, 92], 'floor_mat': 'WoodPlanks', 'wall': [206, 184, 146],
            'wall_mat': 'Wood', 'trim': [118, 84, 56], 'trim_mat': 'Wood', 'roof': [74, 128, 66], 'roof2': [96, 150, 80], 'roof_mat': 'Grass',
            'glass': [160, 230, 200], 'glow': [140, 255, 220]}

SPEC = {""")
s = s.replace("""    ext_l = s.get('half_l', 20) + (s.get('tower_w', 0) + 30 if s['kind'] == 'church' else 4)
    lo, hi = footprint_ground(cx, cz, rot, s.get('half_w', s.get('radius', 20)) + 8, ext_l)""",
"""    ext_l = s.get('half_l', s.get('radius', 20)) + (s.get('tower_w', 0) + 30 if s['kind'] == 'church' else 4)
    lo, hi = footprint_ground(cx, cz, rot, s.get('half_w', s.get('radius', 20)) + 8, ext_l)""")
s = s.replace("""    else:
        put('F34_crystal_cluster', 0, 0, 0, 1.0)""", """    elif s['kind'] == 'elfhouse':
        R0 = s['radius']
        put('A84_table', 0, -2, 0)
        put('K21_magic_orb', 0, -2, 0, 3.0)
        put('K20_bookshelf', 0, -R0 + 2.2, 0)
        for (x, z, r) in ((-7, 2, 90), (7, 2, 270)):
            put('F33_elf_bench', x, z, r)
        for (x, z) in ((-9, -7), (9, -7), (-10, 6), (10, 6)):
            put('F22_giant_leaf_plant' if x < 0 else 'F25_glow_flower_1', x, z, 30, 0, scale=0.6 if x < 0 else 1.0)
        put('F28_elf_standing_lantern', -4, R0 - 3, 0)
        put('F28_elf_standing_lantern', 4, R0 - 3, 0)
        put('F34_crystal_cluster', 8, -9, 40, 0, scale=0.6)
    else:
        put('F34_crystal_cluster', 0, 0, 0, 1.0)""")
s = s.replace("mapplan\\\\v2_interiors.json", "mapplan\\\\v3_interiors.json").replace("'area': 'v2_interiors'", "'area': 'v3_interiors'")
open('enterable.py', 'w', encoding='utf-8').write(s)
print('ok', s.count('elfhouse'), s.count('v3_interiors'))
