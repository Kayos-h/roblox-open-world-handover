# Phase 1 map rebuild report (29 Oct, 02:45-04:00)

Every change was checked by moving the Studio camera and looking at real window pictures (`shots\final`, `shots\o`, `shots\c`, `shots\en`).

## What changed
- **The old overnight build was archived, not deleted.** It's in `ServerStorage.Phase1Archive_v1`. Town 1 and its additions were kept.
- **New terrain for the whole island.** It was generated in 56 seconds by `rebuild\terrain_gen.luau` from `rebuild\world.py`:
  - natural rolling land with an irregular coastline, beaches, rocky headlands and sea stacks
  - forested hills in the north-west, dry badlands with mesas in the south-east
  - Town 1's river continues outside the walls into two lakes
  - all roads are curved cobblestone (dirt for the two ring roads) with smooth banks
  - no more square cliffs or mud stripes
- **The roads**: Town 1 north to the capital, east to the alpine village, west to the elf city, south to the harbour, and south-east to the rusty town. A dirt ring road runs on each side.

## Areas
| Area | What it is now |
|---|---|
| Royal capital | Walled city, 1,400 x 1,000 studs: grand gate, paved avenue with double lamps, 4 cross streets and 2 lanes lined with houses and shops, gate square, market square (fountain, 9 stalls, carts, bunting), cathedral square, upper plaza, noble mansions, gardens inside the blocks. A switchback road climbs to the castle on the sea cliff: curtain walls, towers, gatehouse, keep, spires, courtyard, royal gardens. |
| Alpine village | **Moved into the tower mountain** as you asked: a shelf cut into its south-east side at height 115, with the summit (the tower site) above it. A mountain road climbs from the plains. Chalets, square with a well, stone chapel, sawmill and pond, barn and goat pen, watchtower, snowy pines. |
| Rusty town | Crooked dirt main street ending at the church, two lanes, tavern square, water tower, blacksmith, windmill, tents, junk, dead trees, cracked dry ground, fenced graveyard. |
| Harbour | Town on a slope down to the quay, 3 piers, galleon, merchant ship, fishing boats, warehouses, cranes, market stalls, lighthouse and fort on rocky headlands. |
| Elf city | World tree centre, glowing stone paths, 7 treehouses, palace, moon pool, lake with waterfall cliff, dense jungle trees, ferns and glowing mushrooms. |
| Countryside | 4 farms (fields, fences, windmills, hay), forests by biome, groves, ruins, stone circles, watchtowers, shrines, campsites, wagon wrecks, region arches on every road, signposts, milestones, rustic lamps near the gates, coastal rocks, reeds and lily pads. |

## Enterable buildings (built from parts, furnished with my models)
| Town | Building | Inside |
|---|---|---|
| Rusty town | **Big church**: 60 x 124 nave, 104-stud tower with spire, stained glass, buttresses, apse, rusted metal roof | Pews, red carpet, pillars, chandeliers, altar, organ, pulpit, candle stands, broken barrels |
| Capital | Grand cathedral (white marble, blue roof), on the cathedral square | Same as the church, plus candelabras and tapestries |
| Harbour | Tavern by the quay | Bar, barrels, tables, stools, fireplace, ship bell, anchor |
| Alpine | Log lodge on the square | Tables, chairs, fireplace, firewood, sled |
| Elf | Moon shrine, a ring of glowing columns | Crystal, pool, benches, glowing flowers |
| Town 1 | Its existing interiors (blacksmith, chapel, guild hall) | unchanged |

## Town 1 fixes
- The skull HQ now **faces the plaza**. It was facing north. It's scaled to 62% (164 studs tall instead of 265), coloured bone, and has a stone court under it.
- The brown bald hilltops inside the walls are now grass.
- The terrain outside the walls has been rebuilt, which removed the mud trenches, the hole by the north wall and the ridge.

## Decisions I made
- I archived the old build instead of fixing it. The terrain shapes were the main problem, and every area depended on them.
- I chose a shelf on the mountain's south-east side for the alpine village. That keeps the summit free for the magic tower and gives the village a cliff behind it and a sea view.
- I used terrain cobblestone for the roads instead of road-piece models. It follows curves and slopes without gaps.
- I built the enterable buildings from parts, because every Blender building model is a solid box inside.
- The Town 1 river level is -3, below sea level, so it can't join the sea. It flows into two inland lakes instead.
- I made the haze lighter (Atmosphere Density 0.24, Haze 0.7) so distant towns are visible.

## Numbers
- Phase1Map: 58,942 parts plus Town 1's 19,793. All are anchored (0 unanchored). There are 2,241 lights.
- StreamingEnabled is on. The capital alone is 23,500 parts, which may be heavy on phones.

## Open issues
1. **The place is not saved.** The Studio tab still says "Untitled Experience". Use File, then Save to Roblox.
2. I didn't run a Play test this session. Everything is anchored, but nobody has walked it yet.
3. The cliff behind the alpine village is the old low-poly mountain and looks flat and striped up close.
4. The capital's grid layout is regular, and the houses repeat. See BLENDER_NEEDS.md.
5. The cracked dry ground in the rusty town looks blotchy from high above. It's fine at ground level.
6. Things Blender can't make, which are still missing: animals, NPCs, skybox, sounds.
