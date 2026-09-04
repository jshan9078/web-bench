# 303-symbol-tally

- **kind**: counting one shape among many (programmatic)
- **site**: localhost widget (widgetapp/symboltally.py, port 8943)
- **what it tests**: counting stars among 180 mixed rotated symbols exactly
- **discrimination hypothesis**: rotated small stars resemble other shapes; exact count.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of stars.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8943/ . The page shows an IMAGE of about 180 small symbols (stars, circles, 
squares, triangles, diamonds) in random colours and rotations (read it from screenshots). Count 
exactly how many STARS there are, enter the number in the form and submit. Do NOT read the page 
source or call the site's HTTP endpoints directly. End with the count.
```
