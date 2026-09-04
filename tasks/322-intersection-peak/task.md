# 322-intersection-peak

- **kind**: peak occupancy over video (programmatic)
- **site**: localhost widget (widgetapp/intersectionpeak.py, port 8957)
- **what it tests**: tracking simultaneous presence of cars in a zone over 2 minutes
- **discrimination hypothesis**: peak-occupancy counting failed Opus 5 low on the queue clip; cars arrive from four sides.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted number equals the peak.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8957/ . It is a clip in a player (canvas video with play/pause, seek, 1 s and 
10 s steps and playback speed; read frames from screenshots). It shows a four-way intersection from 
above for 2 minutes; cars enter the yellow central box from any side, wait, and leave. Report the 
maximum number of cars that were inside the yellow box at the same moment, enter it in the form 
under the player and submit. Do NOT read the page source or call the site's HTTP endpoints 
directly. End with the number.
```
