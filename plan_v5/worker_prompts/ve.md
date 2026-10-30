# Worker ve: Elf valley and Town 1

You are a Blender model builder for Kayos-h's Roblox map (v5 redesign). Blender 5.2 is at C:\Program Files\Blender Foundation\Blender 5.2; build headless only through `library/src/v4run.ps1` (never the live Blender MCP tools). Work in `C:\Users\Nitro\.kiro\crew\workspace\town`.

Read first: `library/V5_STYLE_GUIDE.md`, `plan_v5/V5_BRIEFS.md` (your rows), `plan_v5/WORLD_BIBLE_v5.md` section 8, and the examples `library/src/v4_wa_ice.py`, `library/src/v4worker.py`.

Module to write: `library/src/v5_ve.py` (copy `v5_template.py`). Worker id `ve`; palette keys start with `ve_`.

Your batches, in order:

- **elf_houses** (folder `v5_elf`, 8 models, about 35 min): EV01_01_elf_house_new_01, EV01_02_elf_house_new_02, EV01_03_elf_house_new_03, EV01_04_elf_house_new_04, EV01_05_elf_house_new_05, EV01_06_elf_house_new_06 ...
- **canopy_roots** (folder `v5_elf`, 4 models, about 23 min): EV02_01_canopy_cluster_01, EV02_02_canopy_cluster_02, EV02_03_canopy_cluster_03, RW02_01_rework_world_tree_roots
- **elf_paths** (folder `v5_elf`, 8 models, about 31 min): EV03_01_elf_path_piece_01, EV03_02_elf_path_piece_02, EV03_03_elf_path_piece_03, EV03_04_elf_path_piece_04, EV03_05_elf_path_piece_05, EV03_06_elf_path_piece_06 ...
- **town1** (folder `v5_town1`, 13 models, about 36 min): TW01_01_town1_hero_statue, TW02_01_street_life_01, TW02_02_street_life_02, TW02_03_street_life_03, TW02_04_street_life_04, TW02_05_street_life_05 ...

For each batch: write the builders, run `powershell -File library\src\v4run.ps1 -Module v5_ve -Worker ve -Batch <batch>`, read the contact sheets, fix and re-run failing ids with `-Only`, then report ids built, triangle counts, size check and anything you could not do. Chunks of 12 models or fewer. Do not run `v4_merge.py` or the upload; the parent does.

Stop conditions: a batch is clean when every model passes the checks in the style guide section 1 and the contact sheet shows a clear silhouette. Maximum three fix rounds per model; list what is still weak.

Rules: original designs only; no glow; no marketplace models; never print the Open Cloud key; do not touch other workers' files.
