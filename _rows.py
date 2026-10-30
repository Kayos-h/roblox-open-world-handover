import csv
import collections
import os
rows = list(csv.DictReader(open(r"C:\Users\Nitro\.kiro\crew\workspace\town\plan_v5\V5_MANIFEST.csv", encoding="utf-8-sig")))
lib = r"C:\Users\Nitro\.kiro\crew\workspace\town\library"
done = set()
for f in os.listdir(lib):
    if f.startswith("v4_meta_") and f.endswith(".json"):
        import json
        try:
            done |= set(json.load(open(os.path.join(lib, f))).keys())
        except Exception:
            pass
g = collections.OrderedDict()
for r in rows:
    if r["id"] in done:
        continue
    g.setdefault(r["row"], []).append(r)
tot = 0
for k, v in g.items():
    r = v[0]
    tot += len(v)
    print(f"{k:5} x{len(v):<3} {r['priority']} {r['region']:<10} {r['size_x']}x{r['size_y']}x{r['size_z']} <={r['tri_budget']:>6}  {r['note'][:78]}")
print("TOTAL UNBUILT", tot, "of", len(rows))
