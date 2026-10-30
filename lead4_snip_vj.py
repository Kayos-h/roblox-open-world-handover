def rw01_01():
    return LK.wrap(mesa_closed, prune=[dict(keys=None, max_size=32.0, thin=4.2, max_z=18.0)])()


# --- lead4 registration ---
import v5_leadkit as LK
BATCHES['lead4_vj'] = ('v5_rework', mk([('RW01_01_rework_existing_01', rw01_01)], 0.1))
