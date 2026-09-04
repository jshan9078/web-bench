# 273-maze-exit

- **kind**: visual path finding plus precise click (programmatic)
- **site**: localhost widget (widgetapp/mazeexit.py, port 8927)
- **what it tests**: determining which of three openings is connected to the start through a maze and clicking that cell
- **discrimination hypothesis**: two openings are sealed off; reachability must be traced through the maze; the click must land in the right cell.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the confirmed click lies in the reachable exit's cell.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8927/ . The page shows a maze as an IMAGE at the page's top-left (read it 
from screenshots; click with raw coordinates via click --at X,Y; screenshot pixels map 1:1). The 
red dot is the start; three border openings are marked E, but only one is reachable from the start 
without crossing walls. Click inside the cell of the reachable opening (a blue circle marks your 
click; re-click to move it), then click Confirm. Do NOT read the page source or call the site's 
HTTP endpoints directly. End with which side of the maze the exit is on.
```
