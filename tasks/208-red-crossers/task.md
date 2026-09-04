# 208-red-crossers

- **kind**: correlating two visual states over video (programmatic)
- **site**: localhost widget (widgetapp/redcrossers.py, port 8876)
- **what it tests**: attributing each crossing to the signal state at the moment it started
- **discrimination hypothesis**: the signal and the crossing are in different parts of the frame and the start moment matters; exact count.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of crossings started on DON'T WALK.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8876/ . It is a 2-minute crosswalk camera clip in a player (canvas video with 
play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots). A 
pedestrian signal at the top right cycles between WALK and DON'T WALK (red hand). People cross the 
road at various times. Count exactly how many people STARTED crossing while the signal showed DON'T 
WALK, enter the number in the form under the player and submit. Do NOT read the page source or call 
the site's HTTP endpoints directly. End with the count.
```
