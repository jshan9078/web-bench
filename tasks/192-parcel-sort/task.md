# 192-parcel-sort

- **kind**: tracking items to an outcome over video (programmatic)
- **site**: localhost widget (widgetapp/parcelsort.py, port 8870)
- **what it tests**: following each of 26-36 parcels through a junction and counting those diverted to one chute
- **discrimination hypothesis**: the outcome is decided in the last three seconds of each parcel's six-second pass; sampling at the belt misses it; exact count.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of parcels sent to the left chute.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8870/ . It is a 2-minute parcel-sorter clip in a player (canvas video with 
play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots). Parcels 
travel along the belt to a junction where a diverter sends each one up to the LEFT chute or down to 
the RIGHT chute. Count exactly how many parcels went to the LEFT chute during the clip, enter the 
number in the form under the player and submit. Do NOT read the page source or call the site's HTTP 
endpoints directly. End with the count.
```
