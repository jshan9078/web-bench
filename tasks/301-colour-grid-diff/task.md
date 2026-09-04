# 301-colour-grid-diff

- **kind**: colour comparison across two grids (programmatic)
- **site**: localhost widget (widgetapp/griddiff.py, port 8942)
- **what it tests**: finding the one cell of 49 whose colour differs moderately between two grids
- **discrimination hypothesis**: cell-by-cell comparison of colours; exact cell.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted cell is the differing one.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8942/ . The page shows two 7x7 colour grids side by side as an IMAGE (read it 
from screenshots). They are identical except one cell whose colour differs. Report that cell as row 
letter plus column number (for example D3), enter it in the form and submit. Do NOT read the page 
source or call the site's HTTP endpoints directly. End with the cell.
```
