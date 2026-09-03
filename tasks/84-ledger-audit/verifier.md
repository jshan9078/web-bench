# 84-ledger-audit, verifier

**Method:** Programmatic (the site's `/__state` is captured as `pixel_state`; `complete` is the verdict).

## Pass criteria

`pixel_state.complete` is true: a submission names the correct vendors for both extremes (case-insensitive) and the Q4 total within 0.005.

**Endpoint bypass rule:** agent-driven calls to `/__answer`, `/__state`, or `/__reset` (eval/fetch, navigate, or a shell tool) fail the run regardless of state.

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually navigated to and evidence it captured THIS run.
