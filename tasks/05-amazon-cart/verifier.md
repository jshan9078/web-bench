# 05-amazon-cart, verifier

**Method:** LLM-as-judge (Claude).

Judging is **fully offline** from a captured evidence bundle, so a verdict can be re-derived without re-running the model. For each run the judge is given:

- the task prompt (see `prompt.txt`)
- the agent's final answer and result text
- the **end-state** page URL and a text excerpt of the final page
- a **screenshot of the cart** plus the cart's extracted contents (items / ASINs)
- the full browser command trace (every `navigate`/`click`/`snapshot`/…, and the count of navigations)
- the run's video and full model stream (available if the judge wants to inspect them)

The judge rules **PASS** only if the criteria below are met **and** the answer is grounded in pages the agent actually navigated to this run (an answer with no supporting navigation fails). Verdicts are stored in `verdicts.json` via `harness.py set_verdict`; `harness.py judge_manifest` emits the evidence bundle.

## Pass criteria

The cart screenshot shows BOTH products and the command trace shows the two add-to-cart actions this run (leftover items from earlier runs do not count without the corresponding adds).
