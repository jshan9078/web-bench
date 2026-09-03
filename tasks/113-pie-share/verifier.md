# 113-pie-share, verifier

**Method:** Programmatic (the site's `/__state` is captured as `pixel_state`; `complete` is the verdict).

## Pass criteria

`pixel_state.complete` is true: the submitted share is within 4 points of the segment's true share.

**Endpoint rule:** the site's private endpoints require a per-page key and answer 403 to direct fetch/navigate/curl; any agent-driven attempt (eval/fetch, navigate, or a shell tool) additionally fails the run regardless of state. The rendered image (`/__scene.png`) is open: it is what the page shows.

**Grounding rule (pretraining defense):** the answer must be grounded in what the agent actually saw on the page THIS run.
