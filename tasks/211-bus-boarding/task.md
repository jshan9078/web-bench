# 211-bus-boarding

- **kind**: directional counting at events over video (programmatic)
- **site**: localhost widget (widgetapp/busboard.py, port 8878)
- **what it tests**: counting boardings across several bus stops, distinguishing boarding from alighting passengers at the door
- **discrimination hypothesis**: passengers move through the door one after another in both directions; direction is the only cue; exact count.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of boardings.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8878/ . It is a 2-minute bus-stop camera clip in a player (canvas video with 
play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots). A bus stops 
several times; at each stop some passengers get off (moving down from the door) and some get on 
(moving up into the door). Count exactly how many passengers BOARDED during the whole clip, enter 
the number in the form under the player and submit. Do NOT read the page source or call the site's 
HTTP endpoints directly. End with the count.
```
