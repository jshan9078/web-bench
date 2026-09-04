# 245-recycling-sort

- **kind**: destination attribution over video (programmatic)
- **site**: localhost widget (widgetapp/recyclesort.py, port 8908)
- **what it tests**: attributing each drop to one of three adjacent bins
- **discrimination hypothesis**: adjacent bins and a brief drop; exact count.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of glass-bin drops.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8908/ . It is a 2-minute recycling station camera clip in a player (canvas 
video with play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots). 
People walk up and drop an item into one of three bins: PAPER (blue, left), GLASS (green, middle) 
or GENERAL (grey, right). Count exactly how many items were dropped into the GLASS bin, enter the 
number in the form under the player and submit. Do NOT read the page source or call the site's HTTP 
endpoints directly. End with the count.
```
