# 281-count-intersections

- **kind**: exact counting of geometric crossings (programmatic)
- **site**: localhost widget (widgetapp/intersections.py, port 8926)
- **what it tests**: counting crossing points among eight segments exactly
- **discrimination hypothesis**: near-parallel and near-endpoint crossings are easy to miss or double count; exact.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of crossings.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8926/ . The page shows an IMAGE of eight coloured straight line segments 
(read it from screenshots). Count exactly how many points there are where two segments cross, enter 
the number in the form below the image and submit. Do NOT read the page source or call the site's 
HTTP endpoints directly. End with the count.
```
