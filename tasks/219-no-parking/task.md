# 219-no-parking

- **kind**: zone attribution over video (programmatic)
- **site**: localhost widget (widgetapp/noparking.py, port 8881)
- **what it tests**: counting distinct cars that stopped in a marked zone, ignoring bay parkers and pass-throughs
- **discrimination hypothesis**: stops in the zone last four to nine seconds; drive-throughs in the adjacent lane and bay parkers are decoys; exact count.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of cars that stopped in the zone.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8881/ . It is a 2-minute street camera clip in a player (canvas video with 
play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots). Cars arrive 
from the left; some park in the marked bays, some stop in the hatched NO PARKING zone, and some 
just drive past without stopping. Count exactly how many different cars stopped in the NO PARKING 
zone during the clip, enter the number in the form under the player and submit. Do NOT read the 
page source or call the site's HTTP endpoints directly. End with the count.
```
