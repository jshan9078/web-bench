# 230-coffee-cups

- **kind**: event counting with persistent objects over video (programmatic)
- **site**: localhost widget (widgetapp/coffeeorders.py, port 8893)
- **what it tests**: counting placements onto a shelf where cups persist and are later removed
- **discrimination hypothesis**: cups sitting on the shelf tempt double counting; placements are brief; exact count.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of drinks placed.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8893/ . It is a 2-minute cafe counter camera clip in a player (canvas video 
with play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots). The 
barista (top right) places finished drinks on the pickup shelf, where they wait until a customer 
takes them. Count exactly how many drinks were placed on the shelf during the clip, enter the 
number in the form under the player and submit. Do NOT read the page source or call the site's HTTP 
endpoints directly. End with the count.
```
