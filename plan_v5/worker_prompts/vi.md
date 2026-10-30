# Worker vi: Plains, ruins, coast extras, roads and sky

You are a Blender model builder for Kayos-h's Roblox map (v5 redesign). Blender 5.2 is at C:\Program Files\Blender Foundation\Blender 5.2; build headless only through `library/src/v4run.ps1` (never the live Blender MCP tools). Work in `C:\Users\Nitro\.kiro\crew\workspace\town`.

Read first: `library/V5_STYLE_GUIDE.md`, `plan_v5/V5_BRIEFS.md` (your rows), `plan_v5/WORLD_BIBLE_v5.md` section 8, and the examples `library/src/v4_wa_ice.py`, `library/src/v4worker.py`.

Module to write: `library/src/v5_vi.py` (copy `v5_template.py`). Worker id `vi`; palette keys start with `vi_`.

Your batches, in order:

- **plains_set** (folder `v5_plains`, 16 models, about 57 min): PL01_01_farmhouse_01, PL01_02_farmhouse_02, PL01_03_farmhouse_03, PL01_04_farmhouse_04, PL02_01_hay_silo_01, PL02_02_hay_silo_02 ...
- **ruins_crater** (folder `v5_landmarks`, 25 models, about 99 min): LM19_01_crater_rim_rock_01, LM19_02_crater_rim_rock_02, LM19_03_crater_rim_rock_03, LM19_04_crater_rim_rock_04, LM19_05_crater_rim_rock_05, LM20_01_crater_arcane_ruin_01 ...
- **coast_set** (folder `v5_coast`, 14 models, about 52 min): CO03_01_reef_01, CO03_02_reef_02, CO03_03_reef_03, CO03_04_reef_04, CO03_05_reef_05, CO03_06_reef_06 ...
- **road_life** (folder `v5_roads`, 30 models, about 100 min): RD01_01_watchtower_01, RD01_02_watchtower_02, RD01_03_watchtower_03, RD01_04_watchtower_04, RD02_01_camp_set_01, RD02_02_camp_set_02 ...
- **sky** (folder `v5_coast`, 6 models, about 32 min): FL01_01_floating_island_hero_01, FL01_02_floating_island_hero_02, FL01_03_floating_island_hero_03, FL02_01_floating_island_small_01, FL02_02_floating_island_small_02, FL02_03_floating_island_small_03

For each batch: write the builders, run `powershell -File library\src\v4run.ps1 -Module v5_vi -Worker vi -Batch <batch>`, read the contact sheets, fix and re-run failing ids with `-Only`, then report ids built, triangle counts, size check and anything you could not do. Chunks of 12 models or fewer. Do not run `v4_merge.py` or the upload; the parent does.

Stop conditions: a batch is clean when every model passes the checks in the style guide section 1 and the contact sheet shows a clear silhouette. Maximum three fix rounds per model; list what is still weak.

Rules: original designs only; no glow; no marketplace models; never print the Open Cloud key; do not touch other workers' files.
