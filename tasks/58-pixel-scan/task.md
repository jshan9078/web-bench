# 58-pixel-scan

- **kind**: action + vision (programmatic)
- **site**: localhost widget (widgetapp/pixelscan.py, port 8792)
- **what it tests**: scrolling a scene taller than the viewport, translating screenshot pixels to click coordinates after scrolling, ignoring decoys, ordered bookkeeping across 10 targets
- **discrimination hypothesis**: the 5-target pixel task is saturated; ten small targets on a scrolling page with numbered square decoys require the agent to keep a consistent coordinate frame across scrolls and to never take the 'obvious' numbered decoy. Models with weak spatial grounding or sloppy scroll bookkeeping click a square or skip a number.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: circles hit in click order are exactly 1..10 and no decoy square was ever hit.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8792/ . The page is one tall image (900x1500) that scrolls: it shows ten small
numbered CIRCLES and several numbered SQUARES. The shapes are NOT in the DOM, so `snapshot`/`text`/`eval`
reveal nothing; take a `screenshot` to SEE them. Click the CIRCLES in ASCENDING numeric order (1, then
2, ... up to 10) using raw viewport pixel coordinates (`browser <sid> click --at X,Y`; the screenshot's
pixels map 1:1 to click coordinates). Never click a square: squares are decoys and a single click on one
fails the task. Some circles are below the fold: scroll, take a fresh screenshot, and remember that click
coordinates are viewport pixels after scrolling. Finish once you have clicked all ten circles in order. Do
NOT read the page source or call the site's HTTP endpoints directly; interact visually.
```
