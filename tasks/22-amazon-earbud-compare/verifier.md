# 22-amazon-earbud-compare, verifier

**Method:** LLM-as-judge (Claude).

Judging is **fully offline** from a captured evidence bundle, so a verdict can be re-derived
without re-running the model. For each run the judge is given:

- the task prompt (see `prompt.txt`)
- the agent's final answer and result text
- the **end-state** page URL and a text excerpt of the final page
- the full browser command trace (every `navigate`/`click`/`screenshot`/... this run)
- the run's screenshots, video, and full model stream
- a **screenshot of the cart** plus the cart's extracted contents (items / ASINs)

## Pass criteria

Both products' price/rating/count/battery figures match their captured pages, the added item is the
higher-rated of the two, and the cart evidence plus trace confirm the add happened this run. Live
listings and ratings make the comparison unanswerable from memory.

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually
navigated to and evidence it captured THIS run. A correct-sounding answer with no supporting
navigation or capture in the trace fails, and where the live page disagrees with the answer, the
captured page wins.
