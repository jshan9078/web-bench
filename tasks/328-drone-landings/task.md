# 328-drone-landings

- **kind**: counting over video (programmatic)
- **site**: localhost widget (widgetapp/dronepads.py, port 8962)
- **what it tests**: counting landings on one of three pads over 2 minutes
- **discrimination hypothesis**: landings are events, not states; pad B must be distinguished; ~7 target events.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the true count.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8962/ . It is a clip in a player (canvas video with play/pause, seek, 1 s and 
10 s steps and playback speed; read frames from screenshots). It shows three landing pads A, B and 
C for 2 minutes; drones fly in, land on a pad, and take off again. Count exactly how many drones 
LANDED on pad B, enter the number in the form under the player and submit. Do NOT read the page 
source or call the site's HTTP endpoints directly. End with the count.
```
