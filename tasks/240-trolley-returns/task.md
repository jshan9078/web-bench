# 240-trolley-returns

- **kind**: delayed outcome tracking over video (programmatic)
- **site**: localhost widget (widgetapp/lostcart.py, port 8903)
- **what it tests**: tracking each shopper's trolley through an eight-second sequence to see whether it is returned
- **discrimination hypothesis**: the decisive movement is in the last three seconds; abandoned trolleys accumulate by the cars as a check; exact count.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of trolleys left by cars.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8903/ . It is a 2-minute supermarket car park camera clip in a player (canvas 
video with play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots). 
Shoppers push trolleys from the bay (top left) to their cars; afterwards some return the trolley to 
the bay and others leave it beside the car. Count exactly how many trolleys were left by a car 
instead of returned, enter the number in the form under the player and submit. Do NOT read the page 
source or call the site's HTTP endpoints directly. End with the count.
```
