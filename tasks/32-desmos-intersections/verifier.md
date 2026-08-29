# 32-desmos-intersections, verifier

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

The screenshot (which the judge must open) shows both entered curves and a Desmos coordinate label
on the leftmost visible intersection, and the reported count and coordinates match that screenshot.
The tool's rendered label is the ground truth, not mental math; a report without the labeled
screenshot fails.

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually
navigated to and evidence it captured THIS run. A correct-sounding answer with no supporting
navigation or capture in the trace fails, and where the live page disagrees with the answer, the
captured page wins.
