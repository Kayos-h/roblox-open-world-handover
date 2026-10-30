# Round 3 review — TERRAIN & ENVIRONMENT (whole island)

Unavailable this session: `@Roblox_Studio` MCP server (declared but not configured). Review done from photos only, as the brief requires.

## Special checks (answered directly)
1. **Sea gradient & foam.** Partly. g02/g05 show a believable turquoise-to-blue tone and there IS a shallow sand band around land. But there is almost NO navy "deep" — open water (g02, h00 edges) stays one bright cyan the whole way out. It reads as a shallow pool, not a deep-teal-to-navy sea like the reference. Foam is the worst offender: the rings are **hard geometric white polygon strips** (g01 islet, g05 islet) with straight cut edges and corners — clearly artificial outlines, not soft surf. The reference surf is a soft feathered ring; these look like someone traced the coast in white tape.
2. **Floating / torn geometry — NOT clean, failures remain.** g05 (and g01 corner, g04 right) show **rooted islets that FLOAT**: a rock disc hovers with open water visible *beneath* it, its sand shoal sitting lower and detached. This is exactly the "floating plate" class the patch claimed to fix — it is still present on the outer islets (~ (469,5,2359) and the two east of it near (700,5,2350)). So I cannot say "none"; the main-island seabed looks fixed but the ringed islets do not.
3. **Horizon seam.** Yes — a hard dark line where ocean meets sky on every fog-off high shot (h02/h03/h04 left edges, g03, g11). The ocean plane ends in a crisp straight edge against the skybox. Expected with fog off, but it is a clean rectangle edge, so the sea plane is finite/too small.
4. **Road network legibility from above.** Weak. In h00 I can read the capital grid and the main capital→Town1 avenue, and faint tan threads near Town1, but the dense branching tan web of the reference (every settlement linked) is largely invisible — roads are too thin/overgrown and low-contrast against grass. h01 is a little better but still sparse.
5. **Snow range & badlands.** Snow range (NE): convincing and the best terrain on the map — real relief, layered snow, crags, a natural snowline (g10, g11, h03). Badlands (SE): the mesas read as badlands but are **over-regular** — g12 shows ~identical round layer-cake buttes repeated like stamps; real mesas vary in width/height/tilt. Good from distance (h00), cartoonish up close.
6. **Forest.** Still mostly uniform "broccoli". g06 is pure identical round-blob canopy; g03/g09 add some pines and a few orange trees for break-up but the dominant tree is one repeated bright-green ball. Needs more species, size variance and darker value clumps.
7. **Top-down vs reference (h00).** ~5.5/10 match. Right: silhouette shape, biome placement (snow NE, badlands SE, capital N, Town1 centre, harbour S), colour zones. Wrong: sea far too pale/flat, foam fake, road web missing, forest too uniform/bright, islets floating, no visible rivers threading as in reference. Five changes to close the gap are in the FIX list (#1–5).

## Scores
- **Sea & shoreline — 4/10.** Shallow band is okay; deep water never goes navy, and the foam rings are hard white polygons. Islets float. Biggest single drag on realism.
- **Terrain landforms — 7/10.** Snow massif and west crags (g03/g11) are genuinely good; relief, snowline and rock faces convince. Badlands shape is right but repetitive. Main landmass reads solid, no tears seen on it.
- **Forest / vegetation — 5/10.** Dense and lush from afar (h04), but near-field is repeated broccoli blobs and over-saturated green. Pines and autumn trees help but are sparse.
- **Rivers & lakes — 5/10.** Silverrun (g07) and the NE river (h03 blue thread) are nice ribbons; twin lakes (g08) read. But water is flat bright-blue with no depth shading, and the river channels are narrow slots that look cut, not carved.
- **Readability from above — 5/10.** Biomes legible; road network and river web are not. A player map-screen would look under-connected.

## BUGS (with approx world positions)
- **Floating rooted islet**, rock disc hovering above its shoal, water visible under it — g05 centre, ~ **(469, 5, 2359)**; two more similar islets just E/NE near **(700, 10, 2360)** and **(820, 10, 2330)**. Same class in g01 fore-islet ~ **(300, 5, 1900)** and g04 right islet ~ **(2900, 5, -1350)**.
- **Hard polygon foam rings** (artificial white outline, straight edges/corners) around every islet and shoreline — visible g01, g05, g02; global.
- **Finite ocean plane / hard horizon seam** — straight dark sea edge on h02/h03/h04, g03, g11; the sea plane does not extend to the skybox.
- **Over-pale flat open sea** — single cyan tone with no navy, g02 / h00 outer ring; not a crash bug but reads broken against the reference.
- **Repeated identical mesas** (stamped look) — g12, badlands field centred ~ **(1500–2100, 30, 900–1100)**.
- No black voids, no z-fighting, and no tears on the main island were seen (good). Faint low-poly facet banding on far snow slopes (h03) is minor.

## KEEP (do not change)
- The NE snow massif: relief, snowline, crags, waterfall and alpine village nestled below (g10, g11, h03). Best area on the map.
- West coast craggy rock towers and the stone arch (g03, g11) — strong silhouette, matches reference intent.
- Overall island silhouette and biome layout — reads correctly from h00 against the reference.
- Silverrun river ribbon and its rocky banks (g07); twin-lakes shapes (g08).
- Badlands striped buttes + ochre church cluster read well at mid distance (h00, h03 far).

## FIX LIST (ranked, highest payoff per effort first)
1. **Replace hard polygon foam with a soft feathered ring** — swap the white strip meshes for a thin alpha-gradient decal/texture band (fade 0→1 over ~6 studs, slight wobble). CHEAP (material/decal edit, no terrain). Biggest realism win.
2. **Add a real deep-water gradient** — darken open sea toward navy (e.g. shallow RGB ~ (40,150,180) → deep ~ (12,45,90)) via depth-based tint or a second darker water material past the shelf. MEDIUM (shader/material; no new terrain). Fixes the "pool not ocean" read.
3. **Re-ground the floating islets** — drop each hovering rock disc so its base meets the seabed and the shoal, or delete the gap voxels under them. CHEAP-MEDIUM per islet (terrain edit on ~5 islets at the positions above).
4. **Thicken & brighten the road web** — widen rural roads to ~12–14 studs, raise tan contrast vs grass, and actually connect harbour↔Town1↔capital↔rusty↔alpine as in the reference. MEDIUM (needs path regen/painting). Makes the top-down read like the target.
5. **Break up the forest** — mix 3–4 canopy shapes, vary tree scale ±30%, add darker-green and more autumn/pine clumps, reduce the single bright broccoli blob's dominance. CHEAP-MEDIUM (asset swap + scatter re-seed), no terrain.
6. **Extend the ocean plane to the skybox** (or add distance fog horizon blend even in "fog off" hero shots) to kill the straight sea-edge seam. CHEAP (resize water part / sky blend).
7. **Vary the badlands mesas** — randomize radius, height, tilt and layer count so no two cakes match; add a few collapsed/eroded ones. MEDIUM (regen or hand-vary 44 mesas).
8. **Deepen rivers/lakes with a depth tint** so Silverrun and twin lakes aren't flat cyan slots (darker centre, lighter edge). CHEAP (water material).
9. **Soften far snow-slope faceting** — one more voxel smoothing pass on distant alpine faces (h03). MEDIUM (terrain).
10. **Add visible river threads from above** — widen/brighten the NE river and any main watercourses so they read in h00 like the reference's blue veins. MEDIUM.
11. **Reduce overall grass saturation ~10%** toward the reference's slightly muted lush green; current green is a touch neon in g06/g09. CHEAP (colour).
12. **Add scattered deep-sea rocks/reefs and tonal variation** in the empty open water so it isn't a dead flat sheet. CHEAP (prop scatter).

Terrain-generation (expensive): #3 (partly), #4, #7, #9, #10. Cheap object/colour/material edits: #1, #2, #5, #6, #8, #11, #12.

## Player verdict
A typical Roblox player would give this map about **6/10** today — impressive scale and a great snow mountain, but the fake white foam rings and flat pale sea instantly cheapen it. The single highest-impact change is **Fix #1 (soft feathered foam) + #2 (deep-water gradient)** — making the sea look like a real ocean would lift the whole island a full point.
