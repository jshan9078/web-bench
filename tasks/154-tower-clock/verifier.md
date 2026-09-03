# 154-tower-clock, verifier

**Method:** Programmatic (the site's `/__state` is captured as `pixel_state`; `complete` is the verdict).

## Pass criteria

`pixel_state.complete` is true: the last submitted time is within 2 minutes of the tower clock (12-hour).

**Endpoint rule:** the site's private endpoints require a per-page key and answer 403 to direct fetch/navigate/curl; any agent-driven attempt (eval/fetch, navigate, or a shell tool) additionally fails the run regardless of state. Rendered images (`/__scene.png`, the magnifier crop) are open: they are what the page shows.

**Grounding rule (pretraining defense):** the answer must be grounded in what the agent actually saw on the page THIS run.
