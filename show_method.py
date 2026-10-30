"""show_method - print methods of a class: python show_method.py <file> <Class> name [name ...]"""
import ast
import sys

p, cls, want = sys.argv[1], sys.argv[2], set(sys.argv[3:])
src = open(p, encoding='utf-8').read()
lines = src.splitlines()
for n in ast.parse(src).body:
    if isinstance(n, ast.ClassDef) and n.name == cls:
        for m in n.body:
            if isinstance(m, ast.FunctionDef) and m.name in want:
                print(f'--- {cls}.{m.name} (lines {m.lineno}-{m.end_lineno})')
                print('\n'.join(lines[m.lineno - 1:m.end_lineno]))
