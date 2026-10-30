# v5 review — slice A (sheets review_001–005)

Reviewer A of 7. Models 1–60: wizard tower (WT) and the first Himalayan road kit (HM) plus the NE village signs.

## Verdict counts
- OK: 46
- MINOR: 8
- MAJOR: 6
- REDO: 0
- Total: 60

## Wizard tower scoring (WT, per-category 1–10; min 8 required)
| id | ext | int | shelves | map | silh | mat | result |
|---|---|---|---|---|---|---|---|
| WT01_01_wizard_tower_shell | 9 | 8 | 8 | 9 | 9 | 8 | pass |
| WT02_01_wizard_tower_interior | 8 | 8 | **3** | **3** | 8 | 8 | MAJOR |
| WT05_01_wizard_round_map_table | 8 | 8 | 8 | 10 | 9 | 9 | pass |

The tower **exterior, silhouette, materials and the standalone map table are excellent** (clear island landmark, believable stacked-drum form, good warm materials, map reads perfectly as a brass-rimmed island relief). The failing categories are *inside the tower*: `WT02_01_wizard_tower_interior` has walkable floors and spiral stairs but **no bookshelves placed floor-to-ceiling and no circular map on any floor**. The assets exist (WT03/WT04 shelves, WT05 map) but are not integrated into the interior, so the interior scores 3/3 on those two categories → MAJOR.

## Non-OK models
| id | verdict | what is wrong | how to fix |
|---|---|---|---|
| WT02_01_wizard_tower_interior | MAJOR | no bookshelves and no circular map inside the walkable tower | dress a library floor with WT03/WT04 shelves floor-to-ceiling and set WT05 map on a floor |
| HM04_02_tunnel_lining_02 | MAJOR | black inverted/inside-out faces across the interior; reads as holes | recalculate normals outward / solidify shell, give inner faces lit stone colour |
| HM06_01_switchback_wall_01 | MAJOR | blocky two-tone grey checkerboard camouflage on wall face | replace checker with graded stone tones + real block relief |
| HM06_03_switchback_wall_03 | MAJOR | same grey checkerboard camouflage as _01 | same fix as _01 |
| HM08_02_cairn_shrine_02 | MAJOR | a red-roof hut, not a cairn; off-concept vs its set | rebuild as stacked-rock cairn / whitewashed chorten |
| NE01_01_village_sign_01 | MAJOR | ambiguous grey slab + cylinders + tiny flag; doesn't read as a sign | rebuild as a legible notice board on a post, matching the NE01 set |
| WT13_01_plateau_terrace_set_01 | MINOR | flat cream slab, no relief | add edge trim / steps |
| WT08_02_wizard_study_set_02 | MINOR | sparse bare frame for its tri count | add bedding/drapery detail |
| HM04_01_tunnel_lining_01 | MINOR | inner bore faces look unlit/near-black | give inner faces a lit stone colour |
| HM05_01_cliff_gallery_01 | MINOR | flat grey cliff backing, little relief | vary rock colour/angles |
| HM05_02_cliff_gallery_02 | MINOR | flat grey cliff; snow cap floats as a flat plane | break up rock, seat the snow cap |
| HM06_02_switchback_wall_02 | MINOR | plain flat slabs, bland curve | add coursing/relief |
| HM07_04_prayer_flag_string_04 | MINOR | washed-out near-white flags, low variety | give distinct flag colours |
| NE01_04_village_sign_04 | MINOR | dominant blank tapered plinth | slim base to a post / add detail |

## Systemic issues
1. **Checkerboard two-tone colour camouflage on stone/wall faces** (HM06_01, HM06_03; milder on HM06_02). Alternating light/dark grey blocks read as a flat chequer, not masonry. Fix: use graded stone tones with geometric block relief instead of two-colour alternation.
2. **Flat grey rock with no relief** on the Himalayan cliff/wall pieces (HM05_01/02, HM06_02, HM04 linings). Rock masses are single flat-grey slabs. Fix: add facet/colour variation so cliffs don't read as one grey wall.
3. **Hero interior not "furnished"** — the tower interior (WT02) scores well on structure but fails bookshelves + map because those sub-assets, though well built separately, are not placed inside. Any "enterable landmark + its contents" pair should be reviewed/assembled together, not as loose parts.
4. **Inside-out / unlit interior faces on hollow pieces** (HM04_02 clearly, HM04_01 mild). Tunnel/cave interiors show black patches. Fix: enforce outward normals + a lit interior colour on all enterable/hollow models.
5. **One off-concept member per set** (HM08_02 hut among cairns; NE01_01 slab among signs). Fix: a quick per-set silhouette consistency pass to catch members that don't match their siblings.

## Could not judge
- None requiring it. Interior bookshelf/map integration for WT02 was judged from the hero_002 four-angle sheet; a single hero view can hide a shelf tucked on an unseen floor, so if a builder states shelves exist on a lower floor not shown, WT02 should be re-shot before rebuild.
