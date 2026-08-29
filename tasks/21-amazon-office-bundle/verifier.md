# 21-amazon-office-bundle, verifier

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

The cart evidence (screenshot plus cart text) shows both items, each item's captured rating is 4.0
or higher, the subtotal is under $100 pre-tax, and the trace shows both add-to-cart actions this
run. Leftover cart items without corresponding adds do not count.

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually
navigated to and evidence it captured THIS run. A correct-sounding answer with no supporting
navigation or capture in the trace fails, and where the live page disagrees with the answer, the
captured page wins.
