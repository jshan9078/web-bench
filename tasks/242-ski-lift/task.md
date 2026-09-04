# 242-ski-lift

- **kind**: per-chair occupancy counting over video (programmatic)
- **site**: localhost widget (widgetapp/liftqueue.py, port 8905)
- **what it tests**: counting skiers boarding chairs that pass every few seconds, with zero, one or two per chair
- **discrimination hypothesis**: chairs are frequent and occupancy varies; exact count.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of skiers boarded.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8905/ . It is a 2-minute chairlift base camera clip in a player (canvas video 
with play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots). Chairs 
pass along the cable every few seconds; at the base, skiers waiting on the snow board some chairs 
(one or two per chair) while other chairs go up empty. Count exactly how many skiers boarded during 
the clip, enter the number in the form under the player and submit. Do NOT read the page source or 
call the site's HTTP endpoints directly. End with the count.
```
