# 347-checkout-lanes

- **kind**: event counting over video (programmatic)
- **site**: localhost widget (widgetapp/checkoutlanes.py, port 8980)
- **what it tests**: counting served customers at one of three lanes using a 0.8 s PAID flash
- **discrimination hypothesis**: brief event marker; three lanes run concurrently; ~12 target events.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted value equals the true value.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8980/ . It is a clip in a player (canvas video with play/pause, seek, 1 s and 
10 s steps and playback speed; read frames from screenshots). It shows three store checkout lanes 
for 2 minutes; customers walk up, are served (the lane display flashes PAID) and leave. Count 
exactly how many customers were served at LANE 2, enter the number in the form under the player and 
submit. Do NOT read the page source or call the site's HTTP endpoints directly. End with the count.
```
