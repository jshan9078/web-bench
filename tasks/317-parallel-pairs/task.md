# 317-parallel-pairs

- **kind**: three-degree parallelism judgement (programmatic)
- **site**: localhost widget (widgetapp/parallelpairs.py, port 8955)
- **what it tests**: spotting the one pair of lines that diverges by 3 degrees
- **discrimination hypothesis**: fine angular discrimination without references.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted letter is the non-parallel pair.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8955/ . The page shows an IMAGE of six labelled pairs of lines (read it from 
screenshots). Five pairs are parallel and one pair is not. Report the letter of the non-parallel 
pair, enter it in the form and submit. Do NOT read the page source or call the site's HTTP 
endpoints directly. End with the letter.
```
