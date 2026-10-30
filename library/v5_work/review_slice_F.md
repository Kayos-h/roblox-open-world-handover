# Review slice F (sheets 026-030)

Reviewer F, 60 models (desert mesa/ruins, Skull City-adjacent desert, crater/floating/ruin landmarks, plains, coastal). No hero sheets or wizard towers fall in this slice.

## Verdict counts
- OK: 15
- MINOR: 28
- MAJOR: 17
- REDO: 0

## Non-OK models

| id | verdict | what is wrong | how to fix |
|----|---------|---------------|------------|
| SD01_04_red_mesa_cluster_04 | MAJOR | stacked flat slabs, not a broad flat-topped mesa; teetering pancake tower | rebuild as wide flat-topped butte with sloped strata sides |
| SD01_05_red_mesa_cluster_05 | MAJOR | reads as a stack of coins/slabs; narrow unstable | one solid wide red rock mass, eroded flanks, keep banding |
| SD01_06_red_mesa_cluster_06 | MAJOR | slab-stack tower; flat base debris planes | broad buttressed mesa; chunky fallen rocks for debris |
| SD02_01_desert_ruin_block_01 | MINOR | thin flat base debris planes; sibling overlap | replace flat slabs with 3D rubble |
| SD02_02_desert_ruin_block_02 | MINOR | flat base planes; similar massing | volumetric rubble, vary broken skyline |
| SD02_04_desert_ruin_block_04 | MINOR | flat base planes; recolour of 01 | distinct silhouette + 3D rubble |
| SD02_05_desert_ruin_block_05 | MINOR | thin base planes; variety overlap | vary massing, chunky debris |
| SD02_06_desert_ruin_block_06 | MINOR | flat jutting base planes | solid rubble blocks |
| LM19_01_crater_rim_rock_01 | MINOR | flat grey, dark facets | colour variation, break up flat faces |
| LM19_02_crater_rim_rock_02 | MAJOR | near-black facets read as holes/inverted faces | fix normals, lighten, add relief/warm tone |
| LM19_03_crater_rim_rock_03 | MINOR | flat grey, dark facets, crude | colour variation, verify normals |
| LM19_04_crater_rim_rock_04 | MAJOR | dark/near-black facets read as inverted | recalc normals, warm tone, relief |
| LM19_05_crater_rim_rock_05 | MAJOR | big flat near-black face (inverted normal) | fix inverted face, break up block |
| LM20_02_crater_arcane_ruin_02 | MINOR | blue runes risk emissive look; stray green nub | keep runes matte; drop stray prop geo |
| LM21_02_floating_rock_02 | MINOR | underside chunks look semi-detached | merge underside into tapered root |
| LM21_04_floating_rock_04 | MINOR | underside chunks loose; recolour of siblings | vary outline, cohesive underside |
| LM26_01_ruin_arena_segment_01 | MINOR | flat white infill bars; very like siblings | depth on columns, vary broken top |
| LM26_02_ruin_arena_segment_02 | MINOR | near-identical to 01; flat bars | differentiate silhouette, thicken geo |
| LM26_03_ruin_arena_segment_03 | MINOR | flat bars; variety overlap | vary damage, add colonnade depth |
| LM27_01_ruin_aqueduct_arch_01 | MAJOR | solid black patches across parapet read as holes; stray green nubs | fill/backface the black gaps; remove specks |
| LM27_02_ruin_aqueduct_arch_02 | MAJOR | black holes on broken parapet; green nubs | close/backface gaps; remove floating bits |
| LM28_01_ruin_column_set_01 | MINOR | striped drums; small floating debris | soften bands, ground debris |
| LM28_02_ruin_column_set_02 | MINOR | striped drums; floating chunks | reduce band contrast, ground rubble |
| LM28_03_ruin_column_set_03 | MINOR | recolour of other sets; stripes | vary heights/breaks, tone down stripes |
| LM29_01_ruin_tower_stump_01 | MINOR | floating broken-top chunks | attach crenellation debris |
| LM29_02_ruin_tower_stump_02 | MAJOR | plain cream box, square, no relief | rebuild round/battered, eroded broken top |
| LM31_01_ruined_castle_module_01 | MINOR | moss bands look painted | break moss into patches |
| LM31_02_ruined_castle_module_02 | MINOR | continuous green rings; like 01 | vary damage, scatter moss |
| LM31_03_ruined_castle_module_03 | MAJOR | two plain flat grey slabs, no detail | add thickness, broken crenellations, slits, relief |
| PL02_01_hay_silo_01 | MINOR | reads as hay sheaves not a silo | relabel or add true silo variant |
| PL03_02_farm_cart_02 | MINOR | near-identical to cart_01 | vary shape/cargo |
| PL05_01_ruined_watchtower_plains_01 | MINOR | floating broken-top chunks | attach debris to wall top |
| PL05_02_ruined_watchtower_plains_02 | MAJOR | plain cream box, square, crude | rebuild round/battered with eroded top |
| PL05_03_ruined_watchtower_plains_03 | MINOR | intact/new, not ruined as id says | add damage or relabel as intact |
| PL06_01_rock_arch_natural_01 | MINOR | flat grey, little colour | warm tone variation, relief |
| PL06_02_rock_arch_natural_02 | MINOR | flat grey; stray base specks | tone variation, remove specks |
| CO03_01_reef_01 | MAJOR | blocky dark camouflage patches; flat slab | even tone, 3D relief |
| CO03_02_reef_02 | MAJOR | square dark patches; flat jumbled slabs | coherent colour, relief, settle slabs |
| CO03_03_reef_03 | MAJOR | blocky patches; flat, samey | recolour evenly, 3D shaping, vary |
| CO03_04_reef_04 | MAJOR | dark patches; jumbled overlapping planes (clipping) | solid reef mound, even colour |
| CO03_05_reef_05 | MAJOR | square patches; messy overlapping plates | consolidate body, even tone, relief |
| CO03_06_reef_06 | MAJOR | camouflage patches; flat recolour | even recolour, relief, differentiate |
| CO04_01_sea_arch_01 | MINOR | flat grey stone | weathered tone variation |
| CO04_02_sea_arch_02 | MINOR | flat grey; close to 01 | vary profile, stone colour |
| CO05_01_ruin_islet_01 | MINOR | hard flat grass-on-rock seam; jumbled base | sloped grass rim, tidy boulders |
| CO05_02_ruin_islet_02 | MINOR | hard grass seam; like 01 | soften rim, vary layout |
| CO05_03_ruin_islet_03 | MAJOR | blocky tan camouflage patches on base rock; hard seam | remove patches, coherent colour, blend grass |

## Systemic issues
1. **Blocky camouflage colour patches on rock** (whole CO03 reef set, CO05_03) — random dark/tan polygon blotches painted on flat rock tops. Fix: use smooth tonal variation per-rock, never per-face random blotches.
2. **Dark/near-black facets = inverted normals** on grey rock piles (LM19 series). Fix: recalculate face normals outward and verify no black interior faces show.
3. **Plain rectangular boxes standing in for round towers** (LM29_02, PL05_02) — crude square silhouettes for pieces that should be round/battered ruins. Fix: round/taper the body and model an eroded broken top with relief.
4. **Black-hole gaps in ruin parapets** (LM27 aqueducts) — open backless rectangles read as holes. Fix: fill or backface every opening.
5. **Flat thin "debris" planes at building/mesa bases** (SD01/SD02) — look like clipping planes, not rubble. Fix: replace with small solid 3D rock chunks resting on ground.
6. **Low variety within sets** (SD02, LM26, LM31, CO04, CO05, farm carts) — siblings read as recolours. Fix: change massing/silhouette, not just colour.
7. **Flat grey natural rock** (LM19, PL06, CO04 arches) — grey default look. Fix: add earth-tone variation and surface relief.

## Could not judge
None requiring a close-up beyond what the sheets showed; no hero/wizard pieces in this slice.
