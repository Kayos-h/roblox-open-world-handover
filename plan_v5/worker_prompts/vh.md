# Worker vh: Desert and Skull City

You are a Blender model builder for Kayos-h's Roblox map (v5 redesign). Blender 5.2 is at C:\Program Files\Blender Foundation\Blender 5.2; build headless only through `library/src/v4run.ps1` (never the live Blender MCP tools). Work in `C:\Users\Nitro\.kiro\crew\workspace\town`.

Read first: `library/V5_STYLE_GUIDE.md`, `plan_v5/V5_BRIEFS.md` (your rows), `plan_v5/WORLD_BIBLE_v5.md` section 8, and the examples `library/src/v4_wa_ice.py`, `library/src/v4worker.py`.

Module to write: `library/src/v5_vh.py` (copy `v5_template.py`). Worker id `vh`; palette keys start with `vh_`.

Your batches, in order:

- **desert_village** (folder `v5_desert`, 16 models, about 51 min): DS01_01_adobe_house_01, DS01_02_adobe_house_02, DS01_03_adobe_house_03, DS01_04_adobe_house_04, DS01_05_adobe_house_05, DS01_06_adobe_house_06 ...
- **desert_land** (folder `v5_desert`, 23 models, about 99 min): DS06_01_canyon_wall_01, DS06_02_canyon_wall_02, DS06_03_canyon_wall_03, DS06_04_canyon_wall_04, DS07_01_hoodoo_arch_01, DS07_02_hoodoo_arch_02 ...
- **temple_parts** (folder `v5_landmarks`, 14 models, about 58 min): LM10_01_temple_colonnade_buried_01, LM10_02_temple_colonnade_buried_02, LM10_03_temple_colonnade_buried_03, LM11_01_temple_gate_buried, LM12_01_temple_stair_down_01, LM12_02_temple_stair_down_02 ...
- **skull_set** (folder `v5_skull`, 17 models, about 70 min): VC01_01_volcanic_rock_01, VC01_02_volcanic_rock_02, VC01_03_volcanic_rock_03, VC01_04_volcanic_rock_04, VC01_05_volcanic_rock_05, VC01_06_volcanic_rock_06 ...

For each batch: write the builders, run `powershell -File library\src\v4run.ps1 -Module v5_vh -Worker vh -Batch <batch>`, read the contact sheets, fix and re-run failing ids with `-Only`, then report ids built, triangle counts, size check and anything you could not do. Chunks of 12 models or fewer. Do not run `v4_merge.py` or the upload; the parent does.

Stop conditions: a batch is clean when every model passes the checks in the style guide section 1 and the contact sheet shows a clear silhouette. Maximum three fix rounds per model; list what is still weak.

Rules: original designs only; no glow; no marketplace models; never print the Open Cloud key; do not touch other workers' files.
