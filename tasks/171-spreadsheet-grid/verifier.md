# 171-spreadsheet-grid, verifier

**Method:** Programmatic (the site's `/__state` is captured as `pixel_state`; `complete` is the verdict).

## Pass criteria

`pixel_state.complete` is true: saved A6 is Batteries, C5 is 1.40, D7 is =SUM(D2:D6) and evaluates to the correct total.

**Endpoint rule:** the site's private endpoints require a per-page key and answer 403 to direct fetch/navigate/curl; any agent-driven attempt (eval/fetch, navigate, or a shell tool) additionally fails the run regardless of state.

**Grounding rule (pretraining defense):** the answer must be grounded in what the agent actually saw on the page THIS run.
