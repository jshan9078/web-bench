# 75-map-explorer, verifier

**Method:** Programmatic (the site's `/__state` is captured as `pixel_state`; `complete` is the verdict).
The harness endpoint-bypass guard fails a run that calls `/__act` or `/__state` directly instead of using
the page.

## Pass criteria

`pixel_state.complete` is true: the target place's id is in `opened` (its popup was opened by clicking its
marker) and `routed` equals exactly `[target]` (Route clicked once, for the target only). Routing from any
other place fails. The reported category and distance are informational; the objective state decides.

**Endpoint bypass rule:** agent-driven calls to `/__act`, `/__state`, `/__reset` (eval/fetch, navigate, or a
shell tool) fail the run regardless of state; the page's own JavaScript calls `/__act` legitimately and never
appears in the browser command log. Viewing `__scene.png` directly is allowed.
