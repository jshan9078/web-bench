# 20-nasa-apod-vision

- **kind**: read + vision (LLM-judge)
- **site**: apod.nasa.gov
- **what it tests**: reading a daily page plus genuinely describing an image from a screenshot
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: the description matches the screenshot the agent captured, and title/date match the page.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open NASA's Astronomy Picture of the Day (https://apod.nasa.gov/apod/astropix.html). Report today's
title and date, take a SCREENSHOT of the page, and describe the image in two or three sentences of
specific visual detail (colors, shapes, positions of objects), based on what you see in the
screenshot. Then give a one-sentence gist of the written explanation. End with title, date, your
visual description, and the gist.
```
