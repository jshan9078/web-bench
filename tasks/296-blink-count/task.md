# 296-blink-count

- **kind**: counting brief events over video (programmatic)
- **site**: localhost widget (widgetapp/blinkcount.py, port 8940)
- **what it tests**: counting 9-16 sub-second blinks of one lamp among three over a minute
- **discrimination hypothesis**: blinks last 0.8 s; sampling misses them; the other lamps are decoys; exact.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the amber blinks.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8940/ . It is a 1-minute control-panel clip in a player (canvas video with 
play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots). Three lamps 
blink on their own schedules; each blink lasts under a second. Count exactly how many times the 
AMBER lamp blinked during the clip, enter the number in the form under the player and submit. Do 
NOT read the page source or call the site's HTTP endpoints directly. End with the count.
```
