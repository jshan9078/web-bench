# 38-seterra-europe, verifier

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

The trace shows repeated screenshot-then-pixel-click cycles on the quiz map, and the final
screenshot (which the judge must open) shows the quiz's own score/accuracy consistent with the
report after at least five prompts. Quiz prompt order varies; the performance is created state. Leniency note: the map has no zoom,
so microstates (San Marino, Monaco, Vatican, Andorra, Liechtenstein, Malta) are genuinely hard
pixel targets; a near-miss on a microstate with clearly correct intent should not by itself fail
the run, provided five prompts were attempted and the score display was captured.

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually
navigated to and evidence it captured THIS run. A correct-sounding answer with no supporting
navigation or capture in the trace fails, and where the live page disagrees with the answer, the
captured page wins.
