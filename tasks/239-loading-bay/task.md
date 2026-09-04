# 239-loading-bay

- **kind**: outcome attribution over video (programmatic)
- **site**: localhost widget (widgetapp/dockloading.py, port 8902)
- **what it tests**: following each carried box to the store room or the reject bin
- **discrimination hypothesis**: the diversion happens mid-walk; exact count.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of boxes reaching the store room.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8902/ . It is a 2-minute loading bay camera clip in a player (canvas video 
with play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots). 
Workers carry boxes from the truck on the left toward the store room on the right; some boxes are 
diverted into the red REJECT bin in the middle instead. Count exactly how many boxes were carried 
into the store room, enter the number in the form under the player and submit. Do NOT read the page 
source or call the site's HTTP endpoints directly. End with the count.
```
