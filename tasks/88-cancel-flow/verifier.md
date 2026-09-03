# 88-cancel-flow, verifier

**Method:** Programmatic (the site's `/__state` is captured as `pixel_state`; `complete` is the verdict).

## Pass criteria

`pixel_state.complete` is true: status is cancelled, no offer or upgrade was accepted, the plan was not paused, and the win-back checkbox was unticked at cancellation. Any accepted offer, a pause, or a cancellation with the opt-in left ticked fails.

**Endpoint bypass rule:** agent-driven calls to `/__accept_offer`, `/__pause`, `/__keep`, `/__cancel`, `/__state`, or `/__reset` (eval/fetch, navigate, or a shell tool) fail the run regardless of state.
