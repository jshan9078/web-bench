# 04-x-projects, verifier

**Method:** LLM-as-judge (Claude).

Judging is **fully offline** from a captured evidence bundle, so a verdict can be re-derived without re-running the model. For each run the judge is given:

- the task prompt (see `prompt.txt`)
- the agent's final answer and result text
- the **end-state** page URL and a text excerpt of the final page
- the full browser command trace (every `navigate`/`click`/`snapshot`/…, and the count of navigations)
- the run's video and full model stream (available if the judge wants to inspect them)

The judge rules **PASS** only if the criteria below are met **and** the answer is grounded in pages the agent actually navigated to this run (an answer with no supporting navigation fails). Verdicts are stored in `verdicts.json` via `harness.py set_verdict`; `harness.py judge_manifest` emits the evidence bundle.

## Pass criteria

The project list and direct links match what is reachable from the X profile, and the benchmarked models reported for the on-device SLM vulnerability-detection project match that project's linked article.
