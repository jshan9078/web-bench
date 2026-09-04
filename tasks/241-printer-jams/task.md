# 241-printer-jams

- **kind**: event outcome counting over video (programmatic)
- **site**: localhost widget (widgetapp/printqueue.py, port 8904)
- **what it tests**: classifying each print job as completed or jammed from the light, the page and the cover
- **discrimination hypothesis**: jobs are three seconds apart with brief cues; exact count.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of completed jobs.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8904/ . It is a 2-minute print room camera clip in a player (canvas video 
with play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots). Print 
jobs run one after another: a successful job shows a green light and a page slides out into the 
tray; a jammed job shows a red light and the cover is opened with no page. Count exactly how many 
jobs completed successfully, enter the number in the form under the player and submit. Do NOT read 
the page source or call the site's HTTP endpoints directly. End with the count.
```
