"""v4_list - regenerate library\\V4_MODEL_LIST.md (same layout as the file the user attached) from the manifest + merged metadata.
Optional: library\\v4_work\\KNOWN_DEFECTS.md is appended at the end as the 'Known defects and notes' section.
Run: python v4_list.py
"""
import os, sys, json, time
SRC = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SRC)
import v4_manifest as M

LIB = M.LIB


def main():
    meta = json.load(open(os.path.join(LIB, 'v4_meta.json')))
    ok = {k: e for k, e in meta.items() if os.path.exists(os.path.join(LIB, e.get('category', ''), k + '.fbx'))}
    slot = {'_'.join(k.split('_')[:2]): k for k in ok}
    rows = M.expand()
    for r in rows:
        k = r['id'] if r['id'] in ok else slot.get('_'.join(r['id'].split('_')[:2]))
        r['saved'] = k
    built = [r for r in rows if r['saved']]
    sec = {}
    for r in rows:
        s = sec.setdefault(r['section'], [0, 0])
        s[1] += 1
        s[0] += 1 if r['saved'] else 0
    L = ['# Blender model list (V4 manifest)', '',
         f'Generated {time.strftime("%Y-%m-%d %H:%M")}. Source: `V4_MANIFEST.json` and `v4_meta.json` in `C:\\Users\\Nitro\\.kiro\\crew\\workspace\\town\\library`.', '',
         f'**Total models: {len(rows)}. Built: {len(built)}. Remaining: {len(rows) - len(built)}.**', '',
         '| Section | Title | Total | Built | Remaining |', '|---|---|---|---|---|']
    for s, (title, defs) in M.SECTIONS.items():
        L.append(f'| {s} | {title} | {sec[s][1]} | {sec[s][0]} | {sec[s][1] - sec[s][0]} |')
    L += ['', 'Files: each built model is `<folder>\\<ID>.fbx` and `<folder>\\<ID>.blend` under `C:\\Users\\Nitro\\.kiro\\crew\\workspace\\town\\library`. '
          'FBX files are split per colour, each piece under 18,000 triangles. Units: 1 unit = 1 stud, Z up, model front faces -Y, origin at bottom centre. '
          'Where the saved file name differs from the manifest ID (some workers used descriptive names such as `F05_01_bush_round`), the Notes column starts with `saved as`.', '',
          'Nothing has been uploaded to Roblox and the Studio map has not been changed for these models.', '']
    for s, (title, defs) in M.SECTIONS.items():
        L += [f'## {s}. {title}', '', '| ID | Priority | Status | Triangles | Size (studs) | Folder | Notes |', '|---|---|---|---|---|---|---|']
        for r in rows:
            if r['section'] != s:
                continue
            k = r['saved']
            if k:
                e = ok[k]
                size = ' x '.join(str(round(v)) for v in e.get('size', []))
                note = ('saved as ' + k + '. ' if k != r['id'] else '') + r['desc']
                L.append(f'| {r["id"]} | {r["priority"]} | built | {e.get("tris", ""):,} | {size} | {e.get("category", "")} | {note} |' if isinstance(e.get('tris'), int)
                         else f'| {r["id"]} | {r["priority"]} | built | {e.get("tris", "")} | {size} | {e.get("category", "")} | {note} |')
            else:
                L.append(f'| {r["id"]} | {r["priority"]} | todo |  |  |  | {r["desc"]} |')
        L.append('')
    kd = os.path.join(LIB, 'v4_work', 'KNOWN_DEFECTS.md')
    L += ['## Known defects and notes', '']
    L += open(kd, encoding='utf-8').read().splitlines() if os.path.exists(kd) else ['- (to be filled in after the independent review)']
    out = os.path.join(LIB, 'V4_MODEL_LIST.md')
    open(out, 'w', encoding='utf-8').write('\n'.join(L))
    print(f'wrote {out}: {len(built)} built of {len(rows)}')


if __name__ == '__main__':
    main()
