# 224-crane-lifts

- **kind**: direction attribution over video (programmatic)
- **site**: localhost widget (widgetapp/cranelifts.py, port 8887)
- **what it tests**: tracking each container lift's direction between ship and quay
- **discrimination hypothesis**: lifts take six seconds and alternate irregularly; the quay stack offers a check; exact count.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of ship-to-quay moves.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8887/ . It is a 2-minute port crane camera clip in a player (canvas video 
with play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots). A 
gantry crane lifts containers between the ship on the right and the quay on the left, in both 
directions. Count exactly how many containers were moved from the SHIP to the QUAY, enter the 
number in the form under the player and submit. Do NOT read the page source or call the site's HTTP 
endpoints directly. End with the count.
```
