# 235-tennis-serves

- **kind**: outcome classification over video (programmatic)
- **site**: localhost widget (widgetapp/tennisserves.py, port 8898)
- **what it tests**: classifying each serve as in or out from the landing spot and the call
- **discrimination hypothesis**: in and out serves follow similar arcs; the landing spot and banner decide; exact count.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of in serves.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8898/ . It is a 2-minute court camera clip in a player (canvas video with 
play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots). Serves come 
from the bottom; a serve that lands in the service box is IN, one that lands beyond the line is 
called OUT (an OUT banner appears and the line judge raises an arm). Count exactly how many serves 
were IN, enter the number in the form under the player and submit. Do NOT read the page source or 
call the site's HTTP endpoints directly. End with the count.
```
