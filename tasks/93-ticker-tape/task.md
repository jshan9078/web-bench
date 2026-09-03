# 93-ticker-tape

- **kind**: moving-content coverage (programmatic)
- **site**: localhost widget (widgetapp/ticker.py, port 8813)
- **what it tests**: systematically covering a 40 s scrolling loop (about six of 24 symbols visible at once) so a maximum can be taken over the whole set, or discovering the hover pause
- **discrimination hypothesis**: the two best gainers sit far apart on the tape and differ by under half a point, so partial coverage picks the wrong one; the delayed watchlist table shows a symbol with a bigger stale gain, so a DOM-only agent answers from the wrong source.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the submitted symbol is the true top gainer on the tape (percentage within 0.15).

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8813/ . The band at the top is a live scrolling market ticker drawn on a 
canvas (read it from screenshots; it is not in the DOM). Identify the symbol with the LARGEST 
percentage gain shown on the ticker itself and its percentage change (the delayed watchlist table 
on the page is NOT the ticker). Enter the symbol and percentage in the form at the bottom and 
submit. Do NOT read the page source or call the site's HTTP endpoints directly. End with the symbol 
and percentage.
```
