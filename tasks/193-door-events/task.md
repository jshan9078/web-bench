# 193-door-events

- **kind**: event detection over video (programmatic)
- **site**: localhost widget (widgetapp/doorevents.py, port 8871)
- **what it tests**: distinguishing door openings with a person passing from empty openings across 16-22 events
- **discrimination hypothesis**: each opening lasts four seconds and the person is visible for under three; sampled frames confuse the two; exact count.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of empty openings.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8871/ . It is a 2-minute entrance camera clip in a player (canvas video with 
play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots). An 
automatic sliding door opens repeatedly; sometimes a person walks through, sometimes it opens with 
nobody passing. Count exactly how many times the door opened with NOBODY passing through, enter the 
number in the form under the player and submit. Do NOT read the page source or call the site's HTTP 
endpoints directly. End with the count.
```
