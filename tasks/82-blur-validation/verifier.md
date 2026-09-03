# 82-blur-validation, verifier

**Method:** Programmatic (the site's `/__state` is captured as `pixel_state`; `complete` is the verdict).

## Pass criteria

`pixel_state.complete` is true: some recorded submission has no errors and equals the target address field for field (postal code compared case-insensitively). A submission that saved the billing address (pre-ticked option left on) fails even though the page showed a reference.

**Endpoint bypass rule:** agent-driven calls to `/__validate`, `/__submit`, `/__state`, or `/__reset` (eval/fetch, navigate, or a shell tool) fail the run
regardless of state; the page's own JavaScript uses them legitimately.
