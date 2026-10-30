# Concept map 2: what I understand and what it changes

Picture: `plan_v5\concept_map_2.png`, pasted by the user on 30 Oct 2026 at 22:57. North is up. Its side panel says "Same map. More depth." It is a layout and mood reference, not a survey, so places are mapped by relative position on our island. We take the layout only: no clover emblem, no Black Clover title or names in the game.

## 1. Places in the picture, north to south
| Place | Where in the picture | In our plan now | What changes |
|---|---|---|---|
| Waterfall Cave | north, behind a tall waterfall cliff | nothing | NEW: waterfall and a cave behind it |
| Castle Town | north centre, castle on a rise in a round red-roof city with a moat | v5_capital, oval wall, keep CP09 and CP10 | make the ring round with a river moat, keep the keep |
| Wizard Tower | north, just east of the waterfall cliff | on the Roof Plateau (1380,-1320) | DECISION (default: follow the picture) |
| Frosthold Fortress | north-east snow mountains | LM03 fortress, LM04 and LM05 | none |
| Roof Plateau | west foot of the snow mountains | plateau and WT13 terraces | none (the tower may leave it) |
| Hidden Monastery | east side of the snow | HM09 monastery outposts | none |
| Mountain Pass | north-east: bridges, cliffs, tunnels | roads_v5: 12 bridges, 3 tunnels; HM01 and HM02 bridges, HM03 and HM04 tunnels, LM08 span bridge | add cliff bridges where roads cross gorges |
| The Elden Tree and Forest Bridge | north-west forest | elf plan | add a natural stone bridge nearby |
| Elf Valley | west | v5_elf | none |
| Watcher's Peak | west coast cliffs | nothing | NEW: rock spire with a lookout |
| The Ruins | east of the castle, west of Skull City | LM25 to LM31 ruin sets, VC03 | none |
| The Skull City | east: dark ground, giant skull, lava | VC02 skull cliff, VC04 buildings, TW03 avenue | lava is red paint only, no glow |
| Crystal Lake | centre | nothing (terrain only) | NEW: lake basin, rim rocks, crystals (no glow) |
| Greenheart Plains | south-west centre: fields and a windmill | PL set | add a windmill |
| Harbour City | south-west coast | HB01 harbour towers, CP18 quay walls (partial) | MOVE from the south centre, add piers, boats, lighthouse |
| Sands of Elysium | south-east desert with sandstone mesas | DS and SD sets | add more mesas |
| Ancient Grove | south, forested peninsula | nothing | NEW |
| Coastal caves, Sunken ruins | coast (panel only) | FR03 cave mouths, CO04 sea arches, CO05 ruin islets | reuse, add a few |
| The Crater with cave | panel only, not drawn | LM18 to LM20 crater set | add a cave |
| Town 1 | not named | centre, zone x +-318, z -545..311 | keep (ask) |

## 2. Terrain the picture asks for
- A tall waterfall cliff just north of Castle Town. A river runs from its basin through the castle moat, on to Crystal Lake in the centre, and out to the south coast.
- A glacial lake in the north-east snow, a lake basin in the centre, small ponds between.
- Much more height: cliffs, plateaus and layered terraces. The north-east range is the highest, the west coast is cliffs.
- Black volcanic ground around the skull. Lava is red paint on rock, no glow.
- Sandstone mesas in the south-east desert.
- A forested peninsula in the south and small islands around the coast.
- No hard biome borders: forest runs into hills, snow into rock, desert into scrub over 100 studs or more. Our current terrain data has hard patches, so it needs blend zones.

## 3. Stand-in rules (user, 22:57: free models, placeholders or downloads are fine for now, with a list)
1. Our 404 Blender models first.
2. Block placeholders next: named, coloured by type, anchored.
3. Free Roblox Creator Store models: insert, delete every Script, LocalScript and ModuleScript inside (free models can hide backdoors), keep parts anchored, then log the asset id, name, creator and place of use as a new row in `STANDIN_LIST.csv`.
4. Web downloads: CC0 only (Poly Haven, Poly Pizza CC0, Kenney). Log URL and licence. Nothing under CC-BY goes in without the user's OK. These go through Blender, so they wait until memory is free.
5. No Neon, no emissive, no glowing particles. Standing rule.
6. Every stand-in is temporary and has a Blender model to replace it in the list.

## 4. The list
`plan_v5\STANDIN_LIST.csv` has one row per gap: what we have, what is missing, the stand-in for now, and the Blender model to make later. If every gap gets a real model that is about 40 new models (rough, plus or minus 2x). Nothing is placed or downloaded yet, so every row says "planned".

## 5. Questions for the user (my default in brackets)
1. Wizard Tower: north of the castle by the waterfall as in the picture, or on the Roof Plateau as in the old plan? (picture)
2. Harbour City on the south-west coast, not the south centre? (yes)
3. Castle Town ring round with a river moat, not oval? (yes)
4. Town 1 stays in the centre? (yes)
5. Keep no glow even for the lava, the Elden Tree and the crystal water? (yes, colour only)
6. Upload the finished 404 models: tonight or tomorrow? (key and creator id are set, Blender is closed)

## 6. Tomorrow, in order
1. The user answers the questions above.
2. Studio: File > Save to File as a local backup. The world exists only as the Roblox cloud save of 06:05.
3. Upload the finished models (canary of 3 first).
4. Terrain pass with the new landforms and blend zones.
5. Place models from the plans, then stand-ins from the list, then the wizard tower.
6. Photo rounds: the lead looks at them, the user reviews.
