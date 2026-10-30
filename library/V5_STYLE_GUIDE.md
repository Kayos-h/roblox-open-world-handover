# V5 Blender style guide (all new models)

Written 30 Oct 2026. Applies to every row in `plan_v5/V5_MANIFEST.md`. Plan and reasons: `plan_v5/WORLD_BIBLE_v5.md`. Per-row text: `plan_v5/V5_BRIEFS.md`.

## 1. Hard rules
- **Original designs only.** No Black Clover names, emblems, title art or recognisable character shapes. No marketplace models.
- **No glow.** Every palette key has emission 0. Warm light comes from Roblox lights placed in Studio. Lava veins and runes are terrain paint or carved relief.
- **Units and axes:** 1 Blender unit = 1 stud. Z is up. The front (the side you walk up to) faces -Y. Pivot is the centre of the footprint at z = 0. Long-axis models (bridges, walls) run along X.
- **Size:** within +-10% of the manifest size. **Triangles:** each MeshPart at most 20k, the whole model at most the manifest budget (the wizard tower rows are the only ones allowed above 60k).
- **Watertight and clean:** no floating pieces, no flipped normals, no hidden interior junk, no pieces thinner than 0.3 studs. Walls of enterable buildings at least 4 studs thick. Doors, portcullises, banners and gates that should move are separate meshes with their pivot at the hinge.
- **Materials:** at most 8 palette keys per model. Keys are `<worker>_<name>` (for example `vd_roof_orange`) registered as `PAL['vd_name'] = ((r,g,b), 'RobloxMaterial', metallic, roughness, 0)`. Roblox materials to prefer: Cobblestone, Slate, Limestone, Brick, WoodPlanks, Wood, Fabric, Metal, CorrodedMetal, Sand, Snow, Ice, Grass, Ground.
- **Colour per place:** use the palette in the row brief. One dominant roof family per settlement. Vary value, not hue, inside a family.

## 2. What makes a model look good in this game
- **Silhouette first.** It must read at 500 studs on a 256 px render. Break straight edges: roof overhangs, buttresses, chimneys, finials, uneven heights.
- **Three scales of detail:** big forms (the massing), medium (windows, beams, stairs, balconies), small (trim, nails, hanging lamps). Skip the medium level and it looks like a box.
- **Believable structure:** things carry loads; stairs go somewhere; every raised floor has a way up (stairs or ladder with `ladder_bottom` / `ladder_top` markers).
- **Weathering by shape and colour,** not noise: stains by value, moss on the north side, chipped corners, uneven stone courses.
- **Natural places stay natural:** forest and elf pieces are wood, stone and moss with curved forms; no neon, no metal pipes.
- **No arches at entrances.** The plain arch is gone; entrances are roads, trees, boulders and a sign. Real gatehouses in walls (capital, fortress) are fine.

## 3. Interiors (wizard tower and any enterable building)
- Clear height 28 per floor in the tower (10 minimum elsewhere), door openings 8 x 12, nothing narrower than 7 studs on a walking route, stairs: rise at most 1.2, run at least 2.2, landings 10 deep, handrails both sides.
- Build interiors so they can be walked on: floors are flat boxes or flat meshes, no tiny bumps. Export a `<model>_collision.json` (boxes) for large interiors; visible meshes of props do not collide.

## 4. Worker procedure (same as v4)
1. Copy `library/src/v5_template.py` to `library/src/v5_<worker>.py`; write one builder function per model and a `BATCHES` dict (batch name -> (category folder, [(id, builder), ...])).
2. Run through `v4run.ps1 -Module v5_<worker> -Worker v<x> -Batch <batch>` (headless, factory startup, two Blender processes at most, calls over 60 s lose the reply, so keep batches to 12 models or fewer).
3. Look at the contact sheets in `library/v4_sheets/`, fix, re-run only the failing ids with `--only`.
4. When a batch is clean, ask an independent reviewer (see `MODEL_REVIEW_BRIEF.md`). Fix what it lists.
5. `python library/src/v4_merge.py` folds the metadata into `v4_meta.json` and the palettes into `palette.json`. Then `upload_v5.ps1`.
6. Never print or paste the Open Cloud key. The user closes Blender before the upload.

## 5. Naming
Ids are exactly the ids in the manifest (for example `CP01_02_ring_wall_straight_02`). Category folders: v5_wizard, v5_himalaya, v5_capital, v5_elf, v5_town1, v5_entrances, v5_landmarks, v5_coast, v5_roads, v5_forest, v5_plains, v5_desert, v5_skull.
