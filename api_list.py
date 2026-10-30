"""api_list - print the signatures and the first docstring line of the functions and methods in the given module files."""
import ast
import sys

for p in sys.argv[1:]:
    src = open(p, encoding='utf-8').read()
    tree = ast.parse(src)
    print('=====', p.split('\\')[-1], len(src.splitlines()), 'lines')

    def show(node, ind=''):
        for n in node.body:
            if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
                if n.name.startswith('__') and n.name != '__init__':
                    continue
                if isinstance(n, ast.FunctionDef):
                    a = n.args
                    names = [x.arg for x in a.args]
                    defs = [ast.unparse(d) for d in a.defaults]
                    pairs = names[:len(names) - len(defs)] + [f'{nm}={d}' for nm, d in zip(names[len(names) - len(defs):], defs)]
                    sig = ', '.join(pairs)
                else:
                    sig = ''
                doc = (ast.get_docstring(n) or '').split('\n')[0][:150]
                print(f'{ind}{"class " if isinstance(n, ast.ClassDef) else "def "}{n.name}({sig})  {doc}')
                if isinstance(n, ast.ClassDef):
                    show(n, ind + '    ')
    show(tree)
