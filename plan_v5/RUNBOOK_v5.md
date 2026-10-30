# V5 runbook: what to do next, in order

State at 30 Oct 2026, 12:20. Everything that needs neither Blender nor Studio is done. Blender is parked and Studio is not installed. The built world exists only in Roblox's cloud save of 06:05 (place 103847533321973).

## Files made offline (all in `town\plan_v5` unless noted)
| File | What |
|---|---|
| `WORLD_BIBLE_v5.md`, `PRIORITY_AREAS_v5.md`, `WIZARD_TOWER_BRIEF.md` | The design, the priority areas, the tower |
| `V5_MANIFEST.md/.csv/.json`, `v5_manifest.py` | 399 new models (P1 106, P2 289, P3 4) + 5 reworks, with sizes and triangle budgets |
| `V5_BRIEFS.md`, `library\V5_STYLE_GUIDE.md`, `MODEL_REVIEW_BRIEF.md`, `v5_worker_plan.md/.json`, `worker_prompts\*.md`, `library\src\v5_template.py`, `make_v5_briefs.py` | Everything a Blender worker needs |
| `world_v5_terrain.json`, `terrain_v5.py` | The planned landforms as data, and the code that applies them |
| `roads_v5.json`, `ROADS_V5.md`, `route_v5.py` | 26 routes, 12 bridges, 3 tunnels, hairpins |
| `mapplan\v5_*.json`, `mapplan\town1_v5.json`, `PLACEMENT_V5.md`, `make_v5_plans.py`, `plan_overlay_items_v5.jpg` | 934 draft placements for 396 of the 399 new models |
| `shots\v5\views_v5_*.csv`, `shots\v5\photo_round_v5.ps1`, `shots\v5\reviews\BRIEF_v5.md`, `make_v5_reviews.py` | 121 cameras and the review brief |
| `rebuild\v5\perf_scan_v5.luau`, `perf_probe_client_v5.luau` | Instance inventory and frame-rate probe (drafts, untested) |
| `rebuild\v5\place_v5_ph.luau`, `build_v5_ph.ps1` | Block placeholders for unbuilt models (drafts, untested) |
| `town\upload_v5.ps1` | Upload script (dry run tested) |
| `topview_sketch_v5.jpg`, `concept_vs_sketch.jpg`, `wizard_map_*` | Pictures and the tower map data |

## A. When the user allows Blender
1. `resource_status`: two Blender processes need about 6 GB free. Do not start while memory is critical.
2. Start the workers in this order with `spawn_run` (one task per file in `worker_prompts`; `include_memory=false`): **va and vb first (wizard tower)**, then vc, vd, ve, vf. Workers vg, vh, vi are the P2 queues. Blender is driven only through `library\src\v4run.ps1` (two at a time).
3. Each batch: build, read the contact sheets, fix, independent reviewer with `MODEL_REVIEW_BRIEF.md`, fix again. The tower needs 8 or more in every category before anything else is judged finished.
4. `python library\src\v4_merge.py`, then the user closes Blender, then `.\upload_v5.ps1 -dry`, then `.\upload_v5.ps1` (key read from the environment, never printed).
5. Reworks (RW02 roots, RW01 four models) replace old models: remove the old row from `asset_ids.csv` first.

## B. When Studio is installed
1. Install, sign in, plugins are in `%LOCALAPPDATA%\Roblox\Plugins` (copies in `studio_plugins`). Open the place, start the bridge (`_start_bridge.ps1`), click Connect, ping with `st.ps1`. Check GrassLength 0.3. Save a local `.rbxl` into the Desktop backup.
2. Baseline: run `perf_scan_v5.luau` (record the numbers).
3. Arch scan: list instances named like `H12_region_entrance_arch`, `A104_wooden_gate`, `D04_06_gate_arch_a`, `D04_07_gate_arch_b`, `F08_13_gate_arch_stone`, `F08_14_gate_arch_timber`. Move them to `ServerStorage.Phase1Archive_v5` (archive, never delete). Leave the capital gates, rose arches, ruin, root and rock arches.
4. **Terrain pass (one regeneration, about 8 minutes plus replays).** The generator chain is `patch_terrain_gen_v4d.py`, `widen_trails.py`, `gen_v4c.ps1`, then `swap_brick.luau`, `look_pass3.luau`, `look_pass3b.luau`, `r3_fix1.luau`. To do on the first Studio day: write `patch_terrain_gen_v5.py` so the generator adds the deltas of `world_v5_terrain.json` (hills, crater, canyons, Skull floor, peaks, ridges, gorges, Roof Plateau with the tower pad at (1380,-1320) floor y 324) and carves the road cuts and tunnels from `roads_v5.json`; keep the Town 1 zone (x +-318, z -545..311) untouched. Then replay road paint (from `roads_v5.json`), plinths (`r3_fix3` plinth part), ice and desert patches, pond collars and the `r4_fix1` repaints.
5. **Placeholders first:** `rebuild\v5\build_v5_ph.ps1 -area <plan>` for each plan (himalaya, roads, entrances, capital, elf, town1_v5, landmarks, regions), then `verify_folders.luau`. Run `shots\v5\photo_round_v5.ps1 -round r0` and have reviewers (`shots\v5\reviews\BRIEF_v5.md`) judge the layout from the photos before real models exist.
6. **Real models:** as each model is uploaded, archive its placeholders and run `rebuild\v4\build_v4.ps1 -area <plan> -batch 30 -nocollide <small groups>` (the command per plan is in `PLACEMENT_V5.md`). Re-seat on the live ground with `reseat_env.luau`, then verify. Before the capital plan: archive the old capital wall, gates and houses inside the ring. Before the elf plan: clear small plants inside each new house footprint (`cr` in the plan item is the radius).
7. Assemble the wizard tower: tower plan group `WizardTower`, then `WizardTowerInterior` (y_offset is the floor height), collision proxies from `tower_collision.json`, warm PointLights, window panes, doors on hinges.
8. Photo rounds and reviewer loops until the whole map is rated 8 or higher; then `perf_scan_v5.luau` again and the play-test with `perf_probe_client_v5.luau`; export the ServerStorage archives (about 80,000 instances) to `.rbxm` and remove them before any publish.

## C. Rules that always apply
Original designs only (no Black Clover names or shapes, no marketplace models). No glow anywhere (elf valley especially). Everything anchored. At most 1-2 enterable buildings per settlement, except the wizard tower. Archive, never delete. Never print the Open Cloud key. Reviewers look at the photos, not me. Memory first: no reviewer or Blender run while `resource_status` says critical.


## D. Status (2026-10-30 22:35): fix rounds ended after round 2; then two lead passes (no sub-agents)
- **Models:** all 404 manifest rows are built in Blender, saved and exported (`library\<category>\<id>.blend` and `.fbx`), merged into `library\v4_meta.json` and `library\palette.json` (1407 palette keys, 0 missing, 0 emissive, 0 round-1 colours changed). Nothing is placed in Studio and nothing is uploaded.
- **Reviews (all by independent reviewers who saw pictures only):** round 1 (front views): OK 212, MINOR 115, MAJOR 70, REDO 7. Fix round 1 rebuilt 198 models. Round 2 panel (front and back, stricter) on those: OK 118, MINOR 65, MAJOR 15. Round 3 panel on the 177 never-rebuilt models: OK 113, MINOR 54, MAJOR 10. Fix round 2 changed 91 models. Round 4 panel on 78 of them plus 12 blind controls: rebuilt OK 42, MINOR 24, MAJOR 10, REDO 2; controls OK 7, MINOR 3, MAJOR 2.
- **Lead passes (2026-10-30, no sub-agents, user's instruction):** pass 1 (19:50) rebuilt 31 models, pass 2 (22:30) rebuilt 87 more (9 never reviewed + 78 MINOR), 118 in total. Each was checked by the lead's own eyes plus numbers (`python lead_verify.py <ids.json>`: 31/31 and 86/87 pass; the one note is CP02_03 depth 21.4 vs 24). Not judged by reviewers; the user reviews them. Lists: `library\v5_work\lead\fixed_ids.json` (31) and `library\v5_work\lead2\worklist.json` (87). Before/after/back sheets: `library\v5_work\lead\fixed_01..04.jpg` and `library\v5_work\lead2\b1_01.jpg` ... `b7_02.jpg`. Old files are archived (copy only) in `library\v5_fix3_archive` and `library\v5_fix4_archive`. Code: `v5_fx_*` modules (functions listed per batch in `lead4_snip_*.py`), the hook kit `library\src\v5_leadkit.py` (wrap, recolor, prune, post, automatic de-z-fight) and helpers `patch_fn.py`, `lead2_tools.py`.
- **Key finding:** boxes whose faces lie in the same plane and overlap render as black seams or black tops (shadow-ray self hit). The kit now pushes the smaller box's conflicting face 0.04 outward; that removed black bars from the stair, gatehouse, temple stairs, colonnade and tunnel lining.
- **Latest verdict per model** (`library\v5_work\FINAL_VERDICTS_v5.json`): OK 285, FIXED by the lead 118 (awaiting the user), MAJOR 1 (WT02_01). Reviewer lists with the original notes: `library\v5_work\r3\NOT_OK_r3.md` and `r4\NOT_OK_r4.md`. Automatic check flags 19 of 404 (was 33 -> 25 -> 19).
- **Still open:** WT02_01 tower interior is a placement matter, not a model flaw: the WT03/WT04 bookshelves and the WT05 map must be placed inside it by the tower plan (`v5_tower_assembly.py`, `tower_check.ps1`; first solve rated FIX, second solve `tower_check\fixed2` not reviewed; `mapplan\v5_himalaya.json` unchanged).
- **Originality and glow (fixed in the lead pass):** the gold star badges on CP15_01 and CP17_01 are replaced by a bronze ring with a tower glyph and a bronze urn; the glow-looking parts on WT13_06 (lantern), FR02_04 (gold tip) and TW03_02 (gold rim) are replaced by dull stone, ash and bronze. No v5 model uses any glow key (57 old glow keys exist in the merged palette from v1-v4 models only).
- **Reviewer noise:** 5 of 12 controls rated OK by one panel were rated lower by the next panel, so a single verdict is not a guarantee.
- **Tower interior:** solver `library\src\v5_tower_assembly.py` (`tower_check.ps1`). The first solve was rated FIX; a second solve with more stair clearance (`library\v5_work\tower_check\fixed2`) is not reviewed. `mapplan\v5_himalaya.json` is unchanged. Not verified: walk test of the stair, shelves on the upper floors, medallion against the stair.
- **Automatic checks:** `library\v5_work\AUTOCHECK_V5.md` flags 25 of 404 (size drift 22, material count 7, over budget: CP16_04/05 at 12,304 tris against 11,000).
- **Pictures:** `library\v5_work\gallery_final\` (final state, made by `make_gallery_final.py`). The round-1 galleries in `library\v5_work\gallery\` are kept as they were.
- **Backup:** `backup_to_desktop.ps1` ran at 19:00 (incremental).
- **Upload:** a separate later step. Close Blender first. Do not run `upload_v5.ps1` before the user asks.


## E. New reference (2026-10-30 23:10)
- The user gave a better top-down picture: `plan_v5\concept_map_2.png` (north up, "Same map. More depth."). What I understand from it, how it differs from the v5 plan and the open questions: `plan_v5\CONCEPT_MAP_2_NOTES.md`. Gaps and stand-ins: `plan_v5\STANDIN_LIST.csv` (about 40 new Blender models if every gap gets a real model, rough, plus or minus 2x).
- The user allows stand-ins for now (22:57): block placeholders, free Roblox Creator Store models (delete every script, log each one in the CSV) and CC0 downloads (through Blender, so later). He reviews the list the next day. Original-design and no-glow rules still apply.
- Differences that need his answer: Wizard Tower (picture: north by the waterfall; plan: Roof Plateau), Harbour City (picture: south-west coast), round castle ring with moat, Town 1, no glow for lava/tree/crystal, upload timing.
- State at this note: nothing changed in Studio, nothing uploaded. Blender closed, Studio running, RAM 0.4 to 0.9 GB free (critical), Windows sleeps after 5 minutes idle on AC, no local `.rbxl` copy of the world yet. `ROBLOX_OPEN_CLOUD_API_KEY` and `ROBLOX_CREATOR_USER_ID` are set (User scope).
