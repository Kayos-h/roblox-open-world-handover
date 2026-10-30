# V5 briefs: one entry per manifest row (P1 first)

Read `library/V5_STYLE_GUIDE.md` first. Every model: original design, no emissive or glowing parts, 1 Blender unit = 1 stud, each MeshPart at most 20k triangles, size within +-10% of the manifest, ids exactly as listed. Rows marked REWORK change an existing model.

### WT01 ×1 · P1 · highlands · 110 x 300 x 110 · up to 150,000 triangles each

- Ids: WT01_01_wizard_tower_shell
- What: Exterior of the giant wizard tower for the pad at (1380,-1320), floor y 324: Himalayan monastery base (whitewashed bands, tapered timber windows, stone buttresses) rising into a slim spiral-staggered stone spire with copper-green roofs; 10 MeshParts of at most 20k triangles (plinth, 8 stacked levels, crown); walls 6 studs thick so the inside is enterable
- Extra: READ plan_v5/WIZARD_TOWER_BRIEF.md first and follow it exactly (sections 2 and 3 for this row). 
- Palette (wizard): granite (176,172,180), limestone band (226,214,190), whitewash (238,234,226), ochre trim (196,150,76), red-brown timber (112,60,48), indigo slate roof (52,60,96), copper-green (92,150,128), brass (200,164,84), parchment (226,208,170), book spines in 12 muted colours
- Orientation: Building: entrance side faces -Y, pivot = centre of the footprint at ground (z=0). Enterable where the row says so: walls at least 4 studs thick, door openings 8 x 12, nothing narrower than 7 studs on a walking route.
- Queue: worker va, batch tower_shell, folder v5_wizard

### WT12 ×1 · P1 · highlands · 40 x 36 x 24 · up to 24,000 triangles each

- Ids: WT12_01_wizard_door_porch
- What: Entrance porch with big carved timber doors in a rectangular frame (not an arch), steps and lantern posts
- Extra: READ plan_v5/WIZARD_TOWER_BRIEF.md first and follow it exactly (sections 2 and 3 for this row). 
- Palette (wizard): granite (176,172,180), limestone band (226,214,190), whitewash (238,234,226), ochre trim (196,150,76), red-brown timber (112,60,48), indigo slate roof (52,60,96), copper-green (92,150,128), brass (200,164,84), parchment (226,208,170), book spines in 12 muted colours
- Orientation: Building: entrance side faces -Y, pivot = centre of the footprint at ground (z=0). Enterable where the row says so: walls at least 4 studs thick, door openings 8 x 12, nothing narrower than 7 studs on a walking route.
- Queue: worker va, batch tower_porch, folder v5_wizard

### WT11 ×1 · P1 · highlands · 70 x 50 x 70 · up to 22,000 triangles each

- Ids: WT11_01_wizard_armillary_crown
- What: Armillary rings around the crown of the tower (static; Studio can rotate them later)
- Extra: READ plan_v5/WIZARD_TOWER_BRIEF.md first and follow it exactly (sections 2 and 3 for this row). 
- Palette (wizard): granite (176,172,180), limestone band (226,214,190), whitewash (238,234,226), ochre trim (196,150,76), red-brown timber (112,60,48), indigo slate roof (52,60,96), copper-green (92,150,128), brass (200,164,84), parchment (226,208,170), book spines in 12 muted colours
- Orientation: Building: entrance side faces -Y, pivot = centre of the footprint at ground (z=0). Enterable where the row says so: walls at least 4 studs thick, door openings 8 x 12, nothing narrower than 7 studs on a walking route.
- Queue: worker va, batch tower_porch, folder v5_wizard

### WT02 ×1 · P1 · highlands · 100 x 280 x 100 · up to 90,000 triangles each

- Ids: WT02_01_wizard_tower_interior
- What: Interior shell: 8 floor plates, open central atrium, wide helical stair (rise at most 1.2, run at least 2), railings, wall linings, window reveals; plus tower_collision.json (boxes for floors, walls, stair treads) so Studio can build invisible collision
- Extra: READ plan_v5/WIZARD_TOWER_BRIEF.md first and follow it exactly (sections 2 and 3 for this row).  Export tower_collision.json (boxes in tower-local coordinates) next to the model.
- Palette (wizard): granite (176,172,180), limestone band (226,214,190), whitewash (238,234,226), ochre trim (196,150,76), red-brown timber (112,60,48), indigo slate roof (52,60,96), copper-green (92,150,128), brass (200,164,84), parchment (226,208,170), book spines in 12 muted colours
- Orientation: Interior prop: front faces -Y, pivot = centre of the footprint at the floor (z=0). Placed with Studio y_offset = floor height. Keep the back flat so it can sit against a curved wall.
- Queue: worker vb, batch interior_shell, folder v5_wizard

### WT05 ×1 · P1 · highlands · 44 x 12 x 44 · up to 60,000 triangles each

- Ids: WT05_01_wizard_round_map_table
- What: THE CIRCULAR MAP: a 44-stud round relief map of the whole island on a stone-and-brass table, built from the real terrain data (terrain_map.json) with tiny landmark models, a brass compass ring and a walkway rail; 3 MeshParts
- Extra: READ plan_v5/WIZARD_TOWER_BRIEF.md first and follow it exactly (sections 2 and 3 for this row).  Source data is ready: plan_v5/wizard_map_relief.obj (about 16k triangles, 44 studs across) and plan_v5/wizard_map_color.png; import them, then build the table, brass rings and landmark tokens around them.
- Palette (wizard): granite (176,172,180), limestone band (226,214,190), whitewash (238,234,226), ochre trim (196,150,76), red-brown timber (112,60,48), indigo slate roof (52,60,96), copper-green (92,150,128), brass (200,164,84), parchment (226,208,170), book spines in 12 muted colours
- Orientation: Interior prop: front faces -Y, pivot = centre of the footprint at the floor (z=0). Placed with Studio y_offset = floor height. Keep the back flat so it can sit against a curved wall.
- Queue: worker vb, batch map_table, folder v5_wizard

### WT06 ×1 · P1 · highlands · 80 x 1 x 80 · up to 8,000 triangles each

- Ids: WT06_01_wizard_floor_medallion
- What: Round floor inlay for the Map Hall: compass rose, star ring, inlaid stone and brass
- Extra: READ plan_v5/WIZARD_TOWER_BRIEF.md first and follow it exactly (sections 2 and 3 for this row). 
- Palette (wizard): granite (176,172,180), limestone band (226,214,190), whitewash (238,234,226), ochre trim (196,150,76), red-brown timber (112,60,48), indigo slate roof (52,60,96), copper-green (92,150,128), brass (200,164,84), parchment (226,208,170), book spines in 12 muted colours
- Orientation: Interior prop: front faces -Y, pivot = centre of the footprint at the floor (z=0). Placed with Studio y_offset = floor height. Keep the back flat so it can sit against a curved wall.
- Queue: worker vb, batch map_table, folder v5_wizard

### WT03 ×3 · P1 · highlands · 24 x 28 x 6 · up to 12,000 triangles each

- Ids: WT03_01_wizard_bookshelf_curved_01, WT03_02_wizard_bookshelf_curved_02, WT03_03_wizard_bookshelf_curved_03
- What: Full-height curved bookshelf bays that follow the round tower wall (radius 38, 30 and 22): packed books, scroll racks, glass-fronted cabinet, rolling-ladder rail
- Extra: READ plan_v5/WIZARD_TOWER_BRIEF.md first and follow it exactly (sections 2 and 3 for this row). 
- Palette (wizard): granite (176,172,180), limestone band (226,214,190), whitewash (238,234,226), ochre trim (196,150,76), red-brown timber (112,60,48), indigo slate roof (52,60,96), copper-green (92,150,128), brass (200,164,84), parchment (226,208,170), book spines in 12 muted colours
- Orientation: Interior prop: front faces -Y, pivot = centre of the footprint at the floor (z=0). Placed with Studio y_offset = floor height. Keep the back flat so it can sit against a curved wall.
- Queue: worker vb, batch shelves, folder v5_wizard

### WT04 ×2 · P1 · highlands · 14 x 26 x 5 · up to 10,000 triangles each

- Ids: WT04_01_wizard_bookshelf_straight_01, WT04_02_wizard_bookshelf_straight_02
- What: Straight bookshelf and a free-standing island shelf with ladder
- Extra: READ plan_v5/WIZARD_TOWER_BRIEF.md first and follow it exactly (sections 2 and 3 for this row). 
- Palette (wizard): granite (176,172,180), limestone band (226,214,190), whitewash (238,234,226), ochre trim (196,150,76), red-brown timber (112,60,48), indigo slate roof (52,60,96), copper-green (92,150,128), brass (200,164,84), parchment (226,208,170), book spines in 12 muted colours
- Orientation: Interior prop: front faces -Y, pivot = centre of the footprint at the floor (z=0). Placed with Studio y_offset = floor height. Keep the back flat so it can sit against a curved wall.
- Queue: worker vb, batch shelves, folder v5_wizard

### WT07 ×4 · P1 · highlands · 18 x 14 x 12 · up to 10,000 triangles each

- Ids: WT07_01_wizard_lab_set_01, WT07_02_wizard_lab_set_02, WT07_03_wizard_lab_set_03, WT07_04_wizard_lab_set_04
- What: Alchemy bench with glassware, herb rack with jars, specimen shelf, orrery and astrolabe stand
- Extra: READ plan_v5/WIZARD_TOWER_BRIEF.md first and follow it exactly (sections 2 and 3 for this row). 
- Palette (wizard): granite (176,172,180), limestone band (226,214,190), whitewash (238,234,226), ochre trim (196,150,76), red-brown timber (112,60,48), indigo slate roof (52,60,96), copper-green (92,150,128), brass (200,164,84), parchment (226,208,170), book spines in 12 muted colours
- Orientation: Interior prop: front faces -Y, pivot = centre of the footprint at the floor (z=0). Placed with Studio y_offset = floor height. Keep the back flat so it can sit against a curved wall.
- Queue: worker vb, batch furniture, folder v5_wizard

### WT08 ×3 · P1 · highlands · 18 x 12 x 14 · up to 9,000 triangles each

- Ids: WT08_01_wizard_study_set_01, WT08_02_wizard_study_set_02, WT08_03_wizard_study_set_03
- What: Archmage desk with open books and quill, bed alcove with drapes, globe and sea-chart stand
- Extra: READ plan_v5/WIZARD_TOWER_BRIEF.md first and follow it exactly (sections 2 and 3 for this row). 
- Palette (wizard): granite (176,172,180), limestone band (226,214,190), whitewash (238,234,226), ochre trim (196,150,76), red-brown timber (112,60,48), indigo slate roof (52,60,96), copper-green (92,150,128), brass (200,164,84), parchment (226,208,170), book spines in 12 muted colours
- Orientation: Interior prop: front faces -Y, pivot = centre of the footprint at the floor (z=0). Placed with Studio y_offset = floor height. Keep the back flat so it can sit against a curved wall.
- Queue: worker vb, batch furniture, folder v5_wizard

### WT09 ×2 · P1 · highlands · 20 x 8 x 20 · up to 6,000 triangles each

- Ids: WT09_01_wizard_chandelier_ring_01, WT09_02_wizard_chandelier_ring_02
- What: Ring chandeliers with candles (warm light only, no glow)
- Extra: READ plan_v5/WIZARD_TOWER_BRIEF.md first and follow it exactly (sections 2 and 3 for this row). 
- Palette (wizard): granite (176,172,180), limestone band (226,214,190), whitewash (238,234,226), ochre trim (196,150,76), red-brown timber (112,60,48), indigo slate roof (52,60,96), copper-green (92,150,128), brass (200,164,84), parchment (226,208,170), book spines in 12 muted colours
- Orientation: Interior prop: front faces -Y, pivot = centre of the footprint at the floor (z=0). Placed with Studio y_offset = floor height. Keep the back flat so it can sit against a curved wall.
- Queue: worker vb, batch furniture, folder v5_wizard

### WT10 ×1 · P1 · highlands · 14 x 24 x 14 · up to 20,000 triangles each

- Ids: WT10_01_wizard_observatory_telescope
- What: Giant brass telescope on a mount for the top dome
- Extra: READ plan_v5/WIZARD_TOWER_BRIEF.md first and follow it exactly (sections 2 and 3 for this row). 
- Palette (wizard): granite (176,172,180), limestone band (226,214,190), whitewash (238,234,226), ochre trim (196,150,76), red-brown timber (112,60,48), indigo slate roof (52,60,96), copper-green (92,150,128), brass (200,164,84), parchment (226,208,170), book spines in 12 muted colours
- Orientation: Interior prop: front faces -Y, pivot = centre of the footprint at the floor (z=0). Placed with Studio y_offset = floor height. Keep the back flat so it can sit against a curved wall.
- Queue: worker vb, batch furniture, folder v5_wizard

### HM01 ×3 · P1 · highlands · 120 x 14 x 10 · up to 12,000 triangles each

- Ids: HM01_01_rope_suspension_bridge_01, HM01_02_rope_suspension_bridge_02, HM01_03_rope_suspension_bridge_03
- What: Himalayan rope-and-plank suspension bridges with stone anchor towers and prayer flags, three spans (60, 90, 116 studs); the 116 crosses Frost Gorge; walkable deck, hand ropes
- Extra: Himalayan rope-and-plank suspension bridges in three spans (60, 90, 116 studs): stone anchor towers at both ends, plank deck 7 wide, two hand ropes, prayer flags on the ropes. The 116 crosses Frost Gorge.
- Palette (himalaya): weathered grey stone (128,124,120), dark slate (84,86,96), snow (240,244,250), ice (196,226,242), weathered timber (112,92,70), rope (176,150,104), cloth flags in this order: blue (60,120,200), white (250,250,250), red (200,60,50), green (60,160,90), yellow (240,200,60)
- Orientation: Long axis along X (like the library bridges). Pivot = centre of the footprint, bottom at z=0. Add markers `end_a`, `end_b` and `deck` (deck centreline height) with v4util.marker where the row is a bridge or walkway.
- Queue: worker vc, batch bridges, folder v5_himalaya

### HM03 ×3 · P1 · highlands · 30 x 24 x 20 · up to 12,000 triangles each

- Ids: HM03_01_tunnel_portal_01, HM03_02_tunnel_portal_02, HM03_03_tunnel_portal_03
- What: Rock-cut road tunnel mouths (plain, snow-capped, timber-framed): a rectangular timber frame set in a rock face, not a freestanding arch
- Extra: Rock-cut road tunnel mouths: plain, snow-capped, timber-framed. A rectangular timber frame set in a 40-stud-wide rock face that blends into terrain. Not a freestanding arch.
- Palette (himalaya): weathered grey stone (128,124,120), dark slate (84,86,96), snow (240,244,250), ice (196,226,242), weathered timber (112,92,70), rope (176,150,104), cloth flags in this order: blue (60,120,200), white (250,250,250), red (200,60,50), green (60,160,90), yellow (240,200,60)
- Orientation: The passage runs along Y; the opening faces -Y (front). Clear passage 14 wide x 16 high. Pivot = centre of the opening at ground.
- Queue: worker vc, batch tunnels, folder v5_himalaya

### HM04 ×2 · P1 · highlands · 24 x 20 x 24 · up to 8,000 triangles each

- Ids: HM04_01_tunnel_lining_01, HM04_02_tunnel_lining_02
- What: Tunnel lining segments (24-stud straight, 30-degree bend) with rock walls, timber ribs and lantern brackets (warm, no glow)
- Extra: Tunnel lining segments, 24 studs: straight and a 30-degree bend. Rock walls, timber ribs every 8 studs, lantern brackets (warm, unlit).
- Palette (himalaya): weathered grey stone (128,124,120), dark slate (84,86,96), snow (240,244,250), ice (196,226,242), weathered timber (112,92,70), rope (176,150,104), cloth flags in this order: blue (60,120,200), white (250,250,250), red (200,60,50), green (60,160,90), yellow (240,200,60)
- Orientation: The passage runs along Y; the opening faces -Y (front). Clear passage 14 wide x 16 high. Pivot = centre of the opening at ground.
- Queue: worker vc, batch tunnels, folder v5_himalaya

### NE01 ×6 · P1 · entrances · 10 x 18 x 4 · up to 6,000 triangles each

- Ids: NE01_01_village_sign_01, NE01_02_village_sign_02, NE01_03_village_sign_03, NE01_04_village_sign_04, NE01_05_village_sign_05, NE01_06_village_sign_06
- What: One carved sign per settlement on a post or stone (Town 1, elf valley, alpine, rusty, harbour, desert village; the west village reuses the rusty sign set): the only marker at a natural entrance, no arch, no gate
- Extra: One carved sign per settlement (post or stone), 10 x 18 x 4. Town 1: stone slab with a carved jaw motif and iron bracket. Elf: living-wood board on a root post. Alpine: log post with a snow cap and a small bell. Rusty: salvage plate on sandstone. Harbour: whitewashed board with an anchor and rope. Desert village: painted clay slab on a beam. No arch, no gate.
- Palette (entrance): carve each sign in the palette of its settlement: Town 1 dark stone and iron; elf living wood; alpine log and snow; rusty salvage plate on sandstone; harbour whitewashed board with rope; desert painted clay on timber
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vc, batch signs, folder v5_entrances

### CP01 ×3 · P1 · capital · 40 x 20 x 10 · up to 9,000 triangles each

- Ids: CP01_01_ring_wall_straight_01, CP01_02_ring_wall_straight_02, CP01_03_ring_wall_straight_03
- What: 40-stud wall segments (plain, arrow slits, buttressed); 8-stud wide red-brown wall-walk, white-capped inner parapet, crenellated outer edge; replaces B02_05
- Extra: 8-stud wide wall-walk with a red-brown deck, white-capped inner parapet, crenellated outer edge. Variants: a) plain, b) arrow slits, c) buttressed. 40 studs long, ends square so segments butt against towers and corners.
- Palette (capital): plaster (232,214,188), timber (112,80,60), roofs orange-red (198,88,52) (214,104,58) (178,72,46) with (140,62,48) accents, stone grey-lilac (150,142,158), cone roofs maroon (120,44,52), wall-walk deck (150,88,70), parapet cap (232,226,230)
- Orientation: Long axis along X (like the library bridges). Pivot = centre of the footprint, bottom at z=0. Add markers `end_a`, `end_b` and `deck` (deck centreline height) with v4util.marker where the row is a bridge or walkway.
- Queue: worker vd, batch walls_towers, folder v5_capital

### CP02 ×3 · P1 · capital · 24 x 22 x 24 · up to 12,000 triangles each

- Ids: CP02_01_ring_wall_corner_01, CP02_02_ring_wall_corner_02, CP02_03_ring_wall_corner_03
- What: Polygon joints of 135, 90 and 150 degrees with a tower seat; replaces B02_06
- Extra: Polygon joints at 135, 90 and 150 degrees with a round tower seat (socket radius 11). Wall-walk continues through the corner.
- Palette (capital): plaster (232,214,188), timber (112,80,60), roofs orange-red (198,88,52) (214,104,58) (178,72,46) with (140,62,48) accents, stone grey-lilac (150,142,158), cone roofs maroon (120,44,52), wall-walk deck (150,88,70), parapet cap (232,226,230)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vd, batch walls_towers, folder v5_capital

### CP03 ×2 · P1 · capital · 20 x 20 x 14 · up to 7,000 triangles each

- Ids: CP03_01_ring_wall_stair_end_01, CP03_02_ring_wall_stair_end_02
- What: Stair up to the wall-walk and a wall end cap
- Extra: Stone stair from ground up to the wall-walk (height 20) with a railing, built against the inner face; ends flush with a wall segment.
- Palette (capital): plaster (232,214,188), timber (112,80,60), roofs orange-red (198,88,52) (214,104,58) (178,72,46) with (140,62,48) accents, stone grey-lilac (150,142,158), cone roofs maroon (120,44,52), wall-walk deck (150,88,70), parapet cap (232,226,230)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vd, batch walls_towers, folder v5_capital

### CP04 ×4 · P1 · capital · 22 x 48 x 22 · up to 14,000 triangles each

- Ids: CP04_01_tower_round_cone_01, CP04_02_tower_round_cone_02, CP04_03_tower_round_cone_03, CP04_04_tower_round_cone_04
- What: Round towers in 4 sizes (16, 22, 28, 34 studs wide) with maroon cone roofs and slit windows
- Extra: Round towers 16, 22, 28 and 34 studs wide: slit windows, a string course, maroon cone roof (120,44,52) with a small finial. Open bottom, no floor.
- Palette (capital): plaster (232,214,188), timber (112,80,60), roofs orange-red (198,88,52) (214,104,58) (178,72,46) with (140,62,48) accents, stone grey-lilac (150,142,158), cone roofs maroon (120,44,52), wall-walk deck (150,88,70), parapet cap (232,226,230)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vd, batch walls_towers, folder v5_capital

### CP05 ×2 · P1 · capital · 14 x 26 x 14 · up to 8,000 triangles each

- Ids: CP05_01_turret_crenellated_01, CP05_02_turret_crenellated_02
- What: Round crenellated turrets for the outer ring (the foreground silhouette in the reference)
- Extra: none beyond the style guide
- Palette (capital): plaster (232,214,188), timber (112,80,60), roofs orange-red (198,88,52) (214,104,58) (178,72,46) with (140,62,48) accents, stone grey-lilac (150,142,158), cone roofs maroon (120,44,52), wall-walk deck (150,88,70), parapet cap (232,226,230)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vd, batch walls_towers, folder v5_capital

### CP06 ×2 · P1 · capital · 30 x 52 x 30 · up to 16,000 triangles each

- Ids: CP06_01_gate_flank_tower_01, CP06_02_gate_flank_tower_02
- What: Twin towers that flank the main gatehouse
- Extra: Twin towers that flank the main gatehouse: machicolated top, banner mounts, slit windows, cone roof.
- Palette (capital): plaster (232,214,188), timber (112,80,60), roofs orange-red (198,88,52) (214,104,58) (178,72,46) with (140,62,48) accents, stone grey-lilac (150,142,158), cone roofs maroon (120,44,52), wall-walk deck (150,88,70), parapet cap (232,226,230)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vd, batch walls_towers, folder v5_capital

### CP07 ×1 · P1 · capital · 60 x 56 x 40 · up to 30,000 triangles each

- Ids: CP07_01_gatehouse_main
- What: Portcullis arch, banner mounts, walkable passage; replaces B02_07
- Extra: Gatehouse built into the ring wall: passage 18 wide x 22 high, raised portcullis as a separate mesh, two machicolated bays, banner mounts, crenellated top, walkable passage with a clear collision gap. Replaces the old C04/K08/B02_07 gates.
- Palette (capital): plaster (232,214,188), timber (112,80,60), roofs orange-red (198,88,52) (214,104,58) (178,72,46) with (140,62,48) accents, stone grey-lilac (150,142,158), cone roofs maroon (120,44,52), wall-walk deck (150,88,70), parapet cap (232,226,230)
- Orientation: Building: entrance side faces -Y, pivot = centre of the footprint at ground (z=0). Enterable where the row says so: walls at least 4 studs thick, door openings 8 x 12, nothing narrower than 7 studs on a walking route.
- Queue: worker vd, batch gates_keep, folder v5_capital

### CP08 ×1 · P1 · capital · 40 x 30 x 30 · up to 18,000 triangles each

- Ids: CP08_01_water_gate
- What: Arched river gate where the capital river passes under the wall
- Extra: River gate where the capital river passes under the wall: water passage 20 wide, iron grille as a separate mesh, quay steps either side.
- Palette (capital): plaster (232,214,188), timber (112,80,60), roofs orange-red (198,88,52) (214,104,58) (178,72,46) with (140,62,48) accents, stone grey-lilac (150,142,158), cone roofs maroon (120,44,52), wall-walk deck (150,88,70), parapet cap (232,226,230)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vd, batch gates_keep, folder v5_capital

### CP09 ×1 · P1 · capital · 130 x 120 x 110 · up to 50,000 triangles each

- Ids: CP09_01_keep_terrace_hero
- What: Grey stone keep with 8+ turrets and cone roofs on a raised terrace at the back of the enclosure; replaces the B02_01 silhouette
- Extra: Keep on the castle terrace: stepped massing with a central tower, four corner and four mid turrets with cone roofs, buttresses, arched windows, balconies, portcullis gate at the base. Must NOT look like the old B02_01 keep.
- Palette (capital): plaster (232,214,188), timber (112,80,60), roofs orange-red (198,88,52) (214,104,58) (178,72,46) with (140,62,48) accents, stone grey-lilac (150,142,158), cone roofs maroon (120,44,52), wall-walk deck (150,88,70), parapet cap (232,226,230)
- Orientation: Building: entrance side faces -Y, pivot = centre of the footprint at ground (z=0). Enterable where the row says so: walls at least 4 studs thick, door openings 8 x 12, nothing narrower than 7 studs on a walking route.
- Queue: worker vd, batch gates_keep, folder v5_capital

### CP10 ×2 · P1 · capital · 60 x 70 x 50 · up to 28,000 triangles each

- Ids: CP10_01_keep_wing_01, CP10_02_keep_wing_02
- What: Wings that widen the keep silhouette
- Extra: Wings that flank the keep, same family and palette as the keep, lower roofline, covered walkway to the keep.
- Palette (capital): plaster (232,214,188), timber (112,80,60), roofs orange-red (198,88,52) (214,104,58) (178,72,46) with (140,62,48) accents, stone grey-lilac (150,142,158), cone roofs maroon (120,44,52), wall-walk deck (150,88,70), parapet cap (232,226,230)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vd, batch gates_keep, folder v5_capital

### CP12 ×2 · P1 · capital · 40 x 22 x 10 · up to 8,000 triangles each

- Ids: CP12_01_terrace_retaining_wall_01, CP12_02_terrace_retaining_wall_02
- What: Straight and curved retaining wall under the keep terrace, grassy top
- Extra: Retaining wall for the castle terrace: buttressed stone, 40 studs long, parapet on top, drain spouts.
- Palette (capital): plaster (232,214,188), timber (112,80,60), roofs orange-red (198,88,52) (214,104,58) (178,72,46) with (140,62,48) accents, stone grey-lilac (150,142,158), cone roofs maroon (120,44,52), wall-walk deck (150,88,70), parapet cap (232,226,230)
- Orientation: Long axis along X (like the library bridges). Pivot = centre of the footprint, bottom at z=0. Add markers `end_a`, `end_b` and `deck` (deck centreline height) with v4util.marker where the row is a bridge or walkway.
- Queue: worker vd, batch terrace_skyline, folder v5_capital

### CP13 ×2 · P1 · capital · 30 x 22 x 40 · up to 9,000 triangles each

- Ids: CP13_01_grand_stair_01, CP13_02_grand_stair_02
- What: Wide stair from the gate court up the terrace, plus a narrow side stair
- Extra: Grand stair with landings and a balustrade, rise at most 1.2, run at least 2.2, 30 studs wide.
- Palette (capital): plaster (232,214,188), timber (112,80,60), roofs orange-red (198,88,52) (214,104,58) (178,72,46) with (140,62,48) accents, stone grey-lilac (150,142,158), cone roofs maroon (120,44,52), wall-walk deck (150,88,70), parapet cap (232,226,230)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vd, batch terrace_skyline, folder v5_capital

### CP14 ×5 · P1 · capital · 30 x 110 x 30 · up to 30,000 triangles each

- Ids: CP14_01_skyline_tower_01, CP14_02_skyline_tower_02, CP14_03_skyline_tower_03, CP14_04_skyline_tower_04, CP14_05_skyline_tower_05
- What: Five different tall towers: clock, bell, observatory, beacon (unlit), water tower
- Extra: Five different skyline towers, each a clear silhouette from 800 studs: clock tower (faces on four sides), bell tower (open belfry), observatory (dome with slit), beacon tower (open brazier cage, no glow), water tower (tank on stone legs). 110 tall.
- Palette (capital): plaster (232,214,188), timber (112,80,60), roofs orange-red (198,88,52) (214,104,58) (178,72,46) with (140,62,48) accents, stone grey-lilac (150,142,158), cone roofs maroon (120,44,52), wall-walk deck (150,88,70), parapet cap (232,226,230)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vd, batch terrace_skyline, folder v5_capital

### CP15 ×3 · P1 · capital · 90 x 60 x 70 · up to 40,000 triangles each

- Ids: CP15_01_order_hq_01, CP15_02_order_hq_02, CP15_03_order_hq_03
- What: Knights-order headquarters (own name and shape, not copied) plus 2 annex buildings
- Extra: Order headquarters: wide hall with two wings and a banner tower, own name, own heraldry, no Black Clover shapes. Three variants: main hall and two annexes that sit beside it.
- Palette (capital): plaster (232,214,188), timber (112,80,60), roofs orange-red (198,88,52) (214,104,58) (178,72,46) with (140,62,48) accents, stone grey-lilac (150,142,158), cone roofs maroon (120,44,52), wall-walk deck (150,88,70), parapet cap (232,226,230)
- Orientation: Building: entrance side faces -Y, pivot = centre of the footprint at ground (z=0). Enterable where the row says so: walls at least 4 studs thick, door openings 8 x 12, nothing narrower than 7 studs on a walking route.
- Queue: worker vd, batch terrace_skyline, folder v5_capital

### CP19 ×2 · P1 · capital · 60 x 28 x 26 · up to 26,000 triangles each

- Ids: CP19_01_grand_bridge_01, CP19_02_grand_bridge_02
- What: Towered stone bridge over the capital river, and a drawbridge
- Extra: Towered stone bridge for the capital river: two gate towers, cobbled deck 14 wide, parapets, long axis X.
- Palette (capital): plaster (232,214,188), timber (112,80,60), roofs orange-red (198,88,52) (214,104,58) (178,72,46) with (140,62,48) accents, stone grey-lilac (150,142,158), cone roofs maroon (120,44,52), wall-walk deck (150,88,70), parapet cap (232,226,230)
- Orientation: Long axis along X (like the library bridges). Pivot = centre of the footprint, bottom at z=0. Add markers `end_a`, `end_b` and `deck` (deck centreline height) with v4util.marker where the row is a bridge or walkway.
- Queue: worker vd, batch terrace_skyline, folder v5_capital

### EV01 ×8 · P1 · forest · 26 x 30 x 26 · up to 14,000 triangles each

- Ids: EV01_01_elf_house_new_01, EV01_02_elf_house_new_02, EV01_03_elf_house_new_03, EV01_04_elf_house_new_04, EV01_05_elf_house_new_05, EV01_06_elf_house_new_06, EV01_07_elf_house_new_07, EV01_08_elf_house_new_08
- What: Eight new elf house types so the valley stops repeating three round houses: tall tower house, bridge house, library, healer hut, archery lodge, bathhouse, council hall, weavers hall (wood and stone, warm lantern hooks, no glow)
- Extra: Eight house types: tall tower house, bridge house, library, healer hut, archery lodge, bathhouse, council hall, weavers hall. Wood and stone, warm lantern hooks, NO glow, ladder or stairs to the ground on anything raised.
- Palette (elf): living wood (140,104,70), pale bark (176,150,112), moss (86,130,70), leaf greens (70,120,60) (104,150,80), warm stone (150,140,120), shingle teal-green (80,120,100); lantern light only, no glow
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker ve, batch elf_houses, folder v5_elf

### EV02 ×3 · P1 · forest · 70 x 40 x 70 · up to 30,000 triangles each

- Ids: EV02_01_canopy_cluster_01, EV02_02_canopy_cluster_02, EV02_03_canopy_cluster_03
- What: Canopy village clusters: 3-4 platforms, rope bridges, small huts, ladders to the ground; for 90-140 studs up around the world tree
- Extra: Canopy clusters 90-140 studs up: 3-4 platforms, rope bridges, small huts, ladders to the ground (markers ladder_bottom / ladder_top). Natural, no glow.
- Palette (elf): living wood (140,104,70), pale bark (176,150,112), moss (86,130,70), leaf greens (70,120,60) (104,150,80), warm stone (150,140,120), shingle teal-green (80,120,100); lantern light only, no glow
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker ve, batch canopy_roots, folder v5_elf

### RW02 ×1 · P1 · rework · 0 x 0 x 0 · up to 0 triangles each

- Ids: RW02_01_rework_world_tree_roots
- What: D05_02 world tree roots: rounded buttress roots tinted to the bright bark (reviewers: flat reddish fan, cardboard from above)
- Extra: REWORK of D05_02 world tree roots: 8-10 rounded buttress roots, soft taper, bright bark tinted like the trunk, moss patches. Keep the old footprint so the export replaces the old mesh in place.
- Palette (elf): living wood (140,104,70), pale bark (176,150,112), moss (86,130,70), leaf greens (70,120,60) (104,150,80), warm stone (150,140,120), shingle teal-green (80,120,100); lantern light only, no glow
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker ve, batch canopy_roots, folder v5_elf

### LM03 ×1 · P1 · highlands · 300 x 220 x 260 · up to 60,000 triangles each

- Ids: LM03_01_frost_fortress_hero
- What: Fortress built into a snowy mountain flank (own name and design)
- Extra: Frosthold fortress built into a snowy mountain flank (own name and design): terraced ramparts, cliff towers, gate tunnel, no copied shapes.
- Palette (himalaya): weathered grey stone (128,124,120), dark slate (84,86,96), snow (240,244,250), ice (196,226,242), weathered timber (112,92,70), rope (176,150,104), cloth flags in this order: blue (60,120,200), white (250,250,250), red (200,60,50), green (60,160,90), yellow (240,200,60)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vf, batch heroes_a, folder v5_landmarks

### LM22 ×1 · P1 · forest · 240 x 260 x 120 · up to 60,000 triangles each

- Ids: LM22_01_colossal_fall_cliff_hero
- What: Colossal multi-fall cliff for the river valley
- Extra: Colossal waterfall cliff for the elf valley west rim, 240 wide: three tiers with ledges and pools; the water is added in Studio.
- Palette (forest): bark (96,74,56), moss (86,130,70), fern green (70,120,60), ancient stone (130,126,118), root brown (110,80,58)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vf, batch heroes_a, folder v5_landmarks

### LM25 ×1 · P1 · plains · 90 x 80 x 30 · up to 40,000 triangles each

- Ids: LM25_01_ruin_gate_hero
- What: Gate of the ancient civilization, half collapsed
- Extra: Gate of the ancient civilization, half collapsed: massive pillars and a broken lintel.
- Palette (plains): whitewash (236,226,206), terracotta roof (206,120,84), thatch (190,160,100), timber (112,80,60), field stone (150,142,128), hay (214,190,110)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vf, batch heroes_a, folder v5_landmarks

### LM30 ×1 · P1 · plains · 140 x 70 x 120 · up to 50,000 triangles each

- Ids: LM30_01_ruined_castle_hero
- What: Ruined castle with a broken keep
- Extra: Ruined castle with a broken keep, 140 wide, open to the sky.
- Palette (plains): whitewash (236,226,206), terracotta roof (206,120,84), thatch (190,160,100), timber (112,80,60), field stone (150,142,128), hay (214,190,110)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vf, batch heroes_a, folder v5_landmarks

### LM09 ×1 · P1 · desert · 180 x 90 x 160 · up to 55,000 triangles each

- Ids: LM09_01_temple_buried_hero
- What: Desert temple half buried in sand: the top third and one gate show
- Extra: Buried temple, half under sand: stepped entrance down, colonnade, guardian statues nearby. Sandstone, no glow.
- Palette (desert): sandstone (214,150,90), red mesa (172,92,56), pale sand (226,200,150), adobe (200,150,106), clay (176,112,76), bleached bone (224,216,196), dark timber (92,70,52)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vf, batch heroes_b, folder v5_landmarks

### LM15 ×1 · P1 · desert · 220 x 60 x 220 · up to 55,000 triangles each

- Ids: LM15_01_ring_temple_hero
- What: Circular ring temple with an inner sanctum (from the concept map)
- Extra: Ring temple: a great stone ring with an inner sanctum, 220 across, worn by wind.
- Palette (desert): sandstone (214,150,90), red mesa (172,92,56), pale sand (226,200,150), adobe (200,150,106), clay (176,112,76), bleached bone (224,216,196), dark timber (92,70,52)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vf, batch heroes_b, folder v5_landmarks

### LM18 ×1 · P1 · centre · 140 x 50 x 140 · up to 40,000 triangles each

- Ids: LM18_01_crater_monolith_ring
- What: Ring of carved standing stones around the crater rim (non-emissive)
- Extra: Crater monolith ring: 12 tall carved stones around a bowl, pale runes carved not glowing.
- Palette (arcane): floating rock (118,116,122), moss, pale runes carved (no glow), ancient stone (130,126,118)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vf, batch heroes_b, folder v5_landmarks

### VC02 ×2 · P1 · east_coast · 200 x 120 x 120 · up to 55,000 triangles each

- Ids: VC02_01_skull_cliff_hero_01, VC02_02_skull_cliff_hero_02
- What: Giant skull carved into a dark cliff, the Skull City landmark (own design)
- Extra: Giant skull carved into a dark cliff, the Skull City landmark (own design, not a copy of any film skull): hollow eye caves, jaw as a gate, 200 wide. Two sites: the main cliff and a smaller one on the east coast.
- Palette (skull): basalt (54,50,58), ash grey (96,92,100), cracked-lava rock (70,56,60), bone (224,216,196), rust iron (122,62,36); no glow (lava veins are terrain paint)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vf, batch skull, folder v5_skull

### VG01 ×3 · P1 · everywhere · 14 x 46 x 14 · up to 9,000 triangles each

- Ids: VG01_01_tree_tall_narrow_01, VG01_02_tree_tall_narrow_02, VG01_03_tree_tall_narrow_03
- What: Poplar and beech, narrow crown
- Extra: Poplar and beech, narrow crown, 3 silhouettes.
- Palette (trees): poplar and beech leaf greens (90,140,70) (120,160,80); old oak dark (52,92,50) with bark (80,62,48); blossom white (244,232,236) and pink (232,176,196); birch bark (232,228,220)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vf, batch trees, folder v5_forest

### VG02 ×2 · P1 · everywhere · 30 x 42 x 30 · up to 14,000 triangles each

- Ids: VG02_01_tree_old_oak_01, VG02_02_tree_old_oak_02
- What: Dark old oaks with a broken crown
- Extra: Dark old oaks with a broken crown, 2 silhouettes.
- Palette (trees): poplar and beech leaf greens (90,140,70) (120,160,80); old oak dark (52,92,50) with bark (80,62,48); blossom white (244,232,236) and pink (232,176,196); birch bark (232,228,220)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vf, batch trees, folder v5_forest

### VG03 ×2 · P1 · everywhere · 22 x 30 x 22 · up to 12,000 triangles each

- Ids: VG03_01_tree_flowering_01, VG03_02_tree_flowering_02
- What: Flowering trees
- Extra: Flowering trees, 2 species (white blossom, pink blossom).
- Palette (trees): poplar and beech leaf greens (90,140,70) (120,160,80); old oak dark (52,92,50) with bark (80,62,48); blossom white (244,232,236) and pink (232,176,196); birch bark (232,228,220)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vf, batch trees, folder v5_forest

### CO01 ×6 · P1 · coast · 110 x 70 x 50 · up to 18,000 triangles each

- Ids: CO01_01_coastal_cliff_01, CO01_02_coastal_cliff_02, CO01_03_coastal_cliff_03, CO01_04_coastal_cliff_04, CO01_05_coastal_cliff_05, CO01_06_coastal_cliff_06
- What: Cliff pieces that replace the archived R04 grey boxes
- Extra: Coastal cliff pieces to replace the archived grey box cliffs: layered rock, ledges, sea-cut notches, 110 wide.
- Palette (coast): sea rock (110,108,110), wet stone (84,88,92), barnacle white (210,206,196), harbour white (238,238,240), harbour blue (92,128,176), brick red (190,90,70)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vf, batch coast, folder v5_coast

### CO02 ×3 · P1 · coast · 40 x 90 x 40 · up to 14,000 triangles each

- Ids: CO02_01_sea_stack_01, CO02_02_sea_stack_02, CO02_03_sea_stack_03
- What: Sea stacks
- Extra: Sea stacks, three silhouettes, 90 tall.
- Palette (coast): sea rock (110,108,110), wet stone (84,88,92), barnacle white (210,206,196), harbour white (238,238,240), harbour blue (92,128,176), brick red (190,90,70)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vf, batch coast, folder v5_coast

### WT13 ×6 · P2 · highlands · 30 x 10 x 30 · up to 7,000 triangles each

- Ids: WT13_01_plateau_terrace_set_01, WT13_02_plateau_terrace_set_02, WT13_03_plateau_terrace_set_03, WT13_04_plateau_terrace_set_04, WT13_05_plateau_terrace_set_05, WT13_06_plateau_terrace_set_06
- What: Terrace retaining wall x2, 40-step stair, prayer-flag pole, cairn and lantern post around the tower
- Extra: READ plan_v5/WIZARD_TOWER_BRIEF.md first and follow it exactly (sections 2 and 3 for this row). 
- Palette (wizard): granite (176,172,180), limestone band (226,214,190), whitewash (238,234,226), ochre trim (196,150,76), red-brown timber (112,60,48), indigo slate roof (52,60,96), copper-green (92,150,128), brass (200,164,84), parchment (226,208,170), book spines in 12 muted colours
- Orientation: Building: entrance side faces -Y, pivot = centre of the footprint at ground (z=0). Enterable where the row says so: walls at least 4 studs thick, door openings 8 x 12, nothing narrower than 7 studs on a walking route.
- Queue: worker va, batch tower_terrace, folder v5_wizard

### HM02 ×2 · P2 · highlands · 36 x 12 x 10 · up to 10,000 triangles each

- Ids: HM02_01_timber_cantilever_bridge_01, HM02_02_timber_cantilever_bridge_02
- What: Timber cantilever bridges with a small roof, spans 28 and 40 (tarn outlet, mountain streams)
- Extra: none beyond the style guide
- Palette (himalaya): weathered grey stone (128,124,120), dark slate (84,86,96), snow (240,244,250), ice (196,226,242), weathered timber (112,92,70), rope (176,150,104), cloth flags in this order: blue (60,120,200), white (250,250,250), red (200,60,50), green (60,160,90), yellow (240,200,60)
- Orientation: Long axis along X (like the library bridges). Pivot = centre of the footprint, bottom at z=0. Add markers `end_a`, `end_b` and `deck` (deck centreline height) with v4util.marker where the row is a bridge or walkway.
- Queue: worker vc, batch road_extras, folder v5_himalaya

### HM05 ×2 · P2 · highlands · 40 x 22 x 14 · up to 9,000 triangles each

- Ids: HM05_01_cliff_gallery_01, HM05_02_cliff_gallery_02
- What: Road galleries cut into a cliff with timber props and a rock roof
- Extra: none beyond the style guide
- Palette (himalaya): weathered grey stone (128,124,120), dark slate (84,86,96), snow (240,244,250), ice (196,226,242), weathered timber (112,92,70), rope (176,150,104), cloth flags in this order: blue (60,120,200), white (250,250,250), red (200,60,50), green (60,160,90), yellow (240,200,60)
- Orientation: Long axis along X (like the library bridges). Pivot = centre of the footprint, bottom at z=0. Add markers `end_a`, `end_b` and `deck` (deck centreline height) with v4util.marker where the row is a bridge or walkway.
- Queue: worker vc, batch road_extras, folder v5_himalaya

### HM06 ×3 · P2 · highlands · 30 x 14 x 14 · up to 7,000 triangles each

- Ids: HM06_01_switchback_wall_01, HM06_02_switchback_wall_02, HM06_03_switchback_wall_03
- What: Stone retaining walls and hairpin corners for mountain roads
- Extra: none beyond the style guide
- Palette (himalaya): weathered grey stone (128,124,120), dark slate (84,86,96), snow (240,244,250), ice (196,226,242), weathered timber (112,92,70), rope (176,150,104), cloth flags in this order: blue (60,120,200), white (250,250,250), red (200,60,50), green (60,160,90), yellow (240,200,60)
- Orientation: Long axis along X (like the library bridges). Pivot = centre of the footprint, bottom at z=0. Add markers `end_a`, `end_b` and `deck` (deck centreline height) with v4util.marker where the row is a bridge or walkway.
- Queue: worker vc, batch road_extras, folder v5_himalaya

### HM07 ×4 · P2 · highlands · 40 x 12 x 2 · up to 3,000 triangles each

- Ids: HM07_01_prayer_flag_string_01, HM07_02_prayer_flag_string_02, HM07_03_prayer_flag_string_03, HM07_04_prayer_flag_string_04
- What: Strings of cloth flags for bridges, cairns and passes
- Extra: none beyond the style guide
- Palette (himalaya): weathered grey stone (128,124,120), dark slate (84,86,96), snow (240,244,250), ice (196,226,242), weathered timber (112,92,70), rope (176,150,104), cloth flags in this order: blue (60,120,200), white (250,250,250), red (200,60,50), green (60,160,90), yellow (240,200,60)
- Orientation: Long axis along X (like the library bridges). Pivot = centre of the footprint, bottom at z=0. Add markers `end_a`, `end_b` and `deck` (deck centreline height) with v4util.marker where the row is a bridge or walkway.
- Queue: worker vc, batch road_extras, folder v5_himalaya

### HM08 ×4 · P2 · highlands · 14 x 12 x 14 · up to 4,000 triangles each

- Ids: HM08_01_cairn_shrine_01, HM08_02_cairn_shrine_02, HM08_03_cairn_shrine_03, HM08_04_cairn_shrine_04
- What: Stone cairns and small roadside shrines
- Extra: none beyond the style guide
- Palette (himalaya): weathered grey stone (128,124,120), dark slate (84,86,96), snow (240,244,250), ice (196,226,242), weathered timber (112,92,70), rope (176,150,104), cloth flags in this order: blue (60,120,200), white (250,250,250), red (200,60,50), green (60,160,90), yellow (240,200,60)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vc, batch road_extras, folder v5_himalaya

### HM09 ×4 · P2 · highlands · 40 x 30 x 30 · up to 14,000 triangles each

- Ids: HM09_01_monastery_outpost_01, HM09_02_monastery_outpost_02, HM09_03_monastery_outpost_03, HM09_04_monastery_outpost_04
- What: Hall, prayer-wheel house, guest house and bell shelter for the hidden monastery pocket beyond Frost Gorge (2450,-1480)
- Extra: none beyond the style guide
- Palette (himalaya): weathered grey stone (128,124,120), dark slate (84,86,96), snow (240,244,250), ice (196,226,242), weathered timber (112,92,70), rope (176,150,104), cloth flags in this order: blue (60,120,200), white (250,250,250), red (200,60,50), green (60,160,90), yellow (240,200,60)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vc, batch road_extras, folder v5_himalaya

### NE02 ×4 · P2 · entrances · 30 x 14 x 22 · up to 5,000 triangles each

- Ids: NE02_01_entry_rock_pair_01, NE02_02_entry_rock_pair_02, NE02_03_entry_rock_pair_03, NE02_04_entry_rock_pair_04
- What: Large boulder pairs (mossy, frosted, sandstone, basalt) that frame a road where it meets a settlement
- Extra: Boulder pairs that frame a road: mossy, frosted, sandstone, basalt. 30 wide so the road passes between them.
- Palette (entrance): carve each sign in the palette of its settlement: Town 1 dark stone and iron; elf living wood; alpine log and snow; rusty salvage plate on sandstone; harbour whitewashed board with rope; desert painted clay on timber
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vc, batch boulders, folder v5_entrances

### CP11 ×2 · P2 · capital · 70 x 60 x 50 · up to 30,000 triangles each

- Ids: CP11_01_great_hall_chapel_01, CP11_02_great_hall_chapel_02
- What: Great hall and royal chapel inside the castle court
- Extra: none beyond the style guide
- Palette (capital): plaster (232,214,188), timber (112,80,60), roofs orange-red (198,88,52) (214,104,58) (178,72,46) with (140,62,48) accents, stone grey-lilac (150,142,158), cone roofs maroon (120,44,52), wall-walk deck (150,88,70), parapet cap (232,226,230)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vd, batch town_extras, folder v5_capital

### CP16 ×12 · P2 · capital · 22 x 28 x 22 · up to 11,000 triangles each

- Ids: CP16_01_townhouse_new_01, CP16_02_townhouse_new_02, CP16_03_townhouse_new_03, CP16_04_townhouse_new_04, CP16_05_townhouse_new_05, CP16_06_townhouse_new_06, CP16_07_townhouse_new_07, CP16_08_townhouse_new_08, CP16_09_townhouse_new_09, CP16_10_townhouse_new_10, CP16_11_townhouse_new_11, CP16_12_townhouse_new_12
- What: Half-timbered orange-roof family: corner house, tall x2, courtyard x2, arcade shop x2, inn, guild hall x2, market hall
- Extra: none beyond the style guide
- Palette (capital): plaster (232,214,188), timber (112,80,60), roofs orange-red (198,88,52) (214,104,58) (178,72,46) with (140,62,48) accents, stone grey-lilac (150,142,158), cone roofs maroon (120,44,52), wall-walk deck (150,88,70), parapet cap (232,226,230)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vd, batch town_extras, folder v5_capital

### CP17 ×2 · P2 · capital · 30 x 34 x 30 · up to 14,000 triangles each

- Ids: CP17_01_plaza_features_01, CP17_02_plaza_features_02
- What: Central plaza monument and a public well
- Extra: none beyond the style guide
- Palette (capital): plaster (232,214,188), timber (112,80,60), roofs orange-red (198,88,52) (214,104,58) (178,72,46) with (140,62,48) accents, stone grey-lilac (150,142,158), cone roofs maroon (120,44,52), wall-walk deck (150,88,70), parapet cap (232,226,230)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vd, batch town_extras, folder v5_capital

### CP18 ×4 · P2 · capital · 30 x 8 x 10 · up to 5,000 triangles each

- Ids: CP18_01_quay_wall_01, CP18_02_quay_wall_02, CP18_03_quay_wall_03, CP18_04_quay_wall_04
- What: River embankment: straight, curve, steps, mooring posts
- Extra: none beyond the style guide
- Palette (capital): plaster (232,214,188), timber (112,80,60), roofs orange-red (198,88,52) (214,104,58) (178,72,46) with (140,62,48) accents, stone grey-lilac (150,142,158), cone roofs maroon (120,44,52), wall-walk deck (150,88,70), parapet cap (232,226,230)
- Orientation: Long axis along X (like the library bridges). Pivot = centre of the footprint, bottom at z=0. Add markers `end_a`, `end_b` and `deck` (deck centreline height) with v4util.marker where the row is a bridge or walkway.
- Queue: worker vd, batch town_extras, folder v5_capital

### EV03 ×6 · P2 · forest · 20 x 6 x 20 · up to 4,000 triangles each

- Ids: EV03_01_elf_path_piece_01, EV03_02_elf_path_piece_02, EV03_03_elf_path_piece_03, EV03_04_elf_path_piece_04, EV03_05_elf_path_piece_05, EV03_06_elf_path_piece_06
- What: Root stairs, carved steps, stone-and-root bridge, garden arch, path posts, plaza paving ring
- Extra: Root stairs, carved steps, stone-and-root bridge, garden arch, path posts, plaza paving ring: small pieces that stitch the valley together.
- Palette (elf): living wood (140,104,70), pale bark (176,150,112), moss (86,130,70), leaf greens (70,120,60) (104,150,80), warm stone (150,140,120), shingle teal-green (80,120,100); lantern light only, no glow
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker ve, batch elf_paths, folder v5_elf

### LM01 ×1 · P2 · forest · 36 x 50 x 36 · up to 30,000 triangles each

- Ids: LM01_01_world_tree_trunk_door
- What: Hollow trunk piece with a door, stair and lantern niche (warm lantern only, no glow)
- Extra: none beyond the style guide
- Palette (forest): bark (96,74,56), moss (86,130,70), fern green (70,120,60), ancient stone (130,126,118), root brown (110,80,58)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker ve, batch elf_paths, folder v5_elf

### LM02 ×1 · P2 · forest · 80 x 110 x 40 · up to 35,000 triangles each

- Ids: LM02_01_world_tree_falls
- What: 3-tier waterfall set for the world tree cliff
- Extra: none beyond the style guide
- Palette (forest): bark (96,74,56), moss (86,130,70), fern green (70,120,60), ancient stone (130,126,118), root brown (110,80,58)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker ve, batch elf_paths, folder v5_elf

### TW01 ×1 · P2 · town1 · 14 x 40 x 14 · up to 16,000 triangles each

- Ids: TW01_01_town1_hero_statue
- What: Statue with a real face for the plaza
- Extra: none beyond the style guide
- Palette (town1): dark stone (78,76,86), warm brick (126,112,98), iron (40,38,37), banner crimson (150,40,48), bone (224,216,196)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker ve, batch town1, folder v5_town1

### TW02 ×8 · P2 · town1 · 12 x 10 x 10 · up to 3,000 triangles each

- Ids: TW02_01_street_life_01, TW02_02_street_life_02, TW02_03_street_life_03, TW02_04_street_life_04, TW02_05_street_life_05, TW02_06_street_life_06, TW02_07_street_life_07, TW02_08_street_life_08
- What: Carts x2, crate stacks x2, barrel stack, hanging signs x2, bench
- Extra: none beyond the style guide
- Palette (town1): dark stone (78,76,86), warm brick (126,112,98), iron (40,38,37), banner crimson (150,40,48), bone (224,216,196)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker ve, batch town1, folder v5_town1

### TW03 ×4 · P2 · town1 · 14 x 14 x 14 · up to 5,000 triangles each

- Ids: TW03_01_skull_avenue_set_01, TW03_02_skull_avenue_set_02, TW03_03_skull_avenue_set_03, TW03_04_skull_avenue_set_04
- What: Braziers x2 and banner poles x2 for the avenue from the skull HQ apron to the plaza
- Extra: none beyond the style guide
- Palette (town1): dark stone (78,76,86), warm brick (126,112,98), iron (40,38,37), banner crimson (150,40,48), bone (224,216,196)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker ve, batch town1, folder v5_town1

### HL01 ×4 · P2 · highlands · 24 x 70 x 24 · up to 8,000 triangles each

- Ids: HL01_01_ice_spire_01, HL01_02_ice_spire_02, HL01_03_ice_spire_03, HL01_04_ice_spire_04
- What: Ice spires
- Extra: none beyond the style guide
- Palette (himalaya): weathered grey stone (128,124,120), dark slate (84,86,96), snow (240,244,250), ice (196,226,242), weathered timber (112,92,70), rope (176,150,104), cloth flags in this order: blue (60,120,200), white (250,250,250), red (200,60,50), green (60,160,90), yellow (240,200,60)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vg, batch highland_set, folder v5_himalaya

### HL02 ×2 · P2 · highlands · 50 x 40 x 14 · up to 9,000 triangles each

- Ids: HL02_01_ice_arch_01, HL02_02_ice_arch_02
- What: Natural ice arches
- Extra: none beyond the style guide
- Palette (himalaya): weathered grey stone (128,124,120), dark slate (84,86,96), snow (240,244,250), ice (196,226,242), weathered timber (112,92,70), rope (176,150,104), cloth flags in this order: blue (60,120,200), white (250,250,250), red (200,60,50), green (60,160,90), yellow (240,200,60)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vg, batch highland_set, folder v5_himalaya

### HL03 ×3 · P2 · highlands · 90 x 24 x 50 · up to 12,000 triangles each

- Ids: HL03_01_glacier_tongue_01, HL03_02_glacier_tongue_02, HL03_03_glacier_tongue_03
- What: Glacier tongues and crevasse edges
- Extra: none beyond the style guide
- Palette (himalaya): weathered grey stone (128,124,120), dark slate (84,86,96), snow (240,244,250), ice (196,226,242), weathered timber (112,92,70), rope (176,150,104), cloth flags in this order: blue (60,120,200), white (250,250,250), red (200,60,50), green (60,160,90), yellow (240,200,60)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vg, batch highland_set, folder v5_himalaya

### HL04 ×2 · P2 · highlands · 40 x 30 x 30 · up to 10,000 triangles each

- Ids: HL04_01_ice_cave_mouth_01, HL04_02_ice_cave_mouth_02
- What: Ice cave entrances
- Extra: none beyond the style guide
- Palette (himalaya): weathered grey stone (128,124,120), dark slate (84,86,96), snow (240,244,250), ice (196,226,242), weathered timber (112,92,70), rope (176,150,104), cloth flags in this order: blue (60,120,200), white (250,250,250), red (200,60,50), green (60,160,90), yellow (240,200,60)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vg, batch highland_set, folder v5_himalaya

### HL05 ×1 · P2 · highlands · 24 x 24 x 24 · up to 9,000 triangles each

- Ids: HL05_01_mountain_shrine
- What: Hidden shrine on a pass
- Extra: none beyond the style guide
- Palette (himalaya): weathered grey stone (128,124,120), dark slate (84,86,96), snow (240,244,250), ice (196,226,242), weathered timber (112,92,70), rope (176,150,104), cloth flags in this order: blue (60,120,200), white (250,250,250), red (200,60,50), green (60,160,90), yellow (240,200,60)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vg, batch highland_set, folder v5_himalaya

### HL06 ×1 · P2 · highlands · 20 x 50 x 20 · up to 11,000 triangles each

- Ids: HL06_01_snow_watchtower
- What: Watchtower for the mountain road
- Extra: none beyond the style guide
- Palette (himalaya): weathered grey stone (128,124,120), dark slate (84,86,96), snow (240,244,250), ice (196,226,242), weathered timber (112,92,70), rope (176,150,104), cloth flags in this order: blue (60,120,200), white (250,250,250), red (200,60,50), green (60,160,90), yellow (240,200,60)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vg, batch highland_set, folder v5_himalaya

### HL07 ×2 · P2 · highlands · 30 x 24 x 24 · up to 9,000 triangles each

- Ids: HL07_01_mine_entrance_01, HL07_02_mine_entrance_02
- What: Timbered mine mouths
- Extra: none beyond the style guide
- Palette (himalaya): weathered grey stone (128,124,120), dark slate (84,86,96), snow (240,244,250), ice (196,226,242), weathered timber (112,92,70), rope (176,150,104), cloth flags in this order: blue (60,120,200), white (250,250,250), red (200,60,50), green (60,160,90), yellow (240,200,60)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vg, batch highland_set, folder v5_himalaya

### SP01 ×6 · P2 · highlands · 60 x 160 x 60 · up to 15,000 triangles each

- Ids: SP01_01_snow_spire_cluster_01, SP01_02_snow_spire_cluster_02, SP01_03_snow_spire_cluster_03, SP01_04_snow_spire_cluster_04, SP01_05_snow_spire_cluster_05, SP01_06_snow_spire_cluster_06
- What: Jagged snow-capped spires and ridgelines for the Frosthold massif (the concept map mountain)
- Extra: none beyond the style guide
- Palette (himalaya): weathered grey stone (128,124,120), dark slate (84,86,96), snow (240,244,250), ice (196,226,242), weathered timber (112,92,70), rope (176,150,104), cloth flags in this order: blue (60,120,200), white (250,250,250), red (200,60,50), green (60,160,90), yellow (240,200,60)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vg, batch highland_set, folder v5_himalaya

### LM04 ×3 · P2 · highlands · 60 x 34 x 20 · up to 14,000 triangles each

- Ids: LM04_01_fortress_rampart_step_01, LM04_02_fortress_rampart_step_02, LM04_03_fortress_rampart_step_03
- What: Stepped ramparts that climb the rock
- Extra: none beyond the style guide
- Palette (himalaya): weathered grey stone (128,124,120), dark slate (84,86,96), snow (240,244,250), ice (196,226,242), weathered timber (112,92,70), rope (176,150,104), cloth flags in this order: blue (60,120,200), white (250,250,250), red (200,60,50), green (60,160,90), yellow (240,200,60)
- Orientation: Long axis along X (like the library bridges). Pivot = centre of the footprint, bottom at z=0. Add markers `end_a`, `end_b` and `deck` (deck centreline height) with v4util.marker where the row is a bridge or walkway.
- Queue: worker vg, batch fortress_parts, folder v5_landmarks

### LM05 ×2 · P2 · highlands · 34 x 80 x 34 · up to 18,000 triangles each

- Ids: LM05_01_fortress_cliff_tower_01, LM05_02_fortress_cliff_tower_02
- What: Towers clinging to the cliff
- Extra: none beyond the style guide
- Palette (himalaya): weathered grey stone (128,124,120), dark slate (84,86,96), snow (240,244,250), ice (196,226,242), weathered timber (112,92,70), rope (176,150,104), cloth flags in this order: blue (60,120,200), white (250,250,250), red (200,60,50), green (60,160,90), yellow (240,200,60)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vg, batch fortress_parts, folder v5_landmarks

### LM06 ×1 · P2 · highlands · 60 x 50 x 60 · up to 24,000 triangles each

- Ids: LM06_01_fortress_tunnel_gate
- What: Gate tunnel cut into the mountain
- Extra: none beyond the style guide
- Palette (himalaya): weathered grey stone (128,124,120), dark slate (84,86,96), snow (240,244,250), ice (196,226,242), weathered timber (112,92,70), rope (176,150,104), cloth flags in this order: blue (60,120,200), white (250,250,250), red (200,60,50), green (60,160,90), yellow (240,200,60)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vg, batch fortress_parts, folder v5_landmarks

### LM07 ×2 · P2 · highlands · 50 x 60 x 60 · up to 16,000 triangles each

- Ids: LM07_01_carved_stair_switchback_01, LM07_02_carved_stair_switchback_02
- What: Switchback stairs carved into the slope
- Extra: none beyond the style guide
- Palette (himalaya): weathered grey stone (128,124,120), dark slate (84,86,96), snow (240,244,250), ice (196,226,242), weathered timber (112,92,70), rope (176,150,104), cloth flags in this order: blue (60,120,200), white (250,250,250), red (200,60,50), green (60,160,90), yellow (240,200,60)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vg, batch fortress_parts, folder v5_landmarks

### LM08 ×1 · P2 · highlands · 90 x 24 x 16 · up to 14,000 triangles each

- Ids: LM08_01_mountain_span_bridge
- What: Stone span between two rock faces on a pass
- Extra: none beyond the style guide
- Palette (himalaya): weathered grey stone (128,124,120), dark slate (84,86,96), snow (240,244,250), ice (196,226,242), weathered timber (112,92,70), rope (176,150,104), cloth flags in this order: blue (60,120,200), white (250,250,250), red (200,60,50), green (60,160,90), yellow (240,200,60)
- Orientation: Long axis along X (like the library bridges). Pivot = centre of the footprint, bottom at z=0. Add markers `end_a`, `end_b` and `deck` (deck centreline height) with v4util.marker where the row is a bridge or walkway.
- Queue: worker vg, batch fortress_parts, folder v5_landmarks

### FR01 ×4 · P2 · forest · 90 x 160 x 90 · up to 40,000 triangles each

- Ids: FR01_01_giant_tree_01, FR01_02_giant_tree_02, FR01_03_giant_tree_03, FR01_04_giant_tree_04
- What: Four giant-tree silhouettes: leaning, twin trunk, arched, broken top (natural, no glow)
- Extra: none beyond the style guide
- Palette (forest): bark (96,74,56), moss (86,130,70), fern green (70,120,60), ancient stone (130,126,118), root brown (110,80,58)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vg, batch forest_set, folder v5_forest

### FR02 ×6 · P2 · forest · 40 x 34 x 30 · up to 10,000 triangles each

- Ids: FR02_01_forest_ruin_01, FR02_02_forest_ruin_02, FR02_03_forest_ruin_03, FR02_04_forest_ruin_04, FR02_05_forest_ruin_05, FR02_06_forest_ruin_06
- What: Overgrown arch, stair, wall, altar and two broken pillars
- Extra: none beyond the style guide
- Palette (forest): bark (96,74,56), moss (86,130,70), fern green (70,120,60), ancient stone (130,126,118), root brown (110,80,58)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vg, batch forest_set, folder v5_forest

### FR03 ×6 · P2 · forest · 40 x 30 x 30 · up to 10,000 triangles each

- Ids: FR03_01_cave_mouth_01, FR03_02_cave_mouth_02, FR03_03_cave_mouth_03, FR03_04_cave_mouth_04, FR03_05_cave_mouth_05, FR03_06_cave_mouth_06
- What: Cave mouths and rock arches for secret caves
- Extra: none beyond the style guide
- Palette (forest): bark (96,74,56), moss (86,130,70), fern green (70,120,60), ancient stone (130,126,118), root brown (110,80,58)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vg, batch forest_set, folder v5_forest

### VG04 ×3 · P2 · everywhere · 14 x 34 x 14 · up to 8,000 triangles each

- Ids: VG04_01_tree_birch_01, VG04_02_tree_birch_02, VG04_03_tree_birch_03
- What: Birch
- Extra: none beyond the style guide
- Palette (trees): poplar and beech leaf greens (90,140,70) (120,160,80); old oak dark (52,92,50) with bark (80,62,48); blossom white (244,232,236) and pink (232,176,196); birch bark (232,228,220)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vg, batch forest_set, folder v5_forest

### LM23 ×3 · P2 · forest · 90 x 80 x 30 · up to 20,000 triangles each

- Ids: LM23_01_gorge_wall_01, LM23_02_gorge_wall_02, LM23_03_gorge_wall_03
- What: Gorge walls below the falls
- Extra: none beyond the style guide
- Palette (forest): bark (96,74,56), moss (86,130,70), fern green (70,120,60), ancient stone (130,126,118), root brown (110,80,58)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vg, batch forest_set, folder v5_forest

### LM24 ×3 · P2 · forest · 30 x 16 x 30 · up to 6,000 triangles each

- Ids: LM24_01_fall_pool_rock_01, LM24_02_fall_pool_rock_02, LM24_03_fall_pool_rock_03
- What: Pool rocks at the base
- Extra: none beyond the style guide
- Palette (forest): bark (96,74,56), moss (86,130,70), fern green (70,120,60), ancient stone (130,126,118), root brown (110,80,58)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vg, batch forest_set, folder v5_forest

### VG05 ×3 · P2 · plains · 22 x 38 x 22 · up to 11,000 triangles each

- Ids: VG05_01_tree_cypress_swamp_01, VG05_02_tree_cypress_swamp_02, VG05_03_tree_cypress_swamp_03
- What: Swamp cypress for marshland
- Extra: none beyond the style guide
- Palette (trees): poplar and beech leaf greens (90,140,70) (120,160,80); old oak dark (52,92,50) with bark (80,62,48); blossom white (244,232,236) and pink (232,176,196); birch bark (232,228,220)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vg, batch marsh_set, folder v5_forest

### VG06 ×2 · P2 · plains · 16 x 6 x 16 · up to 3,000 triangles each

- Ids: VG06_01_marsh_hummock_01, VG06_02_marsh_hummock_02
- What: Grass hummocks
- Extra: none beyond the style guide
- Palette (trees): poplar and beech leaf greens (90,140,70) (120,160,80); old oak dark (52,92,50) with bark (80,62,48); blossom white (244,232,236) and pink (232,176,196); birch bark (232,228,220)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vg, batch marsh_set, folder v5_forest

### VG07 ×2 · P2 · plains · 30 x 4 x 6 · up to 3,000 triangles each

- Ids: VG07_01_boardwalk_01, VG07_02_boardwalk_02
- What: Marsh boardwalk
- Extra: none beyond the style guide
- Palette (trees): poplar and beech leaf greens (90,140,70) (120,160,80); old oak dark (52,92,50) with bark (80,62,48); blossom white (244,232,236) and pink (232,176,196); birch bark (232,228,220)
- Orientation: Long axis along X (like the library bridges). Pivot = centre of the footprint, bottom at z=0. Add markers `end_a`, `end_b` and `deck` (deck centreline height) with v4util.marker where the row is a bridge or walkway.
- Queue: worker vg, batch marsh_set, folder v5_forest

### DS01 ×6 · P2 · desert · 20 x 18 x 20 · up to 8,000 triangles each

- Ids: DS01_01_adobe_house_01, DS01_02_adobe_house_02, DS01_03_adobe_house_03, DS01_04_adobe_house_04, DS01_05_adobe_house_05, DS01_06_adobe_house_06
- What: Desert houses
- Extra: none beyond the style guide
- Palette (desert): sandstone (214,150,90), red mesa (172,92,56), pale sand (226,200,150), adobe (200,150,106), clay (176,112,76), bleached bone (224,216,196), dark timber (92,70,52)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vh, batch desert_village, folder v5_desert

### DS02 ×3 · P2 · desert · 24 x 16 x 18 · up to 6,000 triangles each

- Ids: DS02_01_desert_market_01, DS02_02_desert_market_02, DS02_03_desert_market_03
- What: Well, awning and stall sets
- Extra: none beyond the style guide
- Palette (desert): sandstone (214,150,90), red mesa (172,92,56), pale sand (226,200,150), adobe (200,150,106), clay (176,112,76), bleached bone (224,216,196), dark timber (92,70,52)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vh, batch desert_village, folder v5_desert

### DS03 ×2 · P2 · desert · 18 x 12 x 10 · up to 5,000 triangles each

- Ids: DS03_01_caravan_wagon_01, DS03_02_caravan_wagon_02
- What: Caravan wagons
- Extra: none beyond the style guide
- Palette (desert): sandstone (214,150,90), red mesa (172,92,56), pale sand (226,200,150), adobe (200,150,106), clay (176,112,76), bleached bone (224,216,196), dark timber (92,70,52)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vh, batch desert_village, folder v5_desert

### DS04 ×3 · P2 · desert · 14 x 42 x 14 · up to 6,000 triangles each

- Ids: DS04_01_palm_01, DS04_02_palm_02, DS04_03_palm_03
- What: Oasis palms
- Extra: none beyond the style guide
- Palette (desert): sandstone (214,150,90), red mesa (172,92,56), pale sand (226,200,150), adobe (200,150,106), clay (176,112,76), bleached bone (224,216,196), dark timber (92,70,52)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vh, batch desert_village, folder v5_desert

### DS05 ×2 · P2 · desert · 50 x 10 x 50 · up to 8,000 triangles each

- Ids: DS05_01_oasis_rock_ring_01, DS05_02_oasis_rock_ring_02
- What: Rocks around an oasis pool
- Extra: none beyond the style guide
- Palette (desert): sandstone (214,150,90), red mesa (172,92,56), pale sand (226,200,150), adobe (200,150,106), clay (176,112,76), bleached bone (224,216,196), dark timber (92,70,52)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vh, batch desert_village, folder v5_desert

### DS06 ×4 · P2 · desert · 120 x 90 x 40 · up to 20,000 triangles each

- Ids: DS06_01_canyon_wall_01, DS06_02_canyon_wall_02, DS06_03_canyon_wall_03, DS06_04_canyon_wall_04
- What: Sandstone canyon walls (on top of the 3 existing R06)
- Extra: none beyond the style guide
- Palette (desert): sandstone (214,150,90), red mesa (172,92,56), pale sand (226,200,150), adobe (200,150,106), clay (176,112,76), bleached bone (224,216,196), dark timber (92,70,52)
- Orientation: Long axis along X (like the library bridges). Pivot = centre of the footprint, bottom at z=0. Add markers `end_a`, `end_b` and `deck` (deck centreline height) with v4util.marker where the row is a bridge or walkway.
- Queue: worker vh, batch desert_land, folder v5_desert

### DS07 ×4 · P2 · desert · 40 x 70 x 30 · up to 12,000 triangles each

- Ids: DS07_01_hoodoo_arch_01, DS07_02_hoodoo_arch_02, DS07_03_hoodoo_arch_03, DS07_04_hoodoo_arch_04
- What: Hoodoos and rock arches
- Extra: none beyond the style guide
- Palette (desert): sandstone (214,150,90), red mesa (172,92,56), pale sand (226,200,150), adobe (200,150,106), clay (176,112,76), bleached bone (224,216,196), dark timber (92,70,52)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vh, batch desert_land, folder v5_desert

### DS08 ×3 · P2 · desert · 30 x 24 x 30 · up to 9,000 triangles each

- Ids: DS08_01_underground_entrance_01, DS08_02_underground_entrance_02, DS08_03_underground_entrance_03
- What: Stair-down entrances to the underground
- Extra: none beyond the style guide
- Palette (desert): sandstone (214,150,90), red mesa (172,92,56), pale sand (226,200,150), adobe (200,150,106), clay (176,112,76), bleached bone (224,216,196), dark timber (92,70,52)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vh, batch desert_land, folder v5_desert

### SD01 ×6 · P2 · desert · 120 x 90 x 100 · up to 16,000 triangles each

- Ids: SD01_01_red_mesa_cluster_01, SD01_02_red_mesa_cluster_02, SD01_03_red_mesa_cluster_03, SD01_04_red_mesa_cluster_04, SD01_05_red_mesa_cluster_05, SD01_06_red_mesa_cluster_06
- What: Orange-red mesa and butte clusters (the concept map desert)
- Extra: none beyond the style guide
- Palette (desert): sandstone (214,150,90), red mesa (172,92,56), pale sand (226,200,150), adobe (200,150,106), clay (176,112,76), bleached bone (224,216,196), dark timber (92,70,52)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vh, batch desert_land, folder v5_desert

### SD02 ×6 · P2 · desert · 40 x 30 x 40 · up to 10,000 triangles each

- Ids: SD02_01_desert_ruin_block_01, SD02_02_desert_ruin_block_02, SD02_03_desert_ruin_block_03, SD02_04_desert_ruin_block_04, SD02_05_desert_ruin_block_05, SD02_06_desert_ruin_block_06
- What: Sand-worn ruined city blocks around the ring temple
- Extra: none beyond the style guide
- Palette (desert): sandstone (214,150,90), red mesa (172,92,56), pale sand (226,200,150), adobe (200,150,106), clay (176,112,76), bleached bone (224,216,196), dark timber (92,70,52)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vh, batch desert_land, folder v5_desert

### LM10 ×3 · P2 · desert · 60 x 40 x 20 · up to 14,000 triangles each

- Ids: LM10_01_temple_colonnade_buried_01, LM10_02_temple_colonnade_buried_02, LM10_03_temple_colonnade_buried_03
- What: Colonnade sections sunk into the dunes
- Extra: none beyond the style guide
- Palette (desert): sandstone (214,150,90), red mesa (172,92,56), pale sand (226,200,150), adobe (200,150,106), clay (176,112,76), bleached bone (224,216,196), dark timber (92,70,52)
- Orientation: Long axis along X (like the library bridges). Pivot = centre of the footprint, bottom at z=0. Add markers `end_a`, `end_b` and `deck` (deck centreline height) with v4util.marker where the row is a bridge or walkway.
- Queue: worker vh, batch temple_parts, folder v5_landmarks

### LM11 ×1 · P2 · desert · 40 x 50 x 20 · up to 16,000 triangles each

- Ids: LM11_01_temple_gate_buried
- What: Half-buried gate
- Extra: none beyond the style guide
- Palette (desert): sandstone (214,150,90), red mesa (172,92,56), pale sand (226,200,150), adobe (200,150,106), clay (176,112,76), bleached bone (224,216,196), dark timber (92,70,52)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vh, batch temple_parts, folder v5_landmarks

### LM12 ×2 · P2 · desert · 30 x 24 x 40 · up to 9,000 triangles each

- Ids: LM12_01_temple_stair_down_01, LM12_02_temple_stair_down_02
- What: Stair that leads down into the sand
- Extra: none beyond the style guide
- Palette (desert): sandstone (214,150,90), red mesa (172,92,56), pale sand (226,200,150), adobe (200,150,106), clay (176,112,76), bleached bone (224,216,196), dark timber (92,70,52)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vh, batch temple_parts, folder v5_landmarks

### LM13 ×2 · P2 · desert · 20 x 70 x 20 · up to 18,000 triangles each

- Ids: LM13_01_guardian_statue_01, LM13_02_guardian_statue_02
- What: Original weathered guardian figures
- Extra: none beyond the style guide
- Palette (desert): sandstone (214,150,90), red mesa (172,92,56), pale sand (226,200,150), adobe (200,150,106), clay (176,112,76), bleached bone (224,216,196), dark timber (92,70,52)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vh, batch temple_parts, folder v5_landmarks

### LM14 ×3 · P2 · desert · 10 x 60 x 10 · up to 5,000 triangles each

- Ids: LM14_01_sand_obelisk_01, LM14_02_sand_obelisk_02, LM14_03_sand_obelisk_03
- What: Carved obelisks, leaning
- Extra: none beyond the style guide
- Palette (desert): sandstone (214,150,90), red mesa (172,92,56), pale sand (226,200,150), adobe (200,150,106), clay (176,112,76), bleached bone (224,216,196), dark timber (92,70,52)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vh, batch temple_parts, folder v5_landmarks

### LM16 ×2 · P2 · desert · 50 x 40 x 25 · up to 14,000 triangles each

- Ids: LM16_01_ring_temple_segment_01, LM16_02_ring_temple_segment_02
- What: Ring wall segments for building out the circle
- Extra: none beyond the style guide
- Palette (desert): sandstone (214,150,90), red mesa (172,92,56), pale sand (226,200,150), adobe (200,150,106), clay (176,112,76), bleached bone (224,216,196), dark timber (92,70,52)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vh, batch temple_parts, folder v5_landmarks

### LM17 ×1 · P2 · desert · 60 x 60 x 60 · up to 24,000 triangles each

- Ids: LM17_01_ring_inner_sanctum
- What: Inner sanctum
- Extra: none beyond the style guide
- Palette (desert): sandstone (214,150,90), red mesa (172,92,56), pale sand (226,200,150), adobe (200,150,106), clay (176,112,76), bleached bone (224,216,196), dark timber (92,70,52)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vh, batch temple_parts, folder v5_landmarks

### VC01 ×8 · P2 · east_coast · 60 x 60 x 50 · up to 12,000 triangles each

- Ids: VC01_01_volcanic_rock_01, VC01_02_volcanic_rock_02, VC01_03_volcanic_rock_03, VC01_04_volcanic_rock_04, VC01_05_volcanic_rock_05, VC01_06_volcanic_rock_06, VC01_07_volcanic_rock_07, VC01_08_volcanic_rock_08
- What: Dark volcanic rock formations (basalt colours; lava veins are terrain paint)
- Extra: none beyond the style guide
- Palette (skull): basalt (54,50,58), ash grey (96,92,100), cracked-lava rock (70,56,60), bone (224,216,196), rust iron (122,62,36); no glow (lava veins are terrain paint)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vh, batch skull_set, folder v5_skull

### VC03 ×3 · P2 · east_coast · 60 x 50 x 50 · up to 16,000 triangles each

- Ids: VC03_01_dark_fort_ruin_01, VC03_02_dark_fort_ruin_02, VC03_03_dark_fort_ruin_03
- What: Dark fort ruins
- Extra: none beyond the style guide
- Palette (skull): basalt (54,50,58), ash grey (96,92,100), cracked-lava rock (70,56,60), bone (224,216,196), rust iron (122,62,36); no glow (lava veins are terrain paint)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vh, batch skull_set, folder v5_skull

### VC04 ×6 · P2 · east_coast · 30 x 30 x 30 · up to 11,000 triangles each

- Ids: VC04_01_skull_city_building_01, VC04_02_skull_city_building_02, VC04_03_skull_city_building_03, VC04_04_skull_city_building_04, VC04_05_skull_city_building_05, VC04_06_skull_city_building_06
- What: Ruined dark-stone houses and halls for the forbidden city
- Extra: none beyond the style guide
- Palette (skull): basalt (54,50,58), ash grey (96,92,100), cracked-lava rock (70,56,60), bone (224,216,196), rust iron (122,62,36); no glow (lava veins are terrain paint)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vh, batch skull_set, folder v5_skull

### PL01 ×4 · P2 · plains · 28 x 22 x 24 · up to 10,000 triangles each

- Ids: PL01_01_farmhouse_01, PL01_02_farmhouse_02, PL01_03_farmhouse_03, PL01_04_farmhouse_04
- What: Farmhouses
- Extra: none beyond the style guide
- Palette (plains): whitewash (236,226,206), terracotta roof (206,120,84), thatch (190,160,100), timber (112,80,60), field stone (150,142,128), hay (214,190,110)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vi, batch plains_set, folder v5_plains

### PL02 ×3 · P2 · plains · 14 x 24 x 14 · up to 5,000 triangles each

- Ids: PL02_01_hay_silo_01, PL02_02_hay_silo_02, PL02_03_hay_silo_03
- What: Hay stacks and a silo
- Extra: none beyond the style guide
- Palette (plains): whitewash (236,226,206), terracotta roof (206,120,84), thatch (190,160,100), timber (112,80,60), field stone (150,142,128), hay (214,190,110)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vi, batch plains_set, folder v5_plains

### PL03 ×2 · P2 · plains · 14 x 8 x 8 · up to 3,000 triangles each

- Ids: PL03_01_farm_cart_01, PL03_02_farm_cart_02
- What: Carts
- Extra: none beyond the style guide
- Palette (plains): whitewash (236,226,206), terracotta roof (206,120,84), thatch (190,160,100), timber (112,80,60), field stone (150,142,128), hay (214,190,110)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vi, batch plains_set, folder v5_plains

### PL04 ×1 · P2 · plains · 34 x 30 x 30 · up to 16,000 triangles each

- Ids: PL04_01_mill_waterwheel
- What: Watermill
- Extra: none beyond the style guide
- Palette (plains): whitewash (236,226,206), terracotta roof (206,120,84), thatch (190,160,100), timber (112,80,60), field stone (150,142,128), hay (214,190,110)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vi, batch plains_set, folder v5_plains

### PL05 ×3 · P2 · plains · 20 x 40 x 20 · up to 9,000 triangles each

- Ids: PL05_01_ruined_watchtower_plains_01, PL05_02_ruined_watchtower_plains_02, PL05_03_ruined_watchtower_plains_03
- What: Ruined watchtowers
- Extra: none beyond the style guide
- Palette (plains): whitewash (236,226,206), terracotta roof (206,120,84), thatch (190,160,100), timber (112,80,60), field stone (150,142,128), hay (214,190,110)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vi, batch plains_set, folder v5_plains

### PL06 ×2 · P2 · plains · 60 x 40 x 24 · up to 12,000 triangles each

- Ids: PL06_01_rock_arch_natural_01, PL06_02_rock_arch_natural_02
- What: Natural rock arches that carry paths over streams
- Extra: none beyond the style guide
- Palette (plains): whitewash (236,226,206), terracotta roof (206,120,84), thatch (190,160,100), timber (112,80,60), field stone (150,142,128), hay (214,190,110)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vi, batch plains_set, folder v5_plains

### VL01 ×1 · P2 · plains · 30 x 70 x 40 · up to 20,000 triangles each

- Ids: VL01_01_village_church_spire
- What: Spired church for the west farm village (the concept map Rusty Village)
- Extra: none beyond the style guide
- Palette (plains): whitewash (236,226,206), terracotta roof (206,120,84), thatch (190,160,100), timber (112,80,60), field stone (150,142,128), hay (214,190,110)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vi, batch plains_set, folder v5_plains

### LM19 ×5 · P2 · centre · 60 x 40 x 50 · up to 12,000 triangles each

- Ids: LM19_01_crater_rim_rock_01, LM19_02_crater_rim_rock_02, LM19_03_crater_rim_rock_03, LM19_04_crater_rim_rock_04, LM19_05_crater_rim_rock_05
- What: Broken rim rocks
- Extra: none beyond the style guide
- Palette (arcane): floating rock (118,116,122), moss, pale runes carved (no glow), ancient stone (130,126,118)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vi, batch ruins_crater, folder v5_landmarks

### LM20 ×3 · P2 · centre · 40 x 40 x 40 · up to 14,000 triangles each

- Ids: LM20_01_crater_arcane_ruin_01, LM20_02_crater_arcane_ruin_02, LM20_03_crater_arcane_ruin_03
- What: Small broken magical structures on the crater floor
- Extra: none beyond the style guide
- Palette (arcane): floating rock (118,116,122), moss, pale runes carved (no glow), ancient stone (130,126,118)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vi, batch ruins_crater, folder v5_landmarks

### LM26 ×3 · P2 · plains · 60 x 34 x 30 · up to 14,000 triangles each

- Ids: LM26_01_ruin_arena_segment_01, LM26_02_ruin_arena_segment_02, LM26_03_ruin_arena_segment_03
- What: Arena wall segments
- Extra: none beyond the style guide
- Palette (plains): whitewash (236,226,206), terracotta roof (206,120,84), thatch (190,160,100), timber (112,80,60), field stone (150,142,128), hay (214,190,110)
- Orientation: Long axis along X (like the library bridges). Pivot = centre of the footprint, bottom at z=0. Add markers `end_a`, `end_b` and `deck` (deck centreline height) with v4util.marker where the row is a bridge or walkway.
- Queue: worker vi, batch ruins_crater, folder v5_landmarks

### LM27 ×2 · P2 · plains · 40 x 50 x 12 · up to 12,000 triangles each

- Ids: LM27_01_ruin_aqueduct_arch_01, LM27_02_ruin_aqueduct_arch_02
- What: Aqueduct arches
- Extra: none beyond the style guide
- Palette (plains): whitewash (236,226,206), terracotta roof (206,120,84), thatch (190,160,100), timber (112,80,60), field stone (150,142,128), hay (214,190,110)
- Orientation: Long axis along X (like the library bridges). Pivot = centre of the footprint, bottom at z=0. Add markers `end_a`, `end_b` and `deck` (deck centreline height) with v4util.marker where the row is a bridge or walkway.
- Queue: worker vi, batch ruins_crater, folder v5_landmarks

### LM28 ×3 · P2 · plains · 24 x 40 x 24 · up to 8,000 triangles each

- Ids: LM28_01_ruin_column_set_01, LM28_02_ruin_column_set_02, LM28_03_ruin_column_set_03
- What: Broken column groups
- Extra: none beyond the style guide
- Palette (plains): whitewash (236,226,206), terracotta roof (206,120,84), thatch (190,160,100), timber (112,80,60), field stone (150,142,128), hay (214,190,110)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vi, batch ruins_crater, folder v5_landmarks

### LM29 ×2 · P2 · plains · 26 x 36 x 26 · up to 10,000 triangles each

- Ids: LM29_01_ruin_tower_stump_01, LM29_02_ruin_tower_stump_02
- What: Tower stumps
- Extra: none beyond the style guide
- Palette (plains): whitewash (236,226,206), terracotta roof (206,120,84), thatch (190,160,100), timber (112,80,60), field stone (150,142,128), hay (214,190,110)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vi, batch ruins_crater, folder v5_landmarks

### LM31 ×3 · P2 · plains · 40 x 40 x 30 · up to 14,000 triangles each

- Ids: LM31_01_ruined_castle_module_01, LM31_02_ruined_castle_module_02, LM31_03_ruined_castle_module_03
- What: Wall and tower modules for the ruined castle
- Extra: none beyond the style guide
- Palette (plains): whitewash (236,226,206), terracotta roof (206,120,84), thatch (190,160,100), timber (112,80,60), field stone (150,142,128), hay (214,190,110)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vi, batch ruins_crater, folder v5_landmarks

### CO03 ×6 · P2 · coast · 30 x 6 x 30 · up to 6,000 triangles each

- Ids: CO03_01_reef_01, CO03_02_reef_02, CO03_03_reef_03, CO03_04_reef_04, CO03_05_reef_05, CO03_06_reef_06
- What: Low reefs and sea rocks
- Extra: none beyond the style guide
- Palette (coast): sea rock (110,108,110), wet stone (84,88,92), barnacle white (210,206,196), harbour white (238,238,240), harbour blue (92,128,176), brick red (190,90,70)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vi, batch coast_set, folder v5_coast

### CO04 ×2 · P2 · coast · 70 x 60 x 30 · up to 14,000 triangles each

- Ids: CO04_01_sea_arch_01, CO04_02_sea_arch_02
- What: Sea arches
- Extra: none beyond the style guide
- Palette (coast): sea rock (110,108,110), wet stone (84,88,92), barnacle white (210,206,196), harbour white (238,238,240), harbour blue (92,128,176), brick red (190,90,70)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vi, batch coast_set, folder v5_coast

### CO05 ×3 · P2 · coast · 60 x 40 x 60 · up to 16,000 triangles each

- Ids: CO05_01_ruin_islet_01, CO05_02_ruin_islet_02, CO05_03_ruin_islet_03
- What: Small ruin islets
- Extra: none beyond the style guide
- Palette (coast): sea rock (110,108,110), wet stone (84,88,92), barnacle white (210,206,196), harbour white (238,238,240), harbour blue (92,128,176), brick red (190,90,70)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vi, batch coast_set, folder v5_coast

### HB01 ×3 · P2 · coast · 24 x 40 x 24 · up to 10,000 triangles each

- Ids: HB01_01_harbour_wall_tower_01, HB01_02_harbour_wall_tower_02, HB01_03_harbour_wall_tower_03
- What: Towers for the walled port
- Extra: none beyond the style guide
- Palette (coast): sea rock (110,108,110), wet stone (84,88,92), barnacle white (210,206,196), harbour white (238,238,240), harbour blue (92,128,176), brick red (190,90,70)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vi, batch coast_set, folder v5_coast

### RD01 ×4 · P2 · roads · 20 x 50 x 20 · up to 11,000 triangles each

- Ids: RD01_01_watchtower_01, RD01_02_watchtower_02, RD01_03_watchtower_03, RD01_04_watchtower_04
- What: Two intact and two ruined watchtowers
- Extra: none beyond the style guide
- Palette (roads): weathered timber (112,92,70), canvas (214,200,170), stone (140,134,126), rust (122,62,36), tar black (40,38,37), faded banner red (170,70,60)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vi, batch road_life, folder v5_roads

### RD02 ×6 · P2 · roads · 16 x 10 x 14 · up to 4,000 triangles each

- Ids: RD02_01_camp_set_01, RD02_02_camp_set_02, RD02_03_camp_set_03, RD02_04_camp_set_04, RD02_05_camp_set_05, RD02_06_camp_set_06
- What: Tents x3, cooking rack, supply stack, bedroll
- Extra: none beyond the style guide
- Palette (roads): weathered timber (112,92,70), canvas (214,200,170), stone (140,134,126), rust (122,62,36), tar black (40,38,37), faded banner red (170,70,60)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vi, batch road_life, folder v5_roads

### RD03 ×2 · P2 · roads · 30 x 20 x 24 · up to 10,000 triangles each

- Ids: RD03_01_waystation_01, RD03_02_waystation_02
- What: Roadside waystations
- Extra: none beyond the style guide
- Palette (roads): weathered timber (112,92,70), canvas (214,200,170), stone (140,134,126), rust (122,62,36), tar black (40,38,37), faded banner red (170,70,60)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vi, batch road_life, folder v5_roads

### RD04 ×2 · P2 · roads · 30 x 20 x 24 · up to 11,000 triangles each

- Ids: RD04_01_trading_post_01, RD04_02_trading_post_02
- What: Trading posts
- Extra: none beyond the style guide
- Palette (roads): weathered timber (112,92,70), canvas (214,200,170), stone (140,134,126), rust (122,62,36), tar black (40,38,37), faded banner red (170,70,60)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vi, batch road_life, folder v5_roads

### RD05 ×5 · P2 · roads · 14 x 10 x 10 · up to 3,000 triangles each

- Ids: RD05_01_battlefield_prop_01, RD05_02_battlefield_prop_02, RD05_03_battlefield_prop_03, RD05_04_battlefield_prop_04, RD05_05_battlefield_prop_05
- What: Broken ballista, cart, banner, spear rack, shield pile
- Extra: none beyond the style guide
- Palette (roads): weathered timber (112,92,70), canvas (214,200,170), stone (140,134,126), rust (122,62,36), tar black (40,38,37), faded banner red (170,70,60)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vi, batch road_life, folder v5_roads

### RD06 ×5 · P2 · roads · 22 x 20 x 20 · up to 9,000 triangles each

- Ids: RD06_01_abandoned_house_01, RD06_02_abandoned_house_02, RD06_03_abandoned_house_03, RD06_04_abandoned_house_04, RD06_05_abandoned_house_05
- What: Collapsed or burnt houses
- Extra: none beyond the style guide
- Palette (roads): weathered timber (112,92,70), canvas (214,200,170), stone (140,134,126), rust (122,62,36), tar black (40,38,37), faded banner red (170,70,60)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vi, batch road_life, folder v5_roads

### BR01 ×2 · P2 · roads · 160 x 40 x 20 · up to 24,000 triangles each

- Ids: BR01_01_viaduct_bridge_01, BR01_02_viaduct_bridge_02
- What: Multi-arch stone viaduct across a valley (the long central bridge on the concept map)
- Extra: none beyond the style guide
- Palette (roads): weathered timber (112,92,70), canvas (214,200,170), stone (140,134,126), rust (122,62,36), tar black (40,38,37), faded banner red (170,70,60)
- Orientation: Long axis along X (like the library bridges). Pivot = centre of the footprint, bottom at z=0. Add markers `end_a`, `end_b` and `deck` (deck centreline height) with v4util.marker where the row is a bridge or walkway.
- Queue: worker vi, batch road_life, folder v5_roads

### RV01 ×4 · P2 · rivers · 30 x 10 x 20 · up to 5,000 triangles each

- Ids: RV01_01_bank_rock_01, RV01_02_bank_rock_02, RV01_03_bank_rock_03, RV01_04_bank_rock_04
- What: Bank rocks for lakes and rivers
- Extra: none beyond the style guide
- Palette (roads): weathered timber (112,92,70), canvas (214,200,170), stone (140,134,126), rust (122,62,36), tar black (40,38,37), faded banner red (170,70,60)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vi, batch road_life, folder v5_roads

### FL01 ×3 · P2 · sea_edge · 90 x 60 x 90 · up to 30,000 triangles each

- Ids: FL01_01_floating_island_hero_01, FL01_02_floating_island_hero_02, FL01_03_floating_island_hero_03
- What: Floating islands with a ruin
- Extra: none beyond the style guide
- Palette (arcane): floating rock (118,116,122), moss, pale runes carved (no glow), ancient stone (130,126,118)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vi, batch sky, folder v5_coast

### FL02 ×3 · P2 · sea_edge · 40 x 24 x 40 · up to 10,000 triangles each

- Ids: FL02_01_floating_island_small_01, FL02_02_floating_island_small_02, FL02_03_floating_island_small_03
- What: Small floating rocks
- Extra: none beyond the style guide
- Palette (arcane): floating rock (118,116,122), moss, pale runes carved (no glow), ancient stone (130,126,118)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vi, batch sky, folder v5_coast

### LM21 ×4 · P3 · centre · 40 x 30 x 40 · up to 8,000 triangles each

- Ids: LM21_01_floating_rock_01, LM21_02_floating_rock_02, LM21_03_floating_rock_03, LM21_04_floating_rock_04
- What: Drifting rock slabs over the crater (no glow)
- Extra: none beyond the style guide
- Palette (arcane): floating rock (118,116,122), moss, pale runes carved (no glow), ancient stone (130,126,118)
- Orientation: Front (the side you walk up to) faces -Y, pivot = centre of the footprint at ground (z=0). Size within +-10% of the manifest size.
- Queue: worker vi, batch ruins_crater, folder v5_landmarks

