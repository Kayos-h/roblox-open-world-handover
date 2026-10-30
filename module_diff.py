"""module_diff - which builder functions of a fix module changed compared with the archived copy, and does the module still compile / import its BATCHES text.
  python module_diff.py v5_fx_vi_a
"""
import ast
import sys
import difflib

L = r"C:\Users\Nitro\.kiro\crew\workspace\town\library"
m = sys.argv[1]
new_p, old_p = L + rf"\src\{m}.py", L + rf"\v5_fix1_archive\src\{m}.py"
new, old = open(new_p, encoding='utf-8').read(), open(old_p, encoding='utf-8').read()
try:
    tn = ast.parse(new)
    print('syntax: OK')
except SyntaxError as e:
    print('SYNTAX ERROR:', e)
    sys.exit()


def funcs(src, tree):
    lines = src.splitlines()
    return {n.name: '\n'.join(lines[n.lineno - 1:n.end_lineno]) for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}


fo, fn = funcs(old, ast.parse(old)), funcs(new, tn)
changed = [k for k in fn if k in fo and fn[k] != fo[k]]
added = [k for k in fn if k not in fo]
removed = [k for k in fo if k not in fn]
print(f'{m}: {len(new.splitlines())} lines (was {len(old.splitlines())}); functions changed {len(changed)}: {changed}; added {len(added)}: {added}; removed {len(removed)}: {removed}')
tail_new = new.strip().splitlines()[-4:]
print('last lines:', tail_new)
