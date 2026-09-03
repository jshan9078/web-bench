# 60-form-wizard, verifier

**Method:** Programmatic (the local widget server's `/__state` is captured into the bundle as `pixel_state`; `complete` is the verdict). No LLM judge.

Judging is **fully offline** from a captured evidence bundle, so a verdict can be re-derived
without re-running the model. For each run the judge is given the task prompt, the agent's final
answer and result text, the end-state page URL and text excerpt, the full browser command trace,
and the run's screenshots, video, and full model stream.

## Pass criteria

`pixel_state.complete` is true: a submission matches the expected name and email, `option == answer`, `confirmed` is true, and it was submitted at least 7.5 s after step 3 began.

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually
navigated to and evidence it captured THIS run. A correct-sounding answer with no supporting
navigation or capture in the trace fails, and where the live page disagrees with the answer, the
captured page wins.
