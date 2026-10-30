# Review r3 — Towns B (Elf Village, Harbour, Rusty Desert Town)

Unavailable this session: `@Roblox_Studio` MCP (not configured). Review done from the photos only; no Studio tool used.

## ELF VILLAGE — 5.5/10 (the user's priority; ~60% of this review)

The rebuild is a real, recognisable settlement, not scattered props — treehouses cluster, rope bridges link them, ladders drop to the ground, there is a palace, a pavilion and two pools, and critically **there is NO glow, no neon, no light beams, no particles and no blue/green emissive look anywhere.** That hard requirement is met. But the valley reads dark and cold, the world tree is a silhouette rather than a landmark, and the top-down view still feels under-populated for the "city between the valleys" the user asked for.

**Special checks answered:**
1. **Glow/neon/beams/particles/emissive?** None. Clean natural look — requirement satisfied. The moon pool (t09, bottom-left of tree at ~(-1600,-480)) is plain water, not the glowing cyan it once was. Keep it this way.
2. **City vs scattered props?** Reads as a village. Clear clusters (west cluster t12, east of tree t09), paths radiating from the tree, bridges tree-to-tree, ladders to ground (t11/t12). It passes — but it is a loose village, not yet a *city*; the centre around the world tree is mostly empty lawn.
3. **Scale & density:** Too empty in the core. The huge lawn ring around the world tree (t09, ~150-stud radius) is bare green with only a few scattered bushes. Treehouse models repeat with little variation (t12 shows ~3 identical round huts). Outer valley is fine; the heart is thin.
4. **World tree & waterfall:** Underwhelming as a landmark. In t09/t11 the trunk is a near-black flat brown silhouette with no bark texture, lit from behind so it reads as a dead black column, not a glowing-with-life world tree. The canopy is a single flat green blob. No waterfall is visible in any of the four shots — the brief expects a waterfall at the tree; if it exists it is hidden or off-frame, which is itself a landmark failure.
5. **Terrain integration:** Mostly good — treehouses sit on real trunks, the stream in t12 is cut into the ground naturally. BUT: the moon-pool pavilion and both pools in t09 have hard geometric rims (the round pool bottom-left, the kidney pool right of tree); the central dirt paths in t09 are hard-edged tan strips painted on grass with no blend. The palace plaza (t10) sits on a visible flat pad. No floating buildings seen.
6. **Too dark?** YES — confirmed and it is the single biggest problem. t09, t11 and t12 are markedly darker and more desaturated than harbour/rusty (mean ~70 vs ~120). The tree casts a huge black shadow across the whole valley floor (t09), the trunk is crushed to near-black, and the surrounding mountains are cold grey-blue. The valley looks like dusk while the rest of the island looks like noon. This kills the "lush saturated" target and makes the whole area feel unfinished.

### BUGS (elf)
- **World-tree trunk crushed to black**, ~(-1560,-430). Flat dark-brown faces, no bark material, reads as a dead/burnt column (t09, t11).
- **Valley-wide black shadow**, floor around ~(-1560 to -1400, -430 to -250). The tree's shadow blankets the core lawn; combined with low ambient the whole basin is in gloom (t09).
- **Hard circular pool rim**, round pool at ~(-1680,-520) (t09 bottom-left) — sharp geometric edge, no reed/fern/moss blend despite the brief claiming rims were added.
- **Hard-edged dirt paths** radiating from tree (t09) — tan strips laid on grass with no transition.
- **Palace on a flat pad**, ~(-1470,-655) (t10) — paved plaza edge is a hard step against the grass.
- Possible **missing/off-frame waterfall** at the world tree — not visible in any shot.

### KEEP (elf)
- No glow / no emissive anywhere — exactly as the user demanded. Do not re-add any.
- Treehouse-on-real-trunk construction with railings, ladders and rope bridges (t11/t12) — genuinely good and readable.
- The cut-in stream with the little arched footbridge (t12 foreground) — natural and charming.
- Round-house silhouettes and shingle roofs (t12) — right fantasy vocabulary.

### 8 most valuable elf fixes (ranked)
1. **Lift valley brightness.** Raise ambient/exposure for the basin or reduce shadow density so mean brightness goes from ~70 toward ~110. Cheap lighting/colour edit — biggest single payoff.
2. **Re-skin the world-tree trunk.** Apply a warm lit bark texture (base ~ (92,58,34)) and a second lighter highlight material; split the canopy into 3-4 overlapping clusters instead of one blob. Landmark-defining. ~(-1560,-430).
3. **Add the waterfall.** A 2-3 tier cascade down the mountain face at ~(-1680,-430) feeding the stream, with foam at the base. Expensive-ish (terrain + water) but it is the signature feature and is currently absent.
4. **Fill the core lawn.** Add ~40 ferns, ~25 flower beds, 6-8 mushroom rings and 5 market stalls in the 150-stud ring around the tree, ~(-1560,-430) to ~(-1420,-350). Cheap object scatter; turns empty lawn into a plaza.
5. **Vary the treehouses.** Swap ~1/3 of repeated round huts for taller/wider variants and re-rotate them; retexture roofs in 3 shingle tints. ~(-1720 to -1840, -430 to -540). Cheap.
6. **Soften both pool rims.** Ring the round pool (-1680,-520) and the kidney pool (-1500,-480) with reeds/ferns/moss and feather the terrain edge; remove the hard circular geometry.
7. **Blend the dirt paths.** Replace hard tan strips with a 2-stud grass-to-dirt transition and slight width jitter (t09 radials).
8. **Dress the palace plaza.** Feather the pad edge into grass, add banners, 4 braziers (UNLIT — no glow), benches and planters around ~(-1470,-655) so it reads as a seat of power, not a slab.

---

## HARBOUR — 7.5/10
Strong and convincing. Tudor/timber houses cluster densely up the hillside with good roof-colour variety (navy, red, slate), the inland lawn is now full of trees and beds (t14) so the old emptiness is gone, the beach has clutter, buoys and a nice two-ring surf foam line (t13), and the sea reads the right teal. A plaza with benches and lampposts (t14) gives it a town centre. Best area in my set. Minor: a couple of houses on the slope (t13 right edge) may clip the terrain, and the grass is a loud flat green against the muted buildings.

**3 cheapest harbour fixes:**
1. Desaturate the lawn grass ~10% and add tonal variation so it stops fighting the buildings (t13/t14). Colour edit.
2. Add a cobbled/paved square texture under the plaza at ~(-420,1560) instead of bare grass (t14 centre). Cheap.
3. Check and re-seat the 2-3 slope houses on the right of t13 (~(-260,1760)) that appear to clip the hillside. Cheap object move.

## RUSTY DESERT TOWN — 7/10
The upgrade worked. The proper V4 rusty huts (t16) — stone-and-timber with corrugated rust-metal roofs — are a huge step up from the old hollow placeholders and read as a real frontier settlement. The church is now ochre sandstone (t15/t16) and sits well as the landmark, and the 190 floor props (rocks, dead/acacia trees, tents, carts, debris) genuinely dress the desert floor. The banded mesas behind are strong. Issues: the floor is one uniform flat tan with no sand-colour variation or dunes, so it looks like a painted plane; the church's window glass is a flat bright green (t15/t16) that clashes with the ochre and is the one "fake" note; and prop scatter thins out fast away from the church, leaving bald sand.

**3 cheapest rusty fixes:**
1. Recolour the church window glass from bright green to a warm amber/stained tone to match the ochre (t15/t16). One colour edit, removes the only jarring note.
2. Add sand-tone variation / faint dune ripples and a few darker patches to the flat floor so it stops reading as a flat plane (t15). Cheap paint/terrain-colour edit.
3. Scatter ~30 more rocks + dead trees + debris into the bald mid-ground between church and mesas, ~(1450,1250), to extend the dressing outward (t15). Cheap object scatter.

---
**Player verdict:** A typical Roblox player rates this set ~7/10 today — harbour and rusty sell it, the elf valley drags it down. The single change that raises it most: **brighten the elf valley and re-light/re-skin the world tree** so the priority area stops looking like dusk and the landmark actually reads as a world tree.
