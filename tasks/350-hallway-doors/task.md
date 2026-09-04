# 350-hallway-doors

- **kind**: destination attribution over video (programmatic)
- **site**: localhost widget (widgetapp/hallwaydoors.py, port 8983)
- **what it tests**: tracking which door each passer-by enters
- **discrimination hypothesis**: people fade into doors; walk-throughs and neighbouring doors are decoys; ~8 targets.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted value equals the true value.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8983/ . It is a clip in a player (canvas video with play/pause, seek, 1 s and 
10 s steps and playback speed; read frames from screenshots). It shows a hallway with five numbered 
doors for 2 minutes; people walk along it and either enter a room or walk through. Count exactly 
how many people entered ROOM 3, enter the number in the form under the player and submit. Do NOT 
read the page source or call the site's HTTP endpoints directly. End with the count.
```
