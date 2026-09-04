# 220-ferry-boarding

- **kind**: outcome tracking at a barrier over video (programmatic)
- **site**: localhost widget (widgetapp/ferrycars.py, port 8883)
- **what it tests**: distinguishing vehicles that drove onto the deck from those turned away at a barrier, across 14-20 arrivals
- **discrimination hypothesis**: the outcome is decided in the second half of each pass; turned-away vehicles reverse out; exact count.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of boarded vehicles.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8883/ . It is a 2-minute ferry ramp camera clip in a player (canvas video 
with play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots). 
Vehicles arrive from the left and drive up the ramp; when the barrier is closed they are turned 
away and reverse back out. Count exactly how many vehicles BOARDED the ferry (drove onto the deck), 
enter the number in the form under the player and submit. Do NOT read the page source or call the 
site's HTTP endpoints directly. End with the count.
```
