# 96-slide-diff, verifier

**Method:** Programmatic (the site's `/__state` is captured as `pixel_state`; `complete` is the verdict).

## Pass criteria

`pixel_state.complete` is true: a submission names the changed row (label substring) and its amount equals the corrected value (digits compared).

**Endpoint rule:** the site's private endpoints (`/__data`, `/__slide`, `/__answer`, `/__state`, `/__reset`) require a per-page key and answer 403 to direct fetch/navigate/curl; any agent-driven attempt (eval/fetch, navigate, or a shell tool) additionally fails the run regardless of state.

**Grounding rule (pretraining defense):** the answer must be grounded in what the agent actually saw on the page THIS run.
