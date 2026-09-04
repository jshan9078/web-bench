# 353-arrow-field

- **kind**: exact orientation classification (programmatic)
- **site**: localhost widget (widgetapp/arrowfield.py, port 8985)
- **what it tests**: counting arrows of one orientation among 120
- **discrimination hypothesis**: small rotated glyphs; adjacent orientations (up, left) are decoys; ~15 targets.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted value equals the true value.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8985/ . The page shows an IMAGE (read it from screenshots) of about 120 
arrows pointing in eight directions. Count exactly how many arrows point UP-LEFT (toward the 
top-left corner), enter the number in the form and submit. Do NOT read the page source or call the 
site's HTTP endpoints directly. End with the count.
```
