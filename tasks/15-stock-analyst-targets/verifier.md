# 15-stock-analyst-targets, verifier

**Method:** LLM-as-judge (Claude).

Judging is **fully offline** from a captured evidence bundle, so a verdict can be re-derived
without re-running the model. For each run the judge is given:

- the task prompt (see `prompt.txt`)
- the agent's final answer and result text
- the **end-state** page URL and a text excerpt of the final page
- the full browser command trace (every `navigate`/`click`/`screenshot`/... this run)
- the run's screenshots, video, and full model stream

## Pass criteria

Price, day range, market cap, earnings date, and average price target match the pages captured this
run. All five are live market data and unknowable from pretraining; an answer without the visited
quote and analysis pages in the trace fails.

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually
navigated to and evidence it captured THIS run. A correct-sounding answer with no supporting
navigation or capture in the trace fails, and where the live page disagrees with the answer, the
captured page wins.
