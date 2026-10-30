# First v5 model review (2026-10-30, 16:05 Nepal time)

All 404 manifest rows are built and reviewed once. Nothing has been fixed, placed in Studio or uploaded.

## Result

| verdict | models | share |
|---|---|---|
| OK | 212 | 52% |
| MINOR (small flaw, fixing optional) | 115 | 28% |
| MAJOR (must be fixed) | 70 | 17% |
| REDO (rebuild from scratch) | 7 | 2% |

77 models (19%) need work. They sit in 40 of the manifest's family rows. Eleven families hold three or more failing models each: CO03 reefs (6 of 6), SP01 snow spires (6 of 6), VC04 skull-city buildings (6 of 6), RD05 battlefield props (4 of 5), CP18 quay walls (3 of 4), DS08 underground entrances (3 of 3), FR03 cave mouths (3 of 6), LM19 crater rim rocks (3 of 5), RD06 abandoned houses (3 of 5), SD01 red mesas (3 of 6), VG04 birch trees (3 of 3).

## How the review was done

- Seven independent reviewer agents (A to G). Each got a slice of 4 to 5 contact sheets (12 models per sheet, 34 sheets) and judged silhouette, construction, colour, scale, variety, detail and the rules (no glow, no freestanding plain entrance arch).
- 27 landmark pieces also had a four-angle sheet (3/4 front, 3/4 back, close-up, front elevation). Every other model was judged from one 3/4 picture, with a larger close-up when a reviewer doubted.
- Reviewers did not read builder code, notes or the automatic checks. I looked at no pictures.
- Automatic checks ran separately on all 404 rows (sizes, triangles, files, black thumbnails, markers, emissive colours).
- Files: `C:\Users\Nitro\.kiro\crew\workspace\town\library\v5_work\review_defects_v5.json` (verdict, defects and fix per model), `REVIEW_V5_TABLES.md` (all MAJOR and REDO with the reviewer's fix, the MINOR list, tower scores), `review_slice_A.md` to `review_slice_G.md` (each reviewer's own write-up), `AUTOCHECK_V5.md`, `review_pack\` (the sheets).

## By build queue

| queue | content | models | OK | MINOR | MAJOR | REDO |
|---|---|---|---|---|---|---|
| va | tower exterior | 9 | 8 | 1 | 0 | 0 |
| vb | tower interior, shelves, map, furniture | 18 | 16 | 1 | 1 | 0 |
| vc | Himalayan kit and entrances | 37 | 23 | 9 | 5 | 0 |
| vd | capital | 55 | 38 | 9 | 8 | 0 |
| ve | elf valley, Town 1 | 33 | 22 | 7 | 3 | 1 |
| vf | landmark heroes, trees, coast | 25 | 14 | 8 | 2 | 1 |
| vg | highlands, fortress, forest, marsh | 62 | 28 | 17 | 17 | 0 |
| vh | desert and Skull City | 70 | 32 | 23 | 11 | 4 |
| vi | plains, ruins, coast, road life, sky | 91 | 28 | 40 | 22 | 1 |
| vj | reworks | 4 | 3 | 0 | 1 | 0 |

The tower and the capital, which got the most care, are the strongest. vg, vh and vi are the weakest (45%, 46% and 31% OK). vi also got the least iteration (one numbers check before it was built), which may explain part of its result; I have not verified that.

## Wizard tower

| piece | result |
|---|---|
| WT01 tower shell | pass: exterior 9, interior 8, shelves 8, map 9, silhouette 9, materials 8 |
| WT05 round map table | pass: map 10, silhouette 9, materials 9 |
| WT03 curved shelves, WT04 straight shelves, WT06 to WT12 | OK (two MINOR: WT08_02 sparse bed frame, WT13_01 flat terrace slab) |
| WT02 tower interior | MAJOR: bookshelves 3, circular map 3 |

WT02 fails because the shelves and the map are separate models and the interior mesh has none of them placed. That is how the set was built, but it means the interior only delivers "bookshelves along the walls and the circular map" once they are placed, and placement cannot be done or tested while Studio is uninstalled. Not verified at all: a walk test of the stair, and a cutaway or interior render (the reviewer judged WT02 from one four-angle sheet).

One reviewer also noted that the WT01 shell, although it scores 9 for exterior and silhouette, reads more like a tiered lighthouse than a classic wizard tower (stacked cream drums, teal balconies, green dome). It is rated OK. Whether that look is what you want is your call.

## Rules

- **Glow:** 0 of the 259 colour keys used by v5 models are emissive and none use Neon. Four waterfall pieces still look like light panels in the pictures because they are flat bright white and cyan slabs: LM02_01 and LM22_01 (REDO), LM23_03 and CO01_05 (MAJOR). LM20_02 has blue rune marks that could read as lit (MINOR). These are shape and colour fixes, not data fixes.
- **Entrance arches:** no reviewer reported a freestanding plain entrance arch. RW01_02 is the two separate gateposts that replace the old stone gate arch, and it passed.
- **Originality:** not scored this round. The reviewer brief did not ask for it and nobody reported a copy. It needs an explicit pass.

## What is wrong most often

Counts are over the 77 MAJOR and REDO models, and one model can be in several groups.

| defect | models | examples |
|---|---|---|
| flat, stacked-slab or crude shape | 39 | red mesas SD01_04 to 06, reefs CO03, ruined houses RD06, castle module LM31_03, tower stumps LM29_02 and PL05_02 |
| floating, loose or clipping parts | 32 | all six skull-city buildings (hollow boxes with floating poles), cave mouths FR03, elf path pieces EV03, ring-wall corner CP02_02 |
| square colour patches (camouflage look) | 25 | snow spires SP01, reefs CO03, quay walls CP18, retaining wall CP12, switchback walls HM06, birch trees VG04 |
| does not read as what its name says | 18 | carved stairs LM07, temple stairs LM12, underground entrances DS08, battlefield props RD05, cairn shrine HM08_02, village sign NE01_01 |
| black or inverted-looking faces | 12 | tunnel lining HM04_02, viaduct BR01_02, crater rim rocks LM19, aqueduct arches LM27 |
| waterfall looks like a light panel | 4 | see Rules |

Among the 115 MINOR models the two repeat offenders are recolour-only siblings (tents RD02, palms DS04, bank rocks RV01, floating islands FL01) and flat grey rock with no colour variation.

Landmark heroes that failed: LM02_01 world tree falls (REDO), LM22_01 colossal fall cliff (REDO), LM01_01 world tree trunk door (MAJOR: spiky roots with gaps, open top), LM03_01 frost fortress (MAJOR: the castle is good, the mountain behind it is thin stacked plates). LM30_01 ruined castle is MINOR, close to MAJOR (flat grey).

## Rough fix grouping (from the reviewers' fix sentences, not exact)

| kind of fix | models | note |
|---|---|---|
| recolour only | about 17 | replace camouflage patches with one coherent stone or snow colour |
| waterfall look | 4 | thin stepped pale water instead of bright slabs |
| rebuild the shape | about 41 | stacked-slab mesas, hollow skull-city boxes, stairs, entrances, props, birch trunks |
| local repair | about 15 | attach loose parts, flip normals, close gaps |

## Automatic checks (404 rows)

371 clean, 33 flagged. 32 size flags (17 depth, 8 width, 7 height), 4 models with very few triangles, 2 over the triangle budget, 2 with many materials. Only 4 of the 77 failing models were also flagged by the numbers, and 21 flagged models were rated OK by the reviewers. Known and accepted for now:
- CP04 round towers: four deliberate sizes. HM01 and HM02 bridge spans: the brief defines the span, not the manifest width. WT03 curved shelves: the curve changes the bounding box.
- CP16_04 and CP16_05: 12,304 triangles against an 11,000 budget (12% over).
- RW01_03 and RW01_04 treehouses: 10,712 triangles each, against 58,000 in v4. They are inside the 50,000 limit and rated OK from the front, but they are much simpler than the v4 versions.

## Limits of this review

- The counts above come from each reviewer's per-model file. The reviewers' own hand-typed totals in their write-ups differ by a few models (added up they give OK 223, MINOR 110, MAJOR 64, REDO 7), so I did not use them. The REDO count is the same in both. Four models are OK in the file but MINOR in the write-up: EV02_03, TW03_04, DS03_02 and DS05_02, all "near copy of a sibling" notes. Counting them as MINOR would make it OK 208, MINOR 119.
- 50 of the 212 OK models still carry a small reviewer note that was not counted as a flaw (for example "near-identical to step 01" on the LM04 rampart steps, or "grass caps slightly float" on LM23_01). Seven of them carry a suggested fix about too-similar siblings. The gallery prints each note under its photo.
- One 3/4 picture per model for 377 of 404 models. Backs, undersides and interiors can hide defects.
- First round only. The reviewers are strict on purpose, and a few verdicts may be too harsh or too soft.
- Not yet done: the rock mounds in vc to vf were built before the higher facet count (`DETAIL`) existed, so they are coarser than the mounds in vg to vi. The box bevel is in every queue now (va and vb were rebuilt with it today).
- Nothing was placed in Studio and nothing was uploaded.

## Time and cost

The build ran from the 14:16 build order to the last model at about 15:46, roughly 1 h 30 min against the 3 to 4 h estimate (the 3.5 h figure I wrote in an earlier checkpoint was wrong; the file times say otherwise). Checks, hero views, review pack and the seven reviewers took about another 15 min. The seven reviewers cost roughly 35 credits in total.
