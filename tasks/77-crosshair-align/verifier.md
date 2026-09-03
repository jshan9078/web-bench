# 77-crosshair-align, verifier

**Method:** Programmatic (the widget's `/__state` is captured as `pixel_state`; `complete` is the verdict).

## Pass criteria

`pixel_state.complete` is true: at least one lock, at level 2 (current) exactly one lock, within 2 px of the target centre (level 1 allowed 3 px and two
locks). Locking on the dashed decoy, or a second lock, fails.

**Endpoint bypass rule:** agent-driven calls to `/__move`, `/__lock`, `/__state`, or `/__reset` (eval/fetch,
navigate, or a shell tool) fail the run regardless of state; the page's own key handler uses them.
