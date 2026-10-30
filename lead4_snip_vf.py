def _stack2_post(A):
    G.spire(A, random.Random(5), 7.0, 52.0, [OP['rock'], OP['dark'], OP['rock2']], -13.0, 3.0, 6.0, 10, -0.1, None)


def _gate_post(A):
    for k in range(4):
        A.chunk((8.0 - k * 0.9, 9.0, 5.2), (16.0 + k * 1.1, 0.0, 36.5 + k * 4.4), OP['sand2'] if k % 2 else OP['sand'], (0, 0, 4 * k), 0.08, random.Random(40 + k), (0.95, 0.95))


def _old_oak2():
    reset()
    A = Acc()
    rnd = random.Random(2005)
    G.tree(A, rnd, 38.0, 12.0, ORIG.TKD, 'oak', 0, 0, 0, 1.0, True)
    return _fin(A, 'tree_oak_dead')


def co02_01():
    return LK.wrap(lambda: ORIG._stack(1), recolor=[LK.ramp([OP['moss']], [OP['rock2']])])()


def co02_02():
    return LK.wrap(lambda: ORIG._stack(2), post=_stack2_post, recolor=[LK.ramp([OP['moss']], [OP['sandl']]),
                                                                        LK.ramp([OP['rock'], OP['dark'], OP['rock2']], [OP['sand2'], OP['sand'], OP['sandl']], trange=(0.0, 80.0), wobble=0.05)])()


def co02_03():
    return LK.wrap(lambda: ORIG._stack(3), recolor=[LK.ramp([OP['moss']], [OP['rock2']]),
                                                     LK.ramp([OP['rock'], OP['dark'], OP['rock2']], [OP['rock2'], OP['red'], OP['sand2'], OP['rock2']], trange=(0.0, 80.0), wobble=0.05)])()


def lm25_01():
    return LK.wrap(ORIG.ancient_gate, post=_gate_post, prune=[dict(keys=None, max_size=6.5, max_z=2.0)])()


def vg02_02():
    return LK.wrap(_old_oak2)()


# --- lead4 registration ---
import v5_leadkit as LK
BATCHES['lead4_vf'] = ('v5_coast', mk([('CO02_01_sea_stack_01', co02_01), ('CO02_02_sea_stack_02', co02_02), ('CO02_03_sea_stack_03', co02_03)], 0.1))
BATCHES['lead4_vf_land'] = ('v5_landmarks', mk([('LM25_01_ruin_gate_hero', lm25_01)], 0.1))
BATCHES['lead4_vf_forest'] = ('v5_forest', mk([('VG02_02_tree_old_oak_02', vg02_02)], 0.1))
