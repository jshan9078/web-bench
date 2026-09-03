# 84-ledger-audit

- **kind**: read + dense perception (programmatic)
- **site**: localhost widget (widgetapp/ledger.py, port 8804)
- **what it tests**: reading 120 small figures exhaustively from an image, near-ties at both extremes, lookalike digits, and an exact 30-term sum
- **discrimination hypothesis**: the realistic "audit a scanned statement" job: nothing to navigate, everything to read. One skipped row or one misread digit changes an answer.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: all three findings exact.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8804/ . The page shows a scanned expense ledger as an IMAGE (30 vendors, columns Q1
to Q4); nothing in it is in the DOM, so read it from screenshots. Determine (1) the vendor with the
highest Q3 amount, (2) the vendor with the lowest Q1 amount, and (3) the exact total of the Q4 column (two
decimals). Figures are close in places and the scan uses a font where 3/8 and 6/9 look alike, so read
every row carefully. Enter the three findings in the form below the image and submit. Do NOT read the
page source or call the site's HTTP endpoints directly. End with the three findings.
```
