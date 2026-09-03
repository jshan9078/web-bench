# 118-odometer-read

- **kind**: seven-segment reading under glare (programmatic)
- **site**: localhost widget (widgetapp/odometer.py, port 8836)
- **what it tests**: reading a six-digit seven-segment odometer at a slight angle under glare, and not the trip meter beside it
- **discrimination hypothesis**: seven-segment 0/8/6/9 and 1/7 confusions under glare are common; the trip meter in the same style is the decoy; the answer is exact.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the submitted number equals the odometer reading.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8836/ . It is a dashboard photo taken for a mileage check (read it from 
screenshots; there is some glare). Report the ODOMETER reading (total distance in km, not the trip 
meter), enter the number in the form below the photo and submit. Do NOT read the page source or 
call the site's HTTP endpoints directly. End with the reading.
```
