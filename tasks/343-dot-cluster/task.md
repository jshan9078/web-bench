# 343-dot-cluster

- **kind**: exact visual counting or tracing (programmatic)
- **site**: localhost widget (widgetapp/dotcluster.py, port 8977)
- **what it tests**: exact counting of 55-85 identical dots
- **discrimination hypothesis**: no structure to anchor a count; dots nearly touch.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted value equals the true value.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8977/ . The page shows an IMAGE (read it from screenshots). It shows an 
irregular cluster of blue dots. Count exactly how many dots there are, enter the number in the form 
and submit. Do NOT read the page source or call the site's HTTP endpoints directly. End with the 
count.
```
