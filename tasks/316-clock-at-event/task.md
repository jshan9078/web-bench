# 316-clock-at-event

- **kind**: clock reading at a moment in video (programmatic)
- **site**: localhost widget (widgetapp/clockevent.py, port 8954)
- **what it tests**: finding the frame where a lamp changes and reading a fast-running analog clock there
- **discrimination hypothesis**: combines event localisation in video with minute-level clock reading.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted time is within one minute.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8954/ . It is a 45-second office timelapse in a player (canvas video with 
play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots). The wall 
clock runs fast (timelapse) and the status lamp turns GREEN once. Report the time the wall clock 
showed at the moment the lamp turned green, as HH:MM within one minute, enter it in the form under 
the player and submit. Do NOT read the page source or call the site's HTTP endpoints directly. End 
with the time.
```
