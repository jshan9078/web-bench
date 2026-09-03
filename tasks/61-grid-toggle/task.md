# 61-grid-toggle

- **kind**: action + vision (programmatic)
- **site**: localhost widget (widgetapp/gridtoggle.py, port 8795)
- **what it tests**: shape discrimination at small size (filled circle vs ring vs square), 10 precise clicks with a toggle semantics, verifying the visible selection state after each click and correcting mistakes
- **discrimination hypothesis**: a bookkeeping-and-verification task: the selection is visible only in the re-rendered image, so the agent must re-screenshot to confirm. Agents that click without verifying leave a ring selected or a filled circle unselected; the exact-set criterion catches any single error.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the selected set of cells equals exactly the set of filled-circle cells.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8795/ . The page shows an 8x8 grid as an image. Some cells contain a FILLED circle,
some a hollow RING, some a SQUARE, and some are empty. Nothing is in the DOM; take a `screenshot` to see
it. Select EVERY cell that contains a filled circle, and no other cell, by clicking cells with
`browser <sid> click --at X,Y`. A click toggles the cell (selected cells are highlighted in the
re-rendered image; clicking again deselects). After your clicks, take a fresh screenshot to verify the
highlighted cells are exactly the filled circles and fix any mistakes. Finish when the selection is
correct, and report how many cells you selected. Do NOT read the page source or call the site's HTTP
endpoints directly; interact visually.
```
