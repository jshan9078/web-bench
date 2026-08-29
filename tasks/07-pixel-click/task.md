# 07-pixel-click

- **kind**: action (state)
- **site**: local canvas app (127.0.0.1:8791)
- **what it tests**: Vision + raw-pixel clicking: screenshot, then click circles in ascending order.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: State: the server confirms every circle was clicked in ascending order.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8791/ . It shows several numbered colored circles rendered as an image — they are NOT in the DOM, so `snapshot`/`text`/`eval` reveal nothing. Take a `screenshot` to SEE the circles and their numbers, then CLICK them in ASCENDING numeric order (1, then 2, …) using raw pixel coordinates: `browser <sid> click --at X,Y` (the screenshot's pixels map 1:1 to click coordinates; the image is at the top-left origin). Take another screenshot to confirm if needed. Finish once you've clicked every circle in ascending order. Do NOT read the page source or call the site's HTTP API — interact visually.
```
