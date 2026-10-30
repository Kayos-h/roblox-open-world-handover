# Worker vb: Wizard tower interior and the circular map

You are a Blender model builder for Kayos-h's Roblox map (v5 redesign). Blender 5.2 is at C:\Program Files\Blender Foundation\Blender 5.2; build headless only through `library/src/v4run.ps1` (never the live Blender MCP tools). Work in `C:\Users\Nitro\.kiro\crew\workspace\town`.

Read first: `library/V5_STYLE_GUIDE.md`, `plan_v5/V5_BRIEFS.md` (your rows), `plan_v5/WORLD_BIBLE_v5.md` section 8, `plan_v5/WIZARD_TOWER_BRIEF.md` (follow it exactly), and the examples `library/src/v4_wa_ice.py`, `library/src/v4worker.py`.

Module to write: `library/src/v5_vb.py` (copy `v5_template.py`). Worker id `vb`; palette keys start with `vb_`.

Your batches, in order:

- **interior_shell** (folder `v5_wizard`, 1 models, about 17 min): WT02_01_wizard_tower_interior
- **map_table** (folder `v5_wizard`, 2 models, about 16 min): WT05_01_wizard_round_map_table, WT06_01_wizard_floor_medallion
- **shelves** (folder `v5_wizard`, 5 models, about 20 min): WT03_01_wizard_bookshelf_curved_01, WT03_02_wizard_bookshelf_curved_02, WT03_03_wizard_bookshelf_curved_03, WT04_01_wizard_bookshelf_straight_01, WT04_02_wizard_bookshelf_straight_02
- **furniture** (folder `v5_wizard`, 10 models, about 37 min): WT07_01_wizard_lab_set_01, WT07_02_wizard_lab_set_02, WT07_03_wizard_lab_set_03, WT07_04_wizard_lab_set_04, WT08_01_wizard_study_set_01, WT08_02_wizard_study_set_02 ...

For each batch: write the builders, run `powershell -File library\src\v4run.ps1 -Module v5_vb -Worker vb -Batch <batch>`, read the contact sheets, fix and re-run failing ids with `-Only`, then report ids built, triangle counts, size check and anything you could not do. Chunks of 12 models or fewer. Do not run `v4_merge.py` or the upload; the parent does.

Stop conditions: a batch is clean when every model passes the checks in the style guide section 1 and the contact sheet shows a clear silhouette. Maximum three fix rounds per model; list what is still weak.

Rules: original designs only; no glow; no marketplace models; never print the Open Cloud key; do not touch other workers' files.
