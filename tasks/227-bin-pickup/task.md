# 227-bin-pickup

- **kind**: per-object outcome over video (programmatic)
- **site**: localhost widget (widgetapp/binpickup.py, port 8890)
- **what it tests**: tracking which of eight bins were lifted and emptied as the truck moves along
- **discrimination hypothesis**: skipped bins look identical before the truck reaches them; the lid colour afterwards is the check; exact count.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of emptied bins.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8890/ . It is a 2-minute street camera clip in a player (canvas video with 
play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots). A refuse 
truck works along a row of eight bins; some bins are lifted and emptied into the truck (their lid 
turns grey afterwards), others are skipped. Count exactly how many bins were emptied, enter the 
number in the form under the player and submit. Do NOT read the page source or call the site's HTTP 
endpoints directly. End with the count.
```
