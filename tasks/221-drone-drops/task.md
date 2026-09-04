# 221-drone-drops

- **kind**: destination attribution over video (programmatic)
- **site**: localhost widget (widgetapp/dronedrops.py, port 8884)
- **what it tests**: attributing each drone's drop to house A, house B or an abort, across 18-24 flights
- **discrimination hypothesis**: drones fly in from the same point and diverge late; aborts drop nothing; the growing parcel piles offer a check; exact count.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of drops at house B.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8884/ . It is a 2-minute rooftop camera clip in a player (canvas video with 
play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots) of two 
houses (A on the left, B on the right). Delivery drones fly in from the top and drop a parcel at 
one house, or abort and fly through without dropping. Count exactly how many parcels were dropped 
at HOUSE B, enter the number in the form under the player and submit. Do NOT read the page source 
or call the site's HTTP endpoints directly. End with the count.
```
