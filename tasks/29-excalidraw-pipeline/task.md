# 29-excalidraw-pipeline

- **kind**: action + vision + pixel (LLM-judge)
- **site**: excalidraw.com
- **what it tests**: canvas toolbar use, pixel-placed text elements, screenshot proof
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge, from the final screenshot: the three labels laid out left to right on the canvas.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open Excalidraw (https://excalidraw.com). The drawing area is a canvas: take a SCREENSHOT first to
locate the toolbar, then work with pixel clicks (click --at X,Y). Excalidraw's shape tools need
dragging, which you do not have, so build the diagram from TEXT elements only: select the text
tool, click a spot on the left side of the canvas, type IN, and commit it (press Escape or click
elsewhere). Repeat to place WORK in the middle and OUT on the right, so the three labels read left
to right; optionally place -> between them the same way. Take a final screenshot showing the row
of labels. End by stating what the final screenshot shows.
```
