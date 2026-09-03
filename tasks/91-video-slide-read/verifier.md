# 91-video-slide-read, verifier

**Method:** Programmatic (the site's `/__state` is captured as `pixel_state`; `complete` is the verdict).

## Pass criteria

`pixel_state.complete` is true: a submitted figure equals the one the pointer rests on during the target sentence (digits compared).

**Endpoint bypass rule:** agent-driven calls to any `/__*` endpoint of the site (`/__data`, `/__frame`, `/__lines`, `/__answer`, `/__state`, `/__reset`) via eval/fetch, navigate, or a shell tool fail the run regardless of state. The page's own JavaScript calls them legitimately; those never appear in the agent's command log.

**Grounding rule (pretraining defense):** the answer must be grounded in what the agent actually saw on the page THIS run.
