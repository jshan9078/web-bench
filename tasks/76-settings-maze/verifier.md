# 76-settings-maze, verifier

**Method:** Programmatic (the site's `/__state` is captured as `pixel_state`; `complete` is the verdict).

## Pass criteria

`pixel_state.complete` is true: the saved settings equal the defaults with exactly display_name
"J. Halvorsen", digest "Monthly", and twostep true. Any other changed field (alerts, push, billing email,
session timeout, marketing) or a missing change fails. Unsaved edits do not count.

**Endpoint bypass rule:** agent-driven calls to `/__save`, `/__settings`, `/__state`, or `/__reset`
(eval/fetch, navigate, or a shell tool) fail the run regardless of state; the page's own JavaScript uses
`/__settings` and `/__save` legitimately and never appears in the browser command log.
