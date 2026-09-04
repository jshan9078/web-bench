# 196-turn-count

- **kind**: path tracking over video (programmatic)
- **site**: localhost widget (widgetapp/turncount.py, port 8872)
- **what it tests**: following each of 20-28 vehicles through a junction and counting those that turned left
- **discrimination hypothesis**: the turn happens in the second half of each vehicle's six-second pass; straight and turning vehicles look identical before the junction; exact count.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of left turns.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8872/ . It is a 2-minute intersection camera clip in a player (canvas video 
with play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots). 
Vehicles approach from the bottom and either continue straight up or turn LEFT at the junction. 
Count exactly how many vehicles turned left during the clip, enter the number in the form under the 
player and submit. Do NOT read the page source or call the site's HTTP endpoints directly. End with 
the count.
```
