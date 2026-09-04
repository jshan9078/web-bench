# 232-toll-booth

- **kind**: behaviour classification over video (programmatic)
- **site**: localhost widget (widgetapp/tollbooth.py, port 8895)
- **what it tests**: distinguishing vehicles that paused at a booth from those that rolled through, using the pause and the light
- **discrimination hypothesis**: roll-throughs and stops share the same lane; the light is brief; exact count.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of stopping vehicles.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8895/ . It is a 2-minute toll plaza camera clip in a player (canvas video 
with play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots). 
Vehicles pass through the lane: tag-equipped ones roll through (the light turns green), others stop 
at the booth to pay (the light turns red while they wait). Count exactly how many vehicles stopped 
to pay, enter the number in the form under the player and submit. Do NOT read the page source or 
call the site's HTTP endpoints directly. End with the count.
```
