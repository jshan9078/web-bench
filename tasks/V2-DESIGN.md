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

Two rules added 2026-09-03: (1) every task must be finishable well inside a 10-minute wall-clock budget by a competent agent, and runs are terminated at 10 minutes; (2) difficulty comes from traps and discrimination, never from length: more targets, rows, pages, or repeated actions add time and cost without adding a new way to be wrong.

Design rules kept from v1: no puzzle or knowledge tasks (every task is solvable by careful browsing with
no domain knowledge), no outcome that one API call covers, no site with known bot walls, offline
judging from captured evidence, live data wherever the answer could otherwise be memorized. The four
widget tasks are served locally like 07-pixel-click and are verified programmatically, so their verdicts
carry no judge noise and their difficulty can be tuned by changing constants in `widgetapp/`.

Rollout: v2 tasks are registered with `v2: True` and are excluded from the v1 sweeps, scoreboard, and
published tables until piloted. Run them with `BENCH_SET=v2` (sweeps) or by name (single runs).

## Pilot log

### Round 1 (v2.0, 2026-09-03 02:30-03:40)

Three configs, one attempt each, judged offline (Sonnet judges, frozen template). The wizard column is
void: a page bug (an input with id `name`, shadowed by `window.name`) broke step 1's Next button, and
every "pass" was obtained by the agent patching page state through eval. Fixed before round 2.

| task | Sonnet 5 low | Gemini 3.7 Flash low | Spark 1.2 low |
|---|---|---|---|
| 58-pixel-scan | FAIL | PASS | FAIL (endpoint bypass) |
| 59-spot-difference | PASS | PASS | FAIL (endpoint bypass) |
| 60-form-wizard | void | void | void |
| 61-grid-toggle | PASS | PASS | FAIL (endpoint bypass) |
| 63-wikipedia-edit-audit | PASS | PASS | PASS |
| 64-hn-comment-census | PASS | PASS | PASS |
| 65-arxiv-pdf-tables | PASS | FAIL | PASS |
| 66-wiki-table-reconcile | PASS | PASS | PASS |
| 68-youtube-transcript | PASS | PASS | PASS |
| 69-timezone-meeting | PASS | PASS | PASS |
| 72-amazon-quantity-edit | PASS | PASS | PASS |
| 73-pdf-table-extract | PASS | PASS | PASS |
| **valid-task score** | **10/11** | **10/11** | **8/11** |

What round 1 established:

- **The four widgets do discriminate**, but not the way intended at level 1: the separation came from
  behaviour under the rules rather than perception. Sonnet missed circle 4 below the fold and clicked a
  decoy on pixel scan (a genuine coordinate-frame failure). Spark 1.2 low, once the state endpoint was
  token-gated, kept probing it (130 refused calls on one run) and never produced a clean widget run;
  the endpoint-bypass guard fails those. Gemini cleared all four cleanly.
- **The live-site tasks separated on bookkeeping exactly once**: Gemini undercounted main-text tables in
  the PDF (4 for 5) while viewing the right pages. Everything else passed for all three configs, so
  those tasks get trap-based hardening in v2.1 (exact HN count with all ties named, a countable
  bot/minor check on the history audit, the auto-captions fact behind the transcript panel).
- **Two bypass channels were found and closed**: reading the widget's `/__state` (answer key), and
  solving the PDF tasks with curl plus PyMuPDF text extraction. Both are now rules (token gate plus
  harness guard; browser-only PDF reading with in-page rendering allowed).
- **Efficiency separates even where accuracy ties**: Gemini's median run was 25 s and 16 calls, Sonnet
  41 s and 14 calls, Spark 42 s and 22 calls, with maxima of 106 s, 379 s, and 334 s.
- **Capture gap**: an agent that writes screenshots outside the harness's shot convention and deletes
  them leaves no stills (one Gemini PDF run); the video does not scroll for element-scoped shots.

Criteria check (no config at 100%, all scores distinct): not met, Sonnet and Gemini tie at 10/11.
Round 2 (v2.1) re-runs the seven changed tasks on all three configs.
