# 85-table-diff

- **kind**: read + dense perception + comparison (programmatic)
- **site**: localhost widget (widgetapp/tablediff.py, port 8805)
- **what it tests**: cell-by-cell comparison of two 80-cell tables from an image, including a last-decimal change
- **discrimination hypothesis**: the realistic "what changed since yesterday" audit; skimming finds the big changes and misses the small one, and the set must be exact.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the submitted set of (row, column, Tuesday value) equals the true set.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8805/ . The page shows two dense stock-sheet snapshots ("Monday" and "Tuesday") as
one IMAGE; nothing is in the DOM, so read them from screenshots. Exactly five cells changed between the
two. List every changed cell in the form below the image, one per line as "Row, Column, TuesdayValue"
(row label and column header as printed), and submit. Some changes are a single digit; compare every cell.
Do NOT read the page source or call the site's HTTP endpoints directly. End with the five lines.
```
