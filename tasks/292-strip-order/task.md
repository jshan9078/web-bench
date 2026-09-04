# 292-strip-order

- **kind**: visual continuity reasoning with ordered clicks (programmatic)
- **site**: localhost widget (widgetapp/striporder.py, port 8938)
- **what it tests**: ordering six shuffled image strips by matching edges of a road, a river and hills
- **discrimination hypothesis**: continuity must be checked at every boundary; one swap fails.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the confirmed order reconstructs the picture.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8938/ . The page shows an IMAGE of a landscape picture cut into six vertical 
strips and shuffled (read it from screenshots; click with raw coordinates via click --at X,Y; 
screenshot pixels map 1:1). Click the strips in the order that reconstructs the original picture 
from left to right so the road, the river and the hills join up (a number appears on each clicked 
strip; click again to unselect), then click Confirm order. Do NOT read the page source or call the 
site's HTTP endpoints directly. End with a one-line confirmation.
```
