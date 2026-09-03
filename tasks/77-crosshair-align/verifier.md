# 77-crosshair-align, verifier

**Method:** Programmatic (the widget's `/__state` is captured as `pixel_state`; `complete` is the verdict).

## Pass criteria

`pixel_state.complete` is true: at least one lock, the LAST lock within 3 px of the target centre, and no
more than two locks in total. Locking on the dashed decoy, or a third lock, fails.

**Endpoint bypass rule:** agent-driven calls to `/__move`, `/__lock`, `/__state`, or `/__reset` (eval/fetch,
navigate, or a shell tool) fail the run regardless of state; the page's own key handler uses them.
