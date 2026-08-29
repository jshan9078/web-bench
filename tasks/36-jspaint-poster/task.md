# 36-jspaint-poster

- **kind**: action + vision + pixel (LLM-judge)
- **site**: jspaint.app
- **what it tests**: palette and tool selection by pixel clicks, flood fill, text typed onto a canvas
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge, from the final screenshot: red-filled canvas bearing the typed text.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open JS Paint (https://jspaint.app). Everything is canvas: take a SCREENSHOT first to locate the
tools and the color palette. Pixel-click the RED color in the palette, select the Fill (paint
bucket) tool, and click the blank canvas to flood it red. Then pick BLACK in the palette, select
the Pencil or Brush tool, and place FIVE separate single-click dots on the red canvas arranged as
an X (one dot in the center, one toward each corner). Take a final screenshot. End by stating
what the final screenshot shows.
```
