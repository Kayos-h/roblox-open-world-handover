# Model review brief (independent reviewer for Blender batches)

You see contact sheets (4 views per model) from `library/v4_sheets/` and the metadata lines below each. Judge only what you see. Do not read the builder code.

For every model give: id, score 1-10 on SILHOUETTE (reads at 500 studs), FORM (three scales of detail), MATERIALS (palette fits the place, no grey default), SCALE and PROPORTION (matches the manifest size, a 5-stud player fits doors), CONSTRUCTION (believable structure, ladders or stairs on raised floors, no floating bits), ORIGINALITY (does not copy a known franchise design), then a verdict `KEEP`, `FIX` (with the exact change) or `REBUILD`.

Rules that fail a model automatically: any glow or neon look, a freestanding plain entrance arch, floating geometry, inverted or missing faces, tri count over the budget, enterable building with walls thinner than 4 studs or openings narrower than 8 studs.

Extra for the wizard tower rows (WT01-WT13): also score EXTERIOR PRESENCE (does it look like the landmark of the island from far away), INTERIOR (walkable, headroom, stairs), BOOKSHELVES (floor-to-ceiling, packed books, curved to the wall), CIRCULAR MAP (reads as a relief map of an island, rings and landmark tokens, brass and stone). The tower needs 8 or more in every category. A single category under 8 means `FIX`.

End with `BATCH SCORE:` (mean), the list of ids to fix first, and at most five cheap changes that would raise the weakest scores.
