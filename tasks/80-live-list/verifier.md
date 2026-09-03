# 80-live-list, verifier

**Method:** Programmatic (the site's `/__state` is captured as `pixel_state`; `complete` is the verdict).

## Pass criteria

`pixel_state.complete` is true: exactly one restart was requested, and the server's record shows that host
was the top-CPU host in the refresh window in which the Restart BUTTON was pressed (the confirm click may
land in the next window without penalty). Restarting a host that had
been top in an earlier window fails; more than one restart fails.

**Endpoint bypass rule:** agent-driven calls to `/__rows`, `/__restart`, `/__state`, or `/__reset`
(eval/fetch, navigate, or a shell tool) fail the run regardless of state; the page's own JavaScript polls
`/__rows` and posts `/__restart` legitimately and never appears in the browser command log.

**Latency independence:** the 12-second window is far above any harness round-trip, so a fail here means
the agent acted on a reading from an earlier window, never that its tooling was slow.
