# 183-odd-glyph

- **kind**: visual search among near-identical items (programmatic)
- **site**: localhost widget (widgetapp/oddglyph.py, port 8866)
- **what it tests**: finding the single mirrored icon in a 6x10 grid of identical icons and reporting its grid cell
- **discrimination hypothesis**: a mirrored arrow among sixty is a subtle difference that must be checked cell by cell; wrong cell or off-by-one indexing fails.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted cell is the mirrored icon's cell.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8866/ . It is a print proof sheet: a 6-row by 10-column grid of the same 
arrow icon, rendered as an IMAGE (read it from screenshots). Exactly one icon is printed mirrored 
left-to-right. Identify its cell as row letter plus column number (for example C7), enter it in the 
form below the sheet and submit. Do NOT read the page source or call the site's HTTP endpoints 
directly. End with the cell.
```
