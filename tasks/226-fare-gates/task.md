# 226-fare-gates

- **kind**: state-at-event attribution over video (programmatic)
- **site**: localhost widget (widgetapp/fareevaders.py, port 8889)
- **what it tests**: attributing each of 22-30 gate passages to the gate's colour at the moment of passing
- **discrimination hypothesis**: the light shows for two seconds mid-passage across three gates; exact count.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of red-gate passages.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8889/ . It is a 2-minute station gate-line camera clip in a player (canvas 
video with play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots). 
Passengers walk up through one of three gates; a valid tap lights the gate GREEN, while some 
passengers push through a gate that lights RED (no valid tap). Count exactly how many passengers 
passed through with a RED gate, enter the number in the form under the player and submit. Do NOT 
read the page source or call the site's HTTP endpoints directly. End with the count.
```
