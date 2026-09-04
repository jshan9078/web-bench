# 315-corner-click

- **kind**: vertex precision click (programmatic)
- **site**: localhost widget (widgetapp/cornerclick.py, port 8953)
- **what it tests**: locating a rotated square's top vertex and clicking within 5 px
- **discrimination hypothesis**: vertices are unmarked thin lines; tight tolerance.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the confirmed click is within 5 px of the top vertex.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8953/ . The page shows an IMAGE at the top-left with one rotated square 
outline (read it from screenshots; click with raw coordinates via click --at X,Y; screenshot pixels 
map 1:1). Click the square's TOP-MOST corner within 5 px (a red circle marks your click; re-click 
to move it), then click Confirm. Do NOT read the page source or call the site's HTTP endpoints 
directly. End with the coordinates you chose.
```
