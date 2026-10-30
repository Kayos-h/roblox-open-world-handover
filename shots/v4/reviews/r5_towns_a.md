# Round 5 review — Towns A (castle yard, capital wall, Town 1 plaza, alpine square)

Reviewer: strict senior Roblox art director. Ground-level shots where the GrassLength
change (0.7 -> 0.3) matters most. MCP note: `@Roblox_Studio` was not configured this
session; review done from the photos only, no Studio tool used.

## SPECIAL CHECK 1 — is terrain grass a sensible height now, props clear of it?
PARTLY. The grass fix worked in two shots and failed badly in two.
- Castle yard: still too tall. Blades are knee-to-waist height, spiky and dense; they
  lap the outside of the dark fence and bury the fence feet. Not chest-high anymore, but
  not "sensible" — a drill ground's surround should be mown/trampled.
- Capital wall west: NOT fixed (or broken shot). Grass renders as giant 10-15 stud
  spikes shooting up out of the waterline, and the camera at y=34 is sitting half under
  the water plane. Either GrassLength did not apply to this tile or the cam is below
  terrain. This is the worst frame in the set.
- Town 1 plaza: borderline. Foreground grass is tall and clips the house footing at
  right, but the groomed plaza lawn around the fountain reads fine.
- Alpine square: N/A — snow ground, no grass. Clean.

## SPECIAL CHECK 2 — does the training yard read as a drill ground?
YES. Repainting the floor to packed earth was the right call: flat tan ground, dark
picket fence, a row of straw dummies, pell/target posts and a tree for shade. Garden
strays are gone. It now reads unmistakably as a training pen, not a garden. Best single
improvement in this batch. Only drag on it is the shaggy grass crowding the fence line.

## SPECIAL CHECK 3 — remaining flaws per shot
- Castle yard: tall grass at fence base; dummies are a flat olive-grey and read as blobs
  at distance; the paved path (bottom-right) and a stray crate half-off-frame look tacked
  on; empty dirt center could use a weapon rack or two for silhouette.
- Capital wall west: camera submerged / grass spikes through water; a thin dark diagonal
  seam (shadow or decal) runs up the left wall; a dark triangular slab bottom-right looks
  like a clipped rock or terrain tear.
- Town 1 plaza: foreground grass clips house base; moon/orb sprite floats above the
  statue (sky decal); hero statue face is very smooth/blank; faint dirt-trail decal left
  of the bushes ends abruptly.
- Alpine square: strong shot. Minor — a pale orb floats mid-right (same sky sprite as
  Town 1); a couple of cobble tiles z-fight with snow at the plaza edge; bunting is a bit
  saturated vs the muted snow palette.

## BUGS (world positions approximate from camera data)
- Capital wall west ~(-490,28,-1500): camera/terrain intersection — grass blades spike
  through the water surface and the view is half-submerged. Needs terrain or cam-height
  check. Likely terrain gen touch, not a cheap edit.
- Dark triangular slab, capital wall west, far right ~(-440,30,-1520): looks like a
  clipped rock plinth or seabed tear poking above water.
- Floating pale orb sprite above Town 1 statue ~(0,55,-70) and above alpine square
  ~(1600,175,-910): a sky/sun billboard reading as a floating ball. Cheap to hide/retint.

## KEEP (do not change)
- Castle training yard packed-earth floor + dummy/post layout. Reads correctly; leave it.
- Capital curtain wall: crenellations, blue-roofed towers and cross-slit windows look
  clean and consistent — strong backdrop.
- Town 1 plaza dressing: banners, lamp posts, benches, bush beds and the tiered fountain
  base are well composed and on-theme (skull town).
- Alpine square market: snow-capped A-frame lodges, striped stall awnings, barrels/crates
  and bunting — convincing, lived-in winter market. Palette and clutter are right.

## FIX LIST (ranked, cheap first)
1. Capital wall west: fix the submerged/spiking frame — raise cam or regen the grass tile
   so blades aren't 10x height through water. (terrain gen — expensive, but mandatory)
2. Castle yard: mow/shorten or clear a trampled grass ring just outside the fence so the
   pen sits on groomed ground, not shag. (cheap: GrassLength patch or a dirt apron decal)
3. Town 1 plaza: pull foreground grass back / add a path decal so it stops clipping the
   house footing at right. (cheap)
4. Hide or retint the pale floating orb sprite over Town 1 and alpine square. (cheap)
5. Castle yard: retint dummies warmer (straw/tan) so they don't read as grey blobs; add
   1-2 weapon racks in the empty center for silhouette. (cheap)
6. Capital wall west: remove the dark triangular slab / clipped rock at far right. (cheap)
7. Alpine square: nudge the z-fighting cobble tiles above the snow at the plaza rim; drop
   bunting saturation ~15% to match the muted snow. (cheap)
8. Town 1 plaza: add subtle brow/face detail to the hero statue; trim the dirt-trail
   decal that ends abruptly. (cheap)

## Scores (out of 10)
- Capital wall base: 4 — the wall itself is good, but the ground shot is broken
  (submerged cam, spiking grass). Judged as a presented frame it fails; the asset behind
  it is a 7.
- Castle yard: 6 — up from 5. Packed-earth drill-ground reads now; held back by shaggy
  surround grass and flat dummies.
- Town 1 plaza: 7 — well-dressed, on-theme; foreground grass clip and floating orb are
  the only real knocks.
- Alpine square: 8 — best shot in the batch; clean, atmospheric, convincingly dressed.

ROUND5 SCORES: capital 4, castle yard 6, alpine 8, Town 1 7

## Verdict for these four places
- Castle yard: SHIP (fix grass surround post-ship if time).
- Town 1 plaza: SHIP.
- Alpine square: SHIP.
- Capital wall base: NOT YET — the submerged/spiking ground frame must be fixed first.

## 3 cheapest next changes per place
- Capital wall: (1) raise cam above the waterline / regen the grass tile so blades aren't
  spiking through water; (2) remove the dark triangular slab at far right; (3) retint the
  thin dark diagonal seam on the left wall.
- Castle yard: (1) shorten/trample the grass ring just outside the fence (or add a dirt
  apron decal); (2) retint dummies to straw/tan; (3) add 1-2 weapon racks in the empty
  center.
- Town 1 plaza: (1) pull foreground grass off the house footing / add a path decal; (2)
  hide or retint the floating orb sprite; (3) trim the abrupt dirt-trail decal.
- Alpine square: (1) hide/retint the floating orb sprite; (2) nudge z-fighting cobble
  tiles above the snow; (3) drop bunting saturation ~15%.

Player verdict for this batch today: ~7/10. Single biggest raise: fix the broken
capital-wall ground frame (submerged cam + spiking grass) — it's the only thing here that
looks outright broken rather than merely unpolished.
