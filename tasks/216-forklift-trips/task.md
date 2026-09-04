# 216-forklift-trips

- **kind**: attribute tracking over video (programmatic)
- **site**: localhost widget (widgetapp/forklift.py, port 8879)
- **what it tests**: distinguishing loaded from empty forklift passes and counting only the loaded ones in one direction
- **discrimination hypothesis**: trips alternate direction every few seconds and the pallet is the only difference; exact count.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of loaded dock-to-racks trips.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8879/ . It is a 2-minute warehouse dock camera clip in a player (canvas video 
with play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots). A 
forklift shuttles between the dock on the right and the racks on the left; on some trips it carries 
a pallet, on others its forks are empty. Count exactly how many LOADED trips (carrying a pallet) 
went from the dock to the racks, enter the number in the form under the player and submit. Do NOT 
read the page source or call the site's HTTP endpoints directly. End with the count.
```
