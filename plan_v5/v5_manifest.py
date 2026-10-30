"""v5 manifest: every NEW Blender model needed for the world redesign, with counts, priority, size and triangle budget.
Run:  python v5_manifest.py   -> writes V5_MANIFEST.json, V5_MANIFEST.csv and V5_MANIFEST.md next to this file and prints the totals.
Priority: P1 = core (the redesign's must-haves), P2 = region completion, P3 = optional zones and polish.
Row: (row_code, base_name, count, priority, region, size_studs (x, y, z), tri_budget, description)
Tri budget = whole model; a model may be split into several MeshParts of at most 20k triangles each.
The existing library (391 models, library/v4_meta.json) is reused wherever it already covers the need (see REUSE below).
Rules: no emissive or glowing parts, original designs only (no Black Clover names or shapes), everything anchored,
at most 1-2 enterable buildings per settlement.
"""
import csv
import collections
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

ROWS = [
    # ---- CP: capital and castle town (target look: the castle-town reference picture) ----
    ('CP01', 'ring_wall_straight', 3, 'P1', 'capital', (40, 20, 10), 9000, '40-stud wall segments (plain, arrow slits, buttressed); 8-stud wide red-brown wall-walk, white-capped inner parapet, crenellated outer edge; replaces B02_05'),
    ('CP02', 'ring_wall_corner', 3, 'P1', 'capital', (24, 22, 24), 12000, 'Polygon joints of 135, 90 and 150 degrees with a tower seat; replaces B02_06'),
    ('CP03', 'ring_wall_stair_end', 2, 'P1', 'capital', (20, 20, 14), 7000, 'Stair up to the wall-walk and a wall end cap'),
    ('CP04', 'tower_round_cone', 4, 'P1', 'capital', (22, 48, 22), 14000, 'Round towers in 4 sizes (16, 22, 28, 34 studs wide) with maroon cone roofs and slit windows'),
    ('CP05', 'turret_crenellated', 2, 'P1', 'capital', (14, 26, 14), 8000, 'Round crenellated turrets for the outer ring (the foreground silhouette in the reference)'),
    ('CP06', 'gate_flank_tower', 2, 'P1', 'capital', (30, 52, 30), 16000, 'Twin towers that flank the main gatehouse'),
    ('CP07', 'gatehouse_main', 1, 'P1', 'capital', (60, 56, 40), 30000, 'Portcullis arch, banner mounts, walkable passage; replaces B02_07'),
    ('CP08', 'water_gate', 1, 'P1', 'capital', (40, 30, 30), 18000, 'Arched river gate where the capital river passes under the wall'),
    ('CP09', 'keep_terrace_hero', 1, 'P1', 'capital', (130, 120, 110), 50000, 'Grey stone keep with 8+ turrets and cone roofs on a raised terrace at the back of the enclosure; replaces the B02_01 silhouette'),
    ('CP10', 'keep_wing', 2, 'P1', 'capital', (60, 70, 50), 28000, 'Wings that widen the keep silhouette'),
    ('CP11', 'great_hall_chapel', 2, 'P2', 'capital', (70, 60, 50), 30000, 'Great hall and royal chapel inside the castle court'),
    ('CP12', 'terrace_retaining_wall', 2, 'P1', 'capital', (40, 22, 10), 8000, 'Straight and curved retaining wall under the keep terrace, grassy top'),
    ('CP13', 'grand_stair', 2, 'P1', 'capital', (30, 22, 40), 9000, 'Wide stair from the gate court up the terrace, plus a narrow side stair'),
    ('CP14', 'skyline_tower', 5, 'P1', 'capital', (30, 110, 30), 30000, 'Five different tall towers: clock, bell, observatory, beacon (unlit), water tower'),
    ('CP15', 'order_hq', 3, 'P1', 'capital', (90, 60, 70), 40000, 'Knights-order headquarters (own name and shape, not copied) plus 2 annex buildings'),
    ('CP16', 'townhouse_new', 12, 'P2', 'capital', (22, 28, 22), 11000, 'Half-timbered orange-roof family: corner house, tall x2, courtyard x2, arcade shop x2, inn, guild hall x2, market hall'),
    ('CP17', 'plaza_features', 2, 'P2', 'capital', (30, 34, 30), 14000, 'Central plaza monument and a public well'),
    ('CP18', 'quay_wall', 4, 'P2', 'capital', (30, 8, 10), 5000, 'River embankment: straight, curve, steps, mooring posts'),
    ('CP19', 'grand_bridge', 2, 'P1', 'capital', (60, 28, 26), 26000, 'Towered stone bridge over the capital river, and a drawbridge'),
    # ---- LM: the seven landmark types ----
    ('LM01', 'world_tree_trunk_door', 1, 'P2', 'forest', (36, 50, 36), 30000, 'Hollow trunk piece with a door, stair and lantern niche (warm lantern only, no glow)'),
    ('LM02', 'world_tree_falls', 1, 'P2', 'forest', (80, 110, 40), 35000, '3-tier waterfall set for the world tree cliff'),
    ('LM03', 'frost_fortress_hero', 1, 'P1', 'highlands', (300, 220, 260), 60000, 'Fortress built into a snowy mountain flank (own name and design)'),
    ('LM04', 'fortress_rampart_step', 3, 'P2', 'highlands', (60, 34, 20), 14000, 'Stepped ramparts that climb the rock'),
    ('LM05', 'fortress_cliff_tower', 2, 'P2', 'highlands', (34, 80, 34), 18000, 'Towers clinging to the cliff'),
    ('LM06', 'fortress_tunnel_gate', 1, 'P2', 'highlands', (60, 50, 60), 24000, 'Gate tunnel cut into the mountain'),
    ('LM07', 'carved_stair_switchback', 2, 'P2', 'highlands', (50, 60, 60), 16000, 'Switchback stairs carved into the slope'),
    ('LM08', 'mountain_span_bridge', 1, 'P2', 'highlands', (90, 24, 16), 14000, 'Stone span between two rock faces on a pass'),
    ('LM09', 'temple_buried_hero', 1, 'P1', 'desert', (180, 90, 160), 55000, 'Desert temple half buried in sand: the top third and one gate show'),
    ('LM10', 'temple_colonnade_buried', 3, 'P2', 'desert', (60, 40, 20), 14000, 'Colonnade sections sunk into the dunes'),
    ('LM11', 'temple_gate_buried', 1, 'P2', 'desert', (40, 50, 20), 16000, 'Half-buried gate'),
    ('LM12', 'temple_stair_down', 2, 'P2', 'desert', (30, 24, 40), 9000, 'Stair that leads down into the sand'),
    ('LM13', 'guardian_statue', 2, 'P2', 'desert', (20, 70, 20), 18000, 'Original weathered guardian figures'),
    ('LM14', 'sand_obelisk', 3, 'P2', 'desert', (10, 60, 10), 5000, 'Carved obelisks, leaning'),
    ('LM15', 'ring_temple_hero', 1, 'P1', 'desert', (220, 60, 220), 55000, 'Circular ring temple with an inner sanctum (from the concept map)'),
    ('LM16', 'ring_temple_segment', 2, 'P2', 'desert', (50, 40, 25), 14000, 'Ring wall segments for building out the circle'),
    ('LM17', 'ring_inner_sanctum', 1, 'P2', 'desert', (60, 60, 60), 24000, 'Inner sanctum'),
    ('LM18', 'crater_monolith_ring', 1, 'P1', 'centre', (140, 50, 140), 40000, 'Ring of carved standing stones around the crater rim (non-emissive)'),
    ('LM19', 'crater_rim_rock', 5, 'P2', 'centre', (60, 40, 50), 12000, 'Broken rim rocks'),
    ('LM20', 'crater_arcane_ruin', 3, 'P2', 'centre', (40, 40, 40), 14000, 'Small broken magical structures on the crater floor'),
    ('LM21', 'floating_rock', 4, 'P3', 'centre', (40, 30, 40), 8000, 'Drifting rock slabs over the crater (no glow)'),
    ('LM22', 'colossal_fall_cliff_hero', 1, 'P1', 'forest', (240, 260, 120), 60000, 'Colossal multi-fall cliff for the river valley'),
    ('LM23', 'gorge_wall', 3, 'P2', 'forest', (90, 80, 30), 20000, 'Gorge walls below the falls'),
    ('LM24', 'fall_pool_rock', 3, 'P2', 'forest', (30, 16, 30), 6000, 'Pool rocks at the base'),
    ('LM25', 'ruin_gate_hero', 1, 'P1', 'plains', (90, 80, 30), 40000, 'Gate of the ancient civilization, half collapsed'),
    ('LM26', 'ruin_arena_segment', 3, 'P2', 'plains', (60, 34, 30), 14000, 'Arena wall segments'),
    ('LM27', 'ruin_aqueduct_arch', 2, 'P2', 'plains', (40, 50, 12), 12000, 'Aqueduct arches'),
    ('LM28', 'ruin_column_set', 3, 'P2', 'plains', (24, 40, 24), 8000, 'Broken column groups'),
    ('LM29', 'ruin_tower_stump', 2, 'P2', 'plains', (26, 36, 26), 10000, 'Tower stumps'),
    ('LM30', 'ruined_castle_hero', 1, 'P1', 'plains', (140, 70, 120), 50000, 'Ruined castle with a broken keep'),
    ('LM31', 'ruined_castle_module', 3, 'P2', 'plains', (40, 40, 30), 14000, 'Wall and tower modules for the ruined castle'),
    # ---- WT: the giant ENTERABLE wizard tower on the Roof Plateau (replaces the abandoned magic tower rows LM32-LM35; 30 Oct 11:30). Needs the most care of anything in v5. See WIZARD_TOWER_BRIEF.md ----
    ('WT01', 'wizard_tower_shell', 1, 'P1', 'highlands', (110, 300, 110), 150000, 'Exterior of the giant wizard tower for the pad at (1380,-1320), floor y 324: Himalayan monastery base (whitewashed bands, tapered timber windows, stone buttresses) rising into a slim spiral-staggered stone spire with copper-green roofs; 10 MeshParts of at most 20k triangles (plinth, 8 stacked levels, crown); walls 6 studs thick so the inside is enterable'),
    ('WT02', 'wizard_tower_interior', 1, 'P1', 'highlands', (100, 280, 100), 90000, 'Interior shell: 8 floor plates, open central atrium, wide helical stair (rise at most 1.2, run at least 2), railings, wall linings, window reveals; plus tower_collision.json (boxes for floors, walls, stair treads) so Studio can build invisible collision'),
    ('WT03', 'wizard_bookshelf_curved', 3, 'P1', 'highlands', (24, 28, 6), 12000, 'Full-height curved bookshelf bays that follow the round tower wall (radius 38, 30 and 22): packed books, scroll racks, glass-fronted cabinet, rolling-ladder rail'),
    ('WT04', 'wizard_bookshelf_straight', 2, 'P1', 'highlands', (14, 26, 5), 10000, 'Straight bookshelf and a free-standing island shelf with ladder'),
    ('WT05', 'wizard_round_map_table', 1, 'P1', 'highlands', (44, 12, 44), 60000, 'THE CIRCULAR MAP: a 44-stud round relief map of the whole island on a stone-and-brass table, built from the real terrain data (terrain_map.json) with tiny landmark models, a brass compass ring and a walkway rail; 3 MeshParts'),
    ('WT06', 'wizard_floor_medallion', 1, 'P1', 'highlands', (80, 1, 80), 8000, 'Round floor inlay for the Map Hall: compass rose, star ring, inlaid stone and brass'),
    ('WT07', 'wizard_lab_set', 4, 'P1', 'highlands', (18, 14, 12), 10000, 'Alchemy bench with glassware, herb rack with jars, specimen shelf, orrery and astrolabe stand'),
    ('WT08', 'wizard_study_set', 3, 'P1', 'highlands', (18, 12, 14), 9000, 'Archmage desk with open books and quill, bed alcove with drapes, globe and sea-chart stand'),
    ('WT09', 'wizard_chandelier_ring', 2, 'P1', 'highlands', (20, 8, 20), 6000, 'Ring chandeliers with candles (warm light only, no glow)'),
    ('WT10', 'wizard_observatory_telescope', 1, 'P1', 'highlands', (14, 24, 14), 20000, 'Giant brass telescope on a mount for the top dome'),
    ('WT11', 'wizard_armillary_crown', 1, 'P1', 'highlands', (70, 50, 70), 22000, 'Armillary rings around the crown of the tower (static; Studio can rotate them later)'),
    ('WT12', 'wizard_door_porch', 1, 'P1', 'highlands', (40, 36, 24), 24000, 'Entrance porch with big carved timber doors in a rectangular frame (not an arch), steps and lantern posts'),
    ('WT13', 'plateau_terrace_set', 6, 'P2', 'highlands', (30, 10, 30), 7000, 'Terrace retaining wall x2, 40-step stair, prayer-flag pole, cairn and lantern post around the tower'),
    # ---- HL: frozen highlands extras ----
    ('HL01', 'ice_spire', 4, 'P2', 'highlands', (24, 70, 24), 8000, 'Ice spires'),
    ('HL02', 'ice_arch', 2, 'P2', 'highlands', (50, 40, 14), 9000, 'Natural ice arches'),
    ('HL03', 'glacier_tongue', 3, 'P2', 'highlands', (90, 24, 50), 12000, 'Glacier tongues and crevasse edges'),
    ('HL04', 'ice_cave_mouth', 2, 'P2', 'highlands', (40, 30, 30), 10000, 'Ice cave entrances'),
    ('HL05', 'mountain_shrine', 1, 'P2', 'highlands', (24, 24, 24), 9000, 'Hidden shrine on a pass'),
    ('HL06', 'snow_watchtower', 1, 'P2', 'highlands', (20, 50, 20), 11000, 'Watchtower for the mountain road'),
    ('HL07', 'mine_entrance', 2, 'P2', 'highlands', (30, 24, 24), 9000, 'Timbered mine mouths'),
    # ---- HM: Himalayan road and bridge kit (30 Oct 11:30: roads cross the mountains, river bridges in Himalayan style; routes in ROADS_V5.md) ----
    ('HM01', 'rope_suspension_bridge', 3, 'P1', 'highlands', (120, 14, 10), 12000, 'Himalayan rope-and-plank suspension bridges with stone anchor towers and prayer flags, three spans (60, 90, 116 studs); the 116 crosses Frost Gorge; walkable deck, hand ropes'),
    ('HM02', 'timber_cantilever_bridge', 2, 'P2', 'highlands', (36, 12, 10), 10000, 'Timber cantilever bridges with a small roof, spans 28 and 40 (tarn outlet, mountain streams)'),
    ('HM03', 'tunnel_portal', 3, 'P1', 'highlands', (30, 24, 20), 12000, 'Rock-cut road tunnel mouths (plain, snow-capped, timber-framed): a rectangular timber frame set in a rock face, not a freestanding arch'),
    ('HM04', 'tunnel_lining', 2, 'P1', 'highlands', (24, 20, 24), 8000, 'Tunnel lining segments (24-stud straight, 30-degree bend) with rock walls, timber ribs and lantern brackets (warm, no glow)'),
    ('HM05', 'cliff_gallery', 2, 'P2', 'highlands', (40, 22, 14), 9000, 'Road galleries cut into a cliff with timber props and a rock roof'),
    ('HM06', 'switchback_wall', 3, 'P2', 'highlands', (30, 14, 14), 7000, 'Stone retaining walls and hairpin corners for mountain roads'),
    ('HM07', 'prayer_flag_string', 4, 'P2', 'highlands', (40, 12, 2), 3000, 'Strings of cloth flags for bridges, cairns and passes'),
    ('HM08', 'cairn_shrine', 4, 'P2', 'highlands', (14, 12, 14), 4000, 'Stone cairns and small roadside shrines'),
    ('HM09', 'monastery_outpost', 4, 'P2', 'highlands', (40, 30, 30), 14000, 'Hall, prayer-wheel house, guest house and bell shelter for the hidden monastery pocket beyond Frost Gorge (2450,-1480)'),
    # ---- FR: ancient forest extras ----
    ('FR01', 'giant_tree', 4, 'P2', 'forest', (90, 160, 90), 40000, 'Four giant-tree silhouettes: leaning, twin trunk, arched, broken top (natural, no glow)'),
    ('FR02', 'forest_ruin', 6, 'P2', 'forest', (40, 34, 30), 10000, 'Overgrown arch, stair, wall, altar and two broken pillars'),
    ('FR03', 'cave_mouth', 6, 'P2', 'forest', (40, 30, 30), 10000, 'Cave mouths and rock arches for secret caves'),
    # ---- PL: greenheart plains ----
    ('PL01', 'farmhouse', 4, 'P2', 'plains', (28, 22, 24), 10000, 'Farmhouses'),
    ('PL02', 'hay_silo', 3, 'P2', 'plains', (14, 24, 14), 5000, 'Hay stacks and a silo'),
    ('PL03', 'farm_cart', 2, 'P2', 'plains', (14, 8, 8), 3000, 'Carts'),
    ('PL04', 'mill_waterwheel', 1, 'P2', 'plains', (34, 30, 30), 16000, 'Watermill'),
    ('PL05', 'ruined_watchtower_plains', 3, 'P2', 'plains', (20, 40, 20), 9000, 'Ruined watchtowers'),
    ('PL06', 'rock_arch_natural', 2, 'P2', 'plains', (60, 40, 24), 12000, 'Natural rock arches that carry paths over streams'),
    # ---- DS: desert wasteland ----
    ('DS01', 'adobe_house', 6, 'P2', 'desert', (20, 18, 20), 8000, 'Desert houses'),
    ('DS02', 'desert_market', 3, 'P2', 'desert', (24, 16, 18), 6000, 'Well, awning and stall sets'),
    ('DS03', 'caravan_wagon', 2, 'P2', 'desert', (18, 12, 10), 5000, 'Caravan wagons'),
    ('DS04', 'palm', 3, 'P2', 'desert', (14, 42, 14), 6000, 'Oasis palms'),
    ('DS05', 'oasis_rock_ring', 2, 'P2', 'desert', (50, 10, 50), 8000, 'Rocks around an oasis pool'),
    ('DS06', 'canyon_wall', 4, 'P2', 'desert', (120, 90, 40), 20000, 'Sandstone canyon walls (on top of the 3 existing R06)'),
    ('DS07', 'hoodoo_arch', 4, 'P2', 'desert', (40, 70, 30), 12000, 'Hoodoos and rock arches'),
    ('DS08', 'underground_entrance', 3, 'P2', 'desert', (30, 24, 30), 9000, 'Stair-down entrances to the underground'),
    # ---- CO: coast and sea ----
    ('CO01', 'coastal_cliff', 6, 'P1', 'coast', (110, 70, 50), 18000, 'Cliff pieces that replace the archived R04 grey boxes'),
    ('CO02', 'sea_stack', 3, 'P1', 'coast', (40, 90, 40), 14000, 'Sea stacks'),
    ('CO03', 'reef', 6, 'P2', 'coast', (30, 6, 30), 6000, 'Low reefs and sea rocks'),
    ('CO04', 'sea_arch', 2, 'P2', 'coast', (70, 60, 30), 14000, 'Sea arches'),
    ('CO05', 'ruin_islet', 3, 'P2', 'coast', (60, 40, 60), 16000, 'Small ruin islets'),
    # ---- RD: roads and environmental storytelling ----
    ('RD01', 'watchtower', 4, 'P2', 'roads', (20, 50, 20), 11000, 'Two intact and two ruined watchtowers'),
    ('RD02', 'camp_set', 6, 'P2', 'roads', (16, 10, 14), 4000, 'Tents x3, cooking rack, supply stack, bedroll'),
    ('RD03', 'waystation', 2, 'P2', 'roads', (30, 20, 24), 10000, 'Roadside waystations'),
    ('RD04', 'trading_post', 2, 'P2', 'roads', (30, 20, 24), 11000, 'Trading posts'),
    ('RD05', 'battlefield_prop', 5, 'P2', 'roads', (14, 10, 10), 3000, 'Broken ballista, cart, banner, spear rack, shield pile'),
    ('RD06', 'abandoned_house', 5, 'P2', 'roads', (22, 20, 20), 9000, 'Collapsed or burnt houses'),
    # ---- VG: vegetation variety (the "green carpet" fix) ----
    ('VG01', 'tree_tall_narrow', 3, 'P1', 'everywhere', (14, 46, 14), 9000, 'Poplar and beech, narrow crown'),
    ('VG02', 'tree_old_oak', 2, 'P1', 'everywhere', (30, 42, 30), 14000, 'Dark old oaks with a broken crown'),
    ('VG03', 'tree_flowering', 2, 'P1', 'everywhere', (22, 30, 22), 12000, 'Flowering trees'),
    ('VG04', 'tree_birch', 3, 'P2', 'everywhere', (14, 34, 14), 8000, 'Birch'),
    ('VG05', 'tree_cypress_swamp', 3, 'P2', 'plains', (22, 38, 22), 11000, 'Swamp cypress for marshland'),
    ('VG06', 'marsh_hummock', 2, 'P2', 'plains', (16, 6, 16), 3000, 'Grass hummocks'),
    ('VG07', 'boardwalk', 2, 'P2', 'plains', (30, 4, 6), 3000, 'Marsh boardwalk'),
    # ---- TW: Town 1 upgrades ----
    ('TW01', 'town1_hero_statue', 1, 'P2', 'town1', (14, 40, 14), 16000, 'Statue with a real face for the plaza'),
    ('TW02', 'street_life', 8, 'P2', 'town1', (12, 10, 10), 3000, 'Carts x2, crate stacks x2, barrel stack, hanging signs x2, bench'),
    # ---- RV: river and lake banks ----
    ('RV01', 'bank_rock', 4, 'P2', 'rivers', (30, 10, 20), 5000, 'Bank rocks for lakes and rivers'),
    # ---- VC: Skull City zone from the concept map (promoted to core on 30 Oct: "follow the top view") ----
    ('VC01', 'volcanic_rock', 8, 'P2', 'east_coast', (60, 60, 50), 12000, 'Dark volcanic rock formations (basalt colours; lava veins are terrain paint)'),
    ('VC02', 'skull_cliff_hero', 2, 'P1', 'east_coast', (200, 120, 120), 55000, 'Giant skull carved into a dark cliff, the Skull City landmark (own design)'),
    ('VC03', 'dark_fort_ruin', 3, 'P2', 'east_coast', (60, 50, 50), 16000, 'Dark fort ruins'),
    ('VC04', 'skull_city_building', 6, 'P2', 'east_coast', (30, 30, 30), 11000, 'Ruined dark-stone houses and halls for the forbidden city'),
    # ---- FL: floating islands from the concept map (promoted to P2) ----
    ('FL01', 'floating_island_hero', 3, 'P2', 'sea_edge', (90, 60, 90), 30000, 'Floating islands with a ruin'),
    ('FL02', 'floating_island_small', 3, 'P2', 'sea_edge', (40, 24, 40), 10000, 'Small floating rocks'),
    # ---- more rows so the world matches the concept map ----
    ('SP01', 'snow_spire_cluster', 6, 'P2', 'highlands', (60, 160, 60), 15000, 'Jagged snow-capped spires and ridgelines for the Frosthold massif (the concept map mountain)'),
    ('SD01', 'red_mesa_cluster', 6, 'P2', 'desert', (120, 90, 100), 16000, 'Orange-red mesa and butte clusters (the concept map desert)'),
    ('SD02', 'desert_ruin_block', 6, 'P2', 'desert', (40, 30, 40), 10000, 'Sand-worn ruined city blocks around the ring temple'),
    ('BR01', 'viaduct_bridge', 2, 'P2', 'roads', (160, 40, 20), 24000, 'Multi-arch stone viaduct across a valley (the long central bridge on the concept map)'),
    ('HB01', 'harbour_wall_tower', 3, 'P2', 'coast', (24, 40, 24), 10000, 'Towers for the walled port'),
    ('VL01', 'village_church_spire', 1, 'P2', 'plains', (30, 70, 40), 20000, 'Spired church for the west farm village (the concept map Rusty Village)'),
    # ---- RW: rework of existing models (not new) ----
    ('RW01', 'rework_existing', 4, 'P2', 'rework', (0, 0, 0), 0, 'R03_03 mesa (open lip top), F08_13 gate (thin dark seam), D01_02 and D01_04 treehouses (cut from 58k to 50k triangles)'),
    ('RW02', 'rework_world_tree_roots', 1, 'P1', 'rework', (0, 0, 0), 0, 'D05_02 world tree roots: rounded buttress roots tinted to the bright bark (reviewers: flat reddish fan, cardboard from above)'),
    # ---- added 30 Oct 10:40 after "elf must look better, the basic arch on every entry, capital, Town 1" ----
    # ---- NE: natural entrances (30 Oct 11:00; scope fixed 11:30: only the PLAIN ARCH family is removed, special gates such as the capital's and the fortress stay) ----
    ('NE01', 'village_sign', 6, 'P1', 'entrances', (10, 18, 4), 6000, 'One carved sign per settlement on a post or stone (Town 1, elf valley, alpine, rusty, harbour, desert village; the west village reuses the rusty sign set): the only marker at a natural entrance, no arch, no gate'),
    ('NE02', 'entry_rock_pair', 4, 'P2', 'entrances', (30, 14, 22), 5000, 'Large boulder pairs (mossy, frosted, sandstone, basalt) that frame a road where it meets a settlement'),
    ('EV01', 'elf_house_new', 8, 'P1', 'forest', (26, 30, 26), 14000, 'Eight new elf house types so the valley stops repeating three round houses: tall tower house, bridge house, library, healer hut, archery lodge, bathhouse, council hall, weavers hall (wood and stone, warm lantern hooks, no glow)'),
    ('EV02', 'canopy_cluster', 3, 'P1', 'forest', (70, 40, 70), 30000, 'Canopy village clusters: 3-4 platforms, rope bridges, small huts, ladders to the ground; for 90-140 studs up around the world tree'),
    ('EV03', 'elf_path_piece', 6, 'P2', 'forest', (20, 6, 20), 4000, 'Root stairs, carved steps, stone-and-root bridge, garden arch, path posts, plaza paving ring'),
    ('TW03', 'skull_avenue_set', 4, 'P2', 'town1', (14, 14, 14), 5000, 'Braziers x2 and banner poles x2 for the avenue from the skull HQ apron to the plaza'),
]

REUSE = [
    'bridges x11 (F08 x7, D04 x2, D09 plank x2)', 'windmills x2, barns x3, crop plots x6, scarecrows x3 (E08-E11)',
    'shrines and ruins x7 (E12 x4, F08 shrines x3), ruin arches x2, standing stones x2, statues x3 (D08)',
    'canyon walls x3 (R06), rock formations x11 (F07), rock faces x10 (E13), boulders x6 (E15), mesas x4 (R03)',
    'ancient trees x5, world tree x3, hollow tree, canopies x3 (D05)', 'waterfall cliffs x4 (D09 x2, R05 x2), frozen waterfall (C09)',
    'signposts x3, milestones x2, gate arches x2, story props x13, trail landmarks x9 (F08, F09, F11)',
    'houses: capital houses x6 (B07), chalets x6 (C01), round houses x3 (D04), rusty huts x6 (A04) - recolour and re-roof, not rebuilt',
    'trees: heartland x6, alpine x5, dry x3, coastal x4 (F01-F04); plants, logs, rocks, flowers (F05, F06, D06)',
]

prio_names = {'P1': 'core', 'P2': 'region completion', 'P3': 'optional'}
models = []
for code, base, count, prio, region, size, tris, desc in ROWS:
    for i in range(1, count + 1):
        name = '%s_%02d_%s' % (code, i, base) if count == 1 else '%s_%02d_%s_%02d' % (code, i, base, i)
        models.append({'id': name, 'row': code, 'base': base, 'prio': prio, 'region': region,
                       'size': list(size), 'tris': tris, 'rework': code.startswith('RW'), 'note': desc})

new = [m for m in models if not m['rework']]
by_prio = collections.Counter(m['prio'] for m in new)
by_region = collections.Counter(m['region'] for m in new)
by_region_prio = collections.defaultdict(collections.Counter)
for m in new:
    by_region_prio[m['region']][m['prio']] += 1
heroes = [m for m in new if m['tris'] >= 40000]
total_tris = sum(m['tris'] for m in new)
rework = sum(1 for m in models if m['rework'])

with open(os.path.join(HERE, 'V5_MANIFEST.json'), 'w', encoding='utf-8') as f:
    json.dump({'models': models, 'reuse': REUSE}, f, indent=1)
with open(os.path.join(HERE, 'V5_MANIFEST.csv'), 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f)
    w.writerow(['id', 'row', 'priority', 'region', 'size_x', 'size_y', 'size_z', 'tri_budget', 'rework', 'note'])
    for m in models:
        w.writerow([m['id'], m['row'], m['prio'], m['region'], *m['size'], m['tris'], 'yes' if m['rework'] else '', m['note']])

L = []
L.append('# V5 Blender manifest (new models for the world redesign)\n')
L.append('Generated by `v5_manifest.py`. Priority: P1 core, P2 region completion, P3 optional. Rules: no glow, original designs, everything anchored.\n')
L.append('## Totals\n')
L.append('| Scope | New models |\n|---|---|')
L.append('| P1 core | %d |' % by_prio['P1'])
L.append('| P1 + P2 (full regions) | %d |' % (by_prio['P1'] + by_prio['P2']))
L.append('| Everything incl. optional P3 | %d |' % len(new))
L.append('| Reworks of existing models (not new) | %d |' % rework)
L.append('| Hero models (40k+ triangles) | %d |' % len(heroes))
L.append('| Triangle budget, all new models | %d k |\n' % (total_tris // 1000))
L.append('## By region\n')
L.append('| Region | P1 | P2 | P3 | Total |\n|---|---|---|---|---|')
for r, n in sorted(by_region.items(), key=lambda kv: -kv[1]):
    c = by_region_prio[r]
    L.append('| %s | %d | %d | %d | %d |' % (r, c['P1'], c['P2'], c['P3'], n))
L.append('\n## Rows\n')
L.append('| Row | Model | Count | Prio | Region | Size (studs) | Tris each | Notes |\n|---|---|---|---|---|---|---|---|')
for code, base, count, prio, region, size, tris, desc in ROWS:
    L.append('| %s | %s | %d | %s | %s | %s | %s | %s |' % (code, base, count, prio, region, 'x'.join(map(str, size)) if tris else '-', tris if tris else '-', desc))
L.append('\n## Already covered by the existing 391 models (not rebuilt)\n')
for r in REUSE:
    L.append('- ' + r)
with open(os.path.join(HERE, 'V5_MANIFEST.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(L) + '\n')

print('NEW models: P1 %d | P2 %d | P3 %d | total %d | reworks %d | heroes(40k+) %d | tri budget %d k' % (
    by_prio['P1'], by_prio['P2'], by_prio['P3'], len(new), rework, len(heroes), total_tris // 1000))
print('P1+P2 =', by_prio['P1'] + by_prio['P2'])
for r, n in sorted(by_region.items(), key=lambda kv: -kv[1]):
    c = by_region_prio[r]
    print('  %-12s P1 %2d  P2 %3d  P3 %2d  total %3d' % (r, c['P1'], c['P2'], c['P3'], n))
print('P1 heroes:', ', '.join(m['base'] for m in heroes if m['prio'] == 'P1'))
