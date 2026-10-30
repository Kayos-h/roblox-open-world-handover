def _curved_post(A):
    R = 24.0
    for a0, a1 in ((-2.0, 0.0), (90.0, 92.0)):
        A.sweep([(R - 6.4, 0.0), (R + 1.4, 0.0), (R + 1.4, 9.0), (R - 6.4, 9.0)], a0, a1, 2, P['stone_m'])
    A.sweep([(R - 6.8, 0.0), (R + 2.0, 0.0), (R + 2.0, 0.8), (R - 6.8, 0.8)], -2, 92, 18, P['stone_d'])


def wt13_01():
    return LK.wrap(terrace_wall_straight, prune=[dict(keys=[P['joint']], max_size=30.0)])()


def wt13_02():
    return LK.wrap(terrace_wall_curved, post=_curved_post)()


def wt13_03():
    return LK.wrap(terrace_stair, recolor=[LK.ramp([P['throat']], [P['stone_d']])])()


# --- lead4 registration ---
import v5_leadkit as LK
BATCHES['lead4_va'] = ('v5_wizard', mk([('WT13_01_plateau_terrace_set_01', wt13_01), ('WT13_02_plateau_terrace_set_02', wt13_02), ('WT13_03_plateau_terrace_set_03', wt13_03)], 0.1))
