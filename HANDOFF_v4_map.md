# Map handoff: Phase-1 island, state of 30 Oct 2026 (v4 build)

Project: Kayos-h's original Black Clover-inspired Roblox game, place "Place1" (id 103847533321973, shows as "Untitled Experience" until published).
Root folder: `C:\Users\Nitro\.kiro\crew\workspace\town`. Desktop backup: `C:\Users\Nitro\Desktop\roblox_backup` (refreshed by `town\backup_to_desktop.ps1`).
Older handoffs: `rebuild\HANDOFF_v3.md` (Studio pipeline details), `HANDOFF_FINAL.md` (the 390 Blender models), `rebuild\v4\RUNBOOK.md` (overnight rules).

## 1. What the player gets
A round island about 5,800 studs across, laid out after the top-down reference picture (`C:\Users\Nitro\.kiro\crew\uploads\943989c5b0354ac5b891320284412c60_pasted-image-20261029-081421324.png`):
walled capital and castle in the north, snow range with the alpine village and frozen lake in the north-east, badlands with the rusty desert town in the south-east, harbour on the south coast, skull town (Town 1) in the centre, elf village with the world tree in the four-mountain valley in the west, rivers, lakes, about 13,300 trees, 11,400 understory plants, 3,700 rocks, 27 tree-topped islets and sea stacks, 44 badlands mesas.
Elf village: natural look, NO glow (audited: no Neon, lights, particles or glow-named parts in the valley).

## 2. Rules the user set (keep following them)
- Quality over speed. Original designs only: no Black Clover copies, no Toolbox models. Anchor everything.
- Never look at map photos yourself: take them with the scripts, hand them to a fresh sub-agent reviewer, read its text report.
- Never lower existing quality; Town 1 only gets a light touch; archive to ServerStorage instead of deleting.
- At most 1-2 enterable buildings per settlement (6 exist: capital cathedral, rusty church, harbour tavern, alpine lodge, elf temple, elf round house).
- Never print the Open Cloud key. The upload of all 390 V4 models is DONE (`asset_ids.csv` has 720 rows).

## 3. Driving Studio from here (lessons that cost hours)
- Bridge: `town\_start_bridge.ps1` starts `npx robloxstudio-mcp` in its own console and it binds port 58741. The KiroCrew-spawned MCP server may take 58742 and then the native tools do NOT reach Studio. Always use the PowerShell wrappers: `town\st.ps1 -file x.luau [-data x.json]` or `-json call.json`.
- After a Studio restart the plugin may need a click on Connect: screen position (1733,754) with `computer_click` method global.
- Save: click the command bar (700,1147), then `computer_press_key ctrl+s` on the command toolbar element; confirm the line "Saved new changes" in the newest Studio log under `%LOCALAPPDATA%\Roblox\logs`.
- Memory: Studio uses about 7 GB for this place. NEVER relaunch Studio while sub-agents are starting (Studio died with "bad allocation" once). Wait for reviewers to finish, then relaunch with `Start-Process 'roblox-studio:1+launchmode:edit+task:EditPlace+placeId:103847533321973+universeId:10770115762'`.
- `Workspace` is itself a Model: use `FindFirstAncestorOfClass('Model')`, never `FindFirstAncestorWhichIsA('Model')`.
- `studio.ps1` re-sends a call if the reply is lost, so every Luau script must be idempotent (guard with attributes). Count results in Studio, not from the driver's own tally.
- Terrain grass blades: `Terrain.Decoration` and `Terrain.GrassLength` are NOT reachable from scripts (they are not valid members for plugin code). They live only in the Properties panel: select Terrain (`Selection:Set({workspace.Terrain})`), click the GrassLength value cell (screen about (1737,244)), type with `town\type_focus.ps1 -text 0.3` (SendKeys into the focused cell). It is set to 0.3 now (default 0.7). Reviewers kept seeing chest-high blades until this was changed; the grass MODELS were never the main cause. Verify by capturing the right-hand panel strip only (never the 3D view).
- Terrain: `WriteVoxels(Water)` does not clear old partly solid cells; the v4d generator clears each chunk with `FillBlock(Air)` first (this was the cause of the floating sand/mud plates).
- Read PowerShell/JSON through files, not inline (the shell strips `$` and mangles quotes).

## 4. Replay recipe (everything is scripted under `rebuild\v4`)
1. Terrain: `python world_v4.py` (world), `python widen_trails.py`, `python patch_terrain_gen_v4d.py`, then `gen_v4c.ps1 -tag v4d` (generation 5 min + clip 2.5 min + floater scan). Town 1 is protected by `keep.town1`. Then `swap_brick.luau`, `look_pass3.luau`, `look_pass3b.luau`, `r3_fix1.luau` (final colours and light).
2. Map export: `export_map.ps1` (terrain_map.json), `export_occ.ps1`, `enterable_fp.luau`.
3. Environment: `env_plan.py` (forest, understory, rocks, pieces, shore), `place_all_v4.ps1`; `STAGE=2 env_plan.py` for mesas (snow-peak models are NOT used: the terrain mountains are taller). Then `reseat_env.luau` with `_reseat_args*.json` (idempotent re-seating onto the ground, archives vegetation on roads or in water).
4. Settlements: `huts_v4.py`, `dress_v4.py`, `elf_dress2.py` write plans into `mapplan\`; place with `build_v4.ps1 -area <plan>` (`place_dress.ps1` does the dress plans). Plans for Town 1 must be named `town1_*`.
5. Fix scripts, in the order they were applied: `fix_hover`, `castle_prep`, `training_yard`, `recolor_fix`, `foam_plan.py` + `foam_build.luau`, `r3_fix1/2/3`, `glow_fix`, `glow_fix2`, `roof_vary`, `road_paint_data.py` + `road_paint.luau`, `far_sea`, `desert_patches`.
6. Photos and review loop: `photo_run.ps1 -mode on|off -csv <views.csv> -dir <out>`, then spawn reviewers with `shots\v4\reviews\BRIEF_r3.md` and `BRIEF_r4.md`.

## 5. Review score history (independent reviewers, strict)
| Round | Environment | Capital | Castle | Alpine | Elf | Harbour | Rusty | Town 1 |
|---|---|---|---|---|---|---|---|---|
| baseline (01:00) | 3 | 6.5 | 5.5 | 6 | 5.5 | 6.5 | 4.5 | 5 |
| round 2 (02:35) | 5.5 | 6.5 | 5.5 | 6 | (old village) | 6.5 | 4.5 | 6 |
| round 3 (04:40) | 6 | 6 | 7 | 7 | 5.5 | 7.5 | 7 | 7 |
| round 4 (05:35) | 7 | 7 | 7 (yard 5) | 7 (ice lake 6) | 7.0 | 8 | 7.5 | 7 |
| round 5 (06:10) | 7.5 | 7 (wall; one bad ground frame scored 4) | 6 (yard) | 8 | 8 (NOT YET, only just) | 8.5 | 7.5 | 7 |
Round 5 verdict: whole map 7 to 7.5 of 10; alpine, Town 1, castle yard and the environment SHIP; capital wall base NOT YET. Open items from round 5 (none applied; mostly replaced by the v5 terrain pass): brown holes in the badlands shore water near (1700..2000, 0, 1150); loose rock near (1850, 95, 1050); elf translucent slab near (-1500, 65, -370), thin waterfall, faint dapple, tuft at (-1560, -430), white orb near (-1500, 150, -430), flat root fan; rusty roof tint did not show; capital west wall frame (-600..-440, -1450..-1520) had the camera half under water; pale orb over Town 1 (0, 55, -70), the alpine (1600, 175, -910) and the elf trunk (probably the sun disc, check Sky.SunAngularSize); knee-high grass at the castle pen fence and Town 1 house footings (paint a Ground ring); thin surf foam, flat offshore depth, blocky islet plinths, hard far-sea edge.
Reports: `shots\v4\reviews\*.md` (r5_env.md, r5_towns_a.md, r5_towns_b.md).
**World redesign (v5):** everything is planned offline in `plan_v5\` (start with `plan_v5\RUNBOOK_v5.md`). 399 new Blender models, the wizard tower on the Himalayan plateau first, roads through the mountains, natural entrances (only the plain arch is removed).
Reference pictures and the world redesign brief (30 Oct): `reference\README.md` (concept map, castle-town picture, original island picture, MASTER_WORLD_REDESIGN_PROMPT.md).

## 6. ServerStorage archives (nothing was deleted)
`Phase1Archive`, `Phase1Archive_v1`, `Phase1Archive_v2_enterable`, `Phase1Archive_v3_country`, `Phase1Archive_v3_elf`, `Phase1Archive_v4` (R04 sea-cliff slabs, buried snow peaks, PartBuilt placeholders, old castle buildings, elf glow props, banners), `Town1_Backup`, `Town1_Removed`, `SkullHQ_v4_backup`. They hold about 80,000 instances. BEFORE PUBLISHING: export them to .rbxm files and remove them from the place (they cost server memory and load time).

## 7. Known issues and next ideas
- Performance: about 270,000 workspace instances; StreamingEnabled is on. Consider merging far tree clusters or thinning the understory.
- Terrain still faceted on far snow slopes; rivers are narrow channels; the road web is painted but trails are still thin compared with the reference.
- The Studio place has never been play-tested. Do a Play test, check spawn at the Town 1 church square and that every enterable building opens.
- The giant tower is now the enterable wizard tower of the v5 plan (`plan_v5\WIZARD_TOWER_BRIEF.md`); it replaces the old "magic tower" idea in `BLENDER_NEEDS.md` item 1. The three unfixed models and the 58k-triangle elf treehouses D01_02 and D01_04 are listed in `library\v4_work\KNOWN_DEFECTS.md`.
- Publish: File > Publish to Roblox (the experience is still "Untitled Experience"); rename it first.

