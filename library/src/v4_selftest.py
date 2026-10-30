"""v4_selftest - tiny two-colour model used only to prove the headless worker pipeline end to end."""
from kitlib import reset, finalize, box, cyl, ball
import kitlib

kitlib.PAL['zz_test_key'] = ((200, 60, 60), 'SmoothPlastic', 0.0, 0.6, 0)


def toy():
    reset()
    box('b', (6, 6, 4), loc=(0, 0, 2), key='stone', bev=0.1)
    cyl('c', 2.0, 5, loc=(0, 0, 4), key='zz_test_key', verts=16)
    ball('s', 1.2, loc=(0, 0, 9.6), key='gold', segs=12, rings=8)
    return finalize('zz_toy', smooth_angle=35)


BATCHES = {'selftest': ('v4_test', [('ZZ_01_toy', toy)])}
