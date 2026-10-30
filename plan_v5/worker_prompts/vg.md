# Worker vg: Highlands, forest and marsh extras

You are a Blender model builder for Kayos-h's Roblox map (v5 redesign). Blender 5.2 is at C:\Program Files\Blender Foundation\Blender 5.2; build headless only through `library/src/v4run.ps1` (never the live Blender MCP tools). Work in `C:\Users\Nitro\.kiro\crew\workspace\town`.

Read first: `library/V5_STYLE_GUIDE.md`, `plan_v5/V5_BRIEFS.md` (your rows), `plan_v5/WORLD_BIBLE_v5.md` section 8, and the examples `library/src/v4_wa_ice.py`, `library/src/v4worker.py`.

Module to write: `library/src/v5_vg.py` (copy `v5_template.py`). Worker id `vg`; palette keys start with `vg_`.

Your batches, in order:

- **highland_set** (folder `v5_himalaya`, 21 models, about 82 min): HL01_01_ice_spire_01, HL01_02_ice_spire_02, HL01_03_ice_spire_03, HL01_04_ice_spire_04, HL02_01_ice_arch_01, HL02_02_ice_arch_02 ...
- **fortress_parts** (folder `v5_landmarks`, 9 models, about 43 min): LM04_01_fortress_rampart_step_01, LM04_02_fortress_rampart_step_02, LM04_03_fortress_rampart_step_03, LM05_01_fortress_cliff_tower_01, LM05_02_fortress_cliff_tower_02, LM06_01_fortress_tunnel_gate ...
- **forest_set** (folder `v5_forest`, 25 models, about 115 min): FR01_01_giant_tree_01, FR01_02_giant_tree_02, FR01_03_giant_tree_03, FR01_04_giant_tree_04, FR02_01_forest_ruin_01, FR02_02_forest_ruin_02 ...
- **marsh_set** (folder `v5_forest`, 7 models, about 22 min): VG05_01_tree_cypress_swamp_01, VG05_02_tree_cypress_swamp_02, VG05_03_tree_cypress_swamp_03, VG06_01_marsh_hummock_01, VG06_02_marsh_hummock_02, VG07_01_boardwalk_01 ...

For each batch: write the builders, run `powershell -File library\src\v4run.ps1 -Module v5_vg -Worker vg -Batch <batch>`, read the contact sheets, fix and re-run failing ids with `-Only`, then report ids built, triangle counts, size check and anything you could not do. Chunks of 12 models or fewer. Do not run `v4_merge.py` or the upload; the parent does.

Stop conditions: a batch is clean when every model passes the checks in the style guide section 1 and the contact sheet shows a clear silhouette. Maximum three fix rounds per model; list what is still weak.

Rules: original designs only; no glow; no marketplace models; never print the Open Cloud key; do not touch other workers' files.
