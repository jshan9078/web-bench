# 81-memory-flow, verifier

**Method:** Programmatic (the site's `/__state` is captured as `pixel_state`; `complete` is the verdict).

## Pass criteria

`pixel_state.complete` is true: the last submission belongs to the current flow instance, its code equals that instance's code, and its room equals both the room chosen at step 2 and the room the page named as the installation location. A stale code from an earlier instance, the device serial, or a different room fails.

**Endpoint bypass rule:** agent-driven calls to `/__start`, `/__choose`, `/__finish`, `/__state`, or `/__reset` (eval/fetch, navigate, or a shell tool) fail the run
regardless of state; the page's own JavaScript uses them legitimately.
