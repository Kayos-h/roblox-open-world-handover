"""make_gallery_final - build v5_gallery_final.py from v5_gallery.py with the latest verdict per model, written to a NEW folder (gallery_final);
the round-1 gallery folder is left untouched (archive, never delete). Then run it."""
import subprocess
import sys

SRC = r"C:\Users\Nitro\.kiro\crew\workspace\town\library\src\v5_gallery.py"
DST = r"C:\Users\Nitro\.kiro\crew\workspace\town\library\src\v5_gallery_final.py"
t = open(SRC, encoding='utf-8').read()


def sub(old, new):
    global t
    assert t.count(old) == 1, ('pattern not found exactly once', old[:60], t.count(old))
    t = t.replace(old, new)


sub("OUT = os.path.join(LIB, 'v5_work', 'gallery')", "OUT = os.path.join(LIB, 'v5_work', 'gallery_final')")
sub("HERO = sorted(glob.glob(os.path.join(LIB, 'v5_work', 'review_pack', 'hero_*.jpg')))",
    "HERO = sorted(glob.glob(os.path.join(LIB, 'v5_work', 'r3', 'pack', 'hero_*.jpg'))) + sorted(glob.glob(os.path.join(LIB, 'v5_work', 'r4', 'pack', 'hero_*.jpg')))")
sub("COL = {'REDO': (176, 28, 44),", "COL = {'FIXED': (46, 112, 196), 'UNREVIEWED': (96, 104, 120), 'REDO': (176, 28, 44),")
sub("size = {}\n", "size = {}\nTRIS = {}\n")
sub("        size[k] = v.get('size') or []", "        size[k] = v.get('size') or []\n        TRIS[k] = v.get('tris')")
sub("tri = e.get('tris')", "tri = TRIS.get(mid)")
old_rev = "rev = {e['id']: e for e in json.load(open(os.path.join(LIB, 'v5_work', 'review_defects_v5.json')))}"
new_rev = '''def _load(p):
    return {e['id']: e for e in json.load(open(os.path.join(LIB, 'v5_work', p)))}


_r1, _r2, _r3, _r4 = _load('review_defects_v5.json'), _load(r'r2\\review_defects_r2.json'), _load(r'r3\\review_defects_r3.json'), _load(r'r4\\review_defects_r4.json')
_fix2 = {e['id'] for e in json.load(open(os.path.join(LIB, 'v5_work', r'r2\\fix2_ids.json')))}
rev = {}
for _i in order:
    if _i in _r4:
        _e = dict(_r4[_i])
    elif _i in _fix2:
        _e = dict(verdict='UNREVIEWED', defects=['rebuilt in fix round 2; this version has no independent review'], fix='')
    elif _i in _r3:
        _e = dict(_r3[_i])
    elif _i in _r2:
        _e = dict(_r2[_i])
    else:
        _e = dict(_r1[_i])
    _e['id'] = _i
    _d = _e.get('defects') or []
    _e['defects'] = [_d] if isinstance(_d, str) else list(_d)
    _e['fix'] = _e.get('fix') or ''
    rev[_i] = _e
_fixed = json.load(open(os.path.join(LIB, 'v5_work', 'lead', 'fixed_ids.json'))) + json.load(open(os.path.join(LIB, 'v5_work', 'lead2', 'worklist.json')))
_NOTE = json.load(open(os.path.join(LIB, 'v5_work', 'lead2', 'notes_all.json')))
for _i in _fixed:
    rev[_i] = dict(id=_i, verdict='FIXED', defects=[_NOTE.get(_i[:7], 'rebuilt in this pass')], fix='')'''
sub(old_rev, new_rev)
sub("groups = [\n    ('A', 'A_defective',", "groups = [\n    ('F', 'F_fixed_now', 'FIXED BY THE LEAD (two passes, 118 models): rebuilt and checked by the lead, waiting for YOUR review', [i for i in order if rev[i]['verdict'] == 'FIXED']),\n    ('A', 'A_defective',")
sub("    ('C', 'C_good', 'GOOD: OK (reviewers saw no reason to fix)', [i for i in order if rev[i]['verdict'] == 'OK']),\n]",
    "    ('C', 'C_good', 'GOOD: OK (reviewers saw no reason to fix)', [i for i in order if rev[i]['verdict'] == 'OK']),\n"
    "    ('D', 'D_not_reviewed', 'NOT REVIEWED: rebuilt in fix round 2, no independent verdict on this version', [i for i in order if rev[i]['verdict'] == 'UNREVIEWED']),\n]")
sub("'v5 Blender models: photos of all 404'", "'v5 Blender models: photos of all 404 (final state after fix round 2)'")
sub("grouped by the reviewers\\' verdict. Under each photo", "grouped by the LATEST independent verdict (front and back views). Under each photo")
sub("(('REDO', 'rebuild from scratch'),", "(('FIXED', 'rebuilt in this pass, for your review'), ('UNREVIEWED', 'rebuilt in round 2, no verdict yet'), ('REDO', 'rebuild from scratch'),")
sub("'After the three groups: four-angle pages (front, back, close-up, elevation) of the 27 big landmark pieces.'",
    "'After the groups: four-angle pages (front, back, close-up, elevation) of the big pieces: first the never-rebuilt ones, then the round-2 ones.'")
sub("'OK models can still carry a small reviewer note; 7 carry a suggested fix about too-similar siblings.'",
    "'OK models can still carry a small reviewer note. A different reviewer can rate the same model one step differently (see the report).'")
open(DST, 'w', encoding='utf-8').write(t)
print('written', DST)
sys.exit(subprocess.call([sys.executable, DST]))
