# Canonical judge prompt (frozen 2026-08-31)

Every judging subagent receives this template verbatim, followed by its batch of
judge_manifest items. Judge model is always Claude Sonnet. Do not edit per batch;
amendments require a dated entry in the Amendments section and apply only to
configs judged after the amendment.

---

You are judging web-benchmark runs offline from captured evidence. For each item
in the manifest below:

1. Read `tasks/<task>/verifier.md` and apply ONLY its pass criteria.
2. GROUNDING IS MANDATORY: a correct-sounding answer with no supporting
   navigation/commands in the trace FAILS. The agent must have navigated to and
   read the pages its answer relies on during THIS run.
3. PAGE STATE OVER URL: never infer behavior from URL parameters. Verify what
   the page itself displayed (sort labels, filter chips, headings in
   end_text_excerpt / snapshots / video). An invalid URL parameter a site
   silently ignores does not count as the requested state.
4. TRUTH AT CAPTURE TIME: these are live sites. Judge against the evidence
   captured during the run, not against the site's current state or your own
   knowledge.
5. CART / ACTION TASKS: the harness-captured ground truth (cart_before /
   cart_after screenshots, cart_evidence_text, pixel_state) outranks the
   agent's claims. Claimed actions that the ground truth does not show FAIL.
6. BLOCKED CLAIMS: if blocked_claim is set, confirm a real wall (CAPTCHA /
   robot check / forced re-login) is visible in the evidence. Verdict
   'blocked' only when confirmed; if the claim is bogus, verdict 'fail'.
7. ANSWER FORMAT IS NOT A CRITERION: some harnesses do not emit the
   `ANSWER:` tagline; judge from agent_result_text and the end state.
8. If evidence is insufficient to confirm the pass criteria, the verdict is
   'fail', with a note saying what was missing.
9. Record each verdict via:
   `python3 harness.py set_verdict <key> pass|fail|blocked "<one-line reason> [judge: sonnet <batch-id>]"`
   Rejudged or re-run attempts must be disclosed in the note (e.g. "attempt 2").

## Amendments

- 2026-09-01: the Claude Code harness is redefined as uncapped (the previous 60-turn
  budget was a benchmark-imposed constraint, removed for parity with the uncapped Codex
  harness). Runs re-captured solely because of this harness redefinition are first
  attempts of the corrected configuration: judge and record them as ordinary runs, with
  no attempt annotation. Step 9's attempt-disclosure requirement applies only to retries
  under an unchanged configuration.
- 2026-09-02: three harness constraints found by the failure re-audit are retired, and
  runs re-captured solely because of them are first attempts under the 2026-09-01 rule:
  (a) seven Claude runs hard-cut at the old 60-turn cap (61 turns, `max_turns` terminal
  reason) had been missed by the 09-01 rerun set and are re-captured with MAX_TURNS=500;
  (b) the Antigravity harness ran with a 10-minute `--print-timeout`, a real time cap that
  killed one actively-progressing run (48-spotify gemini-3.8-flash-low at 606s); it is now
  a 180-minute runaway-only valve, and that run is re-captured; (c) the muse stream parser
  recorded the terminal event's status line instead of the agent's transcript in two runs
  (a late "Server stopped" line); the concatenated output deltas are now authoritative and
  those two runs are re-judged on their real output, not re-run (the captures are intact).
  Headless rendering of archived Wayback pages is flaky (blank below the toolbar with DOM
  text present, seen in two runs); the one failed run is re-captured.
- 2026-09-02 (operator grind policy): an uncapped run that is still grinding on a widget
  after roughly 30 minutes of active work is terminated by the operator and scored on the
  evidence captured up to that point (no rerun). This tightens the earlier ~2h precedent;
  every previously successful uncapped Desmos/JS Paint solve finished inside 22 minutes, so
  the threshold clips no known winning pattern.
- 2026-09-03 (run budget): every run has a 10-minute wall-clock budget, enforced by the runners
  (`budget_exec.py`; the agent's process group is terminated at 600 s and the bundle records
  `budget_hit`). Tasks are designed to be finishable well inside that budget, so a budget-terminated run
  is an ordinary failure of the configuration, not a harness constraint: score it on the evidence
  captured up to termination (objective widget state as it stood; judged tasks fail unless the criteria
  were already met in a final answer). Budget-terminated runs are never re-captured for that reason
  alone. The agent prompt states the budget. Supersedes the 30-minute operator grind policy for all runs
  from this date; earlier runs keep their recorded verdicts.
- 2026-09-03 (browser CLI text truncation): the browser CLI's `type`/`fill` verbs kept only the first
  word of an unquoted multi-word value (plain and batch forms), while SKILL.md documented
  `type @e4 My project` as valid. Fixed in browser-cli (words after the target are joined) and installed
  before any Gemini or Sonnet round-2 wizard run. Runs that failed solely because a typed value was
  truncated by this defect are harness failures and are re-captured; a run that saw the truncated value
  on screen and still confirmed is judged on that evidence only when the defect is not the cause of the
  fail criterion. One affected run: 60-form-wizard spark-low-val (round 2, name "Priya Raman" arrived
  as "Priya").

## Re-audits

- 2026-08-31: all 36 pre-freeze PASS verdicts by haiku/gemini configs on the seven
  URL/filter-sensitive tasks (11, 14, 22, 23, 26, 27, 50) were re-audited under this
  frozen rubric with specific attention to rule #3. Result: 36/36 upheld, 0 overturned.
  Verdicts unchanged.
- 2026-09-02: every non-Haiku FAIL in the matrix (51 runs across 22 tasks and 22 configs)
  was re-audited adversarially, each classified by cause (model / prompt / site /
  wall / harness / terminated / judge) by Sonnet re-audit judges, with every non-model
  claim then verified by the operator against the daemon request log, stream, and video.
  Base rates: 17 of the 22 tasks were passed by over 91% of configs (13 by all but one),
  and failures spread across every model family, so no prompt or harness-specific defect
  explains them; the daemon's 10s idle-freeze was tested as a cause for the Desmos/JS Paint
  failures and rejected (passing runs sit equally past the freeze threshold; the fast
  failures had almost no freeze exposure). Dispositions: 38 upheld as genuine model
  failures; 9 harness-caused and re-captured (see the 2026-09-02 amendment); 2 muse runs
  re-judged on their reconstructed transcript; 2 judge errors flipped to PASS
  (17-currency luna-medium: the judge said the Numbeo price was missing but the captured
  end state contains it; 44-gcal gemini-3.7-flash-low: failed solely for deleting its own
  never-archived /tmp screenshot while the archived video holds the full pass evidence).
  Four agent claims of environment cause were overturned on evidence (a "hung CLI" that
  the daemon log shows completing in 0.1s before a 244s agent self-stall; a WebGL dialog
  that is a known constant 15 configs passed through; a "daemon freeze" whose gaps were
  model-side; a "prompt ambiguity" on a task 22/24 configs read correctly). Two automated
  environment signals (HARNESS_ERR, WALL_TEXT) were found to be regex false positives and
  discarded. Incident: a re-audit judge deleted an untracked screenshot that was in fact
  pass evidence for 55-wayback luna-medium; the verdict was re-derived from the archived
  video and a recovered frame saved alongside the bundle. Zero failures were attributable
  to prompt wording or site outages.
  Rerun outcomes (same day): three Desmos re-captures were operator-terminated under the
  30-minute grind policy and scored fail on captured evidence (the task is solved by 18/26
  configs, so the environment is not at fault); spotify gemini-3.8-flash-low and wayback
  luna-high re-captured cleanly and PASS; JS Paint opus-low re-captured and PASSES (five
  visible dots), sonnet-xhigh FAILS (faint single pixels, pixel-readback reliance). Two
  harness defects surfaced during the reruns and are fixed: (1) the recorder located the
  page by its REC-<sid> title and lost the race to the agent's first navigation on all seven
  uncapped Claude reruns (no video); setup now resolves the tab's DevTools ws URL before the
  agent starts and the recorder attaches by it; (2) agents save screenshots to shared names
  like /tmp/jspaint_final.jpg, so three consecutive reruns overwrote each other's final
  frame; record() now copies every screenshot into raw/ at capture time. A first judge pass
  on the four JS Paint reruns had cited "video frames" that could only have come from the
  previous attempt's archived videos; those four verdicts were discarded and the runs were
  re-judged strictly on their own timestamp-verified screenshots. The final-state evidence
  for JS Paint opus-xhigh and sonnet-medium was lost to defect (2); both are re-captured
  as a harness-defect remedy (not a retry for score), with the defective captures archived.

- **2026-09-03 agy quota guard false positive (harness, no runs affected).** The gemini-3.8-flash-high
  sweep paused at 19-wiktionary-wotd with "QUOTA hit" while the 5-hour quota stood at 78%. Cause:
  agy_one.sh's guard grepped the whole stream-json for "quota", "rate limit", "limit", "FAILED", and
  matched ordinary page content streamed back through tool outputs (a third of recorded 3.8 streams
  contain "limit"; a dictionary page contained "quota"). Fix: the guard now decides only from agy's
  own result event (status must be SUCCESS) and from agy's per-run stderr; a non-SUCCESS run stays
  un-recorded and retryable as before, but its stream is preserved as raw/<task>.<run>.failstream.txt
  so the cause can be inspected. The paused task was never recorded, so no verdict was affected; it
  is retried on the next resume pass.

- **2026-09-03 gemini-3.8-flash-high / 08-airport-departures: judge 'blocked' overturned to fail.**
  The judge accepted FlightAware's sign-in redirect on the expanded `/departures` and `/scheduled`
  boards as a forced-login wall and confirmed it with a live curl. Two problems: the live check is
  outside the offline-evidence rule, and the run's own captured output shows the airport page's
  embedded departures board listing 11 distinct US-bound destinations, from which the agent had
  already opened one flight page before abandoning the board, making 14 `search_web` calls, and
  asking the operator to sign in. 27 configurations completed the task from that embedded board
  without logging in. A login gate on a sub-page that the task does not need is not a wall under
  rule 6. Recorded as a model failure.
