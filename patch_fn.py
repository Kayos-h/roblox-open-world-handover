"""patch_fn - replace top-level functions of a module with the definitions in a snippet file, or insert new ones before 'BATCHES ='.
python patch_fn.py <module.py> <snippet.py>
Every top-level def/assign in the snippet replaces the same-named top-level def/assign in the module; names that do not exist yet are inserted just before the
module's BATCHES assignment.  A snippet may end with a block that starts with a line '# --- leadN registration ---' (N = digits): that block is appended at the END of the
module, replacing an older block with the SAME marker (other markers are kept).  A compile check runs afterwards; on error the original file is restored."""
import ast
import re
import sys
import shutil

RX = re.compile(r'^# --- (lead\d+) registration ---[ \t]*$', re.M)
mod, snip = sys.argv[1], sys.argv[2]
orig = open(mod, encoding='utf-8-sig').read()
shutil.copy2(mod, mod + '.bak')
snip_text = open(snip, encoding='utf-8-sig').read()
tail, mark = '', None
m = RX.search(snip_text)
if m:
    mark = m.group(1)
    snip_text, tail = snip_text[:m.start()], snip_text[m.start():]
if mark:
    for mm in list(RX.finditer(orig)):
        if mm.group(1) == mark:
            nxt = RX.search(orig, mm.end())
            orig = orig[:mm.start()].rstrip('\n') + '\n' + ('\n\n' + orig[nxt.start():] if nxt else '')
            break


def spans(src):
    lines = src.splitlines()
    tree = ast.parse(src)
    out = {}
    for n in tree.body:
        nm = None
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
            nm = n.name
        elif isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name):
            nm = n.targets[0].id
        if nm:
            start = n.lineno - 1
            if getattr(n, 'decorator_list', None):
                start = n.decorator_list[0].lineno - 1
            out[nm] = (start, n.end_lineno)
    return lines, out


lines, have = spans(orig)
sl, sp = spans(snip_text)
new_blocks = {nm: '\n'.join(sl[a:b]) for nm, (a, b) in sp.items()}
replaced, added = [], []
for nm, (a, b) in sorted(((nm, have[nm]) for nm in new_blocks if nm in have), key=lambda t: -t[1][0]):
    lines[a:b] = new_blocks[nm].splitlines()
    replaced.append(nm)
ins = [nm for nm in new_blocks if nm not in have]
if ins:
    lines2, have2 = spans('\n'.join(lines) + '\n')
    at = have2['BATCHES'][0]
    block = '\n\n\n'.join(new_blocks[nm] for nm in ins).splitlines() + ['', '']
    lines[at:at] = block
    added = ins
text = '\n'.join(lines).rstrip('\n') + '\n'
if tail:
    text += '\n\n' + tail.strip('\n') + '\n'
try:
    ast.parse(text)
except SyntaxError as e:
    shutil.copy2(mod + '.bak', mod)
    print('SYNTAX ERROR, original restored:', e)
    sys.exit(1)
open(mod, 'w', encoding='utf-8').write(text)
print('replaced:', replaced, '| added:', added, '| tail:', mark, '| lines', len(orig.splitlines()), '->', len(text.splitlines()))
