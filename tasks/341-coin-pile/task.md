# 341-coin-pile

- **kind**: exact visual counting or tracing (programmatic)
- **site**: localhost widget (widgetapp/coinpile.py, port 8975)
- **what it tests**: exact counting of 30-45 partly overlapping discs
- **discrimination hypothesis**: occlusion breaks counting; symbol tally (180 items) failed Sonnet twice.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted value equals the true value.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8975/ . The page shows an IMAGE (read it from screenshots). It shows coins of 
two sizes scattered on a table, some partly overlapping. Count exactly how many coins there are, 
enter the number in the form and submit. Do NOT read the page source or call the site's HTTP 
endpoints directly. End with the count.
```
