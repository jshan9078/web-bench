# 339-birds-on-wire

- **kind**: counting over video (programmatic)
- **site**: localhost widget (widgetapp/birdswire.py, port 8973)
- **what it tests**: peak occupancy with long dwell times
- **discrimination hypothesis**: peak occupancy failed both Claude configs before; 16-22 birds, peak 6-10.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted value equals the true value.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8973/ . It is a clip in a player (canvas video with play/pause, seek, 1 s and 
10 s steps and playback speed; read frames from screenshots). It is a 2-minute garden recording of 
birds landing on and leaving a wire. Report the maximum number of birds sitting on the wire at the 
same moment, enter it in the form under the player and submit. Do NOT read the page source or call 
the site's HTTP endpoints directly. End with the number.
```
