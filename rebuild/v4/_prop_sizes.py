import json, re
c = json.load(open(r'C:\Users\Nitro\.kiro\crew\workspace\town\mapplan\catalog.json', encoding='utf-8-sig'))
want = ['A41_hedge_straight', 'A42_hedge_corner', 'A100_fence_picket', 'A101_fence_rail', 'A103_fence_iron', 'A97_water_trough', 'A82_bench_wood', 'A83_bench_stone', 'A98_well', 'A99_anvil',
        'A79_hand_cart', 'A80_wagon', 'A78_hay_bale', 'A75_crate_stack', 'A74_crate_large', 'A71_barrel', 'A21_brazier', 'A105_market_stall_fruit', 'A48_planter_box', 'K32_ornate_planter',
        'K33_ornate_bench', 'A95_flag_pole', 'G17_net_rack', 'G15_fish_market_stall', 'D29_patched_tent', 'D31_rusted_cart', 'D32_broken_barrel', 'D36_old_well_pump', 'D33_broken_fence',
        'A52_reeds', 'A34_fruit_tree', 'A33_willow', 'A24_oak_1', 'A56_rock_small_1', 'A58_rock_medium_1', 'E21_log_fence', 'K28_maze_hedge_straight', 'A20_wall_torch']
by = {e['id']: e for e in c}
for w in want:
    e = by.get(w)
    print('%-26s %s' % (w, ('size_x %.1f size_z %.1f h %.1f' % (e['size_x'], e['size_z'], e['height'])) if e else 'MISSING in old catalog'))
m = json.load(open(r'C:\Users\Nitro\.kiro\crew\workspace\town\library\v4_meta.json'))
for w in ['B04_01_barracks', 'B04_02_stables', 'B06_01_stall_fruit', 'B05_05_royal_banner', 'B09_04_rowboat', 'F10_10_beach_fishing_gear', 'C06_01_frozen_dock_01', 'F05_07_reed_clump', 'D06_04_bush_a']:
    e = m.get(w)
    print('%-26s %s' % (w, e['size'] if e else 'missing'))
