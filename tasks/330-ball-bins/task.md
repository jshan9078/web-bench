# 330-ball-bins

- **kind**: counting over video (programmatic)
- **site**: localhost widget (widgetapp/ballbins.py, port 8964)
- **what it tests**: counting fast drop events into one of three bins over 90 s
- **discrimination hypothesis**: each drop lasts 3 s with wobble; 34-44 balls; exact count of one bin.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the true count.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8964/ . It is a clip in a player (canvas video with play/pause, seek, 1 s and 
10 s steps and playback speed; read frames from screenshots). It shows balls dropping through a peg 
board into three bins (LEFT, MIDDLE, RIGHT) for 90 seconds. Count exactly how many balls ended in 
the RIGHT bin, enter the number in the form under the player and submit. Do NOT read the page 
source or call the site's HTTP endpoints directly. End with the count.
```
