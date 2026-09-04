# 285-occluded-circles

- **kind**: counting under occlusion (programmatic)
- **site**: localhost widget (widgetapp/occluded.py, port 8934)
- **what it tests**: counting discs of one colour when many are partly hidden
- **discrimination hypothesis**: partly hidden discs are easy to miss; exact count.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of target-colour discs.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8934/ . The page shows an IMAGE of overlapping coloured discs (read it from 
screenshots). The question under the image names a colour: count exactly how many discs of that 
colour there are, including ones partly hidden behind other discs, enter the number in the form and 
submit. Do NOT read the page source or call the site's HTTP endpoints directly. End with the count.
```
