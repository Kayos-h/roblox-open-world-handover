# Assignment A1: plains, ruins and crater rocks

31 models: REDO 0, MAJOR 8, MINOR 23, OK-with-note 0. Work in the order of the table (worst first).

## Your modules (you own these files and nothing else)

| fix module | worker | new palette prefix | round-1 module to read |
|---|---|---|---|
| `library\src\v5_fx_vi_a.py` | vi | `vi_fa_` | `library\src\v5_vi.py` |

Scratch build: `powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\Nitro\.kiro\crew\workspace\town\scratch.ps1" -Module <fix module> -Ids <id,id,...> -Tag A1`
Sheets land in `library\v5_work\fix_scratch\A1\<id>.png`. Target size is W x D x H in studs (X, Y, Z); the manifest autofit (`mk(..., 0.1)`) rescales a model that is more than 10% off, which distorts it, so design to size.

## Families in this assignment

FL01 x3, LM19 x5, LM20 x1, LM21 x2, LM26 x3, LM27 x2, LM28 x3, LM29 x2, LM31 x3, PL02 x1, PL03 x1, PL05 x3, PL06 x2

## Models

| id | verdict | category | target W x D x H | tri budget | tris now | what the reviewers saw | reviewer suggestion |
|---|---|---|---|---|---|---|---|
| `LM19_02_crater_rim_rock_02` | MAJOR | v5_landmarks | 60 x 50 x 40 | 12000 | 1080 | large very dark/near-black facets read as holes or inverted faces; flat grey, crude | Check face normals on the dark faces and lighten; add relief and warmer rock tone. |
| `LM19_04_crater_rim_rock_04` | MAJOR | v5_landmarks | 60 x 50 x 40 | 12000 | 1080 | large dark/near-black facets read as inverted faces or holes; flat grey, crude | Recalculate normals on the dark faces, lighten and add warm rock tone with more relief. |
| `LM19_05_crater_rim_rock_05` | MAJOR | v5_landmarks | 60 x 50 x 40 | 12000 | 1080 | big flat near-black block face looks like an inverted normal; flat grey rock pile | Fix the inverted/dark face, break up the large flat block and add colour variation. |
| `LM27_01_ruin_aqueduct_arch_01` | MAJOR | v5_landmarks | 40 x 12 x 50 | 12000 | 668 | solid black rectangular patches across the parapet read as holes/gaps; stray green nubs stuck to piers | Fill the black gaps with proper stone blocks (or model them as real openings with back faces); remove stray green bits. |
| `LM27_02_ruin_aqueduct_arch_02` | MAJOR | v5_landmarks | 40 x 12 x 50 | 12000 | 656 | black holes along broken parapet; green nubs clinging to columns | Close/backface the black gaps and remove floating green specks. |
| `LM29_02_ruin_tower_stump_02` | MAJOR | v5_landmarks | 26 x 26 x 36 | 10000 | 370 | reads as a plain cream box, square silhouette; almost no relief, crude for a tower stump | Make the stump round or battered with an eroded broken top and surface relief, not a flat rectangular box. |
| `LM31_03_ruined_castle_module_03` | MAJOR | v5_landmarks | 40 x 30 x 40 | 14000 | 996 | two plain flat grey slabs, minimal detail; crude, reads as blank blocks not castle ruin | Add wall thickness, broken crenellations, window/arrow slits and surface relief so it reads as a ruined wall. |
| `PL05_02_ruined_watchtower_plains_02` | MAJOR | v5_plains | 20 x 20 x 40 | 9000 | 370 | plain cream rectangular box with windows, square silhouette; crude, does not read as a round ruined watchtower | Rebuild as a round/battered tower with eroded broken top and surface relief instead of a flat box. |
| `FL01_01_floating_island_hero_01` | MINOR | v5_coast | 90 x 90 x 60 | 30000 | 16804 | underside is a stack of thin flat square plates, reads artificial close up; top layout near-identical to FL01_02/03 (variety) | Reshape the underside into a tapering natural rock/root mass; vary the tower+tree arrangement between the three heroes. |
| `FL01_02_floating_island_hero_02` | MINOR | v5_coast | 90 x 90 x 60 | 30000 | 16792 | same stacked-plate underside; same ruined tower and tree layout as siblings | Give it a distinct top composition and a less papery underside. |
| `FL01_03_floating_island_hero_03` | MINOR | v5_coast | 90 x 90 x 60 | 30000 | 16768 | stacked-plate underside; layout repeats FL01_01/02 | Differentiate the island shape and props from the other two heroes. |
| `LM19_01_crater_rim_rock_01` | MINOR | v5_landmarks | 60 x 50 x 40 | 12000 | 1080 | flat grey, little relief; some near-black shadowed facets | Add subtle colour variation and break up large flat faces so it reads as weathered rock, not grey default. |
| `LM19_03_crater_rim_rock_03` | MINOR | v5_landmarks | 60 x 50 x 40 | 12000 | 1080 | flat grey rock pile, dark facets; crude chunky blocks | Add colour variation and smaller detail rocks; verify no inverted dark faces. |
| `LM20_02_crater_arcane_ruin_02` | MINOR | v5_landmarks | 40 x 40 x 40 | 14000 | 408 | blue rune marks risk reading as emissive; a stray small green nub near base | Keep rune trim matte (no glow); confirm no stray prop geometry is saved with the model. |
| `LM21_02_floating_rock_02` | MINOR | v5_landmarks | 40 x 40 x 30 | 8000 | 330 | underside rock chunks look loosely jumbled/semi-detached | Merge the underside rock mass into one tapered root so chunks don't read as floating fragments. |
| `LM21_04_floating_rock_04` | MINOR | v5_landmarks | 40 x 40 x 30 | 8000 | 330 | underside chunks slightly disconnected; close recolour of siblings | Vary the island outline and tidy the underside into a cohesive tapered mass. |
| `LM26_01_ruin_arena_segment_01` | MINOR | v5_landmarks | 60 x 30 x 34 | 14000 | 1040 | thin white bars between columns read flat/railing-like; very similar to siblings | Give columns more depth and vary the broken top edge between the three segments. |
| `LM26_02_ruin_arena_segment_02` | MINOR | v5_landmarks | 60 x 30 x 34 | 14000 | 1052 | near-identical to segment_01 (recolour feel); flat white infill bars | Differentiate the broken silhouette and thicken the column/arch geometry. |
| `LM26_03_ruin_arena_segment_03` | MINOR | v5_landmarks | 60 x 30 x 34 | 14000 | 1064 | flat infill bars; variety overlap with other arena segments | Vary ruin damage pattern; add depth to the colonnade. |
| `LM28_01_ruin_column_set_01` | MINOR | v5_landmarks | 24 x 24 x 40 | 8000 | 1064 | grey-white drum banding looks a bit striped; small floating debris | Soften the stripe contrast and settle debris on the ground. |
| `LM28_02_ruin_column_set_02` | MINOR | v5_landmarks | 24 x 24 x 40 | 8000 | 1412 | striped drum look; scattered small floating chunks | Reduce band contrast; ground the rubble. |
| `LM28_03_ruin_column_set_03` | MINOR | v5_landmarks | 24 x 24 x 40 | 8000 | 1240 | two columns read as recolour of the other sets; banding stripes | Vary column heights/breaks and tone down stripes. |
| `LM29_01_ruin_tower_stump_01` | MINOR | v5_landmarks | 26 x 26 x 36 | 10000 | 1628 | floating broken-top chunks sit slightly above the rim | Attach the broken crenellation chunks to the wall top. |
| `LM31_01_ruined_castle_module_01` | MINOR | v5_landmarks | 40 x 30 x 40 | 14000 | 1636 | green moss bands look like painted rings; slight sibling overlap | Break the moss into patches rather than continuous bands. |
| `LM31_02_ruined_castle_module_02` | MINOR | v5_landmarks | 40 x 30 x 40 | 14000 | 2368 | continuous green ring bands; similar to module_01 | Vary the tower damage and scatter the moss. |
| `PL02_01_hay_silo_01` | MINOR | v5_plains | 14 x 14 x 24 | 5000 | 486 | reads as hay sheaves/stooks, not a silo (naming/concept mismatch) | Fine as a grain-sheaf prop; relabel or add a silo variant if a true silo is needed. |
| `PL03_02_farm_cart_02` | MINOR | v5_plains | 14 x 8 x 8 | 3000 | 576 | near-identical to farm_cart_01 (empty vs loaded only difference) | Vary the cart shape or add distinct cargo so the pair isn't a recolour. |
| `PL05_01_ruined_watchtower_plains_01` | MINOR | v5_plains | 20 x 20 x 40 | 9000 | 1628 | floating broken-top chunks above the rim | Attach the broken crenellation debris to the wall top. |
| `PL05_03_ruined_watchtower_plains_03` | MINOR | v5_plains | 20 x 20 x 40 | 9000 | 2920 | looks intact/new with a clean red cone roof, not ruined as the id states | Add damage (broken roof edge, cracks, missing crenellations) to match the 'ruined' concept, or relabel as an intact watchtower. |
| `PL06_01_rock_arch_natural_01` | MINOR | v5_plains | 60 x 24 x 40 | 12000 | 1356 | flat grey rock, little colour variation | Add warm/earth tone variation and relief so it reads as weathered stone, not grey default. |
| `PL06_02_rock_arch_natural_02` | MINOR | v5_plains | 60 x 24 x 40 | 12000 | 1356 | flat grey rock, little colour variation; small floating green/blue bits at base | Add warm stone tone variation and remove stray specks. |