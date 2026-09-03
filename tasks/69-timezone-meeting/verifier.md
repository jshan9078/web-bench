# 69-timezone-meeting, verifier

**Method:** LLM-as-judge (Claude).

Judging is **fully offline** from a captured evidence bundle, so a verdict can be re-derived
without re-running the model. For each run the judge is given the task prompt, the agent's final
answer and result text, the end-state page URL and text excerpt, the full browser command trace,
and the run's screenshots, video, and full model stream.

## Pass criteria

The planner must be configured in the trace with the three cities and next Monday's date (verify the
captured table header). Answer (1) must be consistent with the captured offsets: for offsets near -4/+2/+9
no slot exists and the answer must say so; a fabricated slot fails. Answer (2) must be the earliest
Toronto hour satisfying the stated windows given the captured offsets. The three UTC offsets match the
planner (DST-adjusted for that date).

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually
navigated to and evidence it captured THIS run. A correct-sounding answer with no supporting
navigation or capture in the trace fails, and where the live page disagrees with the answer, the
captured page wins.
