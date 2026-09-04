# 306-shell-game

- **kind**: continuous tracking through occlusion-like swaps (programmatic)
- **site**: localhost widget (widgetapp/shellgame.py, port 8946)
- **what it tests**: tracking one of three identical cups across 14 swaps over 40 s
- **discrimination hypothesis**: identical objects; position identity must be carried through every swap; sampling breaks the chain.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted position is the ball's.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8946/ . It is a 45-second clip in a player (canvas video with play/pause, 
seek, 1 s and 10 s steps and playback speed; read frames from screenshots). A ball is shown under 
one of three identical cups at the start; the cups are then swapped many times. Report the ball's 
final position (1 = left, 2 = middle, 3 = right), enter it in the form under the player and submit. 
Do NOT read the page source or call the site's HTTP endpoints directly. End with the position.
```
