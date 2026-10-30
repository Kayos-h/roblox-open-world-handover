import json, re
c = json.load(open(r'C:\Users\Nitro\.kiro\crew\workspace\town\mapplan\catalog.json', encoding='utf-8-sig'))
print('entries', len(c), 'keys', list(c[0].keys()))
rx = re.compile(r'dummy|target|rack|anvil|forge|well|cart|hay|tent|statue|fountain|flag|barrel|crate|bench|stall|trough|training|hedge|planter|brazier|sign|gazebo|pavilion|carriage|wagon|fence|bale|tree|torch', re.I)
out = []
for e in c:
    if rx.search(e['id']):
        sz = e.get('bbox') or e.get('dims') or e.get('size') or e.get('extent') or ''
        out.append('%s=%s' % (e['id'], sz if not isinstance(sz, list) else 'x'.join(str(round(v)) for v in sz)))
print('  '.join(out))
