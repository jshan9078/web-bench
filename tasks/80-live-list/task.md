# 80-live-list

- **kind**: action + timing + state (programmatic)
- **site**: localhost test site (widgetapp/livelist.py, port 8800)
- **what it tests**: acting on a page that changes under you: reading a live table, choosing the target from current values (two hosts within three points at the top), clicking by a fresh handle rather than by a stale coordinate, confirming a transient dialog, within one refresh window (4 s)
- **discrimination hypothesis**: agents that screenshot, think, then click coordinates restart whatever host moved into that row; agents that snapshot and click by ref (or read and act in one batch) succeed. It measures the read-act loop that live dashboards demand, not length.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: exactly one restart, and its host was the top-CPU host at the instant of the click.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8800/ , a live fleet console: the metrics refresh every few seconds and the table
REORDERS on every refresh, so row positions are never stable. Restart the ONE server that is using the
MOST CPU at the moment you act: read the current table, identify the top-CPU host, click that host's
Restart button and confirm in the dialog (the dialog closes on its own after a few seconds). Two hosts are
usually close at the top, so read the numbers rather than the bar lengths, and act within the same refresh
window as your reading (a click aimed from a stale screenshot lands on whatever row has moved there).
Restart exactly one server. Work through the page's UI only: do NOT read the page source or call the
site's HTTP endpoints directly. End by naming the host you restarted and its CPU figure.
```
