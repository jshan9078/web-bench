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

Three rules added 2026-09-03 (the third later that day): (1) every task must be finishable well inside a 10-minute wall-clock budget by a competent agent, and runs are terminated at 10 minutes; (2) difficulty comes from traps and discrimination, never from length: more targets, rows, pages, or repeated actions add time and cost without adding a new way to be wrong; (3) latency independence: a failure must be attributable to the model and its harness, never to the browser CLI's round-trip time or the machine, so any timing window must comfortably exceed a harness round-trip.

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

## v2.3 additions (2026-09-03): fast-moving, video-like content

Set composition first: after round 10 the 19 tasks every pilot config passed (Sonnet 5 low, Spark 1.2 low,
Opus 5 low) were retired from the v2 set (`"retired": True` in the registry; results kept). The Google
Maps and Google Calendar tasks stay regardless of saturation (`"keep": True`), so the sweep set is the
10 discriminating or kept tasks plus the four below.

The four new local sites share one property real sites have and static benchmarks lack: the information
moves. A screenshot is a sample of a moment, not the page, and the agent has to decide WHEN to look and
how to make the content hold still. None of them rewards speed (every timing window is far above a
harness round-trip, per the latency-independence rule); all of them punish sampling a couple of frames
and guessing.

| task | site | what moves | the honest path | the traps |
|---|---|---|---|---|
| 91-video-slide-read | YouTube-style player (canvas video, autoplay, seek bar, skip, speed, keyboard, clickable transcript) | the slide on screen | locate the FIRST "refund" in the transcript, seek there, read the frame | the Refund summary slide (keyword match), the draft forecast slide (second invoice total), the arbitrary frame that happens to be on screen |
| 92-log-stream | live log tail (4 lines/s, 40-line view, level filter, search, Pause) | lines scroll out of view in about 10 s | filter to ERROR or search "payments", or Pause, or poll steadily for a minute | payments WARN lines containing "error=", a checkout ERROR with its own order id, a second payments ERROR 45 s later |
| 93-ticker-tape | markets page with a scrolling canvas ticker (24 symbols, 40 s loop, hover pauses) | the tape | cover the whole loop (or hover) and take the max | the runner-up sits far away on the tape and is within half a point; the delayed watchlist table shows a bigger stale gain |
| 94-cctv-review | NVR playback (canvas, burned-in clock, timeline with motion marks, seek, 1 s steps, speed) | the recording | jump to the motion marks, identify the red car, read the clock while it is fully in frame | red truck, blue car, partial-frame readings, computing the time from the seek position instead of reading the random-start clock |

Implementation notes: canvas players, not `<video>` files, so every frame is deterministic and there is no
codec or GPU capture path that could fail for CLI or hardware reasons; player clocks run on wall time,
not requestAnimationFrame deltas, so a throttled tab cannot stall them (verified: the headless CLI page
is `visible` at 60 fps, and time advances). Slide frames and stream lines are served by the widget
server (`/__frame`, `/__lines`, `/__data`), which the endpoint-bypass guard now covers.

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

### Opus leg and the latency rule (2026-09-03 05:00-05:25)

Opus 5 low ran the full set once. The live console was then found to violate the latency-independence
rule (a 4 s window made the CLI's round-trip part of the verdict); it was raised to 12 s with the verdict
taken at the Restart button press, the three 4 s captures were voided, and all three configs passed the
re-capture.

```
task                                opus-low-val           sonnet-low-val            spark-low-val
58-pixel-scan                               PASS                     PASS            FAIL (bypass)
59-spot-difference                          PASS                     PASS            FAIL (bypass)
60-form-wizard                              PASS                     PASS                     PASS
61-grid-toggle                              PASS                     PASS                     PASS
63-wikipedia-edit-audit                     PASS                     PASS                     PASS
64-hn-comment-census                        PASS                     PASS                     PASS
65-arxiv-pdf-tables                         PASS                     PASS                     PASS
66-wiki-table-reconcile                     PASS                     PASS                     PASS
68-youtube-transcript                       PASS                     PASS                     PASS
69-timezone-meeting                         PASS                     PASS                     PASS
72-amazon-quantity-edit                     PASS                     PASS                     PASS
73-pdf-table-extract                        PASS                     PASS                     PASS
74-dashboard-triage                         PASS                     PASS                     PASS
75-map-explorer                             PASS                     PASS            FAIL (bypass)
78-gmaps-directions                         PASS                     PASS                     PASS
79-gmaps-place-hours                        PASS                     PASS                     FAIL
76-settings-maze                            PASS                     PASS            FAIL (bypass)
77-crosshair-align                          PASS                     FAIL                     PASS
80-live-list                                PASS                     PASS                     PASS
score (pass/judged)                        19/19                    18/19                    14/19
pending/missing                                0                        0                        0
median s / max s                        39 / 190                 47 / 403                 66 / 295

criteria: no config at 100%: False | all scores distinct: True
```

Opus is clean on every task (fastest median, no endpoint calls, no budget hits) and beat both tasks that
separated the others: the crosshair in one planned batch of 52 moves to 0.0 px, and the map by
navigation. Sonnet's single miss is verification discipline; Spark's are rule-following and one
fabricated figure. The set therefore discriminates the three configs but does not expose a weakness in
Opus; candidate next traps (memory across a flow, blur-only validation with a late dependent field,
reconciliation under a stated precedence rule) target reasoning under UI constraints rather than
perception or timing.

### Round 6 (v2.5, 2026-09-03 05:28-05:34): realistic trap sites

Three sites built on real-product patterns: a pairing flow with no way back (a code shown once must be
recalled at the end; restarting issues a new code), a shipping form with blur-only validation, a late
dependent field, a silent failed submit, and a pre-ticked option that saves the billing address while
showing a success reference, and a parts catalogue whose list and detail pages disagree with a stated
precedence rule. All nine runs passed, cleanly, in 21-42 s. (The catalogue's verify check was made
idempotent after Spark pressed the correct button twice; a repeat click on the right control is not a
navigation failure.)

```
task                                opus-low-val           sonnet-low-val            spark-low-val
58-pixel-scan                               PASS                     PASS            FAIL (bypass)
59-spot-difference                          PASS                     PASS            FAIL (bypass)
60-form-wizard                              PASS                     PASS                     PASS
61-grid-toggle                              PASS                     PASS                     PASS
63-wikipedia-edit-audit                     PASS                     PASS                     PASS
64-hn-comment-census                        PASS                     PASS                     PASS
65-arxiv-pdf-tables                         PASS                     PASS                     PASS
66-wiki-table-reconcile                     PASS                     PASS                     PASS
68-youtube-transcript                       PASS                     PASS                     PASS
69-timezone-meeting                         PASS                     PASS                     PASS
72-amazon-quantity-edit                     PASS                     PASS                     PASS
73-pdf-table-extract                        PASS                     PASS                     PASS
74-dashboard-triage                         PASS                     PASS                     PASS
75-map-explorer                             PASS                     PASS            FAIL (bypass)
78-gmaps-directions                         PASS                     PASS                     PASS
79-gmaps-place-hours                        PASS                     PASS                     FAIL
76-settings-maze                            PASS                     PASS            FAIL (bypass)
77-crosshair-align                          PASS                     FAIL                     PASS
80-live-list                                PASS                     PASS                     PASS
81-memory-flow                              PASS                     PASS                     PASS
82-blur-validation                          PASS                     PASS                     PASS
83-reconcile-rule                           PASS                     PASS                     PASS
score (pass/judged)                        22/22                    21/22                    17/22
pending/missing                                0                        0                        0
median s / max s                        37 / 190                 44 / 403                 60 / 295

criteria: no config at 100%: False | all scores distinct: True
```

Where this leaves the set: it separates Sonnet (one precision miss), Spark (rule-following and one
fabrication), and Gemini (bookkeeping, precision, budget) from each other and from Opus, but nothing in
22 tasks exposes a weakness in Opus 5 low. Realistic traps of the kinds tried (memory, validation state,
policy reconciliation, decoys, timing under a fair window) are all solved by the current best models;
the remaining model-attributable, realistic levers are dense perception (reading small figures in a
dense rendered ledger with near-ties) and instruction discipline under on-page dark patterns.

### Rounds 7 and 8 (v2.6-v2.7, 2026-09-03 05:45-06:10) and the saturation cut

Round 7: dense-perception tasks (scanned ledger audit, stock-sheet diff, unlabeled chart), pixel scan at
level 3, and a Google Calendar scheduling task. Round 8: spot-the-difference at level 3 (design-QA
subtleties) and a subscription-cancellation flow built from dark patterns.

```
task                                opus-low-val           sonnet-low-val            spark-low-val
58-pixel-scan                               PASS                     PASS            FAIL (bypass)
59-spot-difference                          PASS                     PASS            FAIL (bypass)
60-form-wizard                              PASS                     PASS                     PASS
61-grid-toggle                              PASS                     PASS                     PASS
63-wikipedia-edit-audit                     PASS                     PASS                     PASS
64-hn-comment-census                        PASS                     PASS                     PASS
65-arxiv-pdf-tables                         PASS                     PASS                     PASS
66-wiki-table-reconcile                     PASS                     PASS                     PASS
68-youtube-transcript                       PASS                     PASS                     PASS
69-timezone-meeting                         PASS                     PASS                     PASS
72-amazon-quantity-edit                     PASS                     PASS                     PASS
73-pdf-table-extract                        PASS                     PASS                     PASS
74-dashboard-triage                         PASS                     PASS                     PASS
75-map-explorer                             PASS                     PASS            FAIL (bypass)
78-gmaps-directions                         PASS                     PASS                     PASS
79-gmaps-place-hours                        PASS                     PASS                     FAIL
76-settings-maze                            PASS                     PASS            FAIL (bypass)
77-crosshair-align                          PASS                     FAIL                     PASS
80-live-list                                PASS                     PASS                     PASS
81-memory-flow                              PASS                     PASS                     PASS
82-blur-validation                          PASS                     PASS                     PASS
83-reconcile-rule                           PASS                     PASS                     PASS
84-ledger-audit                             PASS                     PASS                     PASS
85-table-diff                               PASS                     PASS                     PASS
86-chart-read                               PASS                     PASS                     PASS
87-gcal-scheduling                          FAIL                     PASS                     FAIL
88-cancel-flow                              PASS                     PASS                     PASS
score (pass/judged)                        26/27                    26/27                    21/27
pending/missing                                0                        0                        0
median s / max s                        36 / 222                 41 / 403                 58 / 295

criteria: no config at 100%: True | all scores distinct: False
```

- **Perception density does not separate these models.** All three read 120 ledger figures, five changed
  cells, and an unlabeled chart exactly; Sonnet and Opus cleared the level-3 pixel scan and design-QA
  differences clean (Opus in a quarter of Sonnet's time). Spark solved every one of them on the merits and
  lost them to the endpoint guard.
- **Opus's first miss is a judgement miss.** On the Calendar task the first weekday carried an all-day
  holiday; Opus reasoned it "doesn't count" and scheduled under it, Spark ignored it, Sonnet caught it and
  moved to Tuesday. The verifier stated the all-day rule from the outset; the prompt now states it too.
- **Dark patterns did not bite**: all three cancelled cleanly, no offers, no pause, opt-in unticked.
- Two verifier fixes during these rounds, both to keep tooling out of verdicts: the table-diff parser no
  longer depends on line breaks (typing newlines is a CLI matter) and the catalogue verify is idempotent.

**Saturation cut (user rule: no task that every config passes, Google Maps kept):** 20 of 27 tasks are
flagged saturated and leave the BENCH_SET=v2 sweep set. The set that remains:

```
58-pixel-scan (level 3), 59-spot-difference (level 3), 75-map-explorer, 76-settings-maze,
77-crosshair-align, 78-gmaps-directions (kept), 79-gmaps-place-hours, 87-gcal-scheduling
```

On it: Opus 7/8, Sonnet 7/8, Spark 2/8. No config at 100%; Opus and Sonnet tie, each on a single miss
of a different kind (judgement versus verification discipline).

### Round 9 (2026-09-03 06:10-06:28): crosshair level 2 and a second Calendar task

Crosshair at 2 px with a single lock: Opus 0.0 px in 23 moves, Spark 0.0 px in 59 moves, Sonnet 6 px off
after 146 moves and 25 screenshots. The second Calendar task (last free weekday, description, colour)
passed for all three and is flagged saturated. Standing: Opus 27/28, Sonnet 27/28, Spark 22/28; no config
at 100%; Opus and Sonnet tie with one miss each (rule interpretation versus pixel estimation).

```
task                                opus-low-val           sonnet-low-val            spark-low-val
58-pixel-scan                               PASS                     PASS            FAIL (bypass)
59-spot-difference                          PASS                     PASS            FAIL (bypass)
60-form-wizard                              PASS                     PASS                     PASS
61-grid-toggle                              PASS                     PASS                     PASS
63-wikipedia-edit-audit                     PASS                     PASS                     PASS
64-hn-comment-census                        PASS                     PASS                     PASS
65-arxiv-pdf-tables                         PASS                     PASS                     PASS
66-wiki-table-reconcile                     PASS                     PASS                     PASS
68-youtube-transcript                       PASS                     PASS                     PASS
69-timezone-meeting                         PASS                     PASS                     PASS
72-amazon-quantity-edit                     PASS                     PASS                     PASS
73-pdf-table-extract                        PASS                     PASS                     PASS
74-dashboard-triage                         PASS                     PASS                     PASS
75-map-explorer                             PASS                     PASS            FAIL (bypass)
78-gmaps-directions                         PASS                     PASS                     PASS
79-gmaps-place-hours                        PASS                     PASS                     FAIL
76-settings-maze                            PASS                     PASS            FAIL (bypass)
77-crosshair-align                          PASS                     FAIL                     PASS
80-live-list                                PASS                     PASS                     PASS
81-memory-flow                              PASS                     PASS                     PASS
82-blur-validation                          PASS                     PASS                     PASS
83-reconcile-rule                           PASS                     PASS                     PASS
84-ledger-audit                             PASS                     PASS                     PASS
85-table-diff                               PASS                     PASS                     PASS
86-chart-read                               PASS                     PASS                     PASS
87-gcal-scheduling                          FAIL                     PASS                     FAIL
88-cancel-flow                              PASS                     PASS                     PASS
89-gcal-last-free                           PASS                     PASS                     PASS
score (pass/judged)                        27/28                    27/28                    22/28
pending/missing                                0                        0                        0
median s / max s                        38 / 233                 44 / 403                 60 / 295

criteria: no config at 100%: True | all scores distinct: False
```

### Round 10 (2026-09-03 06:30-06:34): the dial

A rendered gain dial (needle over a 0-100 tick scale, half-unit keyboard steps, one confirmation, one-tick
tolerance). All three configs missed it on the merits: Spark 38.5 for 40, Sonnet 77 for 81 after 17 s,
Opus 70 for 67. Each read the needle's angle instead of counting ticks from the nearest label, with
unlimited screenshots available. It is the first task every config fails; it stays in the set as a
ceiling task (it is realistic and model-attributable), but it does not separate configs.

Final pilot standing (29 tasks; 21 saturated and cut; 10-task sweep set including the pinned Google Maps
directions task and the second Calendar task):

```
task                                opus-low-val           sonnet-low-val            spark-low-val
58-pixel-scan                               PASS                     PASS            FAIL (bypass)
59-spot-difference                          PASS                     PASS            FAIL (bypass)
60-form-wizard                              PASS                     PASS                     PASS
61-grid-toggle                              PASS                     PASS                     PASS
63-wikipedia-edit-audit                     PASS                     PASS                     PASS
64-hn-comment-census                        PASS                     PASS                     PASS
65-arxiv-pdf-tables                         PASS                     PASS                     PASS
66-wiki-table-reconcile                     PASS                     PASS                     PASS
68-youtube-transcript                       PASS                     PASS                     PASS
69-timezone-meeting                         PASS                     PASS                     PASS
72-amazon-quantity-edit                     PASS                     PASS                     PASS
73-pdf-table-extract                        PASS                     PASS                     PASS
74-dashboard-triage                         PASS                     PASS                     PASS
75-map-explorer                             PASS                     PASS            FAIL (bypass)
78-gmaps-directions                         PASS                     PASS                     PASS
79-gmaps-place-hours                        PASS                     PASS                     FAIL
76-settings-maze                            PASS                     PASS            FAIL (bypass)
77-crosshair-align                          PASS                     FAIL                     PASS
80-live-list                                PASS                     PASS                     PASS
81-memory-flow                              PASS                     PASS                     PASS
82-blur-validation                          PASS                     PASS                     PASS
83-reconcile-rule                           PASS                     PASS                     PASS
84-ledger-audit                             PASS                     PASS                     PASS
85-table-diff                               PASS                     PASS                     PASS
86-chart-read                               PASS                     PASS                     PASS
87-gcal-scheduling                          FAIL                     PASS                     FAIL
88-cancel-flow                              PASS                     PASS                     PASS
89-gcal-last-free                           PASS                     PASS                     PASS
90-dial-set                                 FAIL                     FAIL                     FAIL
score (pass/judged)                        27/29                    27/29                    22/29
pending/missing                                0                        0                        0
median s / max s                        39 / 233                 41 / 403                 63 / 295

criteria: no config at 100%: True | all scores distinct: False
```

No config at 100%. Opus and Sonnet tie at 27/29 with different single misses (Calendar judgement versus
crosshair estimation) plus the shared dial miss; Spark's gap is rule-following. With one run per task, a
one-task tie between the two Claude configs is inside run-to-run noise; separating them reliably needs
repeated attempts on the discriminating set rather than another one-off task.

### Round 11 (2026-09-03): video-like tasks 91-94 at level 1

```
task                            spark-low-val           sonnet-low-val             opus-low-val
91-video-slide-read                      PASS                     PASS                     PASS
92-log-stream                            PASS                     PASS                     PASS
93-ticker-tape                           PASS                     PASS                     PASS
94-cctv-review                  FAIL (bypass)                     PASS                     PASS
```

Every config solved the level-1 versions when it played by the rules (Spark's CCTV miss: after `JSON.stringify(D)`
found nothing, it fetched `/__data` directly; its submitted time was inside the window, so the failure is
rule-following, not perception). Two consequences:

1. **Private endpoints are now unreachable, not just detected.** Every `/__*` endpoint except the rendered scene,
   the handshake and the harness-token endpoints requires a per-page-load key that only the page's own merged
   script holds (single-use token in the HTML, exchanged at load via `/__hello`; see widgetapp/base.py). Direct
   fetch, navigate, curl and token replay from the page source all return 403 (verified in the headless CLI).
   The bypass guard stays as the audit backstop.
2. **Levels 2 for 91, 92, 94** add properties only video has: WHICH figure the pointer rests on during one
   sentence (91); a payments ERROR identified only by a request id that appeared in an earlier checkout WARN
   (92); two identical red cars told apart by direction of travel, invisible in any single frame (94).
   Round 12 pilots these on the same three configs.

### Round 12 (2026-09-03): levels 2 for 91, 92, 94 (endpoints gated)

```
task                            spark-low-val           sonnet-low-val             opus-low-val
91-video-slide-read (pointer)            PASS                     PASS                     PASS
92-log-stream (correlation)              PASS                     PASS                     PASS
94-cctv-review (direction)               FAIL                     PASS                     PASS
```

Spark's CCTV miss is now on the merits: it reported the left-to-right car (98 s) instead of the right-to-left
one (35.5 s). Both Claude configs compared frames to read direction, traced the request id across services,
and read the pointer at the right moment. Cost separated where accuracy did not: Opus used 459 browser actions
on the log stream (a polling loop) against Sonnet's 24 for the same pass. No API errors in any run.

Two further video-only properties added as 95 (occupancy: state accumulated over a sequence of arrivals and
departures) and 96 (slide diff: comparing two frames far apart, with reordered rows and a relabelled row).

### Round 13 (2026-09-03): 95 lot occupancy, 96 slide diff

```
task                            spark-low-val           sonnet-low-val             opus-low-val
95-lot-occupancy                FAIL (bypass)                     PASS                     PASS
96-slide-diff                            PASS                     PASS                     PASS
```

Spark's lot answer was inside the window but it probed private endpoints three times (each answered 403 under
the gate; the attempt itself is the rule violation). Standing over the six video tasks: Sonnet 6/6, Opus 6/6,
Spark 4/6. Per the set-composition rule, 91, 92, 93 and 96 (passed by every pilot config) are flagged saturated
and leave the sweep set; 94 and 95 stay. Sonnet 5 low and Opus 5 low remain tied on every task piloted today.

### Round 14 (2026-09-03): real-world angles, batch 1

```
task                            spark-low-val           sonnet-low-val             opus-low-val
97-locale-ledger                         PASS                     PASS                     PASS
98-icon-toolbar                          PASS                     PASS                     PASS
99-seat-map                     FAIL (bypass)                     PASS                     PASS
100-dual-axis-chart                      PASS                     PASS                     PASS
102-admin-table                          PASS                     PASS                     PASS
103-fine-print                        (voided: prompt omitted the form submission; all three read the serial correctly)
```

The reasoning traps (locale, string sort, dual axis, icon glyphs, seat constraints) were all seen through by both
Claude configs, mostly in under 30 s. Spark's seat-map run reached the right pair but probed private endpoints
four times. 103 is re-run with a corrected prompt in round 16. Lesson for batch 3: after 15 rounds, the only
things that have defeated the Claude configs on the merits are fine visual estimation (dial, crosshair) and a
judgement call (Calendar all-day event); traps that can be reasoned through do not. Batch 3 targets perception.

### Round 15 (2026-09-03): real-world angles, batch 2

```
task                             spark-low-val           sonnet-low-val             opus-low-val
101-otp-relay                             PASS                     PASS                     PASS
104-receipt-total                         PASS                     PASS                     PASS
105-ruler-measure                         PASS                     PASS                     PASS
106-datepicker                            PASS                     PASS                     PASS
107-reorder-list                 FAIL (bypass)                     PASS                     PASS
```

All three configs relayed the one-time code inside its window, read the handwritten total, measured the offset
part to within 1 mm, navigated the calendar 14 months out, and reordered the list (Spark via a probe of the
private endpoints, which fails it). Batch 2 adds one discriminating task (107). Perception rounds 16 and 17 follow.

### Round 16 (2026-09-03): perception batch 1 (+103 re-run)

```
task                             spark-low-val           sonnet-low-val             opus-low-val
103-fine-print                            PASS                     PASS                     PASS
108-shelf-count                           PASS                     PASS                     PASS
109-legend-match                          PASS                     PASS                     PASS
110-analog-clock                          PASS                     PASS                     FAIL
111-fill-level                            PASS                     PASS                     PASS
```

Counting 23-37 boxes, matching six legend colours, reading fill ratios and magnified fine print were all solved.
The analog clock separated: Opus read 11:32 for 11:28 (hour-hand offset). Sonnet 5 low and Opus 5 low now have
distinct scores (29/31 vs 28/31) for the first time. Fine precision remains the productive direction.

### Round 17 (2026-09-03): perception batch 2

```
task                             spark-low-val           sonnet-low-val             opus-low-val
112-gantt-read                            PASS                     PASS                     PASS
113-pie-share                             PASS                     PASS                     PASS
114-scatter-threshold                     PASS                     PASS                     PASS
115-heatmap-max                           PASS                     PASS                     PASS
```

Gantt coverage, pie shares (within 2 points), exact counts above a threshold line and the darkest heatmap cell
were all read correctly by all three. Chart perception is saturated at these tolerances; what has separated
configs is fine geometry (needle angles, hand positions, pixel placement), rule-following on interactive
canvases, and calendar judgement. Batch 7 adds a remote-desktop (image-only UI) task and a dashcam clip.

### Round 18 (2026-09-03): Calendar longest gap, Maps transit, odometer, handwritten note

```
task                             spark-low-val           sonnet-low-val             opus-low-val
116-gcal-longest-gap                (judged separately: all three chose Tue Sep 8, 12:30-13:30, no reminder)
117-gmaps-transit                   (judged separately: all three read depart 7:44, 1 h 1 min, 1 transfer, Line 1)
118-odometer-read                FAIL (bypass)                     PASS                     PASS
119-handwritten-note                      PASS                     PASS                     PASS
```

The two real-site judgement tasks produced identical answers from all three configs (the calendar is nearly
empty, so the longest stretch is the whole of Tuesday). Spark's odometer run probed the private endpoints and
also misread the last digit; the Claude configs read all six seven-segment digits under glare. Discriminating
count after this round: 14.

### Round 19 (2026-09-03): fine precision batch

```
task                             spark-low-val           sonnet-low-val             opus-low-val
120-gauge-needle                          PASS                     PASS                     PASS
122-drop-pin                              PASS                     PASS                     PASS
125-custom-slider                         PASS                     PASS                     PASS
127-clock-ticks                           PASS                     PASS                     FAIL
```

Needle reading to within one minor tick, pin placement within 8 px and slider handles within 5 (all with a
check-and-correct loop) were solved by every config. The tick-only clock separated again: Opus read 11:28 for
5:27 (hand confusion), its second analog-clock miss. Lesson: the dial failed everyone because its tolerance was
a fifth of a tick spacing; the gauge passed everyone at three quarters of a tick. Batch 9 targets sub-tick
interpolation and clock reading in realistic wrappers, plus a slider with no numeric readout.

### Round 20 (2026-09-03): remote desktop, dashcam

```
task                             spark-low-val           sonnet-low-val             opus-low-val
128-remote-desktop               FAIL (bypass)                     PASS                     PASS
136-dashcam-speed                         PASS                     PASS                     PASS
```

Both Claude configs operated the image-only desktop in 4 and 11 clicks; Spark reached the right end state in 33
clicks but probed the private endpoints twice. The dashcam speed was read within tolerance by all three, Spark
after 648 browser actions and 413 s, which the speed and cost charts will show even though accuracy ties.
Discriminating count after this round: 16.

### Round 21 (2026-09-03): crop corners, virtual keypad, traffic count

```
task                              spark-low-val           sonnet-low-val             opus-low-val
137-crop-corners                           FAIL                     FAIL                     PASS
138-virtual-keypad                FAIL (bypass)                     PASS                     PASS
139-traffic-count                 FAIL (bypass)                     PASS                     FAIL
```

Three discriminators in one round. The rotated receipt's bottom-right corner was missed by Spark (63 px) and
Sonnet (12 px against a 10 px tolerance, it clicked the bounding box rather than the rotated corner); Opus
checked and corrected. The keypad and the traffic clip both caught Spark probing endpoints; Opus counted 9 of 10
vehicles in the clip (Sonnet counted correctly after 287 actions). Discriminating count after this round: 19.

### Round 22 (2026-09-03): wind vane, area share, blind slider, tower clock

```
task                              spark-low-val           sonnet-low-val             opus-low-val
141-wind-vane                              PASS                     PASS                     PASS
149-area-share                             PASS                     PASS                     PASS
151-blind-slider                           PASS                     PASS                     PASS
154-tower-clock                            FAIL                     PASS                     PASS
```

Sub-tick bearing (all within 1 degree), area fraction (within 1 point) and the readout-less slider were solved by
all three. The tower clock separated: Spark read 1:44 for 1:47 after zooming. Discriminating count: 20, the target.

### Round 23 (2026-09-03): speedometer, thermometer

```
task                              spark-low-val           sonnet-low-val             opus-low-val
155-speedometer-needle                     PASS                     PASS                     PASS
156-thermometer-read                       PASS                     PASS                     PASS
```

Both sub-tick readings were within 1 unit for every config (the dial's failure was apparently its integer-target
reading rule as much as its precision). Flagged saturated.

## Standing after 23 rounds (2026-09-03)

Pilot configs: Spark 1.2 low (contributor), Sonnet 5 low, Opus 5 low. 54 v2 tasks piloted in total.

| config | pass | accuracy | median s |
|---|---|---|---|
| Opus 5 low | 49/54 | 90.7% | 34 |
| Sonnet 5 low | 51/54 | 94.4% | 33 |
| Spark 1.2 low | 37/54 | 68.5% | 69 |

**20 discriminating tasks** (at least one pilot config fails), which with the two kept Google tasks form the
22-task sweep set (`BENCH_SET=v2`):

- Perception and precision: 58 pixel scan, 59 spot difference, 77 crosshair, 90 dial, 110 analog clock,
  127 tick-only clock, 154 tower clock (zoom), 137 crop corners, 118 odometer.
- Video and time: 94 CCTV direction, 95 lot occupancy, 139 traffic count.
- Interactive canvases and image-only UIs: 75 map explorer, 76 settings maze, 99 seat map, 107 reorder,
  128 remote desktop, 138 virtual keypad.
- Real sites: 79 Maps place hours, 87 Calendar scheduling (all-day judgement); 78 and 89 kept by decision.

What separates the Claude configs on the merits: analog clock reading (Opus twice), event counting over
video (Opus), two-point pixel precision on a rotated shape (Sonnet), fine estimation (crosshair: Sonnet; dial:
all), and calendar all-day judgement (Opus). What separates Spark: rule-following on interactive canvases
(it probes private endpoints, now 403 and still flagged), direction perception, and clock reading.

Thirty-two v2 tasks are flagged saturated by the pilot; they stay in the registry for the full-matrix run,
where weaker configurations may still fail them.

## pass@2 check (2026-09-03)

Every (task, config) pair that failed among the 20 discriminating tasks was re-run once under a "val2" label
(25 pairs). Rule (user's): if the failing config passes on the retry, the failure was noise and the task does not
count as a discriminator.

| task | failing config(s) attempt 1 | attempt 2 | status |
|---|---|---|---|
| 58 pixel scan, 59 spot difference, 76 settings maze, 95 lot occupancy, 99 seat map, 118 odometer, 137 crop corners, 138 keypad, 139 traffic count, 154 tower clock | Spark | Spark fails again (mostly endpoint probing; 118 and 154 misreads) | valid |
| 90 dial | Spark, Sonnet, Opus | Spark and Opus pass, Sonnet fails again | valid (Sonnet) |
| 137 crop corners | Spark, Sonnet | Sonnet passes | valid via Spark |
| 139 traffic count | Spark, Opus | Opus passes (11/11) | valid via Spark |
| 75 map explorer, 94 CCTV, 107 reorder, 128 remote desktop | Spark | Spark passes | invalid |
| 77 crosshair | Sonnet | passes | invalid |
| 110 analog clock, 127 tick clock | Opus | passes | invalid |
| 79 Maps hours, 87 Calendar | Spark; Spark and Opus | pass (judged) | invalid, kept by decision (Google) |

Result: 11 tasks hold under pass@2, 9 are flagged `pass2_invalid` (the two Google ones stay in the sweep set by
decision). Every Claude-side miss on the merits from the single-run pilots (crosshair, both analog clocks, the
Opus dial and traffic count) passed on retry: those were single-run noise. The only Claude failure that
reproduced is Sonnet on the dial. Spark's failures reproduce because endpoint probing is a stable behaviour.
The sweep set is now 15 tasks (11 valid discriminators plus the four Google tasks 78, 79, 87, 89 kept by decision).

## pass@2 iterations toward a validated set (2026-09-03, evening)

Rule: a task counts only if some config fails BOTH attempts. Legitimacy rule (user): tasks must test browsing and
control; failures that reproduce only as endpoint probing are reported separately from capability failures.

### Iteration A: image-only interactive UIs (kiosk, Wi-Fi tray, thermostat, parking meter, defect marking, meter dials)

All six INVALID: Spark's two first-attempt failures were endpoint probing and cleared on retry; Opus misread the
meter's first dial (8902 for 7902) and read it correctly on retry. Image-only click interfaces are solved by all
three configs; no more of these.

### Iteration B: real-site navigation and DOM control

172 (stacked modals, in-element scroll) and 177 (hover mega menu) were solved by all three on attempt 1: INVALID.
171 (spreadsheet grid) was voided: the prompt named cell C4 for Adapters, which is row 5; Opus and Spark edited
the right cell and were marked wrong, Sonnet followed the literal cell. Fixed (C5) and re-run in iteration D.
163 (Maps route options), 164 (Calendar recurrence), 167 (GitHub issue to PR) judged separately; 167's runs
disagree on the issue (#4297 vs #4295), settled against the GitHub API.

### Iteration C: perception-limit tasks

178 dense count (56, 65 and 60 blue boxes among ~150: all exact), 180 radio tuner, 182 map measure and 183 odd
glyph were solved by all three: INVALID. 179 people count HOLDS for Sonnet (21 for 22, then 15 for 19 after 498
actions); Opus's second attempt is re-run separately (a pipeline bug let a Claude run consume the pairs list).
Counting people over a two-minute clip is a genuine, reproducible failure.

### Iteration B2: second attempts on the real-site failures

163 Maps route options: Spark applied both options correctly on the retry (INVALID). 167 GitHub issue-to-PR: Opus
failed both attempts the same way (visited #4297, judged it "closed manually", reported the older #4295/#4298):
VALID, a genuine navigation-and-reading failure verified against the GitHub API.

### Iteration E: video tracking and real-site tracing

184 queue peak HOLDS (Opus 5 for 6 on both attempts) and 185 belt defects HOLDS (Opus 6 for 7 then 6 for 8; Spark
also failed twice, one attempt by probing). Both are reproduced counting-over-time failures. 188 (Wikipedia
category latest edit), 189 (GitHub release for a fix) and 190 (Maps nearby filters) judged separately; 190's
three runs disagree (two different pharmacies, and one config claims no rating filter exists).

Judged: 188 (Wikipedia category latest edit) and 189 (GitHub release for the fix) passed for all three, verified
against the MediaWiki and GitHub APIs; both saturated. 190 (Maps nearby filters) failed Sonnet (missed a closer,
higher-rated result in an incompletely scrolled list) and Opus (reported a 3.9-rated pharmacy); Spark found the
right one. Second attempts queued (E2).

### Iteration F: three tracking clips and two real-site traces

191 direction count, 192 parcel sort and 193 door events all HOLD: Sonnet failed each twice (8 for 14 then 3 for
10; 13 for 20 then 12 for 13; 8 for 9 then 5 for 8); Spark failed 191 and 192 twice (one attempt each by
probing); Opus read 192 and 193 correctly and 191 on retry. 194 (Wikipedia revert) and 195 (GitHub oldest approved
PR, correct answer "none exists") passed for all three, API-verified: saturated.

E2: 190 Maps nearby filters: both Claude configs passed on retry (the live results had changed: no open pharmacy
rated 4.0+, and both reported that correctly), so INVALID under pass@2. Live-site tasks with time-varying answers
are inherently noisy for this test.

### Iteration G: three tracking clips, Calendar hours, Maps transit compare

196 turn count HOLDS (Sonnet 8 for 9 then 5 for 6; Spark twice by probing), 198 pen entry HOLDS (Sonnet 5 for 6
then 1 for 3; Spark twice by probing), 197 checkout scans holds only via Spark's probing (both Claude configs
exact). 204 (Calendar week hours): the week has no timed events, so all three answered zero; judged. 205 (Maps
transit compare): the runs disagree on the fastest route's transfer count; judged against each run's evidence.

### Iteration H: four tracking clips

208 red crossers HOLDS (Sonnet 11 for 13 then 5 for 6; Spark twice), 211 bus boarding HOLDS (Sonnet 6 for 14 then
12 for 18; Spark twice by probing), 206 elevator stops holds only via Spark's probing (both Claude configs exact),
210 tray racks INVALID (all three exact on attempt 1).

G2: 204 Calendar hours: Sonnet covered all seven days on retry (INVALID). 205 Maps transit compare: Opus passed on
retry, and its retry showed that the numerals in the route rows are TTC line numbers, not transfer counts, which
means the attempt-1 verdicts (two passes for "2 transfers") rest on a misread the judge shared; the task's answer
is too ambiguous in Maps' current UI to keep. INVALID and noted as a task-design flaw.

## Scoring rule change (2026-09-04): endpoint probing is not a failure

The user's rule: probing private endpoints is an efficiency attempt, and the environment must simply not let it
succeed. It does not (every private endpoint has answered 403 to anything but the page's own script since the
gate on 2026-09-03 12:51), so an appstate verdict is now the server state alone; widget_bypass() stays as an
audit annotation ("probed" in tables). Runs from BEFORE the gate that probed and reached a complete state are
tainted and count as failures (58, 59, 75, 76 Spark attempt 1; a Gemini run on 75). Results were re-scored from
the recorded server state (38 runs flipped). Tasks that held only through probing are now invalid under pass@2.

### Standing under the state-only rule (2026-09-04, early)

16 tasks hold under pass@2 with a genuine failure: 59 spot difference, 90 dial, 99 seat map, 118 odometer, 154
tower clock, 167 GitHub issue trace, and ten tracking clips (179, 184, 185, 191, 192, 193, 196, 198, 208, 211).
Spark's probing no longer counts, so Spark rarely fails now; the discriminating failures are Sonnet's on
counting over video (large misses after hundreds of actions) and Opus's on one real-site reasoning task.
Iterations I and J add ten more clips in distinct scenarios; the honest ceiling for the set will be reported
when they finish.

### Iteration I: four clips, GitHub reopened issue, Maps cycling savings

217 queue leavers HOLDS (Sonnet: no submission within the 10-minute budget, then 3 for 5). 216 forklift trips,
218 vending dispensed and 219 no-parking were solved by all three (Spark's states complete despite probing):
INVALID. 213 (most recently reopened GitHub issue) and 214 (Maps cycling savings, a genuine tie at 23 minutes for
both destinations) judged separately; Spark's 213 run hit the budget with no answer.

Judged: 214 (Maps cycling savings) passed for all three, a correct tie: INVALID. 213 (most recently reopened
issue): Opus correct once the ground truth excludes pull requests; Sonnet reported the close date and hedged;
Spark produced no answer inside the budget. Retries queued for Sonnet and Spark (I2).

### Iteration J: six tracking clips

222 escalator up (Sonnet 17 for 16, then 16 for 17), 223 goal shots (Sonnet 5 for 9, then 12 for 13) and 225
library returns (Sonnet 14 for 17 then 10 for 12; Spark no answer then 16 for 13) HOLD. 220 ferry boarding, 221
drone drops and 224 crane lifts were solved by all three: INVALID. Under the state-only rule the validated set
stands at 20.

I2: 213 GitHub reopened issue HOLDS through Spark (two runs hitting the 10-minute budget with no answer; Sonnet
found #5817 correctly on retry). Validated set: 21.

### v1 tasks under pass@2 (three pilot configs, 2026-09-04)

Only two v1 pairs had failed at pass@1 among Spark 1.2 low, Sonnet 5 low and Opus 5 low. 10 arXiv agents paper:
Sonnet passed on retry (INVALID as a discriminator for these configs). 36 JS Paint poster: Spark failed again
(single-pixel dots, indistinguishable from noise): HOLDS. So the v1 set contributes 1 task under this rule, for a
combined validated set of 22 (21 v2 + JS Paint).

### Iteration K: six clips

226 fare gates (Sonnet twice) and 228 pool pots (Sonnet and Opus twice) HOLD; 229 bridge boats, 230 coffee cups
and 231 car wash resolved per the table below; 227 bin pickup solved by all three (INVALID).

### Iteration L: six clips

233 bag belt (all three fail twice), 234 hand hygiene (Sonnet twice) and 235 tennis serves (Spark and Sonnet
twice) HOLD; 232 toll booth, 236 bike dock and 237 barrier reversals solved by all three on retry (INVALID).

233 bag belt was VOIDED after inspection: bags placed at similar belt phases overlapped for the whole clip (the
end frame showed 7 distinct bags for an answer of 8), so the count was not legitimately readable. Fixed (phases
evenly spaced with jitter, at least 7 percent of the loop apart) and re-run as iteration M. Until then the
validated set is 29.

Iteration M (corrected 233 bag belt): Opus missed by one, then read it exactly on retry; Spark and Sonnet exact:
INVALID. Validated set 29 (28 v2 + JS Paint). One more batch (N) of four clips follows to reach the target of 30.

### Iteration N and final standing (2026-09-04)

239 loading bay HOLDS (Sonnet 12 for 14 then 8 for 19; Spark 12 for 14 then exact); 238, 240, 241 solved on
retry (INVALID). Correction: 99 seat map does not hold under the state-only rule (Spark's first attempt reached the right pair while
probing), so the validated set is **29 tasks** where at least one of Spark 1.2 low, Sonnet 5 low or Opus 5 low
fails both attempts. The list is in results/validated_set.json. The v1 set contributes one (36 JS Paint poster,
Spark); the other 28 are v2 tasks,
dominated by tracking-over-video clips that Sonnet 5 low fails repeatedly and Opus 5 low fails on several.

One more batch (O) of four clips runs to reach 30.

### Iteration O and final standing (2026-09-04 07:40)

244 dog park HOLDS (Sonnet 17 for 18, then 19 for 21); 242, 243, 245 solved on retry (INVALID). The validated
set reaches **30 tasks** where at least one of Spark 1.2 low, Sonnet 5 low or Opus 5 low fails both attempts,
scored on server state only (endpoint probing is not a failure) with pre-gate probe passes treated as failures.
The list is results/validated_set.json: 29 v2 tasks plus 36 JS Paint from v1. Failing configs across the set:
Sonnet on 22 tasks, Spark on 8, Opus on 5 (some tasks fail more than one). The set is dominated by tracking and
counting over two-minute clips, plus fine perception (dial, odometer, tower clock, spot difference), two
real-site navigation tasks (GitHub issue trace, GitHub reopened issue) and the JS Paint drawing task.

## v4 (2026-09-04): toward 60 validated tasks on Sonnet 5 low and Opus 5 low

Rules now: validation on the two Claude configs only (Spark dropped), pass@2, server state only. The user asked for
genuine browser control and navigation, and later allowed synthetic visual and DOM challenges to probe where the
models fall. Standing at the start: 25 validated (tracking clips, dial, GitHub issue trace, pool pots, coffee cups).

Batches in flight: P (Wikipedia sandbox edit, rich text, flight booking, inbox triage, CRM merge, edit conflict,
keyboard grid, OSM nearest stop), Q (map pan, config editor, helpdesk, team calendar, shop variants, survey builder,
GitHub blame), R (checkout, password reset, timesheet, gallery tagging, GitHub compare), S (shadow/iframe form,
moving target, line trace, maze exit, nested scroll, memory pairs, intersections, hue order).

### Iteration P: browser-control batch 1

250 CRM merge, 251 edit conflict and 252 keyboard grid: solved by both configs (INVALID). 247 rich text: three of four
runs produced the right document with the list wrapped in a stray <p> (what the browser's own editor emits), which
the checker wrongly rejected; checker fixed and runs re-scored (Sonnet's second attempt bolded the period too:
that one stays a fail). 248 flight booking: the task itself was wrong (random target date vs a fixed date in the
prompt); fixed and re-run. 249 inbox triage: the manager's "by end of day" made the star rule ambiguous; wording
fixed and re-run. 246 Wikipedia sandbox edit: hCaptcha blocks anonymous publishing, recorded as an environment
wall. 253 OSM nearest stop: judged against Overpass.

### Iteration Q: browser-control batch 2

All six local tasks (map pan, config editor with auto-close, helpdesk escalation, team calendar slot, shop
variants, survey builder) were solved by both configs on the first attempt: INVALID. 262 GitHub blame: both
reported 0ec7f71 by pgjones, 2023-08-19; judged. Conclusion so far: realistic DOM workflows, even multi-step ones
with validation and traps, are within reach of both configs; the remaining yield is in perception, timing and
synthetic challenges (batches S and T) and in real-site tool use (OSM).

### 2026-09-04: Opus 5 low becomes the only pilot config

Per-config attempt-1 pass rates over the 185 tasks all three configs ran: Opus 5 low 90%, Spark 1.2 low 86%,
Sonnet 5 low 84%. The user decided that further runs use Opus 5 low only and that a task counts as validated when
ANY config has failed it on both pass@2 attempts (earlier Sonnet and Spark evidence is kept). v2_validated.py
recomputes results/validated_set.json on that basis. Iteration R's pending Sonnet reruns were cancelled.

### Iteration R: browser-control batch 3

263 checkout, 265 timesheet, 267 gallery tagging: both configs passed at attempt 1 (INVALID). 269 GitHub compare
tags: both passed (judged against the compare API). 264 password reset: every run failed, but the failure was
ours: the app's password-set endpoint was named /__reset, which collides with the harness's own reset endpoint
(harness-secret only), so the page's submit got 403 and showed nothing. Endpoint renamed to /__setpw; all 264
runs voided (raw/voided, results/voided) and the task re-queued on Opus 5 low.
