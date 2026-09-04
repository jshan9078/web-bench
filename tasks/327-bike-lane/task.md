# 327-bike-lane

- **kind**: counting over video (programmatic)
- **site**: localhost widget (widgetapp/bikelane.py, port 8961)
- **what it tests**: classifying fast movers (cyclists cross in about 2 s) among pedestrians over 2 minutes
- **discrimination hypothesis**: cyclists are visible briefly; 30-40 movers in both directions.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the true count.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8961/ . It is a clip in a player (canvas video with play/pause, seek, 1 s and 
10 s steps and playback speed; read frames from screenshots). It shows a shared path for 2 minutes 
with cyclists (two wheels) and pedestrians passing in both directions across a dashed yellow marker 
line. Count exactly how many CYCLISTS passed the marker line, enter the number in the form under 
the player and submit. Do NOT read the page source or call the site's HTTP endpoints directly. End 
with the count.
```
