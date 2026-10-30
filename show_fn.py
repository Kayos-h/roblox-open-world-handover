"""show_fn - print the source of named top-level functions (and module-level names like the palette block P = ...) of a module file.
python show_fn.py <file> name [name ...]"""
import ast
import sys

p = sys.argv[1]
src = open(p, encoding='utf-8').read()
lines = src.splitlines()
tree = ast.parse(src)
want = set(sys.argv[2:])
for n in tree.body:
    nm = None
    if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
        nm = n.name
    elif isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name):
        nm = n.targets[0].id
    if nm in want:
        s = n.lineno - 1
        e = n.end_lineno
        print(f'--- {nm} (lines {n.lineno}-{n.end_lineno})')
        print('\n'.join(lines[s:e]))
