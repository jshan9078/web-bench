# 185-belt-defects

- **kind**: detail counting over video (programmatic)
- **site**: localhost widget (widgetapp/beltdefects.py, port 8868)
- **what it tests**: spotting a small visual detail (missing cap) on 30-40 items passing at speed and counting exactly
- **discrimination hypothesis**: items pass in five seconds; sampled frames miss items; the detail is small; exactness required.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of capless bottles.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8868/ . It is a 2-minute bottling-line inspection clip in a player (canvas 
video with play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots). 
Bottles pass left to right; a correctly capped bottle has a red cap, a defective one has no cap. 
Count exactly how many defective (capless) bottles pass during the clip, enter the number in the 
form under the player and submit. Do NOT read the page source or call the site's HTTP endpoints 
directly. End with the count.
```
