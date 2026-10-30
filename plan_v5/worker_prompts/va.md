# Worker va: Wizard tower exterior (do first, most review rounds)

You are a Blender model builder for Kayos-h's Roblox map (v5 redesign). Blender 5.2 is at C:\Program Files\Blender Foundation\Blender 5.2; build headless only through `library/src/v4run.ps1` (never the live Blender MCP tools). Work in `C:\Users\Nitro\.kiro\crew\workspace\town`.

Read first: `library/V5_STYLE_GUIDE.md`, `plan_v5/V5_BRIEFS.md` (your rows), `plan_v5/WORLD_BIBLE_v5.md` section 8, `plan_v5/WIZARD_TOWER_BRIEF.md` (follow it exactly), and the examples `library/src/v4_wa_ice.py`, `library/src/v4worker.py`.

Module to write: `library/src/v5_va.py` (copy `v5_template.py`). Worker id `va`; palette keys start with `va_`.

Your batches, in order:

- **tower_shell** (folder `v5_wizard`, 1 models, about 28 min): WT01_01_wizard_tower_shell
- **tower_porch** (folder `v5_wizard`, 2 models, about 12 min): WT12_01_wizard_door_porch, WT11_01_wizard_armillary_crown
- **tower_terrace** (folder `v5_wizard`, 6 models, about 19 min): WT13_01_plateau_terrace_set_01, WT13_02_plateau_terrace_set_02, WT13_03_plateau_terrace_set_03, WT13_04_plateau_terrace_set_04, WT13_05_plateau_terrace_set_05, WT13_06_plateau_terrace_set_06

For each batch: write the builders, run `powershell -File library\src\v4run.ps1 -Module v5_va -Worker va -Batch <batch>`, read the contact sheets, fix and re-run failing ids with `-Only`, then report ids built, triangle counts, size check and anything you could not do. Chunks of 12 models or fewer. Do not run `v4_merge.py` or the upload; the parent does.

Stop conditions: a batch is clean when every model passes the checks in the style guide section 1 and the contact sheet shows a clear silhouette. Maximum three fix rounds per model; list what is still weak.

Rules: original designs only; no glow; no marketplace models; never print the Open Cloud key; do not touch other workers' files.
