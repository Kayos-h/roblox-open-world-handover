# Assignment A2: road life, bridges, coast and reefs

32 models: REDO 1, MAJOR 14, MINOR 17, OK-with-note 0. Work in the order of the table (worst first).

## Your modules (you own these files and nothing else)

| fix module | worker | new palette prefix | round-1 module to read |
|---|---|---|---|
| `library\src\v5_fx_vi_b.py` | vi | `vi_fb_` | `library\src\v5_vi.py` |

Scratch build: `powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\Nitro\.kiro\crew\workspace\town\scratch.ps1" -Module <fix module> -Ids <id,id,...> -Tag A2`
Sheets land in `library\v5_work\fix_scratch\A2\<id>.png`. Target size is W x D x H in studs (X, Y, Z); the manifest autofit (`mk(..., 0.1)`) rescales a model that is more than 10% off, which distorts it, so design to size.

## Families in this assignment

BR01 x2, CO03 x6, CO04 x2, CO05 x3, HB01 x1, RD01 x2, RD02 x4, RD05 x5, RD06 x3, RV01 x4

## Models

| id | verdict | category | target W x D x H | tri budget | tris now | what the reviewers saw | reviewer suggestion |
|---|---|---|---|---|---|---|---|
| `RD05_05_battlefield_prop_05` | REDO | v5_roads | 14 x 10 x 10 | 3000 | 572 | detached floating red and blue disc parts; exploded, not assembled; no coherent object | Rebuild from scratch as a single connected prop; the current parts float apart and read as broken. |
| `BR01_02_viaduct_bridge_02` | MAJOR | v5_roads | 160 x 20 x 40 | 24000 | 3692 | black inverted faces under the arches; unexplained grey slab block sitting on the deck midway | Fix the inverted arch faces and remove or justify the grey block on the deck; it reads as a stray/clipping part. |
| `CO03_01_reef_01` | MAJOR | v5_coast | 30 x 30 x 6 | 6000 | 684 | blocky dark-grey camouflage colour patches on flat rock tops; very flat low slab, little relief | Remove the random dark polygon patches, use smooth tonal variation, and give the reef bumpy 3D relief instead of flat slabs. |
| `CO03_02_reef_02` | MAJOR | v5_coast | 30 x 30 x 6 | 6000 | 524 | square dark camouflage patches on rock; flat jumbled slabs | Replace blotchy patches with coherent rock colour; add rounded relief and settle overlapping slabs. |
| `CO03_03_reef_03` | MAJOR | v5_coast | 30 x 30 x 6 | 6000 | 684 | blocky dark colour patches; flat slab silhouette, samey with set | Recolour evenly and add 3D reef shaping; vary from siblings. |
| `CO03_04_reef_04` | MAJOR | v5_coast | 30 x 30 x 6 | 6000 | 524 | dark camouflage patches; jumbled overlapping flat slabs read as clipping planes | Rebuild as a solid low reef mound with even colour; merge the loose slabs. |
| `CO03_05_reef_05` | MAJOR | v5_coast | 30 x 30 x 6 | 6000 | 684 | square dark patches; messy overlapping flat plates | Consolidate into one reef body, even rock tone, add relief. |
| `CO03_06_reef_06` | MAJOR | v5_coast | 30 x 30 x 6 | 6000 | 524 | camouflage dark patches; flat jumbled slabs, recolour of set | Even recolour, 3D relief, differentiate from siblings. |
| `CO05_03_ruin_islet_03` | MAJOR | v5_coast | 60 x 60 x 40 | 16000 | 11192 | blocky tan/yellow colour patches on the base rock read as camouflage blotches; hard grass seam | Remove the square sand-coloured patches, use coherent rock colour, and blend the grass cap. |
| `RD05_01_battlefield_prop_01` | MAJOR | v5_roads | 14 x 10 x 10 | 3000 | 192 | unreadable silhouette; jumble of brown planks/wheel, no clear object; parts look detached/clipping | Rebuild as a clearly readable prop (broken cart or barricade) with connected parts and a recognisable shape. |
| `RD05_02_battlefield_prop_02` | MAJOR | v5_roads | 14 x 10 x 10 | 3000 | 192 | silhouette does not read as anything; flat plank balanced on a rock/disc | Redesign into an identifiable battlefield item (overturned table, broken shield stack) that reads at 30-60 studs. |
| `RD05_03_battlefield_prop_03` | MAJOR | v5_roads | 14 x 10 x 10 | 3000 | 100 | flat red slab on thin runners, unreadable; no believable object | Rebuild as a recognisable fallen banner or sledge with volume, not a single flat slab. |
| `RD06_01_abandoned_house_01` | MAJOR | v5_roads | 22 x 20 x 20 | 9000 | 772 | large flat grey slab wall with no detail; chimney/parts appear detached; collapse reads as a defect not ruin | Replace the blank grey slab with a broken half-timber wall, anchor the chimney, and make the collapse intentional. |
| `RD06_03_abandoned_house_03` | MAJOR | v5_roads | 22 x 20 x 20 | 9000 | 772 | huge blank dark slab dominates; silhouette unreadable as a house; flat untextured faces | Rebuild the fallen wall as a ruined timber-framed panel with debris; remove the featureless slab. |
| `RD06_05_abandoned_house_05` | MAJOR | v5_roads | 22 x 20 x 20 | 9000 | 772 | blank flat grey slab wall; no house relief; collapse looks broken not designed | Give the standing wall half-timber relief and windows; make the rubble read as deliberate ruin. |
| `BR01_01_viaduct_bridge_01` | MINOR | v5_roads | 160 x 20 x 40 | 24000 | 3680 | dark/inverted patches visible in the arch spandrels under the deck | Check face normals under the arches; fill the spandrels so no black inverted faces show. |
| `CO04_01_sea_arch_01` | MINOR | v5_coast | 70 x 30 x 60 | 14000 | 876 | flat grey stone, little colour variation | Add weathered stone tone variation; silhouette is good. |
| `CO04_02_sea_arch_02` | MINOR | v5_coast | 70 x 30 x 60 | 14000 | 876 | flat grey, close to sea_arch_01 | Vary the arch profile from its sibling and add stone colour relief. |
| `CO05_01_ruin_islet_01` | MINOR | v5_coast | 60 x 60 x 40 | 16000 | 11264 | green grass platform meets rock with a hard flat edge; base rock slightly jumbled | Blend the grass cap onto the rock with a sloped rim and tidy the base boulders. |
| `CO05_02_ruin_islet_02` | MINOR | v5_coast | 60 x 60 x 40 | 16000 | 11192 | hard flat grass-on-rock seam; similar to islet_01 | Soften the grass rim and vary tower/tree arrangement. |
| `HB01_03_harbour_wall_tower_03` | MINOR | v5_coast | 24 x 24 x 40 | 10000 | 336 | plain flat grey box, little relief; reads slightly bland/default | Add stone colour/trim or corner detail so it is not a flat grey cube with two windows. |
| `RD01_02_watchtower_02` | MINOR | v5_roads | 20 x 20 x 50 | 11000 | 370 | plain featureless box, open/hollow top; no roof or crenellation detail | Cap the open top and add a simple roof or crenellation so it does not read as a bare box. |
| `RD01_04_watchtower_04` | MINOR | v5_roads | 20 x 20 x 50 | 11000 | 370 | plain box walls with floating broken-crenellation chunks on top | Anchor the broken battlement pieces to the wall top so none appear detached, and add slight wall relief. |
| `RD02_01_camp_set_01` | MINOR | v5_roads | 16 x 14 x 10 | 4000 | 108 | identical geometry to RD02_02/03, only recolored (variety) | Differentiate the three tents by shape (size, awning, flap) instead of colour only. |
| `RD02_02_camp_set_02` | MINOR | v5_roads | 16 x 14 x 10 | 4000 | 108 | recolor of RD02_01 (variety) | Give it distinct geometry from the other tents, not just a red skin. |
| `RD02_03_camp_set_03` | MINOR | v5_roads | 16 x 14 x 10 | 4000 | 108 | recolor of RD02_01 (variety) | Give it distinct geometry from the other tents, not just a blue skin. |
| `RD02_06_camp_set_06` | MINOR | v5_roads | 16 x 14 x 10 | 4000 | 152 | dark gap/hole at bottom-front of the barrel | Close the end cap so there is no see-through black gap at the barrel foot. |
| `RD05_04_battlefield_prop_04` | MINOR | v5_roads | 14 x 10 x 10 | 3000 | 232 | reads as a spiked barricade but crude/boxy | Vary spike angles and add a base rail so it reads clearly as a cheval-de-frise. |
| `RV01_01_bank_rock_01` | MINOR | v5_roads | 30 x 20 x 10 | 5000 | 576 | near-monochrome flat grey, little colour; reads as default grey rock | Add subtle earth/moss colour variation so it does not read as a grey default blockout. |
| `RV01_02_bank_rock_02` | MINOR | v5_roads | 30 x 20 x 10 | 5000 | 576 | flat grey, same style as siblings (variety/colour) | Vary tone and add a touch of moss/soil; differentiate shape from RV01_01. |
| `RV01_03_bank_rock_03` | MINOR | v5_roads | 30 x 20 x 10 | 5000 | 576 | flat grey monochrome, little relief colour | Introduce colour variation and avoid the uniform grey default look. |
| `RV01_04_bank_rock_04` | MINOR | v5_roads | 30 x 20 x 10 | 5000 | 576 | flat grey, reads like a recolor-less sibling | Add colour/tone variation and distinguish silhouette from the other bank rocks. |