# Handover (written 30 Oct 2026, about 23:40, Nepal time)

## Goal
Build the map in `plan_v5/concept_map_2.png` completely: north up, castle town in the north with a waterfall cliff, snow mountains north-east, volcanic Skull City east, desert south-east, forests west, harbour south-west, Crystal Lake in the centre. The picture says "Same map. More depth." Read `plan_v5/CONCEPT_MAP_2_NOTES.md` first.

## Rules that always apply
- Original designs only. No franchise names, emblems or shapes in the game, no marketplace models (exception below).
- No glow: no Neon, no emissive, no glowing particles. Lava and crystal water are colour only.
- Everything anchored. At most 1-2 enterable buildings per settlement, except the wizard tower.
- Archive, never delete (move old things to `ServerStorage.Phase1Archive_v5`).
- Never put an API key, cookie or token in this repo.
- Stand-ins are allowed for now: block placeholders, free Roblox Creator Store models (delete every script inside, log each in `plan_v5/STANDIN_LIST.csv`), CC0 downloads. Each stand-in is temporary.

## Decisions (user, 30 Oct 23:09: "follow the picture complete")
Wizard Tower north of the castle by the waterfall (not on the Roof Plateau). Harbour City on the south-west coast. Castle Town ring round with a river moat. Town 1 stays in the centre (zone x +-318, z -545..311, untouched).

## State
- Blender models: 404 v5 models are built, saved and exported (`library/<category>/<id>.blend` and `.fbx`). Verdicts in `library/v5_work/FINAL_VERDICTS_v5.json`: 285 OK (independent reviewers), 118 fixed by the lead and not yet reviewed by anyone else, 1 open (`WT02_01`, tower interior: a placement question). Photos of everything: `library/v5_work/gallery_final/ALL_MODELS_v5.pdf`.
- Not viewed by the lead: `PL05_01-03`, `VG07_02`, `WT13_03`, sheet `b1_02`; not viewed after the last change: `WT13_01`, `WT13_02`, `RW01_01`. Seen earlier, not re-checked: `HM04_02` (small black edges), `FR02_03` (a detached slab), `LM12_01`, `LM12_02` (tiny black dots).
- Roblox uploads: 720 earlier models are listed in `asset_ids.csv`. The 399 new v5 models were uploaded through Open Cloud on the night of 30 Oct. Check `asset_ids.csv` for rows starting `v5_`. If `asset_ids_part0.csv`, `_part1.csv` or `_part2.csv` exist, their rows have not been merged: append the rows whose model name is not yet in `asset_ids.csv`, then re-run `upload_v5.ps1`, which uploads only what is missing.
- Studio: nothing is placed and the new terrain is not generated. The world is the Roblox cloud save (Place1). A local backup goes in `game_backup/`.

## Next steps, in order
1. Studio: open Place1, File > Save to File As into `game_backup/`.
2. Upload any v5 models still missing (see above).
3. Terrain pass for the new landforms with blend zones between biomes (no hard biome borders). The generator chain is in `rebuild/`; `patch_terrain_gen_v5.py` still has to be written (see `plan_v5/RUNBOOK_v5.md` section B4).
4. Archive old plain entrance arches; keep capital gates, rose arches, ruins, root and rock arches.
5. Place models from the plans in `mapplan/` (`rebuild/v4/build_v4.ps1 -area <plan>`), then stand-ins from `plan_v5/STANDIN_LIST.csv`, then the wizard tower.
6. About 40 new Blender models are missing for the picture (waterfall, cave interiors, Crystal Lake props, harbour piers and boats, windmill, Ancient Grove, Watcher's Peak, natural forest bridge, sunken ruins). Rough estimate, plus or minus 2x.
7. Photo rounds, performance scan, play-test, export the archives and remove them before any publish.

## Linux notes
- Blender 5.2, Python 3.14 with numpy, pillow, reportlab were used. Blender runs natively on Linux.
- 269 text files contain the Windows path `C:\Users\Nitro\...`. Replace it with your clone path (for example with `grep -rl` and `sed`). Scripts are Python and PowerShell. PowerShell 7 (`pwsh`) can run `upload_v5.ps1` after you change `$base`; the Windows-only power-state call inside it is wrapped in try/catch.
- Roblox Studio has no official Linux version. The community route is Vinegar (unofficial); Roblox updates can break it for several days. The game is safe either way because it lives in Roblox's cloud under your account. Uploads need no Studio: they use the Open Cloud API.
- Open Cloud: create a new API key in Creator Hub (assets read and write), then set `ROBLOX_OPEN_CLOUD_API_KEY` and `ROBLOX_CREATOR_USER_ID` as environment variables. The old key stays in the Windows user environment and is not in this repo.

## Safety of the game
Sign in with the same Roblox account (do not create a new one). Roblox may ask to verify a new device, so keep your 2-step verification or recovery email ready. Old versions of Place1 are in Creator Hub > Place1 > Version History.
