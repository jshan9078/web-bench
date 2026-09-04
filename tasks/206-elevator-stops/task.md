# 206-elevator-stops

- **kind**: state-change counting over video (programmatic)
- **site**: localhost widget (widgetapp/elevatorstops.py, port 8875)
- **what it tests**: counting door-opening stops of an elevator while the floor indicator changes continuously
- **discrimination hypothesis**: stops last four seconds between travel segments; passes without stopping are the trap; exact count.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of stops.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8875/ . It is a 2-minute clip of an elevator indicator and doors in a player 
(canvas video with play/pause, seek, 1 s and 10 s steps and playback speed; read frames from 
screenshots). The floor display changes as the car travels; sometimes the car stops and the doors 
open, sometimes it passes floors without stopping. Count exactly how many times the car stopped 
with its doors opening during the clip, enter the number in the form under the player and submit. 
Do NOT read the page source or call the site's HTTP endpoints directly. End with the count.
```
