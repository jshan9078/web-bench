# 265-timesheet-entry

- **kind**: transcribing a log into a grid (programmatic)
- **site**: localhost widget (widgetapp/timesheet.py, port 8923)
- **what it tests**: mapping 11 log entries into a projects-by-days grid with a daily cap and submitting
- **discrimination hypothesis**: one misplaced cell fails; the cap rejects an over-entry; exactness on 20 cells.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the submitted grid equals the log.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8923/ . It is a weekly timesheet grid with a work log in the notes panel. 
Enter every hour from the work log into the matching project and day cells (leave other cells at 
0), make sure no day exceeds 8 hours, and submit the timesheet (the page confirms). Do NOT read the 
page source or call the site's HTTP endpoints directly. End with the weekly total.
```
