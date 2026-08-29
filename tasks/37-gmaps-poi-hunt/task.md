# 37-gmaps-poi-hunt

- **kind**: read + vision + pixel (LLM-judge)
- **site**: google.com/maps
- **what it tests**: visually locating a labeled feature inside a park and clicking it on the map canvas
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: the place card matches the clicked feature and its live review count.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
On Google Maps (https://www.google.com/maps), search for High Park, Toronto. Zoom the map until
the label for Grenadier Pond (inside the park) is visible, take a SCREENSHOT, and pixel-click
directly on that label on the map (if only a small preview chip opens, click the chip again to
expand the full card). From the place card that opens, report the place name, its
category, star rating, and the current number of reviews. Take a screenshot of the card. End with
those four details.
```
