# 337-slide-deck-value

- **kind**: counting over video (programmatic)
- **site**: localhost widget (widgetapp/slidedeck.py, port 8971)
- **what it tests**: locating one slide among two dozen in a recording and reading a table total
- **discrimination hypothesis**: the slide is on screen 3-8 s; decoy titles (Regional overview, Results summary) exist.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted value equals the true value.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8971/ . It is a clip in a player (canvas video with play/pause, seek, 1 s and 
10 s steps and playback speed; read frames from screenshots). It is a 2-minute recording of a 
presentation with about two dozen slides, each shown for a few seconds. Find the slide titled 
exactly "Regional results" and report its Q3 TOTAL (the Total row, Q3 column, number only without 
the k), enter it in the form under the player and submit. Do NOT read the page source or call the 
site's HTTP endpoints directly. End with the number.
```
