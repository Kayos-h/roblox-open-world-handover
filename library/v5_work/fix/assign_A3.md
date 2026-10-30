# Assignment A3: desert and Skull City

40 models: REDO 4, MAJOR 11, MINOR 23, OK-with-note 2. Work in the order of the table (worst first).

## Your modules (you own these files and nothing else)

| fix module | worker | new palette prefix | round-1 module to read |
|---|---|---|---|
| `library\src\v5_fx_vh.py` | vh | `vh_f_` | `library\src\v5_vh.py` |

Scratch build: `powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\Nitro\.kiro\crew\workspace\town\scratch.ps1" -Module <fix module> -Ids <id,id,...> -Tag A3`
Sheets land in `library\v5_work\fix_scratch\A3\<id>.png`. Target size is W x D x H in studs (X, Y, Z); the manifest autofit (`mk(..., 0.1)`) rescales a model that is more than 10% off, which distorts it, so design to size.

## Families in this assignment

DS01 x2, DS02 x1, DS03 x1, DS04 x3, DS05 x1, DS07 x3, DS08 x3, LM10 x1, LM12 x2, LM13 x2, LM14 x1, LM16 x2, SD01 x3, SD02 x5, VC01 x2, VC03 x2, VC04 x6

## Models

| id | verdict | category | target W x D x H | tri budget | tris now | what the reviewers saw | reviewer suggestion |
|---|---|---|---|---|---|---|---|
| `VC04_01_skull_city_building_01` | REDO | v5_skull | 30 x 30 x 30 | 11000 | 332 | hollow open grey box, not a building; detached wooden poles float above it; no roof, no facade, no identity | Rebuild as a recognisable ruined building with walls, an opening and seated/attached timber beams instead of a hollow box with floating poles. |
| `VC04_02_skull_city_building_02` | REDO | v5_skull | 30 x 30 x 30 | 11000 | 332 | open hollow box; floating detached poles; unreadable | Rebuild as an identifiable structure with attached beams. |
| `VC04_04_skull_city_building_04` | REDO | v5_skull | 30 x 30 x 30 | 11000 | 332 | hollow open box; floating detached poles; no identity | Rebuild as a recognisable building with attached beams. |
| `VC04_05_skull_city_building_05` | REDO | v5_skull | 30 x 30 x 30 | 11000 | 332 | hollow open box; floating detached poles | Rebuild into an identifiable structure; attach the beams. |
| `DS07_04_hoodoo_arch_04` | MAJOR | v5_desert | 40 x 30 x 70 | 12000 | 924 | collapsed into a chaotic pile of blocks with one thin spire; no legible arch; camouflage colour patches | Rebuild as a clear eroded rock arch with a connected span; remove the scattered block rubble and fix colour banding. |
| `DS08_01_underground_entrance_01` | MAJOR | v5_desert | 30 x 30 x 24 | 9000 | 1812 | flat wall with a staircase stuck on its face; jumble of clipping amorphous slabs; no readable entrance/opening; single flat sand colour | Rebuild as a clear sunken doorway/ramp descending into the ground with framing and a dark opening; remove clipping slabs. |
| `DS08_02_underground_entrance_02` | MAJOR | v5_desert | 30 x 30 x 24 | 9000 | 1812 | same confusing clipping-slab mass as 01; no clear entrance | Rebuild with a legible descending entrance and distinct ground opening. |
| `DS08_03_underground_entrance_03` | MAJOR | v5_desert | 30 x 30 x 24 | 9000 | 1824 | same illegible clipping composition; no entrance read | Rebuild as a clear buried entrance; vary design from 01/02. |
| `LM12_01_temple_stair_down_01` | MAJOR | v5_landmarks | 30 x 40 x 24 | 9000 | 1288 | reads as a jumble of flat clipping slabs; no clear descending stair silhouette; small floating boxes top-left | Rebuild as a readable recessed stair cut into the ground with clear step treads and framing walls; remove floating fragments. |
| `LM12_02_temple_stair_down_02` | MAJOR | v5_landmarks | 30 x 40 x 24 | 9000 | 1288 | confusing overlapping slabs; stair not legible; flat single-colour mass | Rebuild with distinct stepped treads descending into a clear pit opening instead of stacked flat planes. |
| `SD01_04_red_mesa_cluster_04` | MAJOR | v5_desert | 120 x 100 x 90 | 16000 | 1368 | silhouette wrong: stacked flat slabs, not a broad flat-topped mesa; teetering pancake-tower look; thin flat debris planes at base | Rebuild as a broad flat-topped butte with sloped sides and horizontal strata, wider than tall; remove the stacked-box tower shape. |
| `SD01_05_red_mesa_cluster_05` | MAJOR | v5_desert | 120 x 100 x 90 | 16000 | 1260 | reads as a stack of coins/slabs, not a mesa; narrow unstable silhouette; flat ground debris planes | Reshape into one solid wide red rock mass with eroded flanks; keep the red/tan banding but lose the pancake stacking. |
| `SD01_06_red_mesa_cluster_06` | MAJOR | v5_desert | 120 x 100 x 90 | 16000 | 1416 | slab-stack tower not a mesa; flat clipping debris planes around base | Rebuild as a broad buttressed mesa form; replace flat base planes with chunky fallen rocks. |
| `VC04_03_skull_city_building_03` | MAJOR | v5_skull | 30 x 30 x 30 | 11000 | 1116 | mostly a hollow box but has a broken tower; poles float detached above | Attach the timber beams to the structure and close/define the box into a readable ruined building. |
| `VC04_06_skull_city_building_06` | MAJOR | v5_skull | 30 x 30 x 30 | 11000 | 1116 | hollow box with a broken tower stub; floating detached poles | Attach beams and define the box into a readable ruined building. |
| `DS01_03_adobe_house_03` | MINOR | v5_desert | 20 x 20 x 18 | 8000 | 1336 | large blue slab against front wall; parapet merlons read as loose blocks | Confirm the blue slab is not part of the model; if it is, remove it. Seat the merlons solidly on the parapet. |
| `DS01_04_adobe_house_04` | MINOR | v5_desert | 20 x 20 x 18 | 8000 | 1260 | stray yellow beam on ground in front | Remove or attach the loose yellow beam lying in front of the house. |
| `DS02_01_desert_market_01` | MINOR | v5_desert | 24 x 18 x 16 | 6000 | 640 | well + loose cylinders read as generic, not clearly a market; small floating/clipping cubes on plank | Rename or redress toward a market stall, or seat the barrels/goods cleanly; remove stray cubes. |
| `DS04_01_palm_01` | MINOR | v5_desert | 14 x 14 x 42 | 6000 | 2420 | thin spindly trunk; sparse drooping fronds look wiry; faint stray wire ring near base | Thicken the trunk slightly and give the fronds more volume/breadth so the canopy reads as a palm; remove the stray wire geometry at the base. |
| `DS04_02_palm_02` | MINOR | v5_desert | 14 x 14 x 42 | 6000 | 2420 | spindly trunk; sparse fronds; near-identical to palm 01/03 | Fuller fronds and a stouter trunk; vary lean/height from siblings. |
| `DS04_03_palm_03` | MINOR | v5_desert | 14 x 14 x 42 | 6000 | 2420 | spindly trunk; sparse fronds; near-identical to siblings | Fuller canopy and varied silhouette from palms 01/02. |
| `DS07_01_hoodoo_arch_01` | MINOR | v5_desert | 40 x 30 x 70 | 12000 | 528 | blocky square red/cream colour patches look like camouflage; reads as two separate spires, not an arch | Blend the colour banding into horizontal strata and connect the tops into a clear arch span. |
| `DS07_02_hoodoo_arch_02` | MINOR | v5_desert | 40 x 30 x 70 | 12000 | 636 | patchy camouflage-like colour blocks; arch connection unclear | Use layered horizontal rock bands instead of square patches and make the arch span read clearly. |
| `LM10_02_temple_colonnade_buried_02` | MINOR | v5_landmarks | 60 x 20 x 40 | 14000 | 3936 | black/inverted face on top of lintel | Recalculate normals on the lintel so the top face is not black. |
| `LM13_01_guardian_statue_01` | MINOR | v5_landmarks | 20 x 20 x 70 | 18000 | 428 | small black/inverted face near head; very thin crude figure | Fix the black face normal and widen the torso/head so it reads as a carved guardian figure. |
| `LM13_02_guardian_statue_02` | MINOR | v5_landmarks | 20 x 20 x 70 | 18000 | 404 | small black/inverted face near head; thin crude figure | Fix the black face normal and bulk up the figure for a clearer statue silhouette. |
| `LM14_03_sand_obelisk_03` | MINOR | v5_landmarks | 10 x 10 x 60 | 5000 | 592 | near-identical recolour of obelisk 01/02 | Vary height, carving marks or erosion so the three obelisks are not identical. |
| `LM16_01_ring_temple_segment_01` | MINOR | v5_landmarks | 50 x 25 x 40 | 14000 | 736 | plain curved slab with little relief; flat single-colour mass | Add carved panelling, step relief or weathering to the curved wall so it is not a featureless slab. |
| `LM16_02_ring_temple_segment_02` | MINOR | v5_landmarks | 50 x 25 x 40 | 14000 | 604 | near-identical to segment 01; flat featureless curved mass | Differentiate from segment 01 with distinct relief/damage and add surface detail. |
| `SD02_01_desert_ruin_block_01` | MINOR | v5_desert | 40 x 40 x 30 | 10000 | 1480 | thin flat debris planes jutting from base; slight variety overlap with siblings | Replace the flat ground slabs with small 3D rubble chunks. |
| `SD02_02_desert_ruin_block_02` | MINOR | v5_desert | 40 x 40 x 30 | 10000 | 1724 | flat debris planes at base; similar massing to other SD02 blocks | Swap flat base planes for volumetric rubble and vary the broken-wall skyline. |
| `SD02_04_desert_ruin_block_04` | MINOR | v5_desert | 40 x 40 x 30 | 10000 | 1480 | flat debris planes at base; reads as recolour/remix of SD02_01 | Give it a distinct broken silhouette and 3D rubble instead of flat slabs. |
| `SD02_05_desert_ruin_block_05` | MINOR | v5_desert | 40 x 40 x 30 | 10000 | 1688 | thin flat base planes; variety overlap with siblings | Vary massing and replace flat ground planes with chunky debris. |
| `SD02_06_desert_ruin_block_06` | MINOR | v5_desert | 40 x 40 x 30 | 10000 | 1968 | flat debris planes jutting at base | Replace flat slabs with small solid rubble blocks. |
| `VC01_07_volcanic_rock_07` | MINOR | v5_skull | 60 x 50 x 60 | 12000 | 2412 | tiny stray block floating at bottom-right | Remove the small detached fragment near the base. |
| `VC01_08_volcanic_rock_08` | MINOR | v5_skull | 60 x 50 x 60 | 12000 | 2512 | small stray fragment at base; set of 8 feel like close variants | Remove the loose fragment; vary spire arrangement across the set. |
| `VC03_01_dark_fort_ruin_01` | MINOR | v5_skull | 60 x 50 x 50 | 16000 | 5840 | a few loose detached blocks/poles at the base | Seat or remove the stray fragments lying at the foot of the walls. |
| `VC03_03_dark_fort_ruin_03` | MINOR | v5_skull | 60 x 50 x 50 | 16000 | 5840 | small detached bits at base | Clean up loose ground fragments. |
| `DS03_02_caravan_wagon_02` | OK | v5_desert | 18 x 10 x 12 | 5000 | 1224 | near-recolour of wagon 01 | Minor: vary the cover shape so the two wagons differ beyond colour. |
| `DS05_02_oasis_rock_ring_02` | OK | v5_desert | 50 x 50 x 10 | 8000 | 2534 | near-recolour of ring 01 | Minor: rearrange rocks so the two rings differ in layout. |