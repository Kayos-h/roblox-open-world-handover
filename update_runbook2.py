"""update_runbook2 - RUNBOOK section D after the second lead pass (87 more models, no sub-agents)."""
p = r"C:\Users\Nitro\.kiro\crew\workspace\town\plan_v5\RUNBOOK_v5.md"
t = open(p, encoding='utf-8').read()
a = t.index("- **Lead pass (2026-10-30 19:50")
b = t.index("- **Still open:**")
new = """- **Lead passes (2026-10-30, no sub-agents, user's instruction):** pass 1 (19:50) rebuilt 31 models, pass 2 (22:30) rebuilt 87 more (9 never reviewed + 78 MINOR), 118 in total. Each was checked by the lead's own eyes plus numbers (`python lead_verify.py <ids.json>`: 31/31 and 86/87 pass; the one note is CP02_03 depth 21.4 vs 24). Not judged by reviewers; the user reviews them. Lists: `library\\v5_work\\lead\\fixed_ids.json` (31) and `library\\v5_work\\lead2\\worklist.json` (87). Before/after/back sheets: `library\\v5_work\\lead\\fixed_01..04.jpg` and `library\\v5_work\\lead2\\b1_01.jpg` ... `b7_02.jpg`. Old files are archived (copy only) in `library\\v5_fix3_archive` and `library\\v5_fix4_archive`. Code: `v5_fx_*` modules (functions listed per batch in `lead4_snip_*.py`), the hook kit `library\\src\\v5_leadkit.py` (wrap, recolor, prune, post, automatic de-z-fight) and helpers `patch_fn.py`, `lead2_tools.py`.
- **Key finding:** boxes whose faces lie in the same plane and overlap render as black seams or black tops (shadow-ray self hit). The kit now pushes the smaller box's conflicting face 0.04 outward; that removed black bars from the stair, gatehouse, temple stairs, colonnade and tunnel lining.
- **Latest verdict per model** (`library\\v5_work\\FINAL_VERDICTS_v5.json`): OK 285, FIXED by the lead 118 (awaiting the user), MAJOR 1 (WT02_01). Reviewer lists with the original notes: `library\\v5_work\\r3\\NOT_OK_r3.md` and `r4\\NOT_OK_r4.md`. Automatic check flags 19 of 404 (was 33 -> 25 -> 19).
"""
t = t[:a] + new + t[b:]
t = t.replace("## D. Status (2026-10-30 19:55): fix rounds ended after round 2; then one lead pass (no sub-agents)", "## D. Status (2026-10-30 22:35): fix rounds ended after round 2; then two lead passes (no sub-agents)")
open(p, 'w', encoding='utf-8').write(t)
print('runbook updated')
