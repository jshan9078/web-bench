# 122-drop-pin

- **kind**: precision placement with feedback (programmatic)
- **site**: localhost widget (widgetapp/droppin.py, port 8840)
- **what it tests**: placing a marker on a named street intersection in a map image by raw coordinates, verifying with a fresh screenshot, and confirming
- **discrimination hypothesis**: reading the intersection from rotated street labels and landing within 8 px needs a check-and-correct loop; agents that trust their first click land on the block, not the corner.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the confirmed pin is within 8 px of the named intersection.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8840/ . It is a street map rendered as an IMAGE at the page's top-left (read 
it from screenshots; click with raw coordinates via click --at X,Y; screenshot pixels map 1:1 to 
click coordinates). The text under the map names an intersection: place the pin so its tip is 
exactly on that intersection (within a few pixels; you may re-click to move it and take a fresh 
screenshot to check), then click Confirm pin. Do NOT read the page source or call the site's HTTP 
endpoints directly. End with the intersection name.
```
