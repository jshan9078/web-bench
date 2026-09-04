# 349-train-cars

- **kind**: classification of fast-passing objects (programmatic)
- **site**: localhost widget (widgetapp/traincars.py, port 8982)
- **what it tests**: counting one car type in a 30-40 car train passing in ~35 s
- **discrimination hypothesis**: each car is on screen about 6 s at 1x; classification while moving; bike lane failed Sonnet twice.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted value equals the true value.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8982/ . It is a clip in a player (canvas video with play/pause, seek, 1 s and 
10 s steps and playback speed; read frames from screenshots). It shows a level crossing for 90 
seconds; a freight train passes at speed. Count exactly how many TANK cars (cylindrical grey tanks) 
the train had, enter the number in the form under the player and submit. Do NOT read the page 
source or call the site's HTTP endpoints directly. End with the count.
```
