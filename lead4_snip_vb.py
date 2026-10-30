def _bay_post(R, chord, H=28.0):
    def post(A):
        half = math.degrees(chord / 2.0 / R)
        a0, a1 = 90.0 - half, 90.0 + half
        for q in range(7):
            ang = a0 + (a1 - a0) * q / 6.0
            x = (R + 0.25) * math.cos(math.radians(ang))
            y = -R + (R + 0.25) * math.sin(math.radians(ang))
            A.box((0.5, 0.8, H - 3.0), (x, y, H / 2.0), VB.K['ochre'], (0, 0, ang), bev=0.05)
        n = max(4, int((a1 - a0) / 4.0))
        for z in (6.0, 14.0, 22.0):
            A.sweep([(R + 0.1, z), (R + 0.6, z), (R + 0.6, z + 0.7), (R + 0.1, z + 0.7)], a0, a1, n, VB.K['limestone'], loc=(0, -R, 0))
    return post


def _shelf1_post(A):
    width, H, depth = 14.0, 26.0, 4.6
    A.box((width - 0.4, 0.4, H - 2.2), (0, depth / 2.0 + 0.2, H / 2.0 + 0.2), VB.K['timber'], bev=0.05)
    for k in range(5):
        A.box((0.5, 0.3, H - 4.5), (-width / 2.0 + 2.0 + k * (width - 4.0) / 4.0, depth / 2.0 + 0.55, H / 2.0), VB.K['ochre'], bev=0.04)
    A.box((width + 0.4, 0.8, 0.7), (0, depth / 2.0 + 0.4, H - 1.0), VB.K['limestone'], bev=0.05)


def _shelf2_post(A):
    width, H = 14.0, 26.0
    for sx in (-1, 1):
        A.box((1.4, 1.4, 1.6), (sx * (width / 2.0 - 0.8), 0, H + 0.8), VB.K['limestone'], bev=0.08)
        A.cyl(0.5, 1.4, (sx * (width / 2.0 - 0.8), 0, H + 2.4), VB.K['brass'], verts=8, r2=0.1)


def wt03_02():
    return LK.wrap(VB.bay_2, post=_bay_post(30.0, 22.0))()


def wt03_03():
    return LK.wrap(VB.bay_3, post=_bay_post(22.0, 20.0))()


def wt04_01():
    return LK.wrap(VB.shelf_1, post=_shelf1_post)()


def wt04_02():
    return LK.wrap(VB.shelf_2, post=_shelf2_post)()


# --- lead4 registration ---
import v5_leadkit as LK
import v5_vb as VB
BATCHES['lead4_vb'] = ('v5_wizard', mk([('WT03_02_wizard_bookshelf_curved_02', wt03_02), ('WT03_03_wizard_bookshelf_curved_03', wt03_03),
                                        ('WT04_01_wizard_bookshelf_straight_01', wt04_01), ('WT04_02_wizard_bookshelf_straight_02', wt04_02)], 0.1))
