# 313-clock-grid

- **kind**: analog clock reading among decoys (programmatic)
- **site**: localhost widget (widgetapp/clockgrid.py, port 8951)
- **what it tests**: reading hour and minute hands on an unnumbered dial to the minute
- **discrimination hypothesis**: clock reading is the Opus 5 low weak spot in earlier rounds; six dials, one target.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted time is within one minute.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8951/ . The page shows an IMAGE of six analog clocks without numerals (read 
it from screenshots). Report the time shown by the clock with the RED rim as HH:MM (12-hour, within 
one minute), enter it in the form and submit. Do NOT read the page source or call the site's HTTP 
endpoints directly. End with the time.
```
