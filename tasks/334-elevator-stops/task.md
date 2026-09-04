# 334-elevator-stops

- **kind**: counting over video (programmatic)
- **site**: localhost widget (widgetapp/elevatorstops.py, port 8968)
- **what it tests**: counting stops at one floor conditioned on the doors lamp
- **discrimination hypothesis**: stops last 4 s; pass-throughs at floor 5 are decoys.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted value equals the true value.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8968/ . It is a clip in a player (canvas video with play/pause, seek, 1 s and 
10 s steps and playback speed; read frames from screenshots). It is a 2-minute recording of an 
elevator floor indicator (G and 1 to 8) with a DOORS OPEN lamp. Count exactly how many times the 
elevator stopped at floor 5 with its doors open, enter the number in the form under the player and 
submit. Do NOT read the page source or call the site's HTTP endpoints directly. End with the count.
```
