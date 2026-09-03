# 184-queue-peak

- **kind**: state tracking over video (programmatic)
- **site**: localhost widget (widgetapp/queuepeak.py, port 8867)
- **what it tests**: tracking a queue's length through arrivals and departures over a two-minute clip to find its peak
- **discrimination hypothesis**: the peak lasts only a few seconds and is reached through overlapping arrivals; sampling misses it and counting arrivals over-counts; exactness required.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted number equals the true peak queue length.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8867/ . It is a 2-minute service-counter camera clip in a player (canvas 
video with play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots). 
People join the queue on the left and leave after being served at the counter. Report the MAXIMUM 
number of people waiting in the queue at the same moment at any point in the clip (exact), enter it 
in the form under the player and submit. Do NOT read the page source or call the site's HTTP 
endpoints directly. End with the number.
```
