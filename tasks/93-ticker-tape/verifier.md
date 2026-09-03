# 93-ticker-tape, verifier

**Method:** Programmatic (the site's `/__state` is captured as `pixel_state`; `complete` is the verdict).

## Pass criteria

`pixel_state.complete` is true: the submitted symbol is the true top gainer on the tape (percentage within 0.15).

**Endpoint bypass rule:** agent-driven calls to any `/__*` endpoint of the site (`/__data`, `/__frame`, `/__lines`, `/__answer`, `/__state`, `/__reset`) via eval/fetch, navigate, or a shell tool fail the run regardless of state. The page's own JavaScript calls them legitimately; those never appear in the agent's command log.

**Grounding rule (pretraining defense):** the answer must be grounded in what the agent actually saw on the page THIS run.
