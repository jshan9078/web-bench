# 40-arxiv-pdf-figure, verifier

**Method:** LLM-as-judge (Claude).

Judging is **fully offline** from a captured evidence bundle, so a verdict can be re-derived
without re-running the model. For each run the judge is given:

- the task prompt (see `prompt.txt`)
- the agent's final answer and result text
- the **end-state** page URL and a text excerpt of the final page
- the full browser command trace (every `navigate`/`click`/`screenshot`/... this run)
- the run's screenshots, video, and full model stream

**Vision evidence:** this task's proof is visual. The judge MUST open the run's
screenshots (and the video if needed) rather than judging from text alone.

## Pass criteria

The paper is first on today's captured listing, and the title, author count, and figure
observation match the run's page-1 screenshot (which the judge must open). Today's listing did not
exist at training time; reading must be visual.

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually
navigated to and evidence it captured THIS run. A correct-sounding answer with no supporting
navigation or capture in the trace fails, and where the live page disagrees with the answer, the
captured page wins.
