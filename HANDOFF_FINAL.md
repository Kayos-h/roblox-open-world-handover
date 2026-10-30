# Total handover: Black Clover-inspired Roblox game, Phase 1 map and the 390 Blender models

Written 29 Oct 2026, about 15:00 Nepal time, at the end of the model-building phase.
`T` = `C:\Users\Nitro\.kiro\crew\workspace\town`. `LIB` = `T\library`.
A full copy of `T` plus the Desktop upload files and your reference picture is in `C:\Users\Nitro\Desktop\roblox_backup`.
Related older file: `T\rebuild\HANDOFF_v3.md` (the Roblox Studio side of the map, read it before touching Studio).

## 1. In one page
- Kayos-h is making an original, high-quality, Black Clover-inspired magic-knight open-world Roblox game. Original names and designs only, never copies of Black Clover content.
- The work started with the map only. Place "Place1", id 103847533321973. Plan: about 7000 x 7000 studs, StreamingEnabled, 7 biomes with mixed settlement types, spawn town first with an original skull HQ as centrepiece, 1-2 enterable buildings per settlement.
- The island is built in Roblox Studio by scripts (a Luau terrain generator, Python layout plans, a placer that uses uploaded Blender models). The models are made in Blender.
- State at the end of this phase:
  - **390 new Blender models ("V4 set") are finished** and sit as `.blend` and `.fbx` files in `LIB\v4_*`. An independent reviewer checked pictures of every one over three passes: **370 OK, 20 MINOR, 0 MAJOR, 0 REDO** (list in `LIB\v4_work\KNOWN_DEFECTS.md`).
  - **None of the V4 models is uploaded to Roblox yet.** Upload with `Desktop\5-upload-v4-models.bat`.
  - **The Roblox map in Studio is the v3 build** (about 52k parts, 0 unanchored). It is **not saved** (the Studio tab said "Untitled Experience") and does not use the V4 models yet.
  - Roblox Studio and your live Blender window were not touched during the V4 phase.

## 2. What you told me, in order
1. **9-10 Oct, the idea.** A high-quality Black Clover-inspired magic-knight open-world game. Start with the map only. Original content. Plan agreed: about 7000 x 7000 studs, StreamingEnabled, 7 varied biomes, spawn town first (about 900 x 900) with the original skull HQ.
2. **Quality directive (stored in memory as `project.roblox_game.build_quality_directive`):** no shortcuts, top Roblox game quality, every model and prop treated as its own proper subtask.
3. **26-28 Oct.** I hand-built 329 shared models plus the skull in Blender (`LIB\alpine`, `capital`, `castle`, `elf`, `harbour`, `nature`, `props`, `roads`, `rusty`, `town1`, `between`, `lighting`). You ran the Desktop `.bat` files to upload all 330 to Roblox (IDs in `T\asset_ids.csv`). An overnight automatic placement built the whole map but you rejected it as blocky, mud-painted and sparse.
4. **v2, then v3 rebuild (29 Oct 04:56 request):** island about 65% of old size with mountains, hills, plateaus, rivers, lakes; Town 1 70% with a bigger church and a large graveyard; capital 70% (castle keeps its size, you like the layout); harbour 70%; rusty town smaller with huts; elf village rebuilt in a valley between four mountains; alpine village not shrunk, with igloos and a huge frozen lake; plus a full list of Blender models. Details: `T\rebuild\HANDOFF_v3.md` section 1.
5. **v4 brief (29 Oct, terrain first):** make the terrain right first (natural, varied, like your reference picture), rebuild the elf village fully (treehouses need ground ladders, no neon or RGB colours, a natural elven feel), and **build ALL ~390 Blender models first, at high quality, before touching the map.** Reference picture: `C:\Users\Nitro\.kiro\crew\uploads\943989c5b0354ac5b891320284412c60_pasted-image-20261029-081421324.png` (copy in `roblox_backup\reference`): dense varied forest, jagged snow peaks, red-brown badlands mesas, rocky coast, offshore tree-topped islets, a big waterfall world-tree.
6. **During the V4 phase:** first "no need for photos", then "show me what quality you make" (photos are in each worker's chat and in the GitHub gallery). "Don't wait for my opinion", make the decisions, be honest about quality.
7. **End of V4 phase:** make sure no other sub-agents run; create ONE new independent sub-agent to review every model ("does it look normal or not"); fix whatever it flags; hand everything over; then this handover, a backup folder `roblox_backup` on the Desktop, and a short report.

## 3. How you want the work done (standing rules)
- Quality before speed. Never call a visual result good without looking at a real picture.
- Original names and designs. No Toolbox or online models: build everything yourself.
- At most 1-2 enterable buildings per settlement. Archive instead of deleting. Anchor everything.
- Plain language, short answers, no filler. Destructive actions need your confirmation.
- Credentialed commands: never paste the Open Cloud API key into chat (it leaked twice and was reset). Kiro's safety layer kills credentialed upload commands (exit code 15), so **you run the Desktop `.bat` files**. Your "memory freeer" app also killed node.exe and uploads earlier: pause it while uploading.
- Never close or change your live Blender window (it held an unsaved skull scene, pid 5892). Save that scene yourself if you still need it.
- A chat can hold only 100 images. Let sub-agents open pictures and report in text.

## 4. Model standard (what "good quality" meant)
Full rules: `LIB\v4_work\WORKER_BRIEF.md` (build rules), `FIX_COMMON.md` (fix-round rules and the rock method), `REVIEWER_BRIEF.md` (how the reviewer judged).
- Look: same level as the finished D-series (elf trees, buildings, cliffs) and the B01 skull. Original designs, silhouettes with variety, course lines on stone, plank seams, shingle rows, trims. Nothing flat, nothing floating, no holes in walls, no see-through gaps, siblings must differ.
- Units and axes: 1 unit = 1 stud, Z up, model front faces -Y, origin at bottom centre. Character 5.5 studs, door at least 7 high x 4 wide, storey 8-9 studs, hollow buildings with walls at least 1.5 thick, a floor, a closed interior.
- Triangle budgets per model: small prop 4k, medium prop 10k, hut or house 30k, big set piece 50k, tree 20k, rock face, cliff, peak or mesa 40k. The exporter splits every colour into pieces under 18k triangles.
- Colour: no neon and no glowing parts except small amounts for lantern glass, candle flames, embers. Colours come from palette keys (`LIB\palette.json`, 883 keys); worker keys start with the worker id. At most about 6 colour keys per piece.
- Rocks: continuous faceted shells with colour by slope and height (not stacked cubes, not dense smooth grids), snow as one band, no stray specks (`FIX_COMMON.md`, "FACET METHOD").
- Minimum feature thickness 0.8 stud.

## 5. What exists (the 390 models)
| Section | Content | Models |
|---|---|---|
| A | replacements for part-built placeholders (igloos, ice shanties, fishing holes, rusty huts, 4 enterable shells) | 20 |
| B | key set pieces: skull HQ, castle set, throne hall, barracks, stables, royal area, market stalls, capital houses, harbour | 36 |
| C | alpine village | 25 |
| D | elf valley rebuild (natural elven look, no neon) | 97 |
| E | graveyard, rusty town, farms, nature | 81 |
| F | new terrain and vegetation brief (trees, plants, ground cover, bridges, story props, water, landmarks) | 111 |
| R | from your reference image: islets, snow peaks, badlands mesas, sea cliffs, waterfall cliffs, canyon walls | 20 |
| | **Total** | **390** |
- Priorities: P1 140, P2 205, P3 45. Total about 3.64 million triangles, average 9.3k, largest 58.6k.
- Where: `LIB\<folder>\<id>.fbx` and `.blend`. Folders: v4_alpine, v4_buildings, v4_capital, v4_castle, v4_elf, v4_farm, v4_graveyard, v4_ground, v4_harbour, v4_landmarks, v4_nature, v4_plants, v4_props, v4_roads, v4_rusty, v4_shells, v4_story, v4_terrain, v4_town1, v4_trees, v4_water, v4_world. The FBX contains one piece per colour.
- Data: `LIB\v4_meta.json` (per model: folder, triangles, size, materials, markers such as doors), `LIB\palette.json`, `LIB\V4_MANIFEST.md` (the plan), `LIB\V4_MODEL_LIST.md` (real status of every model plus the known-defects section).
- Pictures: per model `LIB\v4_sheets\_t_<id>.png`; four-angle sheets `LIB\v4_sheets\<id>.png` (45 big pieces); contact sheets `<worker>_<batch>_<n>.png`; review sheets `LIB\v4_work\review_pack`, `review_pack2`, `review_pack3`, `review_pack4`.
- Gallery on GitHub (private): [roblox-map-models-gallery](https://github.com/Kayos-h/roblox-map-models-gallery), default branch `gallery`. Local copy `T\gallery_repo`.

## 6. How the models were made and checked
1. **Pipeline.** Models are Python builder modules (`LIB\src\v4_*.py`) run headless by `LIB\src\v4worker.py` through `LIB\src\v4run.ps1`. No live Blender is needed. Two Blender processes at most (a named semaphore); previews are CPU path-traced (Cycles, CPU denoiser). The runner saves `.blend`, `.fbx`, metadata `v4_meta_<worker>.json`, palette `palette_<worker>.json`, thumbnails and contact sheets.
2. **Build.** The D-series (97) and the skull were built first through the live Blender in a loop. The other 292 were built by parallel sub-agent workers (waves `wa` to `wk`, five replacements `wd2` `we2` `wf2` `wg2` `wh2` after five workers froze).
3. **Independent review 1** (fresh sub-agent, 33 sheets): 311 OK, 40 MINOR, 36 MAJOR, 3 REDO. Main findings: rocks built as piles of cubes, square camouflage colour patches on castle stone, neon colours, floating or collapsed parts. Files: `REVIEW_REPORT.md`, `review_defects.json`.
4. **Fix round** by six workers `wx1`-`wx6` (79 models, new modules `v4_wx1_rockwalls`, `v4_wx2_facet`, `v4_wx3_*`, `v4_wx4_fix`, `v4_wx5_fix`, `v4_wx6_fixes`). Old files are kept in `LIB\v4_work\backup_pre_fix`. **Review 2:** 55 OK, 26 MINOR, 0 MAJOR (`REVIEW_RECHECK.md`).
5. **Polish round** (the same workers, 49 models changed). Old files in `LIB\v4_work\backup_pre_polish`. **Review 3:** 370 OK, 20 MINOR, 0 MAJOR over the whole library (`REVIEW_POLISH.md`, `KNOWN_DEFECTS.md`).
6. To find the newest builder of a model, search `LIB\src\v4_*.py` for its id; fix modules (`wx*`) beat replacements (`*2`) beat the originals. `v4_merge.py` applies `v4_meta_wx*.json` last so the fixes win.

## 7. Tools (all in `LIB\src` unless noted)
| Command | Purpose |
|---|---|
| `python v4_status.py` | counts of built models, sections, workers, problems |
| `python v4_merge.py` | merge worker metadata and palettes into `v4_meta.json` and `palette.json` (idempotent) |
| `python v4_list.py` | rewrite `V4_MODEL_LIST.md` (appends `v4_work\KNOWN_DEFECTS.md`) |
| `python gallery.py` then `T\publish_gallery.ps1` | rebuild the gallery and push it (private repo, branch `gallery`) |
| `python review_pack.py [--only ids.txt --out folder]` | labelled review sheets, 12 models each |
| `powershell -NoProfile -ExecutionPolicy Bypass -File v4run.ps1 -Module <module> -Worker <w> -Only <ids> [-Quad] -TimeoutSec 900` | rebuild chosen models and their pictures |
| `T\upload_v4.ps1 [-only <folder or id>] [-limit N]` | upload V4 FBX files to Roblox Open Cloud (skips names already in `T\asset_ids.csv`) |
Environment knobs: `V4_EEVEE=1` forces EEVEE, `V4_NODENOISE=1` turns the denoiser off. Shell is Windows PowerShell: write `.ps1` or `.py` files, do not use inline `$` variables or nested quotes.

## 8. Next steps, in order
1. **Save your Roblox place** (File, Save to Roblox, Ctrl+S). It was still "Untitled Experience".
2. **Upload the V4 models:** pause "memory freeer", set `ROBLOX_OPEN_CLOUD_API_KEY` and `ROBLOX_CREATOR_USER_ID` as user environment variables (never paste the key in chat), then double-click `Desktop\5-upload-v4-models.bat`. It uploads about 390 FBX files, skips finished ones, and writes `T\asset_ids.csv` (folder, name, asset id, moderation state). Run it again after any failure. Check moderation states afterwards.
3. **Rebuild the catalog** for the placer: `T\mapplan\catalog.json` covers only the older 330 models. Extend `T\make_catalog.ps1` (or the script that builds it) to read `LIB\v4_meta.json` and the new rows in `asset_ids.csv`.
4. **Rebuild the map terrain first** (v4 brief), then settlements, then place models. Follow `T\rebuild\HANDOFF_v3.md` sections 3-6 (how to drive Studio, pipeline, the Town 1 terrain snapshot rule). Key rules from it: never regenerate terrain unless `_G.T1SNAP ~= nil`; after any terrain regeneration run `fill_voids.luau`, `fill_voids2.luau`, `terrain_clip.luau`, then the repaints; archive to ServerStorage instead of deleting; anchor everything.
5. **Replace placeholders** (`Phase1Map.PartBuilt`, the part-built shells in `Phase1Map.Enterable`) with the new A-section models; use the rebuilt elf valley (section D) with ground ladders and no neon.
6. **Optional polish** of the 20 MINOR models (table in `KNOWN_DEFECTS.md`, each with the suggested fix) and a triangle-reduction pass for the two 58k treehouses D01_02 and D01_04.
7. Re-run `v4_merge.py`, `v4_list.py`, `gallery.py` and `publish_gallery.ps1` after any model change; run a Play test in Studio (never done so far).

## 9. Lessons and incidents (so they are not repeated)
- Several GPU previews at once crashed the NVIDIA driver, so previews run on the CPU. The GPU denoiser ran out of memory with about 3 GB free, so it runs on the CPU, and a failed preview never stops a model from being saved.
- Under low memory some previews came out black or as static. Check pictures with brightness before judging (a model that renders black is usually a failed render, not a bad model).
- Five original workers froze for hours and woke up later, one rebuilt three models with old code. Do not leave obsolete sub-agent rows running; the runtime stops them at 180 minutes.
- Fix workers must keep the saved id and category folder so files overwrite in place, and back up first.
- Sub-agents shared one Blender slot pool; start at most about six at a time.
- The reviewer was stricter than the builders every time. Judge by pictures from the game camera, not by triangle counts.

## 10. File map of `T`
- `library\` models, source (`src\`), pictures (`v4_sheets\`), review and fix material (`v4_work\`).
- `mapplan\` area plans and `catalog.json` (older 330 models). `rebuild\` Studio scripts, handoff, reviews, pictures from tours. `shots\` Studio pictures.
- `asset_ids.csv` uploaded asset IDs (older 330 models). `upload_v4.ps1`, `upload_all.ps1`, `upload_after_export.ps1`. `publish_gallery.ps1`. `gallery_repo\` gallery.
- `MAP_MODEL_LIST.md`, `BLENDER_NEEDS.md`, `REBUILD_REPORT.md` older lists and reports (v3).
- Many small `_*.ps1`, `_*.py` helper scripts and old `b*.lua` Studio scripts from earlier phases; they are scratch and can be ignored.
- Desktop: `1-upload-test-lamp.bat` ... `5-upload-v4-models.bat`, `roblox cloud syncup.bat` (copies are in `roblox_backup\desktop_bats`).
