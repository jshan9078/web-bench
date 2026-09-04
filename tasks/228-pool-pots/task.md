# 228-pool-pots

- **kind**: shot outcome counting over video (programmatic)
- **site**: localhost widget (widgetapp/pooltable.py, port 8891)
- **what it tests**: classifying each shot as potted or missed from a three-second roll
- **discrimination hypothesis**: pots and near-misses share the same approach; only the end position tells; exact count.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of potted balls.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8891/ . It is a 2-minute overhead pool-table camera clip in a player (canvas 
video with play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots). 
Balls are struck toward the pockets; some go in (potted, the ball disappears into a pocket), others 
miss and stop on the table. Count exactly how many balls were potted, enter the number in the form 
under the player and submit. Do NOT read the page source or call the site's HTTP endpoints 
directly. End with the count.
```
