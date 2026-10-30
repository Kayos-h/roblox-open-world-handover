import re
t = open(r"C:\Users\Nitro\.kiro\crew\workspace\town\plan_v5\v5_worker_plan.md", encoding="utf-8").read()
i = t.find("## vf:")
s = t[i:]
s = re.sub(r"```.*?```", "", s, flags=re.S)
s = re.sub(r"\n\s*\n", "\n", s)
print(s)
