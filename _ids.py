import csv
import sys
rows = list(csv.DictReader(open(r"C:\Users\Nitro\.kiro\crew\workspace\town\plan_v5\V5_MANIFEST.csv", encoding="utf-8-sig")))
want = set(sys.argv[1:])
for r in rows:
    if r["row"] in want:
        print(r["id"])
