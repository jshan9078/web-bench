# 323-two-lane-defects

- **kind**: defect counting on a fast belt (programmatic)
- **site**: localhost widget (widgetapp/twolanebelt.py, port 8958)
- **what it tests**: counting small-marked items on one of two lanes over 90 s
- **discrimination hypothesis**: defect counting failed Opus 5 low before; two lanes add a filtering condition.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the upper-lane defects.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8958/ . It is a clip in a player (canvas video with play/pause, seek, 1 s and 
10 s steps and playback speed; read frames from screenshots). It shows a two-lane conveyor for 90 
seconds; each item crosses the frame in about two seconds, and a defective item carries a small 
dark spot. Count exactly how many DEFECTIVE items passed on the UPPER lane, enter the number in the 
form under the player and submit. Do NOT read the page source or call the site's HTTP endpoints 
directly. End with the count.
```
