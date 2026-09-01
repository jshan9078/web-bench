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

## Re-audits

- 2026-08-31: all 36 pre-freeze PASS verdicts by haiku/gemini configs on the seven
  URL/filter-sensitive tasks (11, 14, 22, 23, 26, 27, 50) were re-audited under this
  frozen rubric with specific attention to rule #3. Result: 36/36 upheld, 0 overturned.
  Verdicts unchanged.
