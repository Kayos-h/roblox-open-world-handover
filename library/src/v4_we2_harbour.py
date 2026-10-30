"""Worker we2 - B09 ships + B10 harbour set, category v4_harbour.
The predecessor we never wrote a harbour module. harbour.py (off-limits, imported only)
already carries a sophisticated lofted-hull system (Hull class with sheer/keel-rise/flare,
sail4 billowed sails, square_rig, shrouds/ratlines, anchors, gunports, stern lanterns) plus
a banded lighthouse, brick+timber warehouses and a wooden cargo crane -- all at the D-series
bar. We wrap those builders under the we2 manifest ids rather than reinventing hull lofting.
Each wrapped builder calls reset() + finalize() internally; the runner re-keys the output to
our manifest id, so the inner finalize name is harmless.
"""
import harbour

# ships (B09) -- lofted hulls, curved plank strakes, billowed sails, rigging
def b09_galleon():        return harbour.galleon()          # three masts, gunports, stern castle
def b09_merchant():       return harbour.merchant_ship()    # broad two-mast cargo ship
def b09_fishing():        return harbour.fishing_boat_1()   # one mast, cabin, nets, crates
def b09_rowboat():        return harbour.rowboat()          # clinker planks, thwarts, oars

# harbour set (B10)
def b10_lighthouse():     return harbour.lighthouse()       # rocky base, red/white bands, lantern room
def b10_crane():          return harbour.cargo_crane()      # wooden boom, pulley, hoisted crate
def b10_warehouse_a():    return harbour.warehouse_1()      # brick + timber, big doors, hoist
def b10_warehouse_b():    return harbour.warehouse_2()      # second warehouse, different roof


BATCHES = {
    'ships':   ('v4_harbour', [('B09_01_galleon', b09_galleon,   (1.0, -1.1, 0.32)),
                               ('B09_02_merchant_ship', b09_merchant, (1.0, -1.1, 0.32)),
                               ('B09_03_fishing_boat', b09_fishing, (1.0, -1.2, 0.4)),
                               ('B09_04_rowboat', b09_rowboat, (1.0, -1.2, 0.5))]),
    'harbour': ('v4_harbour', [('B10_01_lighthouse', b10_lighthouse, (1.0, -1.1, 0.4)),
                               ('B10_02_cargo_crane', b10_crane, (1.0, -1.2, 0.4)),
                               ('B10_03_warehouse_a', b10_warehouse_a, (1.0, -1.2, 0.4)),
                               ('B10_04_warehouse_b', b10_warehouse_b, (1.0, -1.2, 0.4))]),
}
