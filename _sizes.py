import json, sys
lib = r'C:\Users\Nitro\.kiro\crew\workspace\town\library\_export_v2'
for fn in ('castle.json', 'harbour.json', 'rusty.json', 'alpine.json', 'capital.json'):
    d = json.load(open(lib + '\\' + fn))
    items = d if isinstance(d, list) else d.get('models', d)
    print('==', fn)
    for it in items:
        if isinstance(it, dict):
            i = it.get('id', '?')
            s = it.get('size')
            if fn == 'castle.json' and not any(i.startswith(p) for p in ('K01', 'K02', 'K03', 'K04', 'K05', 'K06', 'K08', 'K09', 'K10', 'K23', 'K30', 'K37', 'K40', 'K41')):
                continue
            if fn == 'harbour.json' and not any(i.startswith(p) for p in ('G06', 'G07', 'G08', 'G10', 'G11', 'G12', 'G13', 'G16', 'G27')):
                continue
            if fn == 'rusty.json' and not any(i.startswith(p) for p in ('D01', 'D20', 'D21', 'D34')):
                continue
            if fn == 'alpine.json' and not any(i.startswith(p) for p in ('E01', 'E02', 'E05', 'E06', 'E12')):
                continue
            if fn == 'capital.json' and not any(i.startswith(p) for p in ('C05', 'C06', 'C16')):
                continue
            print(' ', i, s)
