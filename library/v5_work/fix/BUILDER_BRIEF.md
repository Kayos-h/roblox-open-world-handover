# Builder brief: v5 fix round

You are a builder in a fix round. A first independent review rated part of a set of 404 Blender models (for a Roblox fantasy open-world game) as flawed. You rebuild the flawed models in your assignment so that a fresh, strict reviewer rates every one of them OK. You are one of six builders working at the same time on different files.

Paths (T = `C:\Users\Nitro\.kiro\crew\workspace\town`, LIB = `T\library`, SRC = `LIB\src`):
- Your assignment: `LIB\v5_work\fix\assign_<A>.md` (named in your task): the models, the reviewers' complaints and suggestions, target size, triangle budget.
- Round-1 photos of what the reviewers saw: `LIB\v5_round1_archive\v4_sheets\_t_<id>.png` (one 3/4 view, 420 px). Open the ones you need.
- Round-1 code: `SRC\v5_v?.py` (the queue modules), `SRC\v5gen.py` (house, round_tower, wall_seg, column, cliff, spire, rock_arch, tree), `SRC\v5kit.py` (the `Acc` geometry accumulator). Read; do not edit.

## What the reviewers judge
One photo per model (big landmarks get four angles), seen from the distance a player normally has (30 to 60 studs). They check: the silhouette reads as what the id says; no floating or detached parts; no holes, black or inverted faces; no square "camouflage" colour patches on rock or walls; no flat single-colour slabs without relief; sensible scale (a character is 5.5 studs, doors on enterable buildings at least 4 wide and 7 high); siblings in a set are really different designs (not recolours); modular pieces tile and rest on the ground; detail level matches the good neighbours (not crude blockouts); the same chunky low-poly fantasy style across the set.
Typical complaints in round 1: stacked flat slabs that look like paper or pancakes instead of rock, parts floating in air, rock coloured by random square patches, a "stair" or "entrance" that does not read as one, props that are an unreadable jumble, near-identical clones differing only in colour, flat grey rock, waterfalls drawn as bright white or cyan slabs that look like light panels.

## Hard rules
- Original designs only. No names or shapes from any existing franchise, no marketplace assets.
- No glow anywhere: no Neon or ForceField material, no pure white or saturated cyan flat slabs. Water is pale, matte, stepped, with foam at the base.
- No freestanding plain entrance arch. Natural rock arches, ruined arches and capital gatehouses are allowed.
- Pivot at the bottom centre of the bounding box on z = 0, front faces -Y, 1 unit = 1 stud. Blender axes: X width, Y depth, Z height. The assignment table gives target W x D x H in these axes. Design to size: `mk(..., 0.1)` autofits any model that is more than 10% off, and that distorts it.
- Triangles must stay within the budget. Do not go far below it either: reviewers called thin models crude. Aim for at least a third of the budget on complex pieces and landmarks.
- Keep the markers the round-1 builder produced (bridges: end_a, end_b, deck; ladders; doors and hinges). Find them with `grep mk_` in the round-1 module and compare the `mk=` field of the scratch output.
- Palette: register NEW keys only, with the prefix given in your assignment (`P = G.reg('<prefix>', {...})`). Never re-register a round-1 key name with another colour, that would recolour models that are not rebuilt. You may reuse round-1 colours through the round-1 module's palette dict (read the top of the module for its name).
- Write only: your own fix module file(s) listed in the assignment, and `LIB\v5_work\fix_scratch\<A>\`. Do not edit `v5kit.py`, `v5gen.py`, any `v5_v?.py`, `kitlib.py`, other builders' modules, the library folders, the metas or the palette files. Do not run Blender yourself, do not touch Roblox Studio, do not upload anything, do not delete anything outside your scratch folder. If you find a bug in the shared kit, describe it in your report; do not work around it by editing the kit.

## The kit (Python inside Blender; units are studs)
```
from kitlib import reset, finalize          # builder = reset(); A = Acc(); ...; A.to_scene(); return finalize('name', 25)
from v5kit import Acc, polar, tang, mk, ids, band, strata
A.box(size, loc, key, rot=(0,0,0), bev=None)      # centred on loc; edges chamfered automatically (bev=0 sharp); rot = Euler XYZ degrees
A.beam(p0, p1, w, h, key)                         # box of section w x h from point to point (rails, poles, rafters)
A.frustum(base(w,d), top(w,d), h, loc, key)       # tapered block / pyramid when top is tiny
A.gable(w, d, h, loc, key, rot)                   # roof prism, ridge along Y (rot=(0,0,90) for X)
A.cyl(r, h, loc, key, verts=16, r2=None, rot=(0,0,0))   # cylinder or cone standing on loc
A.ball(r, loc, key, segs, rings, scale=(1,1,1))  # ellipsoid
A.prism(pts2d, h, loc, key)  A.revolve(profile, loc, key, segs)  A.sweep(poly, a0, a1, n, key, loc)  A.ring_wall(r_in, r_out, z0, z1, openings, key)
A.chunk(size, loc, key, rot, jit, rnd, taper)     # angular rock chunk (box with jittered corners)
A.mound(cx, cy, w, d, h, n, keys, rnd, z0)        # heap of chunks; colour now graded by height (keys bottom to top)
A.append(other_acc, loc, rot, scale)              # copy another Acc (negative scale mirrors)
band(keys, t, rnd)    strata(keys, layer, thick) # graded / banded colour choice: use these instead of random choice for rock and walls
G.cliff(A, rnd, w, d, h, keys, ..., mode='strata'|'grade')   G.spire  G.rock_arch  G.tree  G.house  G.round_tower  G.wall_seg  G.column
```
Every builder starts with `reset()`, draws into one `Acc`, ends with `A.to_scene()` and `return finalize('name', 25)`. Use `random.Random(fixed_seed)` so a model builds the same every time. `ids('RD05')` returns the manifest ids of a row in order: use it, never type ids. A `BATCHES` entry is `'batch_name': ('<category folder from the assignment>', mk([(manifest_id, builder), ...], 0.1))` and every id of your assignment must appear in exactly one entry with the SAME category folder as round 1.
Good rock: angular chunks with a few big masses and many small ones, colours graded by height or in horizontal strata, a darker base, moss or snow only where it would settle, ledges and fallen rubble at the foot that touch the ground. Good stairs and entrances: framed opening, real recessed dark void or visible treads and risers, side walls. Good props: one clear connected silhouette. Good siblings: change the silhouette, proportions and arrangement, not only the colour.

## Tools
- Build and look (scratch only, safe, about 1 to 3 s per model, one build at a time machine-wide, so a call may wait; `SCRATCH_BUSY` means retry):
  `powershell -NoProfile -ExecutionPolicy Bypass -File "T\scratch.ps1" -Module <your fix module> -Ids id1,id2 -Tag <A> [-Views 4] [-Res 360] [-Samples 10]`
  Writes `LIB\v5_work\fix_scratch\<A>\<id>.png` (-Views 4: 2 x 2 sheet = 3/4 front top-left, 3/4 back top-right, close-up bottom-left, front elevation bottom-right; -Views 1: one 3/4 picture, quickest) and prints per model: triangles, size against target, flags (SIZEx/y/z, TRIS, LOW, EMPTY), `FLOAT n` (clusters of parts that touch neither the ground nor the main body, with position and size; expected 0 except for models that are meant to float), `INV n` (closed parts with inverted faces, they render black; expected 0), markers.
  Build at most 10 ids per call. To see the round-1 version of a model, run the same command with the round-1 module (for example `-Module v5_vi`).
- Look at many at once: `python SRC\v5_contact.py <A> all` (or a comma list, add `before` to put the round-1 photo beside the new render). It prints the paths of `contact_N.jpg` sheets. Open pictures with the read tool in Image mode. You are allowed and expected to look at pictures; judge them like the reviewers above, critically.
- Syntax and numbers without pictures: `powershell -NoProfile -ExecutionPolicy Bypass -File "T\v5check.ps1" -Module <fix module>`.

## Process
1. Read your assignment and the round-1 code of your families. Open the round-1 photos of the worst models.
2. Work worst first (REDO, MAJOR, then MINOR). Per family: decide a better design, write the builder(s) in your fix module, scratch-build, look, fix, repeat. At most 6 rounds per family, then move on and record it as not satisfied (say what is still wrong).
3. Fix the cause shared by a family once, then vary it per sibling. MINOR "recolour" notes need genuinely different geometry.
4. At the end, scratch-build all your ids with `-Views 4 -Res 360 -Samples 12` in chunks of at most 10, look at every sheet, and confirm: silhouette reads, FLOAT 0 (unless meant to float), INV 0, size within 8% of target, triangles within budget, no square colour patches, siblings differ.
5. Stop after about 2 hours of work even if not everything is perfect.

## Final answer (at most 25 lines, text only)
Per family: done, partly or not satisfied. A list of ids you are NOT satisfied with and what is wrong. Any bug in the shared kit. The line the lead runs to build: `live_batch.ps1 -Module <fix module> -Worker <worker>` for each of your modules. Do not claim a model "looks good" in general: say what you checked and what you saw.
