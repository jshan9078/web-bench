# 284-rotated-odd-one-out

- **kind**: fine orientation discrimination (programmatic)
- **site**: localhost widget (widgetapp/rotglyph.py, port 8933)
- **what it tests**: spotting a 20-degree rotation difference in one of 64 identical glyphs and reporting its cell
- **discrimination hypothesis**: a small orientation difference among many items; exact cell.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted cell is the odd glyph's.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8933/ . The page shows an IMAGE of an 8x8 grid of the same glyph (read it 
from screenshots). All glyphs are rotated the same way except one, which is rotated a little 
further. Identify its cell as row letter plus column number (for example C7), enter it in the form 
below the image and submit. Do NOT read the page source or call the site's HTTP endpoints directly. 
End with the cell.
```
