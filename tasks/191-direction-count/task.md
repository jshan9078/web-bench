# 191-direction-count

- **kind**: direction-aware counting over video (programmatic)
- **site**: localhost widget (widgetapp/dircount.py, port 8869)
- **what it tests**: counting only the crossings in one direction among 18-26 crossings in both directions over two minutes
- **discrimination hypothesis**: direction is invisible in one frame, so every crossing needs two looks; near-simultaneous crossings in opposite directions are the trap; exact count.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of left-to-right crossings.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8869/ . It is a 2-minute corridor camera clip in a player (canvas video with 
play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots). People 
cross in both directions. Count exactly how many people crossed from LEFT to RIGHT during the whole 
clip, enter the number in the form under the player and submit. Do NOT read the page source or call 
the site's HTTP endpoints directly. End with the count.
```
