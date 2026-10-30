"""v4 master manifest: every Blender model needed for the map, with counts, priority and build status.
Run:  python v4_manifest.py   -> writes library\\V4_MANIFEST.json and library\\V4_MANIFEST.md
Priority: P1 = first pass (placeholders + key look), P2 = second pass, P3 = polish.
Row format: (row_code, base_name, count, priority, description[, explicit_names])
"""
import json, os, re
LIB = r'C:\Users\Nitro\.kiro\crew\workspace\town\library'

SECTIONS = {
 'A': ('Replace part-built placeholders', [
  ('A01', 'igloo', 3, 'P1', 'Snow-block dome, tunnel entrance with back wall, 3 sizes (14/16/18 studs)'),
  ('A02', 'ice_shanty', 4, 'P1', 'Ice-fishing hut 8x9x7, pitched roof with snow, stovepipe, 4 colourways'),
  ('A03', 'fishing_hole', 3, 'P1', 'Ragged ice rim, cracks, dark water, ~4 studs across'),
  ('A04', 'rusty_hut', 6, 'P1', 'Weathered hut 13-15 studs: timber/sandstone/scrap roofs, door, shutters, steps, interior back wall'),
  ('A05', 'shell_rusty_church', 1, 'P1', 'Enterable shell 60x124, hollow nave, door, windows'),
  ('A06', 'shell_capital_cathedral', 1, 'P1', 'Enterable shell at (-186,-1628)'),
  ('A07', 'shell_harbour_tavern', 1, 'P1', 'Enterable shell at (-428,1764)'),
  ('A08', 'shell_alpine_lodge', 1, 'P1', 'Enterable shell at (1585,-880)')]),
 'B': ('Key set pieces', [
  ('B01', 'skull_hq', 1, 'P1', 'Separate colour pieces, hollow interior, entrance through the jaw, 220x148x265'),
  ('B02', 'castle', 7, 'P1', 'Keep, round tower, square tower, spire tower, curtain wall straight, curtain wall corner, gatehouse',
   ['keep', 'round_tower', 'square_tower', 'spire_tower', 'curtain_wall', 'curtain_corner', 'gatehouse']),
  ('B03', 'throne_hall', 1, 'P2', 'Interior set: throne pillars, banners, stairs'),
  ('B04', 'garrison', 2, 'P2', 'Barracks and stables', ['barracks', 'stables']),
  ('B05', 'courtyard', 7, 'P2', 'Royal fountain, knight statue, obelisk, ornate lamp, banner, gazebo, rose arch',
   ['royal_fountain', 'knight_statue', 'obelisk', 'ornate_lamp', 'royal_banner', 'gazebo', 'rose_arch']),
  ('B06', 'castle_stall', 3, 'P2', 'Market stalls: fruit, cloth, potion', ['stall_fruit', 'stall_cloth', 'stall_potion']),
  ('B07', 'capital_house', 6, 'P1', 'New townhouse designs, 6+ roof colours, 4 facade variants for the avenue'),
  ('B08', 'town1_church', 1, 'P1', 'Gothic church 35x85x75, door and rose window east, not enterable'),
  ('B09', 'ship', 4, 'P2', 'Galleon 88x28x60, merchant ship, fishing boat, rowboat, with rigging', ['galleon', 'merchant_ship', 'fishing_boat', 'rowboat']),
  ('B10', 'harbour_set', 4, 'P2', 'Lighthouse, cargo crane, two warehouses', ['lighthouse', 'cargo_crane', 'warehouse_a', 'warehouse_b'])]),
 'C': ('Alpine', [
  ('C01', 'chalet', 6, 'P2', 'Timber and stone chalets with deep snow roofs and icicles'),
  ('C02', 'winter_stall', 3, 'P2', 'Winter-market stalls with striped awnings and lanterns'),
  ('C03', 'ski_rack', 1, 'P3', ''),
  ('C04', 'snowman', 2, 'P3', 'Two sizes'),
  ('C05', 'ice_block', 3, 'P3', 'Ice blocks and a sculpture'),
  ('C06', 'frozen_dock', 1, 'P3', 'Lake-edge dock'),
  ('C07', 'sled', 2, 'P3', ''),
  ('C08', 'frozen_boat', 2, 'P3', 'Boats stuck in ice'),
  ('C09', 'frozen_waterfall', 1, 'P3', 'For the 30-stud step on the ice-lake rim'),
  ('C10', 'snow_pine', 4, 'P1', 'Snow-laden conifers, 4 silhouettes')]),
 'D': ('Elf valley rebuild (natural elven look, no neon)', [
  ('D01', 'treehouse', 6, 'P1', 'Big-tree homes with deck, railing, ladder landing (markers), cabin; six layouts',
   ['treehouse_a', 'treehouse_b', 'treehouse_c', 'treehouse_d', 'treehouse_e', 'treehouse_f']),
  ('D02', 'ladder_stair', 7, 'P1', 'Rope ladder short/tall, wooden ladder, trunk spiral stair, switchback stair, landing platform, lift winch',
   ['rope_ladder_short', 'rope_ladder_tall', 'wood_ladder', 'spiral_stair', 'switchback_stair', 'ladder_landing', 'lift_winch']),
  ('D03', 'platform_walkway', 8, 'P1', 'Platform rings, walkways, rope bridges, anchor post, railing set',
   ['platform_small', 'platform_large', 'walkway_straight', 'walkway_curved', 'rope_bridge_short', 'rope_bridge_long', 'bridge_anchor', 'railing_set']),
  ('D04', 'elf_building', 16, 'P1', 'Round houses x3, temple, palace, gate arches x2, market stalls x3, watch post, stone bridges x2, pavilion, moon pool, workshop',
   ['round_house_a', 'round_house_b', 'round_house_c', 'temple', 'palace', 'gate_arch_a', 'gate_arch_b', 'stall_a', 'stall_b', 'stall_c', 'watch_post', 'stone_bridge_a', 'stone_bridge_b', 'pavilion', 'moon_pool', 'workshop']),
  ('D05', 'elf_tree', 18, 'P1', 'World tree trunk/roots/canopy, ancient trees x5, canopy clusters x3, stumps x3, logs x2, hollow tree, sapling',
   ['world_tree_trunk', 'world_tree_roots', 'world_tree_canopy', 'ancient_tree_a', 'ancient_tree_b', 'ancient_tree_c', 'ancient_tree_d', 'ancient_tree_e',
    'canopy_a', 'canopy_b', 'canopy_c', 'stump_a', 'stump_b', 'stump_c', 'log_a', 'log_b', 'hollow_tree', 'sapling']),
  ('D06', 'elf_plant', 19, 'P2', 'Ferns x3, bushes x3, natural flowers x3, mossy rocks x3, ivy x3, hanging moss x2, mushrooms x2',
   ['fern_a', 'fern_b', 'fern_c', 'bush_a', 'bush_b', 'bush_c', 'flower_a', 'flower_b', 'flower_c', 'moss_rock_a', 'moss_rock_b', 'moss_rock_c',
    'ivy_a', 'ivy_b', 'ivy_c', 'hanging_moss_a', 'hanging_moss_b', 'mushroom_a', 'mushroom_b']),
  ('D07', 'elf_light', 6, 'P1', 'Warm lanterns only: standing x2, hanging x2, brazier, candle cluster',
   ['lantern_post_a', 'lantern_post_b', 'lantern_hang_a', 'lantern_hang_b', 'brazier', 'candle_cluster']),
  ('D08', 'elf_statue_ruin', 12, 'P2', 'Statues x3, ruined arch x2, standing stones x2, carved markers x2, banners x3',
   ['statue_a', 'statue_b', 'statue_c', 'ruin_arch_a', 'ruin_arch_b', 'standing_stone_a', 'standing_stone_b', 'marker_a', 'marker_b', 'banner_a', 'banner_b', 'banner_c']),
  ('D09', 'elf_water', 5, 'P2', 'Waterfall cliff x2, stepping stones, small bridges x2',
   ['waterfall_cliff_a', 'waterfall_cliff_b', 'stepping_stones', 'plank_bridge_a', 'plank_bridge_b'])]),
 'E': ('Graveyard, rusty town, farms, nature (old list)', [
  ('E01', 'gravestone', 8, 'P2', 'Weathered, tilted, moss'),
  ('E02', 'crypt', 3, 'P2', 'Mausoleums'),
  ('E03', 'weeping_statue', 3, 'P2', ''),
  ('E04', 'iron_fence_gate', 2, 'P2', 'Fence section and gate'),
  ('E05', 'dead_tree', 6, 'P2', ''),
  ('E06', 'rusty_debris', 12, 'P2', 'Scrap piles x5, tents x3, collapsed walls x4'),
  ('E07', 'rusty_prop', 9, 'P3', 'Crooked lamps x3, rusted carts x3, broken barrels x3'),
  ('E08', 'barn', 3, 'P2', ''),
  ('E09', 'windmill', 2, 'P2', ''),
  ('E10', 'crop_plot', 6, 'P2', 'Wheat, vegetables, etc.'),
  ('E11', 'scarecrow', 3, 'P3', ''),
  ('E12', 'shrine_ruin', 4, 'P2', ''),
  ('E13', 'rock_face', 10, 'P1', 'Large seamless cliff faces for mountains, 3-4 for the tower massif'),
  ('E14', 'icelake_rim_wall', 4, 'P2', '30-stud cliff step on the lake rim'),
  ('E15', 'boulder', 6, 'P2', 'Natural, not overscaled')]),
 'F': ('New terrain and vegetation brief', [
  ('F01', 'tree_heartland', 6, 'P1', 'Oaks, beech, groves, fruit tree'),
  ('F02', 'tree_alpine', 5, 'P1', 'Spruce, bare birch, wind-bent pines'),
  ('F03', 'tree_dry', 3, 'P1', 'Scrub trees for the frontier'),
  ('F04', 'tree_coastal', 4, 'P1', 'Windswept pines'),
  ('F05', 'undergrowth', 12, 'P2', 'Bushes x4, hedge pieces x2, reeds x2, tall grass x2, coastal grass x2'),
  ('F06', 'ground_detail', 21, 'P3', 'Logs x3, stumps x3, roots x2, pebbles x4, mossy rocks x3, flower patches x4, mushroom patches x2'),
  ('F07', 'rock_formation', 11, 'P2', 'Spires x3, sea stacks x3, arches x2, coastal cliffs x3'),
  ('F08', 'road_piece', 17, 'P2', 'Stone bridges x3, wooden bridges x3, ruined bridge, signposts x3, milestones x2, gate arches x2, roadside shrines x3'),
  ('F09', 'story_prop', 13, 'P2', 'Broken carts x2, camps x3, ruined watchtowers x2, foundations x3, overgrown ruins x3'),
  ('F10', 'water_coast', 10, 'P2', 'Lily pads x2, small waterfall pieces x3, docks x2, beach props x3'),
  ('F11', 'landmark_trail', 9, 'P2', 'Lookouts x2, cave entrances x3, cliff-trail pieces x3, summit tower')]),
 'R': ('From your reference image (islets, peaks, badlands, sea cliffs)', [
  ('R01', 'islet', 4, 'P1', 'Offshore rock islands topped with trees, as in the reference'),
  ('R02', 'snow_peak', 4, 'P1', 'Jagged snow-covered peaks for the north-east range'),
  ('R03', 'badlands_mesa', 4, 'P1', 'Red-brown mesas and rock towers around Rusty Town'),
  ('R04', 'sea_cliff', 3, 'P2', 'Rocky coast cliff faces'),
  ('R05', 'waterfall_cliff_large', 2, 'P2', 'Large waterfall cliffs, for the elf valley and rivers'),
  ('R06', 'canyon_wall', 3, 'P2', 'Tall rock walls for passes')]),
}

def expand():
    rows = []
    for sec, (title, defs) in SECTIONS.items():
        for d in defs:
            code, base, n, pr, desc = d[:5]
            names = d[5] if len(d) > 5 else None
            for i in range(n):
                nm = names[i] if names else f'{base}_{i + 1:02d}'
                mid = f'{code}_{i + 1:02d}_{nm}'
                rows.append({'id': mid, 'section': sec, 'row': code, 'family': base, 'priority': pr, 'desc': desc})
    return rows

if __name__ == '__main__':
    rows = expand()
    meta = {}
    mp = os.path.join(LIB, 'v4_meta.json')
    if os.path.exists(mp):
        meta = json.load(open(mp))
    built = {m: v for m, v in meta.items()}
    # map pilot IDs onto manifest ids
    alias = {'EV01_treehouse_a': 'D01_01_treehouse_a'}
    done = {alias.get(k, k) for k in built}
    for r in rows:
        r['status'] = 'built' if r['id'] in done else 'todo'
    sums = {}
    for r in rows:
        s = sums.setdefault(r['section'], {'total': 0, 'built': 0, 'P1': 0, 'P2': 0, 'P3': 0})
        s['total'] += 1; s['built'] += r['status'] == 'built'; s[r['priority']] += 1
    total = len(rows)
    p = {k: sum(1 for r in rows if r['priority'] == k) for k in ('P1', 'P2', 'P3')}
    json.dump({'total': total, 'by_priority': p, 'by_section': sums, 'models': rows}, open(os.path.join(LIB, 'V4_MANIFEST.json'), 'w'), indent=1)
    md = ['# V4 Blender model manifest', '', f'**Total models: {total}**  (P1 first pass: {p["P1"]}, P2: {p["P2"]}, P3 polish: {p["P3"]})', '',
          '| Section | Models | P1 | P2 | P3 | Built |', '|---|---|---|---|---|---|']
    for sec, (title, defs) in SECTIONS.items():
        s = sums[sec]
        md.append(f'| {sec}. {title} | {s["total"]} | {s["P1"]} | {s["P2"]} | {s["P3"]} | {s["built"]} |')
    md.append(f'| **All** | **{total}** | **{p["P1"]}** | **{p["P2"]}** | **{p["P3"]}** | **{sum(s["built"] for s in sums.values())}** |')
    for sec, (title, defs) in SECTIONS.items():
        md += ['', f'## {sec}. {title}', '', '| ID | Priority | Status | Notes |', '|---|---|---|---|']
        for r in rows:
            if r['section'] == sec:
                md.append(f'| {r["id"]} | {r["priority"]} | {r["status"]} | {r["desc"]} |')
    open(os.path.join(LIB, 'V4_MANIFEST.md'), 'w', encoding='utf-8').write('\n'.join(md))
    print('total', total, p)
    for sec, s in sums.items():
        print(sec, s)
