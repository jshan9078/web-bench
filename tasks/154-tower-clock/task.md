# 154-tower-clock

- **kind**: find + zoom + analog reading (programmatic)
- **site**: localhost widget (widgetapp/towerclock.py, port 8850)
- **what it tests**: locating a small clock in a webcam still, using the magnifier, and reading hour and minute hands with tick-only markings
- **discrimination hypothesis**: unzoomed reading is unreliable and analog reading has already beaten one config twice; both must go right.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted time is within 2 minutes of the tower clock (12-hour).

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8850/ . It is a town-square webcam still with a clock on the tower; the clock 
is small, and the page has a magnifier (click the photo to zoom into that area). What time does the 
tower clock show? Enter it as HH:MM (12-hour, within 2 minutes) in the form below the photo and 
submit. Do NOT read the page source or call the site's HTTP endpoints directly. End with the time.
```
