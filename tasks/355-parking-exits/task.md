# 355-parking-exits

- **kind**: exit attribution over video (programmatic)
- **site**: localhost widget (widgetapp/parkingexits.py, port 8986)
- **what it tests**: attributing each departure to one of two exits over 2 minutes with arrivals as distractors
- **discrimination hypothesis**: departures take 4 s; two exits; ~12 targets.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted value equals the true value.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8986/ . It is a clip in a player (canvas video with play/pause, seek, 1 s and 
10 s steps and playback speed; read frames from screenshots). It shows a ten-space car park for 2 
minutes with EXIT A at the top and EXIT B on the right; cars leave through one of the exits and new 
cars arrive. Count exactly how many cars left through EXIT B, enter the number in the form under 
the player and submit. Do NOT read the page source or call the site's HTTP endpoints directly. End 
with the count.
```
