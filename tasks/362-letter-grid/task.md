# 362-letter-grid

- **kind**: exact glyph counting among confusable letters (programmatic)
- **site**: localhost widget (widgetapp/lettergrid.py, port 8991)
- **what it tests**: counting R among R, P, B, K in mixed weights and rotations (192 glyphs)
- **discrimination hypothesis**: confusable shapes; exact count ~45.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted value equals the true value.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8991/ . The page shows an IMAGE (read it from screenshots). It shows a grid 
of the letters R, P, B and K in mixed weights and slight rotations. Count exactly how many letters 
are R, enter the number in the form and submit. Do NOT read the page source or call the site's HTTP 
endpoints directly. End with the count.
```
