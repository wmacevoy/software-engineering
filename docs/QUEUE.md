# Queue

What is being worked on in this repository, in order, and what would make each item done
([SE1/W10](../guide/08-work.md#w10)). The guide has no requirements document of its own; each item
names the principle it serves instead. An agent may move an item to *review*; only the author marks
it *done*.

| # | Item | Principle | Done when | Status | Since |
| - | ---- | --------- | --------- | ------ | ----- |
| 1 | **`se`, three defects from the DM1 survey:** the label pattern fails on a wrapped label; a guide's own labeled AGENTS.md is taken for SE1's copy (identify SE1's by its `software-engineering/tree/v` line); the working-set rows know only SE1's documents. | SE1/T3, SE1/D9 | a fixture for each, seen red, then green; released as v1.3.1 (a patch: `se.py` is not a copy). | review: fixed in fb7586b and released as v1.3.1, 2026-10-28 | 2026-10-28 |
| 2 | **Codex, run two, with planted defects.** The method and the five defects to plant are in `archive/reviews/REVIEW-METHOD-other-family.md`. | SE1/T3, SE1/U3 | the reviewer's hit rate on the planted set is recorded in FINDINGS before its real findings are weighed; the planted ones are filtered out and the rest acted on. | ready | 2026-10-28 |
| 3 | **A *since* on every principle, mined from git.** `tools/since.js` writes the release and date at which each principle's current text first appeared; `--check` verifies it. | SE1/U7 | every principle carries a computed marker; `node tools/since.js --check` runs in CI; a release re-runs `--write`. | review: done on main, 2026-10-28 | 2026-10-28 |
| 4 | **A hook seen to fire on a real compaction.** Every hook anywhere is "configured, not seen to fire". The work is the compaction project's queue item #12. | SE1/T3, SE1/A11 | that item's *done when*; then the doctor may say "seen to fire", naming the date and transcript. | blocked: on a real compaction in an interactive session | 2026-10-28 |
| 5 | **DM1's migration to v1.3.** The handoff is `~/projects/data-mining/HANDOFF-migrate-to-SE1-v1.3.md`. | SE1/R10, SE1/U7 | the handoff's steps 1–7 done there; this guide's `se` then knows DM1's documents (#1). | blocked: on `git init` and a remote there (the owner's) | 2026-10-28 |
| 7 | **REQUIREMENTS_v1 and DESIGN_v1 for this repository**, rebuilt in W12's order from what the checker, `se`, and the release procedure already enforce, each marked *(inferred)* until the author confirms it. | SE1/W10, SE1/W12 | both exist in `docs/`; the queue and the tests cite their IDs; the doctor's working-set row passes here. | review: written 2026-10-28, every requirement *(inferred)*; the read-back is the five assumptions at the end of REQUIREMENTS_v1 | 2026-10-28 |
| 6 | **The Learning chapter (L1–L6) against U9.** Draft in `archive/reviews/REVIEW-v1.2-learning.md`. | SE1/U9 | the author says chapter, U9 as is, or something between. | blocked: on the author | 2026-10-28 |
| 8 | **`se` reads table-form requirements.** lwext4-bsd's REQUIREMENTS_v10 has 30 requirements in table rows; the doctor counted 0, so its citations and trace rows said "none yet" (FINDINGS 2026-10-29). | SE1/R10, SE1/T3 | a table-form fixture seen red, then green; the doctor counts lwext4-bsd's 30. | review: 2026-10-29; the citations question decided the same day: history (FINDINGS, done rows) is not stale, shorthand takes the version named before it on the line, with fixtures | 2026-10-29 |
