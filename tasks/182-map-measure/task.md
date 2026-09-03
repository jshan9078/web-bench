# 182-map-measure

- **kind**: multi-segment measurement against a scale (programmatic)
- **site**: localhost widget (widgetapp/mapmeasure.py, port 8865)
- **what it tests**: measuring a 4-6 segment route on a map image against its scale bar to within 6 percent
- **discrimination hypothesis**: segment-by-segment estimation accumulates error; eyeballing the straight-line distance or misreading the scale bar fails.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the submitted length is within 6 percent of the route length.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8865/ . It is a trail map rendered as an IMAGE with a scale bar and a red 
route from marker S to marker F made of straight segments (read it from screenshots). Measure the 
route's total length in metres using the scale bar (within 6 percent), enter it in the form below 
the map and submit. Do NOT read the page source or call the site's HTTP endpoints directly. End 
with the length.
```
