# 290-freeze-sum

- **kind**: acting on a moment then reading it (programmatic)
- **site**: localhost widget (widgetapp/freezesum.py, port 8937)
- **what it tests**: freezing a changing table and summing the values that were frozen
- **discrimination hypothesis**: the values change every 3 s; summing from a stale screenshot fails; arithmetic on six numbers must be exact.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted sum equals the frozen sum.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8937/ . It is a live metrics table whose six values change every 3 seconds. 
Press Freeze to lock the table, then add up the six frozen Requests values and enter the sum in the 
form and submit. Do NOT read the page source or call the site's HTTP endpoints directly. End with 
the sum.
```
