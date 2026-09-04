# 234-hand-hygiene

- **kind**: compliance event detection over video (programmatic)
- **site**: localhost widget (widgetapp/handwash.py, port 8897)
- **what it tests**: attributing each entry to whether the dispenser was used (a pause and a green light) beforehand
- **discrimination hypothesis**: users pause briefly; non-users walk straight in; the light is the check; exact count.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of non-users.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8897/ . It is a 2-minute ward entrance camera clip in a player (canvas video 
with play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots). Staff 
walk in from the left and enter the ward door on the right; a sanitiser dispenser beside the door 
lights GREEN when someone uses it. Count exactly how many people entered WITHOUT using the 
dispenser, enter the number in the form under the player and submit. Do NOT read the page source or 
call the site's HTTP endpoints directly. End with the count.
```
