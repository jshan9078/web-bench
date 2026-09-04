# 333-lead-changes

- **kind**: counting over video (programmatic)
- **site**: localhost widget (widgetapp/scoreboardleads.py, port 8967)
- **what it tests**: tracking a two-value state over 2 minutes and counting lead changes
- **discrimination hypothesis**: requires reading every score update (every 3-7 s) and applying the tie rule.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted value equals the true value.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8967/ . It is a clip in a player (canvas video with play/pause, seek, 1 s and 
10 s steps and playback speed; read frames from screenshots). It is a 2-minute arena scoreboard 
recording (Hawks vs Otters); scores update every few seconds. Count exactly how many times the LEAD 
changed hands during the clip (a tie that is then broken by the team that already led is not a 
change; the first team to lead does not count as a change). Enter the number in the form under the 
player and submit. Do NOT read the page source or call the site's HTTP endpoints directly. End with 
the count.
```
