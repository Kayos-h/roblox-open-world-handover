# Independent reviewer brief, fourth review (R4: models rebuilt in the second fix round)

You are a FRESH reviewer. You did not build these models and you have never seen them. Be strict: a generous review is useless. Do NOT open any file other than the ones named below. In particular do not read anything in folders named `fix`, `fix_scratch`, `v5_round1_archive`, `v5_work\gallery` or any file named `REVIEW_*`, `review_*`, `assign_*` or `AUTOCHECK_*`, and do not read code. You judge pictures only.

## What the models are
Blender models for a stylised fantasy open-world Roblox game (chunky low-poly look). Roblox colours every piece from a palette. The grey ground and flat grey-blue sky in every picture are only the photo studio. Original designs only.

Paths (LIB = `C:\Users\Nitro\.kiro\crew\workspace\town\library`):
- Sheets: `LIB\v5_work\r4\pack\review_001.jpg` to `review_008.jpg`: 12 models per sheet (3 columns x 4 rows). Each cell shows the front 3/4 view (left) and the back 3/4 view (right). The caption gives id, triangle count and size in studs (x y z, z = height). `LIB\v5_work\r4\pack\INDEX.md` lists the ids per sheet and which ids also have a four-angle sheet.
- Four-angle sheets: `LIB\v5_work\r4\pack\hero_001.jpg` ... : two models per sheet, each with 3/4 front (top left), 3/4 back (top right), close-up (bottom left), front elevation (bottom right). Use them for every model in your slice that has one.
- Larger single views: front `LIB\v4_sheets\_t_<id>.png`, back `LIB\v5_work\r4\back\<id>.png` (420 px each). Use them to confirm a doubt before condemning a model.
- Look and feel reference: open ONCE `C:\Users\Nitro\.kiro\crew\workspace\town\reference\world_concept_topdown.png`, and, if your slice has capital pieces (ids starting CP), `C:\Users\Nitro\.kiro\crew\workspace\town\reference\castle_town_reference.png`.

## What to check on every model
1. **Silhouette**: it reads as what its id says (a bridge is a bridge, a staircase has visible steps, an entrance has a visible opening).
2. **Construction**: no floating or detached parts, no holes where it should be solid, no see-through gaps, no black or inverted patches, no open boxes, no stripes from overlapping faces. Look at BOTH views.
3. **Surface and colour**: no square "camouflage" colour patches on rock or walls, no flat single-colour slabs without relief, no glowing or neon look (nothing may glow; bright white or cyan flat slabs read as light panels), no unnatural colours, not the plain grey default.
4. **Proportion and scale**: compare with the size in the caption and with siblings; a character is 5.5 studs tall; doors on enterable buildings at least 4 wide and 7 high.
5. **Variety**: siblings that should be different designs must differ in shape and arrangement, not only in colour.
6. **Modular pieces** (walls, cliffs, stairs, bridges, fences, road kit): would they tile and rest on the ground?
7. **Detail level**: a few plain boxes where the id promises a landmark is a defect. Compare with the neighbours on the same sheet.
8. **Rules**: no freestanding plain ENTRANCE ARCH (capital gatehouses, bridges, natural rock arches and ruined arches are fine); nothing glowing.
9. **ORIGINALITY**: flag any model whose design strongly resembles a recognisable existing franchise (a named castle, symbol, emblem, character, creature or building from a game, film or anime; the anime Black Clover in particular: its four-leaf clover emblem, grimoire books, Magic Knight headquarters). Say which one. Generic fantasy forms (towers, keeps, dragons skulls, mushrooms) are fine.

## Verdicts
- `OK`: normal and usable, you would not ask for a change.
- `MINOR`: a small flaw; fixing is optional.
- `MAJOR`: clearly wrong, ugly, crude or broken; must be fixed.
- `REDO`: not salvageable; rebuild from scratch.
Judge from the distance a player normally sees it (30 to 60 studs) and, for hero pieces, also close up. Judge what you SEE, not what the id promises.

## How to work
- Open at most 45 images in total (read tool, Image mode): your sheets, the four-angle sheets for your models, and at most about 15 larger single views.
- After EACH sheet write its findings to `LIB\v5_work\r4\part_<NNN>.json` (NNN = sheet number, for example `part_007.json`): a JSON list with one object per model on that sheet: `{"id": "...", "verdict": "OK|MINOR|MAJOR|REDO", "defects": ["short phrase", ...], "fix": "one concrete sentence, empty if OK", "original": "OK|SIMILAR TO <what>"}`. Mention the view (front or back) in a defect when it is only visible from one side.
- At the end write `LIB\v5_work\r4\slice_<YOUR LETTER>.md`: verdict counts, a table of every non-OK model (id, verdict, what is wrong, how to fix), and the patterns that repeat across several models.
- Do not modify any model, script or source file. Do not run Blender, Roblox Studio or any Blender or Studio tool. Write only the files named above. Do not run commands longer than 2 minutes.

## Final answer (text only, at most 15 lines)
Counts per verdict for your slice, the repeating patterns, the 10 worst models, any originality concern, and anything you could not judge and why. No praise lists.
