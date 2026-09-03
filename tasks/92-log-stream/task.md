# 92-log-stream

- **kind**: live stream observation (programmatic)
- **site**: localhost widget (widgetapp/logtail.py, port 8812)
- **what it tests**: catching a transient event in a fast log stream where an unfiltered view holds only the last ~10 s: using the filter/search/Pause controls (or polling often enough) instead of sampling a few screenshots
- **discrimination hypothesis**: sampling agents miss the line entirely or report the second payments ERROR (45 s later); keyword matchers report the payments WARN lines that contain error= or the earlier checkout ERROR. Timing windows are far above a harness round-trip.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: a submission's order id (digits) and reason code match the first payments ERROR line.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8812/ . It is a live log tail for prod-web streaming several lines per 
second; the view shows only the latest matching lines, and there are level-filter, search and Pause 
controls. Within about a minute an ERROR-level line from the "payments" service will appear. Report 
the order id and the reason code from the FIRST ERROR-level payments line (not WARN lines, not 
other services). Enter both in the form at the bottom and submit. Do NOT read the page source or 
call the site's HTTP endpoints directly. End with the order id and reason.
```
