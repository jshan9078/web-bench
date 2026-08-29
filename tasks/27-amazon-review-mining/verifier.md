# 27-amazon-review-mining, verifier

**Method:** LLM-as-judge (Claude).

Judging is **fully offline** from a captured evidence bundle, so a verdict can be re-derived
without re-running the model. For each run the judge is given:

- the task prompt (see `prompt.txt`)
- the agent's final answer and result text
- the **end-state** page URL and a text excerpt of the final page
- the full browser command trace (every `navigate`/`click`/`screenshot`/... this run)
- the run's screenshots, video, and full model stream

## Pass criteria

Rating and count match the captured page; each of the three complaints is visibly supported by a
captured critical review dated within the last year. Recent-review content is time-anchored and
must come from pages in the trace, not remembered reputation. This task requires the signed-in
profile: Amazon hides critical-review listings from logged-out visitors; a run that cannot reach
them should ask the user, never fabricate.

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually
navigated to and evidence it captured THIS run. A correct-sounding answer with no supporting
navigation or capture in the trace fails, and where the live page disagrees with the answer, the
captured page wins.
