# 351-fish-ring

- **kind**: event counting among distractors (programmatic)
- **site**: localhost widget (widgetapp/fishring.py, port 8984)
- **what it tests**: counting hoop passes among six ambient fish that never pass
- **discrimination hypothesis**: ambient fish approach the hoop but turn away; passes take 5 s; 8-14 events.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted value equals the true value.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8984/ . It is a clip in a player (canvas video with play/pause, seek, 1 s and 
10 s steps and playback speed; read frames from screenshots). It shows an aquarium for 2 minutes 
with a yellow hoop in the middle; fish swim around and some pass through the hoop. Count exactly 
how many times a fish swam through the hoop, enter the number in the form under the player and 
submit. Do NOT read the page source or call the site's HTTP endpoints directly. End with the count.
```
