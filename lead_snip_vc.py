PBR = G.reg('vc_f', {
    'bronze': ((128, 96, 62), 'Metal', 0.3, 0.72),
    'rock_b': ((118, 104, 92), 'Slate', 0.0, 0.93),
    'rock_c': ((146, 128, 108), 'Cobblestone', 0.0, 0.92),
})
WARM = [P['rock_d'], PBR['rock_b'], PBR['rock_c'], P['rock_w'], P['rock_l']]


def _portal2():
    """HM03_02 (round 3, lead) - snow-capped tunnel portal: copy of ORIG._portal(2) with warm banded rock (not plain grey), NO icicles (the thin hanging cones rendered as black
    stripes across the opening), thicker snow caps that sink into the rock instead of lying on it as flat white slabs."""
    reset()
    A = Acc()
    rnd = random.Random(12)
    W, D, H, ow, oh = 30.0, 17.0, 24.0, 14.0, 16.0
    for sg in (-1, 1):
        for k in range(8):
            A.chunk((rnd.uniform(7.0, 8.4), D * rnd.uniform(0.85, 1.0), 3.4), (sg * (11.2 + rnd.uniform(-0.3, 0.4)), rnd.uniform(-0.8, 0.8), 1.6 + 3.0 * k),
                    band(WARM, k / 8.0, rnd), (0, 0, 0), 0.1, rnd, (0.94, 0.96))
    for k in range(6):
        A.chunk((5.8, D * rnd.uniform(0.9, 1.0), 7.4), (-12.5 + k * 5.0, rnd.uniform(-0.6, 0.6), oh + 4.3 + rnd.uniform(-0.2, 0.4)),
                band(WARM, 0.55 + 0.1 * (k % 3), rnd), (0, 0, 0), 0.08, rnd, (0.95, 0.95))
    A.box((ow, D, 0.4), (0, 0, 0.2), VC['slate'])
    for sg in (-1, 1):
        A.box((0.7, D, oh), (sg * (ow / 2 + 0.35), 0, oh / 2), VC['slate'])
    A.box((ow + 1.4, D, 0.8), (0, 0, oh + 0.4), VC['slate'])
    yf = -D / 2 + 0.3
    for sg in (-1, 1):
        A.box((1.5, 1.5, oh + 0.4), (sg * (ow / 2 + 0.75), yf, (oh + 0.4) / 2), VC['timber'])
        A.beam((sg * (ow / 2 + 0.75), yf - 0.2, oh - 3.6), (sg * (ow / 2 - 2.6), yf - 0.2, oh), 0.6, 0.6, VC['timber'])
    A.box((ow + 3.4, 1.7, 1.7), (0, yf, oh + 0.85), VC['timber'])
    for k in range(6):
        A.chunk((5.9, D * 0.92, 2.6), (-12.5 + k * 5.0, 0, H - 0.4), VC['snow'], (0, rnd.uniform(-3, 3), 0), 0.12, rnd, (0.9, 0.9))
    for sg in (-1, 1):
        A.chunk((7.4, D * 0.88, 2.2), (sg * 11.2, 0, 13.4), VC['snow'], (0, 0, 0), 0.12, rnd, (0.9, 0.9))
    v4util.marker('mk_door', (0, -D / 2, 0.3))
    A.to_scene()
    return finalize('tunnel_portal', 25)


def _shrine3():
    """HM08_03 (round 3, lead) - prayer-wheel shrine: four red corner posts joined by tie beams under the roof, a hub block between the wheel and the roof (the old roof sat on two
    thin posts with a wide gap to the drum and looked like it floated), dull bronze bands instead of bright gold."""
    reset()
    A = Acc()
    A.chunk((9.4, 9.4, 1.0), (0, 0, 0.5), VC['stone2'], jit=0.03, rnd=random.Random(103))
    for sx in (-3.6, 3.6):
        for sy in (-3.6, 3.6):
            A.box((0.8, 0.8, 7.4), (sx, sy, 4.7), VC['red'])
    for sx in (-3.6, 3.6):
        A.box((0.6, 7.6, 0.6), (sx, 0, 7.0), VC['red'])
    for sy in (-3.6, 3.6):
        A.box((7.6, 0.6, 0.6), (0, sy, 7.0), VC['red'])
    A.cyl(2.4, 5.0, (0, 0, 1.5), VC['red'], verts=16)
    for z in (1.7, 5.9):
        A.sweep([(2.3, 0.0), (2.65, 0.0), (2.65, 0.6), (2.3, 0.6)], 0, 360, 16, PBR['bronze'], loc=(0, 0, z))
    A.cyl(0.35, 9.0, (0, 0, 1.2), PBR['bronze'], verts=6)
    A.box((2.6, 2.6, 1.8), (0, 0, 7.4), VC['stone'])
    A.box((7.2, 0.6, 0.5), (0, 0, 7.4), VC['timber'])
    A.box((0.6, 7.2, 0.5), (0, 0, 7.4), VC['timber'])
    A.gable(9.4, 8.6, 2.6, (0, 0, 8.2), VC['slate'], (0, 0, 90))
    for k in range(8):
        x, y, _ = polar(2.45, k * 45.0)
        A.box((0.12, 0.5, 2.4), (x, y, 4.0), PBR['bronze'], (0, 0, k * 45.0))
    A.to_scene()
    return v5kit.fit(finalize('cairn_shrine', 25), w=12.8, d=12.0, h=12.4)


# --- lead3 registration ---
BATCHES['lead3'] = ('v5_himalaya', mk([('HM03_02_tunnel_portal_02', _portal2), ('HM08_03_cairn_shrine_03', _shrine3)], 0.1))
