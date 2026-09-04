# 318-week-free-time

- **kind**: calendar free-time judgement (programmatic)
- **site**: localhost widget (widgetapp/weekfree.py, port 8956)
- **what it tests**: computing free hours from a week view with overlaps and busy/free all-day items
- **discrimination hypothesis**: calendar judgement failed Opus 5 low on Google Calendar; local, deterministic version.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted number equals the free hours.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8956/ . It is a week-view calendar. Answer the question shown at the top: how 
many hours are free on the named day between 09:00 and 17:00, counting overlapping meetings once 
and treating all-day items as blocking the whole day only when they are marked busy. Enter the 
number of hours (decimals allowed, e.g. 4.5) in the form and submit. Do NOT read the page source or 
call the site's HTTP endpoints directly. End with the number.
```
