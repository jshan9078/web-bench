# 336-red-light-runners

- **kind**: counting over video (programmatic)
- **site**: localhost widget (widgetapp/redlightrunners.py, port 8970)
- **what it tests**: counting line crossings conditioned on signal state
- **discrimination hypothesis**: each crossing lasts under a second; ~30 cars; the phase at the moment of crossing matters.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted value equals the true value.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8970/ . It is a clip in a player (canvas video with play/pause, seek, 1 s and 
10 s steps and playback speed; read frames from screenshots). It is a 2-minute junction recording 
with a traffic light and a white stop line; cars drive left to right in two lanes at any time. 
Count exactly how many cars crossed the stop line while the light was RED, enter the number in the 
form under the player and submit. Do NOT read the page source or call the site's HTTP endpoints 
directly. End with the count.
```
