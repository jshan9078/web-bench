# 137-crop-corners

- **kind**: two-point precision placement (programmatic)
- **site**: localhost widget (widgetapp/cropcorners.py, port 8845)
- **what it tests**: locating the corners of a rotated document in a photo and clicking within 10 px of each, using the marker feedback to correct
- **discrimination hypothesis**: corners of a rotated rectangle are not at the bounding box's corners; agents that click the axis-aligned extremes, or skip the check-and-correct loop, miss the tolerance.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: both confirmed points are within 10 px of the receipt's true top-left and bottom-right corners.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8845/ . It is a document-scanner step: a photo of a receipt on a desk, 
rendered as an IMAGE at the page's top-left (read it from screenshots; click with raw coordinates 
via click --at X,Y; screenshot pixels map 1:1). Click exactly on the receipt's TOP-LEFT corner, 
then exactly on its BOTTOM-RIGHT corner (markers appear after each click; a third click starts 
over; take a fresh screenshot to check), then click Confirm corners. Do NOT read the page source or 
call the site's HTTP endpoints directly. End with the two coordinates you confirmed.
```
