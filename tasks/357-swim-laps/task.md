# 357-swim-laps

- **kind**: single-target tracking among similar movers (programmatic)
- **site**: localhost widget (widgetapp/swimlaps.py, port 8988)
- **what it tests**: counting lengths of one swimmer over 2 minutes while three others swim at other speeds
- **discrimination hypothesis**: requires following one lane through ~10 turns; sampling every 10 s loses count.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted value equals the true value.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8988/ . It is a clip in a player (canvas video with play/pause, seek, 1 s and 
10 s steps and playback speed; read frames from screenshots). It shows a four-lane pool for 2 
minutes; each swimmer swims wall to wall, pauses, and turns. Count exactly how many pool lengths 
(wall to wall) the swimmer with the RED cap completed by the end of the clip, enter the number in 
the form under the player and submit. Do NOT read the page source or call the site's HTTP endpoints 
directly. End with the count.
```
