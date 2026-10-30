import struct, json, numpy as np
p = r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\fig\phase1_map.glb'
d = open(p, 'rb').read()
magic, ver, length = struct.unpack('<4sII', d[:12])
print('magic', magic, 'version', ver, 'declared', length, 'actual', len(d), 'OK' if length == len(d) else 'LENGTH MISMATCH')
jl, jt = struct.unpack('<II', d[12:20])
js = json.loads(d[20:20 + jl])
o = 20 + jl
bl, bt = struct.unpack('<II', d[o:o + 8])
blob = d[o + 8:o + 8 + bl]
print('json chunk type', hex(jt), 'bin chunk type', hex(bt), 'bin len', bl, 'declared buffer', js['buffers'][0]['byteLength'])
ok = True
for pi, prim in enumerate(js['meshes'][0]['primitives']):
    A = js['accessors']
    pos = A[prim['attributes']['POSITION']]; idx = A[prim['indices']]
    bv = js['bufferViews'][idx['bufferView']]
    ind = np.frombuffer(blob[bv['byteOffset']:bv['byteOffset'] + bv['byteLength']], dtype=np.uint32)
    pv = js['bufferViews'][pos['bufferView']]
    P = np.frombuffer(blob[pv['byteOffset']:pv['byteOffset'] + pv['byteLength']], dtype=np.float32).reshape(-1, 3)
    good = ind.max() < pos['count'] and len(P) == pos['count'] and len(ind) % 3 == 0
    ok &= good
    print(f'prim {pi}: verts {pos["count"]} tris {len(ind)//3} maxIndex {ind.max()} bounds min {P.min(0).round(1)} max {P.max(0).round(1)} {"OK" if good else "BAD"}')
    for k in ('NORMAL', 'COLOR_0'):
        a = A[prim['attributes'][k]]
        if a['count'] != pos['count']:
            ok = False; print('attribute count mismatch', k)
print('GLB structure', 'VALID' if ok else 'PROBLEMS')
# OBJ sanity
v = f = 0
mx = 0
for line in open(r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\fig\phase1_map.obj'):
    if line.startswith('v '): v += 1
    elif line.startswith('f '):
        f += 1
        for t in line.split()[1:]:
            mx = max(mx, int(t.split('/')[0]))
print('OBJ vertices', v, 'faces', f, 'max face index', mx, 'OK' if mx <= v else 'BAD INDEX')
