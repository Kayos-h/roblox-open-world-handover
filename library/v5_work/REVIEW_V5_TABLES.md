# First v5 review: data tables

404 of 404 models have a verdict. OK 212, MINOR 115, MAJOR 70, REDO 7.

## By family

| family | models | OK | MINOR | MAJOR | REDO |
|---|---|---|---|---|---|
| BR | 2 | 0 | 1 | 1 | 0 |
| CO | 20 | 7 | 5 | 8 | 0 |
| CP | 55 | 38 | 9 | 8 | 0 |
| DS | 27 | 15 | 8 | 4 | 0 |
| EV | 17 | 11 | 4 | 2 | 0 |
| FL | 6 | 3 | 3 | 0 | 0 |
| FR | 16 | 7 | 5 | 4 | 0 |
| HB | 3 | 2 | 1 | 0 | 0 |
| HL | 15 | 8 | 7 | 0 | 0 |
| HM | 27 | 18 | 5 | 4 | 0 |
| LM | 63 | 22 | 24 | 15 | 2 |
| NE | 10 | 5 | 4 | 1 | 0 |
| PL | 15 | 8 | 6 | 1 | 0 |
| RD | 24 | 10 | 7 | 6 | 1 |
| RV | 4 | 0 | 4 | 0 | 0 |
| RW | 5 | 4 | 0 | 1 | 0 |
| SD | 12 | 4 | 5 | 3 | 0 |
| SP | 6 | 0 | 0 | 6 | 0 |
| TW | 13 | 10 | 3 | 0 | 0 |
| VC | 19 | 7 | 6 | 2 | 4 |
| VG | 17 | 8 | 6 | 3 | 0 |
| VL | 1 | 1 | 0 | 0 | 0 |
| WT | 27 | 24 | 2 | 1 | 0 |

## REDO (7)

| id | what is wrong | fix |
|---|---|---|
| `LM02_01_world_tree_falls` | waterfalls are flat bright white+cyan vertical slabs that read as glowing light panels, not water; no-glow rule violation; body reads as a random rubble stone stack, not a tree trunk with falls; windo | Rebuild as a believable tree-trunk cliff; make the falls thin layered translucent/pale-blue stepped water with foam at the base and NO emissive bright panels. |
| `LM22_01_colossal_fall_cliff_hero` | waterfalls are bright white+cyan flat emissive-looking vertical slabs floating in front of the cliff; no-glow rule violation; falls float detached from the rock face; cliff is a thin stacked-slab stac | Rebuild falls as thin pale stepped water hugging the rock with foam pools, no glowing slabs; make the cliff chunky faceted rock instead of stacked thin plates. |
| `RD05_05_battlefield_prop_05` | detached floating red and blue disc parts; exploded, not assembled; no coherent object | Rebuild from scratch as a single connected prop; the current parts float apart and read as broken. |
| `VC04_01_skull_city_building_01` | hollow open grey box, not a building; detached wooden poles float above it; no roof, no facade, no identity | Rebuild as a recognisable ruined building with walls, an opening and seated/attached timber beams instead of a hollow box with floating poles. |
| `VC04_02_skull_city_building_02` | open hollow box; floating detached poles; unreadable | Rebuild as an identifiable structure with attached beams. |
| `VC04_04_skull_city_building_04` | hollow open box; floating detached poles; no identity | Rebuild as a recognisable building with attached beams. |
| `VC04_05_skull_city_building_05` | hollow open box; floating detached poles | Rebuild into an identifiable structure; attach the beams. |

## MAJOR (70)

| id | what is wrong | fix |
|---|---|---|
| `CP02_02_ring_wall_corner_02` | detached floating black posts (window bars) hovering in empty air beside the wall; gap between tower and wall | reattach the arrow-slit bars to the wall face and close the gap between the round tower and the straight run |
| `CP05_02_turret_crenellated_02` | thin black posts/spikes poking up through the red cone roof rim; look detached and clip the roof | remove the stray dark vertical bars at the roof rim or seat them as proper finials; do not let them clip the cone |
| `CP11_01_great_hall_chapel_01` | detached dark-red gable triangle floating above the roof ridge | seat the loose red gable/dormer piece onto the roof or delete it; no floating parts |
| `CP12_01_terrace_retaining_wall_01` | blocky square two-tone camo colour patches across the wall face; flat bright-green cap strip looks like a grass slab, not stone coping | replace the random square patches with a single stone colour and subtle relief; recolour the green cap to stone coping |
| `CP15_03_order_hq_03` | crude low-detail octagonal grey block, far below sibling landmark quality; large detached brown box floating in front of it | rebuild to match CP15_01/02 detail (proper facade, roof, trim) and remove or integrate the stray brown box |
| `CP18_01_quay_wall_01` | blocky square two-tone camo colour patches (cream/lilac checker) across the wall face | replace the random square patches with one stone colour; add bollards/course as relief instead of colour noise |
| `CP18_03_quay_wall_03` | blocky square two-tone camo colour patches on wall; stair reads as flat recolour | unify to one stone colour and model the steps with real risers rather than painted patches |
| `CP18_04_quay_wall_04` | blocky square two-tone camo colour patches across the wall face | unify to a single stone colour; keep the chimney/bollard detail as geometry |
| `LM01_01_world_tree_trunk_door` | splayed root buttresses are thin spiky planks with large see-through gaps between them; trunk base reads hollow/holed; top is an open flat green rim (hollow trunk cap) | thicken and merge the roots into a solid flared base with no gaps, close the trunk top, and make the door a clear recessed opening rather than a hollow |
| `LM03_01_frost_fortress_hero` | mountain backdrop is a chaotic stack of thin flat slabs with floating/jutting plates and a messy broken silhouette; slabs read as stacked paper, not snow rock; castle itself is good but overwhelmed by | Rebuild the mountain as chunky faceted snow-rock masses instead of thin stacked slabs; keep the castle and settle slabs so none float. |
| `LM07_01_carved_stair_switchback_01` | carved stair is not readable; looks like a plain rock mound; no visible steps or switchback | Cut clear stepped switchback flights into the rock face so the staircase reads from 30-60 studs. |
| `LM07_02_carved_stair_switchback_02` | steps barely readable, reads as a rough rock pile; silhouette does not say stair | Add defined step treads and a landing so the carved switchback is legible. |
| `LM08_01_mountain_span_bridge` | deck is broken/gappy, pieces look detached and floating; no continuous walkable span; tiny scattered posts read as debris | Rebuild a continuous solid deck with connected rails/supports so it reads as a crossable bridge. |
| `LM12_01_temple_stair_down_01` | reads as a jumble of flat clipping slabs; no clear descending stair silhouette; small floating boxes top-left | Rebuild as a readable recessed stair cut into the ground with clear step treads and framing walls; remove floating fragments. |
| `LM12_02_temple_stair_down_02` | confusing overlapping slabs; stair not legible; flat single-colour mass | Rebuild with distinct stepped treads descending into a clear pit opening instead of stacked flat planes. |
| `LM19_02_crater_rim_rock_02` | large very dark/near-black facets read as holes or inverted faces; flat grey, crude | Check face normals on the dark faces and lighten; add relief and warmer rock tone. |
| `LM19_04_crater_rim_rock_04` | large dark/near-black facets read as inverted faces or holes; flat grey, crude | Recalculate normals on the dark faces, lighten and add warm rock tone with more relief. |
| `LM19_05_crater_rim_rock_05` | big flat near-black block face looks like an inverted normal; flat grey rock pile | Fix the inverted/dark face, break up the large flat block and add colour variation. |
| `LM23_03_gorge_wall_03` | thin flat bright-white waterfall slab clips through the wall as a glowing vertical bar; slab is a single flat panel with no relief | Replace the flat white bar with a recessed stepped water chute in muted blue, seated into the rock, no flat glowing panel. |
| `LM27_01_ruin_aqueduct_arch_01` | solid black rectangular patches across the parapet read as holes/gaps; stray green nubs stuck to piers | Fill the black gaps with proper stone blocks (or model them as real openings with back faces); remove stray green bits. |
| `LM27_02_ruin_aqueduct_arch_02` | black holes along broken parapet; green nubs clinging to columns | Close/backface the black gaps and remove floating green specks. |
| `LM29_02_ruin_tower_stump_02` | reads as a plain cream box, square silhouette; almost no relief, crude for a tower stump | Make the stump round or battered with an eroded broken top and surface relief, not a flat rectangular box. |
| `LM31_03_ruined_castle_module_03` | two plain flat grey slabs, minimal detail; crude, reads as blank blocks not castle ruin | Add wall thickness, broken crenellations, window/arrow slits and surface relief so it reads as a ruined wall. |
| `WT02_01_wizard_tower_interior` | walkable floors with spiral stairs and domed top are good; but NO bookshelves on any interior floor; NO circular relief map inside the tower | place the WT03/WT04 bookshelves floor-to-ceiling on at least one library floor and set the WT05 round map on a floor so the interior delivers the brief's bookshelves and map categories |
| `HM04_02_tunnel_lining_02` | large black inverted/inside-out faces across the top and left of the interior; reads as holes / flipped normals, not lit stone | recalculate normals outward (or solidify the shell) and give the inner faces a stone colour so no black inverted patches remain |
| `HM06_01_switchback_wall_01` | blocky two-tone grey checkerboard camouflage patches across the wall face; stones read as a flat chequer pattern, not masonry | replace the alternating light/dark grey checker with subtler stone tone variation and real block relief |
| `HM06_03_switchback_wall_03` | same blocky grey checkerboard camouflage patches as _01 | remove the two-tone checker; use graded stone tones with block relief |
| `HM08_02_cairn_shrine_02` | reads as a small red-roof hut, not a cairn shrine; does not match its siblings in the HM08 cairn set | rebuild as a stone cairn/chorten (stacked rock or a whitewashed stupa form) consistent with the cairn_shrine set |
| `FR01_03_giant_tree_03` | canopy reduced to two ball blobs on splayed legs; reads as an arch/wishbone, not a giant tree; trunk splits into a bare inverted-V with a gap | Rebuild with a full connected canopy and a solid single trunk so it matches its giant-tree siblings. |
| `FR03_04_cave_mouth_04` | rock arch collapsed into scattered loose blocks, many detached/floating; no solid cave mouth reads | Merge the loose chunks into a solid arched mass seated on the ground with a clear opening. |
| `FR03_05_cave_mouth_05` | same scattered floating-debris problem as 04; silhouette does not read as a cave | Rebuild as one connected rock arch; remove free-floating blocks. |
| `FR03_06_cave_mouth_06` | loose detached blocks, gaps, no solid opening | Consolidate into a solid grounded cave mouth with an actual recessed opening. |
| `PL05_02_ruined_watchtower_plains_02` | plain cream rectangular box with windows, square silhouette; crude, does not read as a round ruined watchtower | Rebuild as a round/battered tower with eroded broken top and surface relief instead of a flat box. |
| `DS07_04_hoodoo_arch_04` | collapsed into a chaotic pile of blocks with one thin spire; no legible arch; camouflage colour patches | Rebuild as a clear eroded rock arch with a connected span; remove the scattered block rubble and fix colour banding. |
| `DS08_01_underground_entrance_01` | flat wall with a staircase stuck on its face; jumble of clipping amorphous slabs; no readable entrance/opening; single flat sand colour | Rebuild as a clear sunken doorway/ramp descending into the ground with framing and a dark opening; remove clipping slabs. |
| `DS08_02_underground_entrance_02` | same confusing clipping-slab mass as 01; no clear entrance | Rebuild with a legible descending entrance and distinct ground opening. |
| `DS08_03_underground_entrance_03` | same illegible clipping composition; no entrance read | Rebuild as a clear buried entrance; vary design from 01/02. |
| `CO01_05_coastal_cliff_05` | thin bright cyan vertical waterfall strip reads as a glowing neon line; no-glow rule violation | Replace the glowing cyan strip with a pale matte stepped waterfall, or remove it. |
| `CO03_01_reef_01` | blocky dark-grey camouflage colour patches on flat rock tops; very flat low slab, little relief | Remove the random dark polygon patches, use smooth tonal variation, and give the reef bumpy 3D relief instead of flat slabs. |
| `CO03_02_reef_02` | square dark camouflage patches on rock; flat jumbled slabs | Replace blotchy patches with coherent rock colour; add rounded relief and settle overlapping slabs. |
| `CO03_03_reef_03` | blocky dark colour patches; flat slab silhouette, samey with set | Recolour evenly and add 3D reef shaping; vary from siblings. |
| `CO03_04_reef_04` | dark camouflage patches; jumbled overlapping flat slabs read as clipping planes | Rebuild as a solid low reef mound with even colour; merge the loose slabs. |
| `CO03_05_reef_05` | square dark patches; messy overlapping flat plates | Consolidate into one reef body, even rock tone, add relief. |
| `CO03_06_reef_06` | camouflage dark patches; flat jumbled slabs, recolour of set | Even recolour, 3D relief, differentiate from siblings. |
| `CO05_03_ruin_islet_03` | blocky tan/yellow colour patches on the base rock read as camouflage blotches; hard grass seam | Remove the square sand-coloured patches, use coherent rock colour, and blend the grass cap. |
| `RD05_01_battlefield_prop_01` | unreadable silhouette; jumble of brown planks/wheel, no clear object; parts look detached/clipping | Rebuild as a clearly readable prop (broken cart or barricade) with connected parts and a recognisable shape. |
| `RD05_02_battlefield_prop_02` | silhouette does not read as anything; flat plank balanced on a rock/disc | Redesign into an identifiable battlefield item (overturned table, broken shield stack) that reads at 30-60 studs. |
| `RD05_03_battlefield_prop_03` | flat red slab on thin runners, unreadable; no believable object | Rebuild as a recognisable fallen banner or sledge with volume, not a single flat slab. |
| `RD06_01_abandoned_house_01` | large flat grey slab wall with no detail; chimney/parts appear detached; collapse reads as a defect not ruin | Replace the blank grey slab with a broken half-timber wall, anchor the chimney, and make the collapse intentional. |
| `RD06_03_abandoned_house_03` | huge blank dark slab dominates; silhouette unreadable as a house; flat untextured faces | Rebuild the fallen wall as a ruined timber-framed panel with debris; remove the featureless slab. |
| `RD06_05_abandoned_house_05` | blank flat grey slab wall; no house relief; collapse looks broken not designed | Give the standing wall half-timber relief and windows; make the rubble read as deliberate ruin. |
| `VG04_01_tree_birch_01` | canopy covered in flat yellow blotches, reads diseased not birch; splayed flat-white trunk looks like an open cone, not bark | Use a slim upright white-bark trunk with dark lenticel marks and a predominantly green canopy with light accents, not large yellow patches. |
| `VG04_02_tree_birch_02` | same yellow-blotch canopy and splayed cone trunk as 01 | Rebuild trunk as a thin upright birch bole and reduce yellow to subtle autumn accents. |
| `VG04_03_tree_birch_03` | clone of 01/02 with same trunk and blotch defects | Fix the trunk and canopy as above and vary the shape from its siblings. |
| `VC04_03_skull_city_building_03` | mostly a hollow box but has a broken tower; poles float detached above | Attach the timber beams to the structure and close/define the box into a readable ruined building. |
| `VC04_06_skull_city_building_06` | hollow box with a broken tower stub; floating detached poles | Attach beams and define the box into a readable ruined building. |
| `SP01_01_snow_spire_cluster_01` | blocky black/grey/white square camouflage patches over the spire; very thin pencil-like spire reads as a pole, weak silhouette; base rocks look detached | Replace the camo patches with coherent snow-over-grey-rock shading, thicken the spire taper, and seat the base rocks into the mass. |
| `SP01_02_snow_spire_cluster_02` | identical camouflage-patch and thin-spire problem as 01 | Same fix as SP01_01; also vary silhouette so it is not a clone. |
| `SP01_03_snow_spire_cluster_03` | camo patches, thin spire, clone of the set | Recolour coherently, thicken, and differentiate shape. |
| `SP01_04_snow_spire_cluster_04` | camo patches, thin spire, clone | Recolour coherently, thicken, and differentiate shape. |
| `SP01_05_snow_spire_cluster_05` | camo patches, thin spire, clone | Recolour coherently, thicken, and differentiate shape. |
| `SP01_06_snow_spire_cluster_06` | camo patches, thin spire, clone | Recolour coherently, thicken, and differentiate shape. |
| `SD01_04_red_mesa_cluster_04` | silhouette wrong: stacked flat slabs, not a broad flat-topped mesa; teetering pancake-tower look; thin flat debris planes at base | Rebuild as a broad flat-topped butte with sloped sides and horizontal strata, wider than tall; remove the stacked-box tower shape. |
| `SD01_05_red_mesa_cluster_05` | reads as a stack of coins/slabs, not a mesa; narrow unstable silhouette; flat ground debris planes | Reshape into one solid wide red rock mass with eroded flanks; keep the red/tan banding but lose the pancake stacking. |
| `SD01_06_red_mesa_cluster_06` | slab-stack tower not a mesa; flat clipping debris planes around base | Rebuild as a broad buttressed mesa form; replace flat base planes with chunky fallen rocks. |
| `BR01_02_viaduct_bridge_02` | black inverted faces under the arches; unexplained grey slab block sitting on the deck midway | Fix the inverted arch faces and remove or justify the grey block on the deck; it reads as a stray/clipping part. |
| `RW01_01_rework_existing_01` | crude stack of offset coloured slabs; silhouette does not read as a clear structure; slabs look loosely piled/unstable | Rebuild as a coherent tower/mesa with aligned, connected courses instead of randomly offset flat slabs. |
| `NE01_01_village_sign_01` | does not read as a village sign: a grey slab with a row of pale cylinders and a small black flag; ambiguous silhouette, looks like an organ or crate, crude versus sibling signs | rebuild as a clear notice board on a post with a legible board face, matching the NE01 sign set |
| `EV03_04_elf_path_piece_04` | stepped bridge planks look detached/floating with gaps between them; green mossy patches look like loose stuck-on blobs; would not tile cleanly | Join the plank steps into a continuous solid deck seated on the ground and integrate the moss rather than floating blobs. |
| `EV03_05_elf_path_piece_05` | loose thin slab plates float with visible gaps and do not connect; reads as scattered debris, not a path | Merge the slabs into one connected walkable path surface with no floating gaps. |

## MINOR (115)

- `CP01_02_ring_wall_straight_02`: near-identical recolour of 01/03, only arrow-slits differ
- `CP03_02_ring_wall_stair_end_02`: small stray stick/plank poking out of right merlon
- `CP06_01_gate_flank_tower_01`: red banner sits slightly off the wall face
- `CP06_02_gate_flank_tower_02`: banner slightly detached from wall
- `CP12_02_terrace_retaining_wall_02`: flat bright-green cap strip on top; plain banded slabs with little relief
- `CP14_04_skyline_tower_04`: thin detached antenna/rail bits on the top deck read as stray
- `CP14_05_skyline_tower_05`: teal/green patch on the water tank vs timber/stone palette
- `CP16_01_townhouse_new_01`: door canopy sits slightly off the facade
- `CP18_02_quay_wall_02`: plain curved slab, little relief
- `LM05_02_fortress_cliff_tower_02`: thin stick-like flag/beam pokes out of side; rock base reads as plain grey slab
- `LM10_02_temple_colonnade_buried_02`: black/inverted face on top of lintel
- `LM13_01_guardian_statue_01`: small black/inverted face near head; very thin crude figure
- `LM13_02_guardian_statue_02`: small black/inverted face near head; thin crude figure
- `LM14_03_sand_obelisk_03`: near-identical recolour of obelisk 01/02
- `LM16_01_ring_temple_segment_01`: plain curved slab with little relief; flat single-colour mass
- `LM16_02_ring_temple_segment_02`: near-identical to segment 01; flat featureless curved mass
- `LM18_01_crater_monolith_ring`: dark monoliths are thin and spiky, ring reads sparse; flat green pad under it looks like a disc, not terrain
- `LM19_01_crater_rim_rock_01`: flat grey, little relief; some near-black shadowed facets
- `LM19_03_crater_rim_rock_03`: flat grey rock pile, dark facets; crude chunky blocks
- `LM20_02_crater_arcane_ruin_02`: blue rune marks risk reading as emissive; a stray small green nub near base
- `LM21_02_floating_rock_02`: underside rock chunks look loosely jumbled/semi-detached
- `LM21_04_floating_rock_04`: underside chunks slightly disconnected; close recolour of siblings
- `LM25_01_ruin_gate_hero`: the tall L-shaped overhang block reads ambiguous, almost like an unfinished arm; red inset panels look like flat stickers
- `LM26_01_ruin_arena_segment_01`: thin white bars between columns read flat/railing-like; very similar to siblings
- `LM26_02_ruin_arena_segment_02`: near-identical to segment_01 (recolour feel); flat white infill bars
- `LM26_03_ruin_arena_segment_03`: flat infill bars; variety overlap with other arena segments
- `LM28_01_ruin_column_set_01`: grey-white drum banding looks a bit striped; small floating debris
- `LM28_02_ruin_column_set_02`: striped drum look; scattered small floating chunks
- `LM28_03_ruin_column_set_03`: two columns read as recolour of the other sets; banding stripes
- `LM29_01_ruin_tower_stump_01`: floating broken-top chunks sit slightly above the rim
- `LM30_01_ruined_castle_hero`: almost entirely flat default grey, reads unfinished/greyed-out; window holes are flat black rectangles; rubble cubes scattered loosely
- `LM31_01_ruined_castle_module_01`: green moss bands look like painted rings; slight sibling overlap
- `LM31_02_ruined_castle_module_02`: continuous green ring bands; similar to module_01
- `WT08_02_wizard_study_set_02`: sparse: a bare blue canopy-bed/frame with little detail for the tri count, crudest of the study set
- `WT13_01_plateau_terrace_set_01`: plain flat cream slab deck with little relief
- `HL01_04_ice_spire_04`: near-identical recolour of the other three spires
- `HL02_02_ice_arch_02`: very close duplicate of HL02_01; scattered base blocks look like floating debris
- `HL03_01_glacier_tongue_01`: brown/tan rock chunks mixed into ice read as dirty camouflage patches; flat scattered slabs
- `HL03_02_glacier_tongue_02`: same brown-patch issue; near-copy of 01
- `HL03_03_glacier_tongue_03`: recolour of 01/02 with brown debris patches
- `HL04_02_ice_cave_mouth_02`: near-identical to HL04_01
- `HL07_02_mine_entrance_02`: very close variant of HL07_01
- `HM04_01_tunnel_lining_01`: interior is a dark cavity; as a modular lining the open back is expected but the inner faces look unlit/near-black
- `HM05_01_cliff_gallery_01`: timber walkway clings to a blocky grey cliff but the rock is plain flat-grey slabs with little relief
- `HM05_02_cliff_gallery_02`: same flat grey cliff backing; white snow slab on top looks like a loose flat plane
- `HM06_02_switchback_wall_02`: mostly plain flat slabs; curved retaining section is bland with little stone detail
- `HM07_04_prayer_flag_string_04`: flags all near-white/pale, little colour variety versus siblings
- `FR01_02_giant_tree_02`: near-recolour of FR01_01
- `FR02_05_forest_ruin_05`: tall thin column looks like a floating plain slab with little relief
- `FR02_06_forest_ruin_06`: lone thin column with a floating cap block; sparse
- `FR03_02_cave_mouth_02`: near-duplicate of FR03_01
- `FR03_03_cave_mouth_03`: recolour/clone of 01-02
- `PL02_01_hay_silo_01`: reads as hay sheaves/stooks, not a silo (naming/concept mismatch)
- `PL03_02_farm_cart_02`: near-identical to farm_cart_01 (empty vs loaded only difference)
- `PL05_01_ruined_watchtower_plains_01`: floating broken-top chunks above the rim
- `PL05_03_ruined_watchtower_plains_03`: looks intact/new with a clean red cone roof, not ruined as the id states
- `PL06_01_rock_arch_natural_01`: flat grey rock, little colour variation
- `PL06_02_rock_arch_natural_02`: flat grey rock, little colour variation; small floating green/blue bits at base
- `DS01_03_adobe_house_03`: large blue slab against front wall; parapet merlons read as loose blocks
- `DS01_04_adobe_house_04`: stray yellow beam on ground in front
- `DS02_01_desert_market_01`: well + loose cylinders read as generic, not clearly a market; small floating/clipping cubes on plank
- `DS04_01_palm_01`: thin spindly trunk; sparse drooping fronds look wiry; faint stray wire ring near base
- `DS04_02_palm_02`: spindly trunk; sparse fronds; near-identical to palm 01/03
- `DS04_03_palm_03`: spindly trunk; sparse fronds; near-identical to siblings
- `DS07_01_hoodoo_arch_01`: blocky square red/cream colour patches look like camouflage; reads as two separate spires, not an arch
- `DS07_02_hoodoo_arch_02`: patchy camouflage-like colour blocks; arch connection unclear
- `CO01_03_coastal_cliff_03`: flat black square cave hole reads as a void/hole in the slab
- `CO04_01_sea_arch_01`: flat grey stone, little colour variation
- `CO04_02_sea_arch_02`: flat grey, close to sea_arch_01
- `CO05_01_ruin_islet_01`: green grass platform meets rock with a hard flat edge; base rock slightly jumbled
- `CO05_02_ruin_islet_02`: hard flat grass-on-rock seam; similar to islet_01
- `RD01_02_watchtower_02`: plain featureless box, open/hollow top; no roof or crenellation detail
- `RD01_04_watchtower_04`: plain box walls with floating broken-crenellation chunks on top
- `RD02_01_camp_set_01`: identical geometry to RD02_02/03, only recolored (variety)
- `RD02_02_camp_set_02`: recolor of RD02_01 (variety)
- `RD02_03_camp_set_03`: recolor of RD02_01 (variety)
- `RD02_06_camp_set_06`: dark gap/hole at bottom-front of the barrel
- `RD05_04_battlefield_prop_04`: reads as a spiked barricade but crude/boxy
- `VG03_01_tree_flowering_01`: pink blossom and green foliage sit as separate blotchy patches rather than blended blossom; reads as two colours slapped on
- `VG03_02_tree_flowering_02`: same patchy pink-on-green blotching as flowering_01
- `VG05_02_tree_cypress_swamp_02`: near-recolour of VG05_01
- `VG05_03_tree_cypress_swamp_03`: near-clone of VG05_01/02
- `VG06_01_marsh_hummock_01`: single flat green faceted slab mound with no relief or detail; no texture of marsh grass/moss
- `VG06_02_marsh_hummock_02`: near-duplicate of 01; flat untextured green
- `TW01_01_town1_hero_statue`: face is crude flat-boxy; staff reads thin
- `TW02_06_street_life_06`: bracket+gong reads ambiguous as a street prop; cylinder on ground looks detached
- `RV01_01_bank_rock_01`: near-monochrome flat grey, little colour; reads as default grey rock
- `RV01_02_bank_rock_02`: flat grey, same style as siblings (variety/colour)
- `RV01_03_bank_rock_03`: flat grey monochrome, little relief colour
- `RV01_04_bank_rock_04`: flat grey, reads like a recolor-less sibling
- `VC01_07_volcanic_rock_07`: tiny stray block floating at bottom-right
- `VC01_08_volcanic_rock_08`: small stray fragment at base; set of 8 feel like close variants
- `VC02_01_skull_cliff_hero_01`: white skull sits in front of a thin stacked-slab cliff; slabs read as stacked paper; skull jaw/teeth block floats slightly below
- `VC02_02_skull_cliff_hero_02`: horned skull version, same thin stacked-slab cliff issue; near recolour/variant of 01
- `VC03_01_dark_fort_ruin_01`: a few loose detached blocks/poles at the base
- `VC03_03_dark_fort_ruin_03`: small detached bits at base
- `FL01_01_floating_island_hero_01`: underside is a stack of thin flat square plates, reads artificial close up; top layout near-identical to FL01_02/03 (variety)
- `FL01_02_floating_island_hero_02`: same stacked-plate underside; same ruined tower and tree layout as siblings
- `FL01_03_floating_island_hero_03`: stacked-plate underside; layout repeats FL01_01/02
- `SD02_01_desert_ruin_block_01`: thin flat debris planes jutting from base; slight variety overlap with siblings
- `SD02_02_desert_ruin_block_02`: flat debris planes at base; similar massing to other SD02 blocks
- `SD02_04_desert_ruin_block_04`: flat debris planes at base; reads as recolour/remix of SD02_01
- `SD02_05_desert_ruin_block_05`: thin flat base planes; variety overlap with siblings
- `SD02_06_desert_ruin_block_06`: flat debris planes jutting at base
- `BR01_01_viaduct_bridge_01`: dark/inverted patches visible in the arch spandrels under the deck
- `HB01_03_harbour_wall_tower_03`: plain flat grey box, little relief; reads slightly bland/default
- `NE01_04_village_sign_04`: board sits on a plain tapered sand-coloured plinth that reads as a blank wedge
- `NE02_01_entry_rock_pair_01`: small stray green/flat patch at base
- `NE02_02_entry_rock_pair_02`: stray white flat patch on upper face
- `NE02_04_entry_rock_pair_04`: very dark near-black rock colour vs cream siblings
- `EV01_01_elf_house_new_01`: stacked ring tiers at base look slightly offset/clipping; loose plank segments at ground
- `EV01_05_elf_house_new_05`: front is a big open dark round doorway with a see-through hollow interior behind the columns; reads as an open gazebo more than a house
- `EV03_03_elf_path_piece_03`: arched deck has an open gap/see-through underside between the ramp and the deck
- `EV03_06_elf_path_piece_06`: flat ring planter, trees inside look placed a bit randomly
- `TW03_01_skull_avenue_set_01`: dark brazier bowl on a thin tripod reads generic, not skull-avenue themed

## Tower scores

| id | verdict | scores |
|---|---|---|
| `WT01_01_wizard_tower_shell` | OK | {"exterior": 9, "interior": 8, "bookshelves": 8, "map": 9, "silhouette": 9, "materials": 8} |
| `WT02_01_wizard_tower_interior` | MAJOR | {"exterior": 8, "interior": 8, "bookshelves": 3, "map": 3, "silhouette": 8, "materials": 8} |
| `WT05_01_wizard_round_map_table` | OK | {"exterior": 8, "interior": 8, "bookshelves": 8, "map": 10, "silhouette": 9, "materials": 9} |