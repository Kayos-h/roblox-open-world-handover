# Assignment A5: Himalayan kit and the capital

31 models: REDO 0, MAJOR 13, MINOR 18, OK-with-note 0. Work in the order of the table (worst first).

## Your modules (you own these files and nothing else)

| fix module | worker | new palette prefix | round-1 module to read |
|---|---|---|---|
| `library\src\v5_fx_vc.py` | vc | `vc_f_` | `library\src\v5_vc.py` |
| `library\src\v5_fx_vd.py` | vd | `vd_f_` | `library\src\v5_vd.py` |

Scratch build: `powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\Nitro\.kiro\crew\workspace\town\scratch.ps1" -Module <fix module> -Ids <id,id,...> -Tag A5`
Sheets land in `library\v5_work\fix_scratch\A5\<id>.png`. Target size is W x D x H in studs (X, Y, Z); the manifest autofit (`mk(..., 0.1)`) rescales a model that is more than 10% off, which distorts it, so design to size.

## Families in this assignment

CP01 x1, CP02 x1, CP03 x1, CP05 x1, CP06 x2, CP11 x1, CP12 x2, CP14 x2, CP15 x1, CP16 x1, CP18 x4, HM04 x2, HM05 x2, HM06 x3, HM07 x1, HM08 x1, NE01 x2, NE02 x3

## Models

| id | verdict | category | target W x D x H | tri budget | tris now | what the reviewers saw | reviewer suggestion |
|---|---|---|---|---|---|---|---|
| `CP02_02_ring_wall_corner_02` | MAJOR | v5_capital | 24 x 24 x 22 | 12000 | 3568 | detached floating black posts (window bars) hovering in empty air beside the wall; gap between tower and wall | reattach the arrow-slit bars to the wall face and close the gap between the round tower and the straight run |
| `CP05_02_turret_crenellated_02` | MAJOR | v5_capital | 14 x 14 x 26 | 8000 | 1754 | thin black posts/spikes poking up through the red cone roof rim; look detached and clip the roof | remove the stray dark vertical bars at the roof rim or seat them as proper finials; do not let them clip the cone |
| `CP11_01_great_hall_chapel_01` | MAJOR | v5_capital | 70 x 50 x 60 | 30000 | 9706 | detached dark-red gable triangle floating above the roof ridge | seat the loose red gable/dormer piece onto the roof or delete it; no floating parts |
| `CP12_01_terrace_retaining_wall_01` | MAJOR | v5_capital | 40 x 10 x 22 | 8000 | 1052 | blocky square two-tone camo colour patches across the wall face; flat bright-green cap strip looks like a grass slab, not stone coping | replace the random square patches with a single stone colour and subtle relief; recolour the green cap to stone coping |
| `CP15_03_order_hq_03` | MAJOR | v5_capital | 90 x 70 x 60 | 40000 | 2136 | crude low-detail octagonal grey block, far below sibling landmark quality; large detached brown box floating in front of it | rebuild to match CP15_01/02 detail (proper facade, roof, trim) and remove or integrate the stray brown box |
| `CP18_01_quay_wall_01` | MAJOR | v5_capital | 30 x 10 x 8 | 5000 | 556 | blocky square two-tone camo colour patches (cream/lilac checker) across the wall face | replace the random square patches with one stone colour; add bollards/course as relief instead of colour noise |
| `CP18_03_quay_wall_03` | MAJOR | v5_capital | 30 x 10 x 8 | 5000 | 680 | blocky square two-tone camo colour patches on wall; stair reads as flat recolour | unify to one stone colour and model the steps with real risers rather than painted patches |
| `CP18_04_quay_wall_04` | MAJOR | v5_capital | 30 x 10 x 8 | 5000 | 692 | blocky square two-tone camo colour patches across the wall face | unify to a single stone colour; keep the chimney/bollard detail as geometry |
| `HM04_02_tunnel_lining_02` | MAJOR | v5_himalaya | 24 x 24 x 20 | 8000 | 772 | large black inverted/inside-out faces across the top and left of the interior; reads as holes / flipped normals, not lit stone | recalculate normals outward (or solidify the shell) and give the inner faces a stone colour so no black inverted patches remain |
| `HM06_01_switchback_wall_01` | MAJOR | v5_himalaya | 30 x 14 x 14 | 7000 | 588 | blocky two-tone grey checkerboard camouflage patches across the wall face; stones read as a flat chequer pattern, not masonry | replace the alternating light/dark grey checker with subtler stone tone variation and real block relief |
| `HM06_03_switchback_wall_03` | MAJOR | v5_himalaya | 30 x 14 x 14 | 7000 | 776 | same blocky grey checkerboard camouflage patches as _01 | remove the two-tone checker; use graded stone tones with block relief |
| `HM08_02_cairn_shrine_02` | MAJOR | v5_himalaya | 14 x 14 x 12 | 4000 | 190 | reads as a small red-roof hut, not a cairn shrine; does not match its siblings in the HM08 cairn set | rebuild as a stone cairn/chorten (stacked rock or a whitewashed stupa form) consistent with the cairn_shrine set |
| `NE01_01_village_sign_01` | MAJOR | v5_entrances | 10 x 4 x 18 | 6000 | 264 | does not read as a village sign: a grey slab with a row of pale cylinders and a small black flag; ambiguous silhouette, looks like an organ or crate, crude versus sibling signs | rebuild as a clear notice board on a post with a legible board face, matching the NE01 sign set |
| `CP01_02_ring_wall_straight_02` | MINOR | v5_capital | 40 x 10 x 20 | 9000 | 1204 | near-identical recolour of 01/03, only arrow-slits differ | vary string-course or merlon spacing so siblings are not clones |
| `CP03_02_ring_wall_stair_end_02` | MINOR | v5_capital | 20 x 14 x 20 | 7000 | 2596 | small stray stick/plank poking out of right merlon | remove the stray thin bar protruding from the top-right crenellation |
| `CP06_01_gate_flank_tower_01` | MINOR | v5_capital | 30 x 30 x 52 | 16000 | 3288 | red banner sits slightly off the wall face | snap the banner flush to the tower wall so it is not floating |
| `CP06_02_gate_flank_tower_02` | MINOR | v5_capital | 30 x 30 x 52 | 16000 | 3492 | banner slightly detached from wall | attach the banner flush to the wall |
| `CP12_02_terrace_retaining_wall_02` | MINOR | v5_capital | 40 x 10 x 22 | 8000 | 708 | flat bright-green cap strip on top; plain banded slabs with little relief | recolour the green coping to stone; add a chamfer or course line for relief |
| `CP14_04_skyline_tower_04` | MINOR | v5_capital | 30 x 30 x 110 | 30000 | 898 | thin detached antenna/rail bits on the top deck read as stray | attach the rooftop rail/antenna pieces to the deck so none float |
| `CP14_05_skyline_tower_05` | MINOR | v5_capital | 30 x 30 x 110 | 30000 | 1394 | teal/green patch on the water tank vs timber/stone palette | recolour the tank patch to match the wood/metal tank body |
| `CP16_01_townhouse_new_01` | MINOR | v5_capital | 22 x 22 x 28 | 11000 | 9112 | door canopy sits slightly off the facade | snap the entry canopy flush to the wall |
| `CP18_02_quay_wall_02` | MINOR | v5_capital | 30 x 10 x 8 | 5000 | 272 | plain curved slab, little relief | add a coping course or subtle stone banding |
| `HM04_01_tunnel_lining_01` | MINOR | v5_himalaya | 24 x 24 x 20 | 8000 | 980 | interior is a dark cavity; as a modular lining the open back is expected but the inner faces look unlit/near-black | give the inner tunnel faces a lit stone colour so the bore does not read as a black hole from grazing angles |
| `HM05_01_cliff_gallery_01` | MINOR | v5_himalaya | 40 x 14 x 22 | 9000 | 644 | timber walkway clings to a blocky grey cliff but the rock is plain flat-grey slabs with little relief | vary the cliff rock colours/angles so it is not one flat grey mass behind the gallery |
| `HM05_02_cliff_gallery_02` | MINOR | v5_himalaya | 40 x 14 x 22 | 9000 | 820 | same flat grey cliff backing; white snow slab on top looks like a loose flat plane | break up the grey rock and seat the snow cap so it conforms to the top rather than floating as a flat sheet |
| `HM06_02_switchback_wall_02` | MINOR | v5_himalaya | 30 x 14 x 14 | 7000 | 512 | mostly plain flat slabs; curved retaining section is bland with little stone detail | add coursing/relief to the wall faces so the curve reads as laid stone |
| `HM07_04_prayer_flag_string_04` | MINOR | v5_himalaya | 40 x 2 x 12 | 3000 | 580 | flags all near-white/pale, little colour variety versus siblings | give this string distinct flag colours so it is not a washed-out copy of the others |
| `NE01_04_village_sign_04` | MINOR | v5_entrances | 10 x 4 x 18 | 6000 | 240 | board sits on a plain tapered sand-coloured plinth that reads as a blank wedge | slim the base to a post or add detail so the plinth does not dominate the sign |
| `NE02_01_entry_rock_pair_01` | MINOR | v5_entrances | 30 x 22 x 14 | 5000 | 576 | small stray green/flat patch at base | remove the stray green vertex/face at the base; keep faceting |
| `NE02_02_entry_rock_pair_02` | MINOR | v5_entrances | 30 x 22 x 14 | 5000 | 576 | stray white flat patch on upper face | delete the flat white sliver face on the top-right boulder |
| `NE02_04_entry_rock_pair_04` | MINOR | v5_entrances | 30 x 22 x 14 | 5000 | 696 | very dark near-black rock colour vs cream siblings | lighten to a natural grey so it matches the other entry rocks |