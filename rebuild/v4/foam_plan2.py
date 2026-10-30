"""foam_plan2.py - chains the shoreline segments, drops small closed loops (islets: they showed up as faceted octagon outlines) and keeps the long main coast.
Output: rebuild/v4/foam_segments_main.json  ({'segments': [...]}), same format as foam_segments.json.
"""
import json, math, collections
V4 = r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\v4'
segs = json.load(open(V4 + r'\foam_segments.json'))['segments']
KEY = 4.0


def k(x, z):
    return (round(x / KEY), round(z / KEY))


adj = collections.defaultdict(list)
for i, s in enumerate(segs):
    adj[k(s[0], s[1])].append(i)
    adj[k(s[2], s[3])].append(i)
seen = [False] * len(segs)
chains = []
for i in range(len(segs)):
    if seen[i]:
        continue
    stack, comp = [i], []
    seen[i] = True
    while stack:
        a = stack.pop()
        comp.append(a)
        s = segs[a]
        for end in (k(s[0], s[1]), k(s[2], s[3])):
            for b in adj[end]:
                if not seen[b]:
                    seen[b] = True
                    stack.append(b)
    chains.append(comp)
keep, drop = [], []
for comp in chains:
    L = sum(math.hypot(segs[a][2] - segs[a][0], segs[a][3] - segs[a][1]) for a in comp)
    (keep if L >= 900 else drop).append((L, comp))
out = [segs[a] for L, comp in keep for a in comp]
json.dump({'segments': out}, open(V4 + r'\foam_segments_main.json', 'w'))
print('chains', len(chains), '| kept (>=900 studs):', len(keep), 'segments', len(out), '| dropped islet loops:', len(drop), 'segments', sum(len(c) for L, c in drop))
print('kept lengths:', sorted((round(L) for L, c in keep), reverse=True)[:8])
print('dropped lengths:', sorted((round(L) for L, c in drop), reverse=True)[:10])
