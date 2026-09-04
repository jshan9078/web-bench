# 223-goal-shots

- **kind**: event outcome counting over video (programmatic)
- **site**: localhost widget (widgetapp/goalshots.py, port 8886)
- **what it tests**: classifying each shot as goal, save or post from a three-second sequence
- **discrimination hypothesis**: saves and post-rebounds look like goals in a single frame; only the ball's final position tells; exact count.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of goals.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8886/ . It is a 2-minute goal-line camera clip in a player (canvas video with 
play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots). Shots come 
in from the bottom: some are saved by the keeper, some hit a post and bounce out, and some cross 
the line into the net. Count exactly how many GOALS were scored, enter the number in the form under 
the player and submit. Do NOT read the page source or call the site's HTTP endpoints directly. End 
with the count.
```
