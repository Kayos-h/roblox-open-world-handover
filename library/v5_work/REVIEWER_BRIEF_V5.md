# v5 independent reviewer brief

You are a FRESH reviewer. You did not build any of these models. Do NOT read builder code, `progress_*` files, `AUTOCHECK_V5.*` or any worker transcript before you have formed your own opinion of a sheet. The owner wants top-quality, believable, well-made assets, so be critical: a generous review is useless. The owner will have everything you rate MAJOR or REDO fixed, so your words decide what gets rebuilt.

## What the models are
404 Blender models for a stylised fantasy open-world Roblox game (chunky low-poly look, original designs, no Black Clover shapes or names). Each model is one saved file; Roblox colours every piece from a palette. The grey ground and flat grey-blue sky in every picture are only the review studio, not the game.

Paths (LIB = `C:\Users\Nitro\.kiro\crew\workspace\town\library`):
- Sheets: `LIB\v5_work\review_pack\review_001.jpg` ... `review_034.jpg`: 12 models per sheet (4 columns x 3 rows). The caption under each cell shows the saved id, triangle count and size in studs (x y z, z = height). `LIB\v5_work\review_pack\INDEX.md` lists the ids per sheet and which `hero_NNN.jpg` sheets exist.
- Hero sheets: `LIB\v5_work\review_pack\hero_001.jpg` ... : four angles (3/4 front, 3/4 back, close-up, front elevation) of the big landmark pieces, 2 per sheet. Use them for every model that has one.
- Close-ups: `LIB\v4_sheets\_t_<id>.png` is the single 3/4 view of one model (larger than its sheet cell). Use it to confirm a doubt before condemning a model.
- Target look: open ONCE `C:\Users\Nitro\.kiro\crew\workspace\town\reference\world_concept_topdown.png` (the island concept map) and, if your slice contains capital pieces (ids starting CP), `C:\Users\Nitro\.kiro\crew\workspace\town\reference\castle_town_reference.png` (ring wall with round cone-roofed towers, keep on a raised terrace, dense half-timbered town with ONE dominant orange-red roof colour).

## What to check on every model
1. **Silhouette**: does it read as what its id says (a bridge is a bridge, a tower a tower, a rock formation natural)?
2. **Construction defects**: floating or detached parts, parts clipping through each other, holes where it should be solid, see-through gaps, black or inverted patches, missing roof or back, open boxes, stripes from overlapping faces.
3. **Surface and colour**: blocky square camouflage colour patches on rock, flat single-colour slabs with no relief, neon or glowing look (NO glow is allowed anywhere), unnatural colours, a grey default look.
4. **Proportion and scale**: compare with the size in the caption and with siblings; doors on enterable buildings at least 4 wide and 7 high; a character is 5.5 studs tall.
5. **Variety**: siblings that should be different designs must not look like recolours of each other.
6. **Modular pieces** (walls, cliffs, stairs, bridges, fences, road kit): would they tile and rest on the ground?
7. **Detail level**: too crude (a few plain boxes where the id promises a landmark) is a defect. Compare with the neighbours in the same sheet.
8. **Rules**: a freestanding plain ENTRANCE ARCH is forbidden (capital gatehouses and bridges, natural rock arches and ruined arches are fine); anything glowing or emissive fails; models must stand on z = 0 with the front facing the camera's left-front.

## Verdicts
- `OK`: normal and usable.
- `MINOR`: a small flaw; fixing is optional.
- `MAJOR`: clearly wrong, ugly, crude or broken; must be fixed.
- `REDO`: the concept or build is not salvageable; rebuild from scratch.
Judge from the distance a player normally sees it (30 to 60 studs) and, for hero pieces, also close up.

## Extra for the wizard tower (ids starting WT01 to WT13)
Score each 1-10: EXTERIOR PRESENCE (does it look like the landmark of the island from far away), INTERIOR (walkable, headroom, stairs), BOOKSHELVES (floor-to-ceiling, packed books, curved to the wall), CIRCULAR MAP (reads as a relief map of an island, rings and landmark tokens, brass and stone), SILHOUETTE, MATERIALS. The tower needs 8 or more in every category. A single category under 8 means MAJOR.

## How to work
- Open at most 40 images in total (read tool, Image mode). Open each of your sheets once, the hero sheets for models in your slice, and at most about 20 close-ups.
- After EACH sheet write its findings to `LIB\v5_work\review_part_<NNN>.json` (NNN = sheet number, for example `review_part_007.json`): a JSON list with one object per model on that sheet: `{"id": "...", "verdict": "OK|MINOR|MAJOR|REDO", "defects": ["short phrase", ...], "fix": "one concrete sentence on how to fix it, empty if OK"}`. Tower models also get `"scores": {"exterior": n, ...}`.
- At the end write `LIB\v5_work\review_slice_<YOUR LETTER>.md`: verdict counts for your slice, a table of every non-OK model (id, verdict, what is wrong, how to fix), and a short 'systemic issues' section for patterns across many models, each with one recommended fix.
- Do not modify any model, script or source file. Do not run Blender, do not touch Roblox Studio or any Blender or Studio tool. Write only the files named above. Do not run commands longer than 2 minutes.

## Final answer (text only, at most 15 lines)
Counts per verdict for your slice, the biggest systemic issues, the 10 worst models, and anything you could not judge and why. No praise lists.
