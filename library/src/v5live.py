"""v5live - build v5 models in any Blender WITHOUT previews or saving, and print a numbers check against the manifest.
  import v5live; v5live.check('v5_va', batches=['tower_shell'])      # or only=['WT01_01_wizard_tower_shell']
Blender axes: X = width, Y = depth, Z = height. Manifest columns size_x, size_y, size_z are Roblox axes (width, HEIGHT, depth).
Prints one line per model: tris/budget, size vs manifest, flags (SIZE, TRIS, LOW, EMPTY, ERROR), build seconds, marker counts.
"""
import os
import sys
import csv
import importlib
import time
import traceback
import bpy

SRC = os.path.dirname(os.path.abspath(__file__))
if SRC not in sys.path:
    sys.path.insert(0, SRC)
import kitlib
import v4util

MAN = r"C:\Users\Nitro\.kiro\crew\workspace\town\plan_v5\V5_MANIFEST.csv"
_man = None


def manifest():
    global _man
    if _man is None:
        _man = {}
        with open(MAN, encoding='utf-8-sig') as f:
            for r in csv.DictReader(f):
                _man[r['id']] = r
    return _man


def load(modname):
    for n in ('v5kit', 'v5gen', modname):
        if n in sys.modules:
            importlib.reload(sys.modules[n])
        else:
            importlib.import_module(n)
    return sys.modules[modname]


def check(modname, batches=None, only=None, tol=0.12):
    mod = load(modname)
    only = set(only or [])
    bad = 0
    n = 0
    for bn, (cat, items) in mod.BATCHES.items():
        if batches and bn not in batches:
            continue
        for it in items:
            mid, fn = it[0], it[1]
            if only and mid not in only:
                continue
            n += 1
            t0 = time.time()
            try:
                ob = fn()
                marks = v4util.extract_markers(ob)
                st = kitlib.stats(ob)
            except Exception:
                bad += 1
                print('ERROR', mid, traceback.format_exc()[-600:])
                continue
            dt = time.time() - t0
            x, y, z = st['size_studs']
            row = manifest().get(mid)
            flags = []
            note = ''
            if st['tris'] < 12:
                flags.append('EMPTY')
            if row:
                sx, sh, sd = float(row['size_x']), float(row['size_y']), float(row['size_z'])
                bud = int(float(row['tri_budget']))
                note = f' | want {sx:g}x{sd:g}x{sh:g} <= {bud}'
                for got, want, nm in ((x, sx, 'x'), (y, sd, 'y'), (z, sh, 'z')):
                    if want > 0 and abs(got - want) / want > tol:
                        flags.append('SIZE' + nm)
                if st['tris'] > bud:
                    flags.append('TRIS')
                if st['tris'] < 0.15 * bud:
                    flags.append('LOW')
            else:
                note = ' | not in manifest'
            bad += 1 if flags else 0
            print(f"{mid}: {st['tris']} tris, {x:g} x {y:g} x {z:g} (W x D x H){note} {' '.join(flags) or 'ok'} {dt:.1f}s mk={ {k: len(v) for k, v in marks.items()} }")
    print(f'CHECKED {n} models, {bad} with flags')
