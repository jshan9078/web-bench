# 90-dial-set, verifier

**Method:** Programmatic (the widget's `/__state` is captured as `pixel_state`; `complete` is the verdict).

## Pass criteria

`pixel_state.complete` is true: exactly one confirmation, and the confirmed value is within 1.0 of the target (the scale has a tick per unit and the needle moves in half-unit steps, so this is one tick either side). A second confirmation, or a value further off, fails.

**Endpoint bypass rule:** agent-driven calls to `/__turn`, `/__confirm`, `/__state`, or `/__reset` (eval/fetch, navigate, or a shell tool) fail the run regardless of state.
