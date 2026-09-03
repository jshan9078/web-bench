# 139-traffic-count

- **kind**: counting events over time in video (programmatic)
- **site**: localhost widget (widgetapp/carcount.py, port 8846)
- **what it tests**: counting vehicles over a two-minute clip with no motion markers, where some pass within a second of each other in opposite directions and pedestrians are excluded
- **discrimination hypothesis**: sampling frames misses fast passes and double-counts long ones; watching at speed or stepping systematically is required. The count is exact.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of vehicles.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8846/ . It is a 2-minute traffic-camera clip in a player (canvas video with 
play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots). Count how 
many VEHICLES (cars and vans, not pedestrians) pass through the frame during the whole clip, enter 
the exact number in the form under the player and submit. Do NOT read the page source or call the 
site's HTTP endpoints directly. End with the count.
```
