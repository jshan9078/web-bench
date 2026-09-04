# 338-forklift-trips

- **kind**: counting over video (programmatic)
- **site**: localhost widget (widgetapp/forklifttrips.py, port 8972)
- **what it tests**: classifying trips by direction and load over 2 minutes
- **discrimination hypothesis**: two aisles interleave; empty and reverse trips are decoys; ~10 target trips.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted value equals the true value.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8972/ . It is a clip in a player (canvas video with play/pause, seek, 1 s and 
10 s steps and playback speed; read frames from screenshots). It is a 2-minute warehouse recording: 
forklifts in two aisles shuttle between the rack on the left and the dock on the right, sometimes 
carrying a brown pallet and sometimes empty. Count exactly how many trips carried a pallet from 
LEFT to RIGHT, enter the number in the form under the player and submit. Do NOT read the page 
source or call the site's HTTP endpoints directly. End with the count.
```
