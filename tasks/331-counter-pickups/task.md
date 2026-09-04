# 331-counter-pickups

- **kind**: counting over video (programmatic)
- **site**: localhost widget (widgetapp/counterpickups.py, port 8965)
- **what it tests**: attributing pickup events to one of three actors over 2 minutes
- **discrimination hypothesis**: each pickup is brief; the actor colour must be read at the moment of pickup; ~10 target events.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the true count.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8965/ . It is a clip in a player (canvas video with play/pause, seek, 1 s and 
10 s steps and playback speed; read frames from screenshots). It shows a kitchen pass for 2 
minutes: plates appear on the counter and one of three waiters (red, blue or green) picks each one 
up. Count exactly how many plates the BLUE waiter picked up, enter the number in the form under the 
player and submit. Do NOT read the page source or call the site's HTTP endpoints directly. End with 
the count.
```
