# Map v4 overnight runbook (30 Oct 2026)

The user (Kayos-h) is asleep from about 01:00 to 08:00 Nepal time. His words: do everything yourself, ask nothing, improvise,
use placeholders for any model that is not uploaded yet, make the map beautiful, send every town / terrain / environment to
sub-agents and keep improving. Read the session ledger first (session_ledger_read); it is authoritative.

## Standing rules
- NEVER look at photos yourself (no `read` Image mode on map pictures). Only sub-agents look at pictures. Use `spawn_sub_agents`
  (blocking, returns their text) with fresh context, max ~20 pictures each, and always include the top-down reference picture
  `C:\Users\Nitro\.kiro\crew\uploads\943989c5b0354ac5b891320284412c60_pasted-image-20261029-081421324.png`.
  Ask for a score out of 10 per area and concrete fixes with coordinates. Tell them to be strict (builders over-rate their work).
- Photos: `town\tour.ps1 -views <csv name,pos,look> -dir <out dir>` (960x602 jpg via PrintWindow). The crop rectangle is hard-coded
  (x=10 y=175 w=1530 h=960); a sub-agent must confirm it still fits this Studio window. Restore the camera afterwards with
  `town\mcp_call.ps1 -tool execute_luau -argsFile town\_cam_restore.json`.
- Original names and designs only; no copied Black Clover content; anchor everything; at most 1-2 enterable buildings per settlement.
- Elf village: NO Neon, NO glow (no emissive parts, no glow lights or particles), natural look, still in the valley between the four mountains.
- Never lower existing quality. Archive to ServerStorage (`Phase1Archive_v3_*`) instead of deleting. Town 1 zone x +-318, z -545..311 stays
  untouched (`keep.town1` in world.json when regenerating terrain, because `_G.T1SNAP` is nil in this session).
- Every Studio change must be replayable from script files under `town\rebuild\v4\`. Record each step in the ledger.
- Acceptance bar: every area >= 8/10 from an independent reviewer, no floating or sunk models, 0 unanchored parts, 0 terrain floaters,
  no glow in the elf village, a top-down overview that resembles the reference.
- RAM is tight (Studio ~4 GB): at most 2 helpers at once, `resource_status` before heavy steps.
- Never print or paste the Open Cloud key. The upload script reads it from the user's environment.

## Upload (V4 models)
`Desktop\5-upload-v4-models.bat` -> `town\upload_v4.ps1` (3 passes, skips finished models). Progress = rows in `town\asset_ids.csv`
(330 old + 390 new = 720 at the end), log `town\upload_v4_log.txt`. A one-model test was verified in Studio (scale 1 unit = 1 stud,
one MeshPart per colour named by palette key). If the upload died: restart with
`powershell -NoProfile -ExecutionPolicy Bypass -File town\upload_v4.ps1` in an independent console (`cmd /c start "V4 upload" /min ...`).
Models not uploaded yet: use the old 330 models or simple parts as placeholders, swap later.

## Studio
- Native robloxstudio tools (`execute_luau`, ...) work; PowerShell wrappers in `town\` are the fallback (HANDOFF_v3.md sections 3-6, 11).
- Never read `Lighting.Technology` or `Terrain.Decoration`. Facing: rot 0 = +Z, 90 = +X, 180 = -Z, 270 = -X.
- Terrain regeneration order afterwards: fill_voids, fill_voids2, terrain_clip (build_clip.py + clip_run.ps1), floater_scan (must be 0),
  repaints (tools_v3\repaint_and_cleanup.luau parts B-E, rusty_repaint.luau, rock_vary.luau, _nograss.json).
- Save after each reviewed step: `AssetService:SavePlaceAsync()` through execute_luau, else Ctrl+S in Studio with the computer tools.

## Loop
build -> photos -> independent reviewer sub-agent(s) -> fix -> repeat. When waiting (upload, reviewer) use `wait` (max 600 s) or `nothing_to_do`.
When the morning report is written: short, with what is done, what is left, save status and photo paths, then `monitor_stop`.


## Steering notes to put at the END of the final morning message (exact format)
[STEERING steer-a2b168ce598743b39a3926ed020ede85: I ran the V4 upload myself from this session with the saved key (never printed). A one-model test passed and was checked in Studio (scale and part names), then the rest was uploaded in a background console.]
[STEERING steer-8e534b3784b04dc18c9e50a3e621d8a4: Worked fully on my own overnight, used placeholders for anything not uploaded, and ran build / photo / sub-agent review / fix rounds on terrain, environment and every town.]
[STEERING steer-88ae591a06694cf68b15b79b39886839: Saved your rule that only sub-agents look at photos (I never opened one myself) and used the long time budget for repeated review rounds.]
