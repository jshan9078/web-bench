# 238-jaywalkers

- **kind**: location attribution over video (programmatic)
- **site**: localhost widget (widgetapp/pedxing.py, port 8901)
- **what it tests**: attributing each crossing to the zebra or elsewhere across 18-26 crossings
- **discrimination hypothesis**: crossings in both directions at four positions; exact count.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of crossings away from the zebra.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8901/ . It is a 2-minute road camera clip in a player (canvas video with 
play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots). Pedestrians 
cross the road either on the zebra crossing in the middle or away from it. Count exactly how many 
people crossed AWAY from the zebra crossing, enter the number in the form under the player and 
submit. Do NOT read the page source or call the site's HTTP endpoints directly. End with the count.
```
