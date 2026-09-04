# 222-escalator-up

- **kind**: direction and lane attribution over video (programmatic)
- **site**: localhost widget (widgetapp/escalator.py, port 8885)
- **what it tests**: counting riders on one of two escalators while others ride the other or walk past
- **discrimination hypothesis**: three movement types share the frame; exact count.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of up riders.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8885/ . It is a 2-minute mall atrium camera clip in a player (canvas video 
with play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots). There 
is an UP escalator on the left and a DOWN escalator on the right; some people walk past along the 
floor without riding. Count exactly how many people rode the UP escalator, enter the number in the 
form under the player and submit. Do NOT read the page source or call the site's HTTP endpoints 
directly. End with the count.
```
