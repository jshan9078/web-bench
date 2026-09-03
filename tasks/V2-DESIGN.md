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

## v2.2 additions (2026-09-03): hard test sites and real-map navigation

The user's framing: the benchmark exists to find the model that can handle browser tasks on sites that
offer no MCP or CLI, so quick, correct navigation of an ordinary UI is the skill, whether or not an API
exists for the same outcome. Two consequences: Google Maps tasks are valid again, and difficult local test
sites with programmatic verification are allowed where live sites cannot verify deterministically.

- **74-dashboard-triage** (local, objective): a SaaS-style helpdesk console. Virtualized list (only rows
  near the scroll position exist in the DOM), 180 tickets behind "Load more" pages of 40, filter chips, a
  custom sort menu that clears filters, a detail drawer, a note-required confirm flow with a toast, a
  similarly named decoy company, and a more recent High ticket from the target company that is Pending
  rather than Open. Pass = exactly the target ticket resolved with a note citing the company's other open
  ticket.
- **75-map-explorer** (local, objective, vision): a map with no search box. Pan buttons or arrow keys,
  zoom buttons, labels only at zoom 2 or more, random layout and target each run, a popup with one
  allowed action. The prompt names the place and its district (filled from the app's per-run state).
  Pass = the target's popup opened and Route clicked for it alone.
- **76-settings-maze** (local, objective): an account-settings app. Top-level tabs, a nested tab strip, an
  accordion, a custom toggle inside a shadow root inside an iframe, an unsaved-changes modal that
  interrupts tab switches, and a footer Save that is the only way to persist. Pass = saved state equals the
  defaults plus exactly the three requested changes (a decoy notification setting and the billing email
  must stay untouched).
- **78-gmaps-directions** and **79-gmaps-place-hours** (live, judged): Google Maps directions with travel-
  mode switching and step details, and a place card with weekday hours, open/closed status, and a Nearby
  search with a displayed distance.

All four are registered in the v2 set; Spark and Gemini capture them in the post-round-2 sweeps, Sonnet
in a round-3 leg.

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

### Rounds 2 and 3 (v2.1 and v2.2, 2026-09-03 03:41-04:45)

Round 2 re-ran the seven changed tasks (level-2 widgets; trap items on the history audit, HN census, and
transcript task). Round 3 added the helpdesk console, map explorer, settings maze, and two Google Maps
tasks. State before round 4 (Gemini's last three runs wait on its quota; the crosshair widget is new):

```
task                              sonnet-low-val     gemini-3.7-flash-low            spark-low-val
58-pixel-scan                               PASS                     FAIL            FAIL (bypass)
59-spot-difference                          PASS                     PASS            FAIL (bypass)
60-form-wizard                              PASS                     PASS                     PASS
61-grid-toggle                              PASS                     PASS                     PASS
63-wikipedia-edit-audit                     PASS                     PASS                     PASS
64-hn-comment-census                        PASS                     PASS                     PASS
65-arxiv-pdf-tables                         PASS                     FAIL                     PASS
66-wiki-table-reconcile                     PASS                     PASS                     PASS
68-youtube-transcript                       PASS                     PASS                     PASS
69-timezone-meeting                         PASS                     PASS                     PASS
72-amazon-quantity-edit                     PASS                     PASS                     PASS
73-pdf-table-extract                        PASS                     PASS                     PASS
74-dashboard-triage                         PASS                     PASS                     PASS
75-map-explorer                             PASS    FAIL (budget, bypass)            FAIL (bypass)
78-gmaps-directions                         PASS                (missing)                     PASS
79-gmaps-place-hours                        PASS                (missing)                     FAIL
76-settings-maze                            PASS                (missing)                     PASS
77-crosshair-align                     (missing)                (missing)                (missing)
score (pass/judged)                        17/17                    11/14                    13/17
pending/missing                                1                        4                        1
median s / max s                        52 / 403                 48 / 603                 63 / 177

criteria: no config at 100%: False | all scores distinct: True
```

Findings:

- **Sonnet 5 low is perfect on 17 tasks**, and clean: no endpoint calls, no budget hits, median 52 s. It
  solved the map explorer the way a person would (zoom, pan toward the named district, one screenshot-
  guided click) in 12 calls.
- **Spark 1.2 low fails by rule-breaking and by fabrication**: it reads page source and drives the
  widgets' private endpoints (state reads, synthetic clicks, a 10 px grid search against the map's click
  endpoint), which the guard fails, and it invented a walking distance on the Google Maps place task that
  no captured panel showed. Where the prompt stated the endpoint rule for the console it complied and
  passed.
- **Gemini 3.7 Flash low fails on bookkeeping and precision**: it undercounted the PDF's main-text tables
  while viewing the right pages, clicked 7 before 6 on the level-2 pixel scan, and burned the entire
  10-minute budget on the map explorer with 937 calls, ending in a brute-force grid search of its own.
- **Level-2 vision widgets did not move the strong tiers** (Sonnet cleared all four in under 70 s each);
  the hardened live tasks produced no new fails. Difficulty that discriminates here is navigation state
  and instruction discipline, not perception.
- Harness fixes during these rounds: the wizard's reserved-id bug, the CLI's multi-word text truncation
  (fixed at the source), the bypass guard's path-only matching, the 10-minute budget, stale-verdict
  skipping in the Claude matrix, and a 55-second CLI outage during the binary swap (one run re-captured).

Criteria check: scores are distinct (Sonnet 17/17, Spark 13/17, Gemini 11/14 so far) but Sonnet is at
100%. Round 4 (v2.3) targets Sonnet's known weakness, precision and state, with the crosshair widget and
the level-2 traps on the console, map, and settings maze.

### Rounds 4 and 5 (v2.3 and v2.4, 2026-09-03 04:40-05:00)

Gemini was dropped from the pilot after its 5-hour quota (user decision); pilot configs from here are
Sonnet 5 low and Muse Spark 1.2 low. Round 4 deployed the level-2 traps on the console (linked-ticket
modal), map (same-named decoy in another district), and settings maze (pre-ticked billing side effect),
plus the crosshair precision widget. Round 5 added the live fleet console.

```
task                              sonnet-low-val            spark-low-val
58-pixel-scan                               PASS            FAIL (bypass)
59-spot-difference                          PASS            FAIL (bypass)
60-form-wizard                              PASS                     PASS
61-grid-toggle                              PASS                     PASS
63-wikipedia-edit-audit                     PASS                     PASS
64-hn-comment-census                        PASS                     PASS
65-arxiv-pdf-tables                         PASS                     PASS
66-wiki-table-reconcile                     PASS                     PASS
68-youtube-transcript                       PASS                     PASS
69-timezone-meeting                         PASS                     PASS
72-amazon-quantity-edit                     PASS                     PASS
73-pdf-table-extract                        PASS                     PASS
74-dashboard-triage                         PASS                     PASS
75-map-explorer                             PASS            FAIL (bypass)
78-gmaps-directions                         PASS                     PASS
79-gmaps-place-hours                        PASS                     FAIL
76-settings-maze                            PASS            FAIL (bypass)
77-crosshair-align                          FAIL                     PASS
80-live-list                                FAIL                     FAIL
score (pass/judged)                        17/19                    13/19
pending/missing                                0                        0
median s / max s                        52 / 403                 66 / 295

criteria: no config at 100%: True | all scores distinct: True
```

Findings:

- **Sonnet's first fails on the merits**: the crosshair (locked at 5.0 px after 11 moves, no verification
  screenshot; Spark took 42 moves and five screenshots to land at 2.2 px) and the live console (its
  confirmed restart hit the 94% host while a 96% host had moved to the top). Both are precision-and-
  timing failures, matching its only v1 misses.
- **The live console fails both configs** the same way: a read from one refresh window, an action in the
  next. It is the read-act-loop test that real live dashboards impose; neither config used a fresh
  snapshot plus ref click inside one window.
- **The level-2 traps did not catch Sonnet** (it declined the linked-ticket modal, ignored the decoy
  gym, unticked the billing side effect), and Spark's level-2 losses were again guard fails for reading
  page data endpoints rather than trap failures.

**Criteria met on the pilot configs**: no config at 100% (Sonnet 17/19, Spark 13/19), scores distinct,
and the failure profiles differ by model (precision/timing versus rule-following/fabrication). Across a
full 36-configuration matrix, "all scores distinct" cannot hold on 19 tasks (20 possible scores); the
achievable goal is a set on which strong configs no longer saturate, which this set now is.
