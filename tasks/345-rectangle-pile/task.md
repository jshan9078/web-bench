# 345-rectangle-pile

- **kind**: exact visual counting or tracing (programmatic)
- **site**: localhost widget (widgetapp/rectpile.py, port 8979)
- **what it tests**: counting overlapping outlined rectangles
- **discrimination hypothesis**: overlaps create spurious rectangles; 18-26 true ones.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted value equals the true value.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8979/ . The page shows an IMAGE (read it from screenshots). It shows outlined 
rectangles drawn on top of each other. Count exactly how many rectangles there are, enter the 
number in the form and submit. Do NOT read the page source or call the site's HTTP endpoints 
directly. End with the count.
```
