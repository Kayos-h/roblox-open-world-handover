# Blender model build loop: instructions for each cycle

GOAL: build ALL 390 models listed in `V4_MANIFEST.md` (data: `V4_MANIFEST.json`) before touching the Roblox map. Quality over speed.
Reference image of the target look: `C:\Users\Nitro\.kiro\crew\uploads\943989c5b0354ac5b891320284412c60_pasted-image-20261029-081421324.png`
(dense varied forest, jagged snow peaks, red-brown badlands mesas, rocky coast, offshore tree-topped islets, big waterfall tree).

## Rules
- Elf look is NATURAL elven: wood, bark, moss, stone, green shingles, warm lantern glow only. NO neon, no glowing or coloured-light plants.
- Treehouses connect to the ground by a ladder or stair (markers ladder_bottom / ladder_top / door / deck).
- Original designs, never copies of Black Clover.
- Do NOT edit the Roblox Studio map in this phase.
- Blender 5.2.2 is attached via execute_blender_code. One Blender job at a time (host memory is tight).
- Units: 1 unit = 1 stud. Z up in Blender. Model front faces -Y. Origin at bottom centre.
- Each piece under 18,000 triangles after export (export splits by colour; the batch runner reports max_tris per model).

## Each cycle = one batch (8 to 16 related models)
1. `session_ledger_read`. Open `V4_MANIFEST.md` and pick the next unbuilt group. Order: D03, D04, D05, D06, D08, D09 (elf), then B, A, R, F, E, C.
2. Read first: `library\src\kitlib.py` (palette keys PAL, shape helpers box/cyl/ball/lathe/tube/torus/poly_prism), `v4util.py` (run_batch, marker, extract_markers),
   `v4_elf.py`, `v4_elf2.py`, `v4_elf3.py` (house style and helpers), `nature.py` (blob, rock, branch_tree). Add new palette keys to `kitlib.PAL` if needed (keep `ev_*` natural).
3. Write `library\src\v4_<group>.py`: builder functions that return the finalized object, plus a `BATCH = [(manifest_id, fn[, view])]` list. Manifest ids are listed in `V4_MANIFEST.md`.
4. Run in Blender (execute_blender_code): add the src folder to sys.path, importlib.reload kitlib, v4util and your module, then
   `v4util.run_batch(BATCH, '<folder e.g. v4_elf>', 'batchNN_<name>')`. It saves .blend + .fbx, runs the per-colour export, and writes ONE contact sheet to `library\v4_sheets\batchNN_<name>.png`.
5. LOOK at that sheet (read tool, Image mode, one image per batch). Judge critically: silhouette, scale, colours, floating parts, clipping, repetition. Fix defects in code and re-run. Never claim quality without looking.
6. `python v4_manifest.py` (working dir `library\src`) refreshes status. Then `session_ledger_record` with the built count, next group and main-chat image count.

## Image limit
A chat holds at most 100 images. The main chat was at 14 when this loop started. Open only ONE sheet per batch and keep a running count.
At 75: call autonudge_stop, write `library\HANDOFF_BLENDER.md` (state, how to run a batch, what is built, what is next, known defects) and tell the user to open a new chat.

## Exit
When the manifest shows all 390 built and every batch was reviewed: autonudge_stop and report totals, file locations, known defects, and what remains for the map build.
Also stop and report if blocked (Blender disconnected twice, or errors you cannot fix). Keep per-cycle chat output short.

## Lessons from batch 03 (read before writing code)
- LEDGER IMAGE LEAK: never put a bare `.png` path into `session_ledger_record(artifacts=...)`. The runtime attaches every bare image path as a real image on EVERY later cycle and burns the 100-image chat limit. Write sheet paths as text with a prefix, e.g. `text only: library\v4_sheets\x.png`.
- `v4_elf.ladder(x, y, z0, z1, ang)` takes the OUTWARD facing angle (the deck's radial direction). Never pass `angle + pi/2`: that turns the ladder sideways to the deck (this bug was in treehouses A-F and was fixed in cycle 1). `v4_elf3._rope_ladder` follows the same rule.
- New marker `mk_conn` (meaning `connect`): open end of a platform, walkway or bridge, at deck height. Add one per open end.
- Modular rule for group D03: every deck mates at `v4_d03.DECK_Z = 11`. Keep new connectors at that height.
- To check ladders, aim the preview at the ladder face: `view` in a batch item may be a function of the markers, e.g. `face_ladder(marks)` returning (x/n, y/n, 0.30) from `marks['ladder_bottom'][0]`.
- Lantern on a post: `lantern(x, y, post_top + 1.12*s, s, hang=False)`. Hanging: `lantern(x, y, arm_z - 0.9*s, s, hang=True)`.
- A batch of 8 models takes about 20 s to build; 8 treehouses about 90 s. Contact sheet cell size is 420 px.

## Known polish items
- Treehouse crowns share one shape: vary tree species and canopy in D05.
- Elf trees: world tree needs trunk + roots + canopy as separate big pieces (D05_01..03).

- kitlib shape helpers (box, cyl, lathe via _place) take rot in DEGREES; obj.rotation_euler is RADIANS. Convert with math.degrees() when passing radians. (Found in D06: tilts were ~0 until fixed.)
- tube(): never pass the same last point twice (Bezier AUTO handles make a long spike). Build index lists with range(0,n+1,3) plus n only if n%3 != 0.
- When a thumbnail shows thin lines that look like outlines, print object bounds before guessing; do not tune widths blindly.

- Absolute .png paths inside session_ledger_record strings are re-attached as images every cycle. Write path-free text ("text only: ...").
- Blender execute_blender_code calls longer than ~60 s lose the reply ("No data received") but the code keeps running. Split build and render into separate calls.
- EXACT booleans on a hollow (solidified) shell fail (result collapses to a sliver) when the cut plane is nearly tangent to a lobe. Put every lower ellipsoid bottom at least 10 below the base cut plane, and drop flat pancake lobes.
- Organic body recipe (skull): noise ellipsoids -> voxel remesh 1.9 -> smooth -> decimate 0.2 -> solidify 6 -> cuts -> colour faces by distance to the outer surface. A gap between two ellipsoids (a waist) shows up as a missing mouth band: add a joining lobe.
- Root teeth and spikes by ray casting from OUTSIDE the finished body onto its outer surface, not from inside, or they grow from the inner wall.
