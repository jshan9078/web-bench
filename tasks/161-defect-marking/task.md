# 161-defect-marking

- **kind**: multi-target precision marking (programmatic)
- **site**: localhost widget (widgetapp/defects.py, port 8857)
- **what it tests**: finding five faint scratches among decoy specks in a textured photo and marking each within 12 px
- **discrimination hypothesis**: missing a faint scratch, marking a speck, or imprecise clicks fail; five targets is a count, not length.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: all five scratches marked within 12 px with at most one stray marker.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8857/ . It is a QA inspection photo of a painted panel with five small 
scratches (thin dark lines) among dust specks. It is rendered as an IMAGE at the page's top-left 
that responds to clicks (use raw coordinates via click --at X,Y; screenshot pixels map 1:1; the 
image refreshes after each click, so take a fresh screenshot to see the result). Place a marker on 
each of the five scratches (click on the scratch; clicking a marker removes it), avoid marking 
specks, then click the Confirm button at the bottom-right of the image. Do NOT read the page source 
or call the site's HTTP endpoints directly. End with the number of markers you confirmed.
```
