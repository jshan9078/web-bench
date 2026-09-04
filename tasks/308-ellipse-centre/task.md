# 308-ellipse-centre

- **kind**: geometric centre precision click (programmatic)
- **site**: localhost widget (widgetapp/ellipsecentre.py, port 8948)
- **what it tests**: locating the centre of a rotated ellipse and clicking within 6 px
- **discrimination hypothesis**: the centre is not marked; estimation from the outline; tight tolerance.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the confirmed click is within 6 px of the centre.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8948/ . The page shows an IMAGE at the top-left with one rotated ellipse 
outline on a speckled background (read it from screenshots; click with raw coordinates via click 
--at X,Y; screenshot pixels map 1:1). Click the ellipse's exact centre, within 6 px (a red cross 
marks your click; re-click to move it), then click Confirm. Do NOT read the page source or call the 
site's HTTP endpoints directly. End with the coordinates you chose.
```
