# 217-queue-leavers

- **kind**: outcome tracking of individuals over video (programmatic)
- **site**: localhost widget (widgetapp/queueleavers.py, port 8880)
- **what it tests**: following each person in a queue to see whether they reach the counter or walk away
- **discrimination hypothesis**: leavers and served people both disappear from the queue; only their direction of exit differs; exact count.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of people who left unserved.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8880/ . It is a 2-minute ticket-counter camera clip in a player (canvas video 
with play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots). People 
join the queue from the right; most are served at the counter on the left, but some give up and 
walk away to the right before being served. Count exactly how many people left the queue WITHOUT 
being served, enter the number in the form under the player and submit. Do NOT read the page source 
or call the site's HTTP endpoints directly. End with the count.
```
