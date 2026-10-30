"""fn_replace - replace (or append) whole top-level functions in a python file from a bundle file.
  python fn_replace.py <target.py> <bundle.py>
For every top-level 'def name(' in the bundle: the same-named top-level function in the target is replaced (decorators not supported);
if the target has none, the function is inserted before the line that starts 'BATCHES' (or appended). Prints what it did.
"""
import re
import sys


def blocks(src):
    """Return {name: (start, end)} line-index spans of top-level defs (end = first following non-indented code line)."""
    lines = src.split('\n')
    out = {}
    i = 0
    while i < len(lines):
        m = re.match(r'def (\w+)\(', lines[i])
        if m:
            j = i + 1
            while j < len(lines) and (lines[j] == '' or lines[j].startswith((' ', '\t'))):
                j += 1
            k = j
            while k > i and lines[k - 1] == '':
                k -= 1
            out[m.group(1)] = (i, k)
            i = j
        else:
            i += 1
    return lines, out


def main():
    tgt, bun = sys.argv[1], sys.argv[2]
    tl, tb = blocks(open(tgt, encoding='utf-8').read())
    bl, bb = blocks(open(bun, encoding='utf-8').read())
    for name, (s, e) in sorted(bb.items(), key=lambda kv: -tb.get(kv[0], (10 ** 9, 0))[0]):
        new = bl[s:e]
        if name in tb:
            a, b = tb[name]
            tl[a:b] = new
            print('replaced', name)
        else:
            at = next((n for n, l in enumerate(tl) if l.startswith('BATCHES')), len(tl))
            tl[at:at] = new + ['', '']
            print('inserted', name)
        tl, tb = blocks('\n'.join(tl))
    open(tgt, 'w', encoding='utf-8', newline='\n').write('\n'.join(tl))


main()
