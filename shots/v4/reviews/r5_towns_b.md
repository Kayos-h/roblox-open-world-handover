# Round 5 review -- Towns B (ELF VILLAGE priority, harbour, rusty)

Reviewer: strict senior Roblox art director. MCP note: the `@Roblox_Studio`
server was declared but NOT configured, so no Studio tools were available; this
review is from the seven supplied photos only. No tool was called.

## ELF VILLAGE (primary -- ~75% of this review)

The valley has turned the corner. In round 4 it scored 7.0 with a black trunk,
no waterfall and a bare lawn ring. It now reads as a lived-in forest city with a
believable world tree, a real (if thin) waterfall, and a proper house ring. It
is the best it has looked and is close to shippable, but the waterfall and the
flat valley grass still hold it back from a clean pass.

### Special check 1 -- the new waterfall (both waterfall shots)

WORKED, with clear caveats. The old dark-blue slab the last reviewer called the
worst thing in the valley is GONE. In both `f_elf_waterfall` and
`f_elf_waterfall_wide` the fall now reads unambiguously as falling water: a
white-to-pale-cyan ribbon with lighter foam banding running down the real rock
descent, a small splash pool and a reed/flower collar at the foot (~ -1730,-745,
Y~20). It is no longer a glitch. It is a genuine win.

What it still gets wrong, and exactly what to add:
- TOO NARROW. The ribbon is one thin strip (~6-8 studs) against a ~120-stud-tall
  cliff. A world-tree waterfall should be a curtain. Widen the water to 3-4
  parallel ribbons spanning ~24-30 studs, staggered in depth so edges overlap.
- TOO STEEP / STRAIGHT. It falls as one near-vertical line. Break it into 2-3
  stepped ledges with a wider foam shelf at each break (around -1740,-720,Y~70
  and -1735,-710,Y~45) so it cascades instead of sliding.
- NO MIST and NO STREAM. The splash pool just ends. Add a soft white
  semi-transparent mist slab (transparency ~0.85) at the base, and a short
  shallow stream of the same water material from the splash pool running ~40-60
  studs across the grass into the elf lake (lake centre ~ -1560,-430) so the
  water has somewhere to go. Both are cheap part edits.
- The cliff behind it is bare triangulated grey rock with hard facet seams
  (`f_elf_waterfall`, left half). Tuck 3-4 moss/fern clumps and one small ledge
  tree against the rock beside the fall to hide the flat facets.

### Special check 2 -- is the valley now a city? (`f_elf_city`, `f_elf_air`)

PARTLY. The ring of round houses around the world tree now reads as a real
settlement: a dozen woven-roof round houses face the tree, with mushroom caps,
flower beds, a white pavilion/gazebo and stalls between them. From the air
(`f_elf_air`) the floor is populated, not bare. It is a village now, not a lawn.

What is still missing to make it a CITY (reference shows a dense bowl of
dwellings, not a thin ring):
- The ring is one house deep. Add a second, slightly higher ring of 8-10 houses
  at ~230-320 studs out (e.g. -1360,-430; -1760,-430; -1560,-230; -1560,-630)
  so the eye sees depth of settlement, not a single necklace.
- TREEHOUSES are barely used. The world tree's own canopy and the big valley
  trees have almost no platforms/bridges in these shots. Add 4-6 canopy
  platforms with rope bridges around the trunk (Y~90-140) -- that is the single
  most "elf" thing missing and the reference leans on it.
- No clear central plaza or path hierarchy. The dirt paths wander. Give the ring
  one paved/packed moon-pool plaza and a main spoke path from the house ring to
  the tree base.

### Special check 3 -- ground colour, pond rims, glow

- GROUND COLOUR: the promised 88 dapple patches do NOT read in these shots. In
  `f_elf_air` and `f_elf_city` the valley floor is a near-uniform flat mid-green.
  The dapple is either too subtle or too small. Make patches larger (30-60 studs)
  and push contrast: base ~ (86,142,70), lighter ~ (120,170,96), darker ~
  (64,108,56), plus a few warm yellow-green scuffs near paths. This is the
  biggest remaining cheap win for the valley.
- POND RIMS: GOOD. The sand collars are gone; the elf lake and the small ponds
  (`f_elf_air` bottom-left and mid-right) now meet grass/reed rims cleanly. Keep.
- GLOW: NONE found. Correct. No glow mushrooms, no cyan parts, no lit glass, no
  point-light bloom anywhere in any elf shot. Requirement met.

### Special check 4 -- grass height

WORKED. The GrassLength halving fixed it. In `f_elf_city` and `f_elf_tree_base`
the blades are ankle-to-shin height; houses, stalls, the gazebo, flower beds and
the splash-pool reeds all stand clear. No more chest-high grass. One nit: a
single tuft of taller bright-green grass sits dead-centre at the tree base
(~ -1560,-430) and looks like a leftover placeholder -- shrink or remove it.

### ELF BUGS
- Z-FIGHTING / stray slab: `f_elf_tree_base` is dominated by a large translucent
  green canopy-leaf plane clipping right through the camera (~ -1500,65,-370).
  It flickers against the trunk and ruins that view. Either it is a mis-scaled
  canopy card or a stray part -- find and fix; it is the ugliest thing in the
  valley now.
- Floating pale sphere: a small white orb hangs mid-air upper-right in
  `f_elf_tree_base` and again near the trunk in `f_elf_air`/`f_elf_city`
  (~ -1500,150,-430). Looks like a stray decal/part, not the "Back" widget.
  Remove it.
- `f_elf_city` upper-right has a faint balloon/teardrop shape against the sky
  (~ -1360,170,-500) -- verify it is the Studio widget and not a stray part.
- Trunk roots: the splayed buttress roots in `f_elf_air` are a flat reddish
  fan with hard radial seams and read as cardboard from above; round the root
  tips and tint them to match the brighter bark.

### ELF KEEP
- Waterfall now reads as water (huge improvement -- do not revert).
- World-tree trunk colour: brighter warm bark, no black crush. Keep.
- Round-house ring + mushroom/flower dressing + white pavilion. Keep.
- Pond/lake grass rims, no sand. Keep.
- Zero glow. Keep.
- Sensible grass height. Keep.

## HARBOUR (`f_harbour_inland`)

Clean and convincing. Dense half-timbered houses in nine roof hues, tidy paved
plaza with benches and lamp posts, lighthouse left and a ruined fort/keep right
framing the bay, calm deep-blue sea with a soft horizon seam (no octagon foam).
Grass height is now correct. Nits: roof-hue distribution is slightly
red-heavy; a couple of lamp posts sit very close to house walls; one gabled
house front-centre is plain grey render (missing material?). Minor only.

## RUSTY HUTS (`f_rusty_huts`)

The layered, non-uniform mesas behind the town (`f_rusty_huts` background) are a
real step up -- banded sandstone, varied heights, good badlands read. Stone
huts, dead trees, barrels, rock scatter and the ochre church with amber panes
all sit well on the tan floor.
PROBLEM: the promised teal / rust-red roofs did NOT land on these huts. Nearly
every roof here is the same dull flat tan/olive, so the town reads monochrome
against monochrome desert. Repaint ~two thirds of the hut roofs to the intended
teal (~ 70,120,120) and rust-red (~ 150,70,50) -- cheap, high payoff. Also the
foreground hut roof (~1200,20,1210) shows hard facet seams; add a ridge cap.

## 8 MOST VALUABLE REMAINING ELF FIXES (ordered by payoff/effort)
1. Remove the translucent canopy slab clipping the camera at ~ -1500,65,-370
   (`f_elf_tree_base`). Cheap, fixes the worst current view.
2. Widen the waterfall to 3-4 ribbons over ~24-30 studs at the fall line
   ~ -1735,-720 to -1730,-745. Cheap parts.
3. Push valley-floor grass dapple: larger, higher-contrast patches across the
   bowl (world tree at -1560,-430, radius ~400). Cheap colour edit.
4. Add a base mist slab + a short stream from the splash pool (~ -1730,-745) into
   the elf lake (~ -1560,-430). Cheap parts.
5. Add 4-6 canopy treehouse platforms with rope bridges on the world tree,
   Y~90-140 around the trunk at -1560,-430. Medium effort, big "elf" payoff.
6. Add a second house ring (8-10 round houses) at ~230-320 studs out from the
   tree (e.g. -1360,-430; -1760,-430; -1560,-230; -1560,-630). Medium.
7. Remove the floating white orb(s) near the trunk (~ -1500,150,-430) and the
   central placeholder grass tuft at -1560,-430. Cheap.
8. Break the fall into 2-3 stepped ledges with foam shelves (~ -1740,-720,Y70 and
   -1735,-710,Y45) and tuck moss/ferns against the bare grey cliff beside it.
   Cheap-to-medium.

## Scores
- ELF VILLAGE: 8 / 10. Waterfall fixed, real house ring, correct grass, zero
  glow -- up from 7.0. Held back by the camera-clipping canopy slab, the
  too-thin single-ribbon fall, and flat valley grass.
- HARBOUR: 8.5 / 10. Dense, tidy, well framed, correct grass; tiny roof-hue and
  placement nits only.
- RUSTY: 7.5 / 10. Mesas and floor props excellent; loses the gain because the
  teal/rust-red roof repaint did not reach these huts -- still monochrome.

ROUND5 SCORES: elf 8, harbour 8.5, rusty 7.5

## VERDICT (elf valley alone)
NOT YET -- but only just. Fixes 1-4 above (all cheap, ~30 min total: delete the
clipping slab, widen the fall, push grass dapple, add mist+stream) would take the
elf valley to a clean SHIP. As-is, the camera-clipping translucent canopy slab
and the thread-thin waterfall are too visible to ship the valley's hero views.
