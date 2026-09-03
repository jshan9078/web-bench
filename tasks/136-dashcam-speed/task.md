# 136-dashcam-speed

- **kind**: video timing + overlay reading (programmatic)
- **site**: localhost widget (widgetapp/dashcam.py, port 8843)
- **what it tests**: finding the moment a specific sign passes in a 90 s clip and reading a continuously changing overlay at that moment
- **discrimination hypothesis**: the overlay changes by several km/h over a few seconds, so the reading must be taken while the red sign is beside the car; four other signs pass, and reading at the wrong moment or the wrong sign fails.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted speed is within 3 km/h of the overlay while the red sign is alongside.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8843/ . It is a dashcam clip review player (canvas video with a speed 
overlay; use the play/pause, seek bar and 1 s steps; read frames from screenshots). Several 
roadside signs pass; exactly one is a RED octagonal sign. Report the speed shown on the overlay at 
the moment the car passes that red sign (within 3 km/h), enter it in the form under the player and 
submit. Do NOT read the page source or call the site's HTTP endpoints directly. End with the speed.
```
