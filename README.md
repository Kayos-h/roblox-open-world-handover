# Roblox open-world map: handover

An original fantasy open-world map for Roblox (place "Place1", id 103847533321973), built from Blender models. This repo is the full handover: plans, scripts, Blender models, the Roblox asset list and notes.

Start with `HANDOVER.md`.

| Path | What |
|---|---|
| `HANDOVER.md` | State, decisions, next steps, Linux notes |
| `plan_v5/` | Design, runbook, concept map (`concept_map_2.png`), stand-in list, manifest of the 404 v5 models |
| `mapplan/` | Placement plans (JSON), 934 draft placements |
| `library/` | Blender models (`.blend`, `.fbx` per category), build scripts (`library/src`), palette, reviews and verdicts (`library/v5_work`) |
| `rebuild/` | Studio-side Luau scripts and build helpers |
| `asset_ids.csv` | Model name to Roblox asset id (Open Cloud uploads) |
| `upload_v5.ps1` | Open Cloud uploader (resumable, skips names already in `asset_ids.csv`) |
| `game_backup/` | Backup of the Roblox place file |

No license: all rights reserved.
