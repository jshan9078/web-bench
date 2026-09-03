# 86-chart-read, verifier

**Method:** Programmatic (the site's `/__state` is captured as `pixel_state`; `complete` is the verdict).

## Pass criteria

`pixel_state.complete` is true: a submission names the correct month (first three letters) and a value within 5 of the true value.

**Endpoint bypass rule:** agent-driven calls to `/__answer`, `/__state`, or `/__reset` (eval/fetch, navigate, or a shell tool) fail the run regardless of state.

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually navigated to and evidence it captured THIS run.
