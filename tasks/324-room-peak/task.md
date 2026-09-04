# 324-room-peak

- **kind**: peak occupancy over video (programmatic)
- **site**: localhost widget (widgetapp/roompeak.py, port 8959)
- **what it tests**: tracking occupancy with two entry points and wandering targets
- **discrimination hypothesis**: occupancy must be maintained across 2 minutes with people moving; peak 6-10.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted number equals the peak.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8959/ . It is a clip in a player (canvas video with play/pause, seek, 1 s and 
10 s steps and playback speed; read frames from screenshots). It shows a meeting room from above 
for 2 minutes with two doors; people come and go through either door and move around inside. Report 
the maximum number of people that were inside the room at the same moment, enter it in the form 
under the player and submit. Do NOT read the page source or call the site's HTTP endpoints 
directly. End with the number.
```
