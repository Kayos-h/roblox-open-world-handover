"""v5 worker module TEMPLATE. Copy to library/src/v5_<worker>.py and implement the builders.
Contract (same as v4, see v4worker.py): run through v4run.ps1 -Module v5_<worker> -Worker v<x> -Batch <batch>.
  BATCHES = {'batch': ('category_folder', [(manifest_id, builder_fn), ...])}
  builder_fn() takes no argument, calls reset(), builds with kitlib primitives, returns finalize('name', smooth_angle=25).
Units: 1 Blender unit = 1 stud, Z up, front faces -Y, pivot = centre of footprint at z=0. Palette keys start with the worker prefix, emission 0.
Read library/V5_STYLE_GUIDE.md and plan_v5/V5_BRIEFS.md for the rows you build. Use v4_wa_ice.py / v4_we_castle.py as examples.
"""
import math, random
import kitlib
from kitlib import (reset, finalize, box, cyl, ball, lathe, tube, torus, poly_prism)
from arch import F, faces, lbox, lbeam, beam3, slab, lslab, nm
from nature import blob, rock
import v4util

PAL = kitlib.PAL
PAL['vx_stone'] = ((150, 142, 158), 'Slate', 0.00, 0.90, 0)     # key: ((r,g,b), RobloxMaterial, metallic, roughness, emission)
PAL['vx_roof'] = ((198, 88, 52), 'Brick', 0.00, 0.85, 0)


def example_block():
    """ZZ_V5_TEMPLATE - a small house shape to prove the pipeline end to end. Delete when real builders exist."""
    reset()
    box(nm('body'), (10, 8, 6), loc=(0, 0, 3), key='vx_stone', bev=0.2)
    box(nm('roof'), (11, 9, 1.2), loc=(0, 0, 6.6), key='vx_roof', bev=0.2)
    return finalize('v5_template_block', smooth_angle=25)


BATCHES = {
    'selftest': ('v4_test', [('ZZ_V5_TEMPLATE', example_block)]),
}
