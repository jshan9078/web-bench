# 271-moving-target

- **kind**: re-observe before acting under DOM reshuffles (programmatic)
- **site**: localhost widget (widgetapp/movingtarget.py, port 8930)
- **what it tests**: identifying a subtly marked element among identical siblings whose order changes every 5 seconds, five times in a row
- **discrimination hypothesis**: acting on a stale snapshot clicks a decoy; the window is generous relative to a round trip; five consecutive successes are required.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the best streak reached 5.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8930/ . The page shows twelve buttons that all say Proceed; only the one with 
a small blue dot inside it is real, and the buttons reshuffle every 5 seconds. Click the real 
Proceed button five times in a row (a click on a decoy resets the streak; the page shows the 
streak). Take a fresh look before each click. Do NOT read the page source or call the site's HTTP 
endpoints directly. End with a one-line confirmation.
```
