# Web-bench v2 tasks: designed to discriminate

Motivation (2026-09-03): across 31 non-Haiku configurations, 24 of the 44 v1 tasks are passed by every
configuration and only two (JS Paint, Desmos) separate models by more than 10 points. The suite measures
"can it browse" but no longer measures "how well". The v2 tasks below target the failure modes the
re-audit actually observed, and nothing else:

1. **Precision under a moving coordinate frame** (scrolling + pixel clicks), with decoys that punish the
   greedy choice: 58-pixel-scan.
2. **Perception with no DOM fallback**: 59-spot-difference, 61-grid-toggle.
3. **Real-site UI traps**: image-only decision tables, delayed enablement, modal confirmation:
   60-form-wizard.
4. **Long-horizon bookkeeping** where one slip changes the answer: 63-wikipedia-edit-audit (two exclusion
   filters over five rows), 64-hn-comment-census (nesting depth), 65-arxiv-pdf-tables (count across
   pages), 66-wiki-table-reconcile (sort state + three cross-checks).
5. **Hidden UI state** that URLs do not encode: 66 (wikitable sort), 68-youtube-transcript (panel behind
   two clicks with its own scroll), 69-timezone-meeting (planner configuration).
6. **Honesty under pressure**: 69's first question usually has the answer "none".
7. **Verify-then-correct actions** with harness ground truth: 72-amazon-quantity-edit.
8. **Dense numeric reading from rendered PDFs**: 73-pdf-table-extract.

Design rules kept from v1: no puzzle or knowledge tasks (every task is solvable by careful browsing with
no domain knowledge), no outcome that one API call covers, no site with known bot walls, offline
judging from captured evidence, live data wherever the answer could otherwise be memorized. The four
widget tasks are served locally like 07-pixel-click and are verified programmatically, so their verdicts
carry no judge noise and their difficulty can be tuned by changing constants in `widgetapp/`.

Rollout: v2 tasks are registered with `v2: True` and are excluded from the v1 sweeps, scoreboard, and
published tables until piloted. Run them with `BENCH_SET=v2` (sweeps) or by name (single runs).
