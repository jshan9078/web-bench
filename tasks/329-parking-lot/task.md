# 329-parking-lot

- **kind**: counting over video (programmatic)
- **site**: localhost widget (widgetapp/parkinglot.py, port 8963)
- **what it tests**: peak occupancy of an 8-space lot over 2 minutes
- **discrimination hypothesis**: peak occupancy failed both Claude configs before; long dwell times force full-clip tracking.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the true count.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8963/ . It is a clip in a player (canvas video with play/pause, seek, 1 s and 
10 s steps and playback speed; read frames from screenshots). It shows an 8-space car park for 2 
minutes; cars arrive, park and leave. Report the maximum number of cars parked at the same moment, 
enter it in the form under the player and submit. Do NOT read the page source or call the site's 
HTTP endpoints directly. End with the number.
```
