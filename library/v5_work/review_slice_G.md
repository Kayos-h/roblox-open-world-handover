# Review slice G (sheets 031–034)

Reviewer G of 7. Models: RD (road life), RV (river bank rocks), FL (floating islands), BR (viaducts), HB (harbour towers), VL (church), RW01 (reworks). 44 models.

## Verdict counts
- OK: 23
- MINOR: 14
- MAJOR: 6
- REDO: 1
- Total: 44

## Non-OK models

| id | verdict | what is wrong | how to fix |
|----|---------|---------------|------------|
| RD01_02_watchtower_02 | MINOR | plain box, open hollow top, no roof | cap top, add roof/crenellation |
| RD01_04_watchtower_04 | MINOR | box walls, floating broken-battlement chunks | anchor battlement pieces, add wall relief |
| RD02_01_camp_set_01 | MINOR | tent identical to 02/03, recolor only | differentiate geometry not just colour |
| RD02_02_camp_set_02 | MINOR | recolor of 01 | distinct tent shape |
| RD02_03_camp_set_03 | MINOR | recolor of 01 | distinct tent shape |
| RD02_06_camp_set_06 | MINOR | dark gap/hole at barrel foot | close the end cap |
| RD05_01_battlefield_prop_01 | MAJOR | unreadable jumble, parts detached/clipping | rebuild as a clear broken cart/barricade |
| RD05_02_battlefield_prop_02 | MAJOR | plank on rock, no readable object | redesign into an identifiable item |
| RD05_03_battlefield_prop_03 | MAJOR | flat red slab on runners, unreadable | rebuild with volume as banner/sledge |
| RD05_04_battlefield_prop_04 | MINOR | crude boxy barricade | vary spikes, add base rail |
| RD05_05_battlefield_prop_05 | REDO | detached floating red/blue disc parts, exploded | rebuild as one connected prop |
| RD06_01_abandoned_house_01 | MAJOR | blank grey slab wall, detached chimney | broken half-timber wall, anchor chimney |
| RD06_03_abandoned_house_03 | MAJOR | huge blank dark slab, not a house | rebuild as ruined timber panel + debris |
| RD06_05_abandoned_house_05 | MAJOR | flat grey slab wall, no relief | add half-timber relief/windows, deliberate rubble |
| RV01_01_bank_rock_01 | MINOR | flat monochrome grey, default look | add earth/moss colour variation |
| RV01_02_bank_rock_02 | MINOR | flat grey, sibling sameness | vary tone and shape |
| RV01_03_bank_rock_03 | MINOR | flat grey, little relief colour | colour variation |
| RV01_04_bank_rock_04 | MINOR | flat grey recolor-less sibling | colour + silhouette variation |
| FL01_01_floating_island_hero_01 | MINOR | stacked thin-plate underside, layout repeats siblings | natural rock/root underside, vary top |
| FL01_02_floating_island_hero_02 | MINOR | same plate underside + same layout | distinct top composition |
| FL01_03_floating_island_hero_03 | MINOR | plate underside, repeats 01/02 | differentiate island + props |
| BR01_01_viaduct_bridge_01 | MINOR | dark/inverted faces in arch spandrels | fix normals, fill spandrels |
| BR01_02_viaduct_bridge_02 | MAJOR | inverted arch faces + stray grey slab on deck | fix normals, remove/justify deck block |
| HB01_03_harbour_wall_tower_03 | MINOR | flat grey box, bland | add stone colour/trim/corner detail |
| RW01_01_rework_existing_01 | MAJOR | crude pile of offset coloured slabs, unstable read | rebuild as coherent tower/mesa, aligned courses |

(RW01_02 is the intended two-gatepost natural entrance — OK, not an arch violation.)

## Systemic issues
1. **Blank flat slabs standing in for collapsed/ruined walls** (RD06_01/03/05, RW01_01). The "damage" reads as a modelling defect, not deliberate ruin. Fix: model ruined walls as broken timber-frame panels with relief and deliberate rubble, never one featureless slab.
2. **Battlefield props (RD05) don't read as objects.** Several are unidentifiable or have detached/floating parts. Fix: redesign each around one clear, connected silhouette readable at 30–60 studs.
3. **Variety by recolor only.** Camp tents (RD02_01/02/03) and bank rocks (RV01) and the three FL01 heroes differ mainly by colour / repeat the same layout. Fix: vary geometry and composition, not just palette.
4. **Flat monochrome grey = default look.** Bank rocks and HB01_03 read as untextured blockouts. Fix: add subtle colour/tone variation.
5. **Inverted/missing faces under viaduct arches** (BR01_01/02). Fix: recompute normals and close spandrel gaps so no black patches show from player height.

## Could not judge / notes
- RW01 reworks have no hero four-angle sheet; judged from sheet cells only, so interior/back of RW01_01 and the tree-deck RW01_03/04 could not be fully verified (fronts look fine).
