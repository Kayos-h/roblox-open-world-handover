def _rope3_post(A):
    half = 58.0
    zd = lambda x: 5.0 - 2.4 * (1.0 - (x / half) ** 2)
    x = -half
    while x < half - 0.1:
        x2 = min(half, x + 5.8)
        for y in (-3.45, 3.45):
            A.beam((x, y, zd(x) - 0.95), (x2, y, zd(x2) - 0.95), 0.95, 0.85, VC['timber'])
            A.beam((x, y, zd(x) + 1.95), (x2, y, zd(x2) + 1.95), 0.55, 0.5, VC['timber'])
        x = x2
    for xx in range(int(-half), int(half) + 1, 8):
        for y in (-3.45, 3.45):
            A.box((0.6, 0.6, 2.2), (xx, y, zd(xx) + 0.9), VC['timber'], bev=0.04)


def _flags1_post(A):
    for k, key in enumerate((VC['f_red'], VC['f_yellow'], VC['f_blue'])):
        A.box((1.5, 0.12, 0.7), (0.85, 0.0, 13.5 - k * 0.85), key, bev=0.02)


def _hall3_back(A):
    for r in range(2):
        for k in range(6):
            yb = 10.75 - r * 0.45
            A.box((2.2, 0.5, 3.0), (-11.0 + k * 4.4, yb, 5.4 + r * 10.0), VC['slate'])
            A.box((2.8, 0.5, 0.4), (-11.0 + k * 4.4, yb + 0.1, 7.1 + r * 10.0), VC['red'])
    A.box((4.0, 0.6, 6.0), (0, 10.95, 4.2), VC['timber'])
    for k in range(12):
        A.box((1.4, 0.7, 1.1), (-13.0 + k * 2.4, 10.5, 22.8), VC['white'])
    for st in range(3):
        A.box((8.0 - st * 1.6, 1.6, 0.4 * (st + 1)), (0, 12.2 - st * 1.0 + 0.0, 1.2 + 0.2 * (st + 1)), VC['stone'])


def _switch3_post(A):
    A.box((30.2, 5.0, 0.6), (0, 0, 7.45), P['rock_l'])
    A.box((30.4, 1.2, 0.3), (0, -2.65, 7.4), P['rock_m'], bev=0.05)
    for z in (2.1, 4.2):
        A.box((30.4, 0.5, 0.45), (0, -2.45, z), P['rock_l'], bev=0.04)
    A.box((29.0, 2.6, 0.15), (0, 0.4, 7.82), VC['stone2'])


RAMP_A = [PBR['rock_b'], PBR['rock_c'], P['rock_w'], P['rock_l']]
RAMP_B = [PBR['rock_b'], PBR['rock_c'], P['rock_w'], P['rock_l'], P['rock_w']]
RAMP_C = [PBR['rock_b'], P['rock_m'], PBR['rock_c'], P['rock_w']]
STONE3 = [VC['stone'], VC['stone2'], VC['slate']]


def hm01_03():
    return LK.wrap(ORIG.rope_bridge_3, post=_rope3_post)()


def hm02_01():
    return LK.wrap(ORIG.cantilever_1, recolor=[LK.ramp([VC['stone'], VC['stone2']], RAMP_A, zlim=(-1.0, 7.4), trange=(0.0, 7.0), wobble=0.08)])()


def hm02_02():
    return LK.wrap(ORIG.cantilever_2, recolor=[LK.ramp([VC['stone'], VC['stone2']], RAMP_C, zlim=(-1.0, 7.4), trange=(0.0, 7.0), wobble=0.08),
                                               LK.ramp([VC['slate']], [P['band_r']], zlim=(9.0, 30.0))])()


def hm03_01():
    return LK.wrap(ORIG.portal_1, recolor=[LK.ramp(STONE3, RAMP_A, trange=(0.0, 24.0), wobble=0.07)])()


def hm03_03():
    return LK.wrap(ORIG.portal_3, recolor=[LK.ramp(STONE3, RAMP_B, trange=(0.0, 24.0), wobble=0.07)])()


def hm06_03():
    return LK.wrap(lambda: _switchback(3), post=_switch3_post)()


def hm08_01():
    return LK.wrap(ORIG.shrine_1, post=_flags1_post, prune=[dict(keys=[VC['f_blue'], VC['f_white'], VC['f_red'], VC['f_green'], VC['f_yellow']], max_size=3.0)],
                   recolor=[LK.ramp(STONE3, RAMP_A, zlim=(-1.0, 11.5), trange=(0.0, 11.0), wobble=0.08)])()


def hm09_03():
    return LK.wrap(ORIG.outpost_3, post=_hall3_back)()


def ne01_03():
    return LK.wrap(ORIG.sign_3, recolor=[LK.ramp([VC['white']], [P['board']]), LK.ramp([VC['snow']], [P['rock_m']], zlim=(-1.0, 1.4))])()


def ne02_03():
    return LK.wrap(lambda: _boulders(3), recolor=[LK.ramp([P['rock_d']], [PBR['rock_b'], PBR['rock_c']], trange=(0.0, 14.0), wobble=0.1)])()


# --- lead4 registration ---
import v5_leadkit as LK
BATCHES['lead4'] = ('v5_himalaya', mk([('HM01_03_rope_suspension_bridge_03', hm01_03), ('HM02_01_timber_cantilever_bridge_01', hm02_01), ('HM02_02_timber_cantilever_bridge_02', hm02_02),
                                       ('HM03_01_tunnel_portal_01', hm03_01), ('HM03_03_tunnel_portal_03', hm03_03), ('HM04_02_tunnel_lining_02', lining_2),
                                       ('HM06_03_switchback_wall_03', hm06_03), ('HM08_01_cairn_shrine_01', hm08_01), ('HM09_03_monastery_outpost_03', hm09_03)], 0.1))
BATCHES['lead4_ent'] = ('v5_entrances', mk([('NE01_03_village_sign_03', ne01_03), ('NE02_03_entry_rock_pair_03', ne02_03)], 0.1))
