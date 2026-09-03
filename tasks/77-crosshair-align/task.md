# 77-crosshair-align

- **kind**: action + vision + precision (programmatic)
- **site**: localhost widget (widgetapp/crosshair.py, port 8799)
- **what it tests**: estimating a target's pixel position from a screenshot, converting the estimate into keyboard moves, verifying with fresh screenshots, and committing under a two-lock limit; a dashed decoy ring tests reading the instruction
- **discrimination hypothesis**: the closest thing to a mouse-free JS Paint: precision under feedback. Agents that lock after one coarse move miss the 3 px tolerance; agents that aim at the decoy fail outright. The skill is estimation plus iteration, not length.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: last lock within 3 px of the target centre, at most two locks.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8799/ . The page is one image showing a SOLID blue ring with a centre dot, a DASHED
decoy ring, and a thin blue crosshair; none of it is in the DOM, so take a `screenshot` to see it. Move
the crosshair onto the centre of the SOLID ring using the arrow keys (each press moves 1 px; hold Shift
for 10 px), taking fresh screenshots to check your position, and press Enter to lock it once it is within
3 px of the centre. The page must have keyboard focus for the keys to work (click on the page first if
needed). You may lock at most twice, so verify before pressing Enter. The footer shows the crosshair's
current pixel coordinates but never the target's. Do NOT read the page source or call the site's HTTP
endpoints directly. End by reporting the coordinates you locked at.
```
