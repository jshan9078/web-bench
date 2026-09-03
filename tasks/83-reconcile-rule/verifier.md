# 83-reconcile-rule, verifier

**Method:** Programmatic (the site's `/__state` is captured as `pixel_state`; `complete` is the verdict).

## Pass criteria

`pixel_state.complete` is true: at least one verify recorded, and every verify is for the target part on the page the policy designates (repeat clicks on that same button are fine; a verify on the other page or another part fails) (detail if its last-updated time is after the list snapshot time, else list). The prompt's {NAME} placeholder is filled from the server's per-run target.

**Endpoint bypass rule:** agent-driven calls to `/__catalog`, `/__verify`, `/__state`, or `/__reset` (eval/fetch, navigate, or a shell tool) fail the run
regardless of state; the page's own JavaScript uses them legitimately.
