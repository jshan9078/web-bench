# 198-pen-entry

- **kind**: net-flow tracking over video (programmatic)
- **site**: localhost widget (widgetapp/penentry.py, port 8874)
- **what it tests**: tracking animals moving through a gate in both directions and computing the final count in the pen from a shown starting count
- **discrimination hypothesis**: each crossing must be attributed to a direction and summed; a single missed crossing changes the answer; exact.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number in the pen at the end.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8874/ . It is a 2-minute barn camera clip in a player (canvas video with 
play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots). Animals 
pass through the gate from the field into the pen and from the pen back to the field; the number in 
the pen at the start is shown on screen. Work out exactly how many animals are in the pen at the 
END of the clip, enter the number in the form under the player and submit. Do NOT read the page 
source or call the site's HTTP endpoints directly. End with the count.
```
