# 326-crosswalk-signal

- **kind**: counting over video (programmatic)
- **site**: localhost widget (widgetapp/crosswalksignal.py, port 8960)
- **what it tests**: counting direction-filtered crossings conditioned on the signal state at the moment of entry
- **discrimination hypothesis**: two conditions must be checked per person across 2 minutes; ~25 crossings.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the true count.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8960/ . It is a clip in a player (canvas video with play/pause, seek, 1 s and 
10 s steps and playback speed; read frames from screenshots). It shows a crosswalk for 2 minutes 
with a pedestrian signal (WALK in green, DON'T WALK in red) at the top right; people cross in both 
directions at any time. Count exactly how many people crossed from RIGHT to LEFT while the signal 
showed WALK at the moment they stepped onto the crossing. Enter the number in the form under the 
player and submit. Do NOT read the page source or call the site's HTTP endpoints directly. End with 
the count.
```
