# 360-bird-feeder

- **kind**: re-identification of brief visits (programmatic)
- **site**: localhost widget (widgetapp/birdfeeder.py, port 8990)
- **what it tests**: counting visits of one colour when visits overlap and repeat
- **discrimination hypothesis**: two birds at once, brief visits; blue is half the visits.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted value equals the true value.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8990/ . It is a clip in a player (canvas video with play/pause, seek, 1 s and 
10 s steps and playback speed; read frames from screenshots). It shows a bird feeder for 2 minutes 
visited by red, yellow and blue birds; a visit is one landing followed by a departure, and two 
birds may be present at once. Count exactly how many visits BLUE birds made, enter the number in 
the form under the player and submit. Do NOT read the page source or call the site's HTTP endpoints 
directly. End with the count.
```
