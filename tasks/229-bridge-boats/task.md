# 229-bridge-boats

- **kind**: state-gated event counting over video (programmatic)
- **site**: localhost widget (widgetapp/liftbridge.py, port 8892)
- **what it tests**: counting boats that passed while the bridge was raised, excluding those that turned back
- **discrimination hypothesis**: boats approach identically; the bridge state decides; exact count.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of boats that passed.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8892/ . It is a 2-minute canal camera clip in a player (canvas video with 
play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots). Boats 
approach a lift bridge from both sides; when the bridge is RAISED they pass under it, when it is 
DOWN they turn back. Count exactly how many boats passed under the bridge, enter the number in the 
form under the player and submit. Do NOT read the page source or call the site's HTTP endpoints 
directly. End with the count.
```
