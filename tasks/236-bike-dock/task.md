# 236-bike-dock

- **kind**: net-flow accounting over video (programmatic)
- **site**: localhost widget (widgetapp/bikedock.py, port 8899)
- **what it tests**: computing the final dock count from a shown start count and a sequence of docks and undocks
- **discrimination hypothesis**: each event must be attributed to a direction and summed; the rack itself offers a check at the end; exact.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the final number docked.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8899/ . It is a 2-minute bike-share dock camera clip in a player (canvas 
video with play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots). 
Riders dock bikes (arriving from the left) and undock bikes (riding away to the right); the number 
docked at the start is shown on screen. Work out exactly how many bikes are in the dock at the END 
of the clip, enter the number in the form under the player and submit. Do NOT read the page source 
or call the site's HTTP endpoints directly. End with the count.
```
