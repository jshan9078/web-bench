# 66-wiki-table-reconcile, verifier

**Method:** LLM-as-judge (Claude).

Judging is **fully offline** from a captured evidence bundle, so a verdict can be re-derived
without re-running the model. For each run the judge is given the task prompt, the agent's final
answer and result text, the end-state page URL and text excerpt, the full browser command trace,
and the run's screenshots, video, and full model stream.

## Pass criteria

The trace must show the sort control being used and the table order changing (screenshot or page text
after sorting). The three buildings are the top three by completion year on the captured table (ties
broken as the table displays them). Architect, floor count, and infobox height match each captured
article; the agreement statement is correct for each. Using the table's default order, or reporting
infobox values without opening the article, fails.

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually
navigated to and evidence it captured THIS run. A correct-sounding answer with no supporting
navigation or capture in the trace fails, and where the live page disagrees with the answer, the
captured page wins.
