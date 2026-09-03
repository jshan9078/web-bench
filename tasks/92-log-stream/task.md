# 92-log-stream

- **kind**: live stream observation + cross-referencing (programmatic)
- **site**: localhost widget (widgetapp/logtail.py, port 8812, level 2)
- **what it tests**: correlating two transient lines in a fast stream (a payments ERROR and an earlier checkout WARN sharing a request id) using the viewer's filter and search over its buffer instead of sampling screenshots
- **discrimination hypothesis**: three payments ERRORs arrive over two minutes and only the middle one correlates; agents that report the first ERROR they see, or that never search the buffer for the request id, answer wrong. Several checkout WARNs with other request ids make a level-only filter insufficient. All timing windows are far above a harness round-trip.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: a submission's order id (digits) and reason code match the payments ERROR whose request id appears in an earlier checkout WARN.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8812/ . It is a live log tail for prod-web streaming several lines per 
second; the view shows only the latest matching lines, and there are level-filter, search and Pause 
controls. Over the next couple of minutes several ERROR-level lines from the "payments" service 
will appear. Exactly one of them has a request id (req=...) that ALSO appears in an EARLIER WARN 
line from the "checkout" service. Report that payments ERROR's order id and reason code. Enter both 
in the form at the bottom and submit. Do NOT read the page source or call the site's HTTP endpoints 
directly. End with the order id and reason.
```
