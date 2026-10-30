"""update_runbook - section D of RUNBOOK_v5.md after the lead pass (no sub-agents, user reviews the photos)."""
p = r"C:\Users\Nitro\.kiro\crew\workspace\town\plan_v5\RUNBOOK_v5.md"
t = open(p, encoding='utf-8').read()
a = t.index('- **Latest verdict per model**')
b = t.index('- **Reviewer noise:**')
new = """- **Lead pass (2026-10-30 19:50, no sub-agents, user's instruction):** 31 models rebuilt by the lead and checked by the lead's own eyes plus numbers (`python lead_verify.py`: 31/31 pass, no glow key, no changed colour, 11 new palette keys). They are NOT judged by reviewers; the user reviews them. List: `library\\v5_work\\lead\\fixed_ids.json`. Before/after sheets: `library\\v5_work\\lead\\fixed_01.jpg` to `fixed_04.jpg`. Old files are archived (copy only) in `library\\v5_fix3_archive`. Fix code is in the `v5_fx_*` modules (functions `_switch_stairs`, `_gate_tunnel`, `_altar_ruin`, `_pool_rock`, `hq_1`, `plaza_monument`, `quay_2`, `_path01`, `tree_falls`, `_stall`, `_sign_smith`, `_brazier2`, `_avenue04`, `_portal2`, `_shrine3`, `cairn`, `lantern_post`, `natural_gate`, `_magic_ruin`, `_float_rock`, and edits inside `_skull_building`, `_ring_segment`, `_sea_arch`, `_ruin_house`, `_bank`, `_rim_rock`); helper scripts `patch_fn.py`, `lead_edits.py`.
- **Latest verdict per model** (`library\\v5_work\\FINAL_VERDICTS_v5.json`): OK 285, MINOR 78, FIXED (lead pass, awaiting the user) 31, not reviewed 9 (LM26_02/03, LM28_02, LM29_01/02, PL02_01, PL05_01/02/03), MAJOR 1 (WT02_01). Reviewer lists with notes: `library\\v5_work\\r3\\NOT_OK_r3.md` and `r4\\NOT_OK_r4.md`.
- **Still open:** WT02_01 tower interior is a placement matter, not a model flaw: the WT03/WT04 bookshelves and the WT05 map must be placed inside it by the tower plan (`v5_tower_assembly.py`, `tower_check.ps1`; first solve rated FIX, second solve `tower_check\\fixed2` not reviewed; `mapplan\\v5_himalaya.json` unchanged).
- **Originality and glow (fixed in the lead pass):** the gold star badges on CP15_01 and CP17_01 are replaced by a bronze ring with a tower glyph and a bronze urn; the glow-looking parts on WT13_06 (lantern), FR02_04 (gold tip) and TW03_02 (gold rim) are replaced by dull stone, ash and bronze. No v5 model uses any glow key (57 old glow keys exist in the merged palette from v1-v4 models only).
"""
t = t[:a] + new + t[b:]
t = t.replace("## D. Status (2026-10-30 19:10): fix rounds ended after round 2 (the user's decision; no third round)", "## D. Status (2026-10-30 19:55): fix rounds ended after round 2; then one lead pass (no sub-agents)")
open(p, 'w', encoding='utf-8').write(t)
print('runbook updated; section D lines:', len(t[t.index('## D. Status'):].splitlines()))
