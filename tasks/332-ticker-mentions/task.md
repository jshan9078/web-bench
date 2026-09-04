# 332-ticker-mentions

- **kind**: counting over video (programmatic)
- **site**: localhost widget (widgetapp/newsticker.py, port 8966)
- **what it tests**: reading a fast scrolling ticker and de-duplicating a looping list
- **discrimination hypothesis**: text moves at 180 px/s; the loop must be recognised to count distinct headlines.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted value equals the true value.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8966/ . It is a clip in a player (canvas video with play/pause, seek, 1 s and 
10 s steps and playback speed; read frames from screenshots). It is a 2-minute news channel 
recording with a scrolling ticker at the bottom; the ticker loops through a fixed list of 
headlines. Count exactly how many DISTINCT headlines in the ticker mention the word HARBOR, enter 
the number in the form under the player and submit. Do NOT read the page source or call the site's 
HTTP endpoints directly. End with the count.
```
