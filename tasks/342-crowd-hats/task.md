# 342-crowd-hats

- **kind**: exact visual counting or tracing (programmatic)
- **site**: localhost widget (widgetapp/crowdhats.py, port 8976)
- **what it tests**: exact counting of a colour attribute across ~140 small figures
- **discrimination hypothesis**: small red arcs among 140 heads; other hat colours as decoys.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted value equals the true value.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8976/ . The page shows an IMAGE (read it from screenshots). It shows a dense 
crowd of about 140 people from above; some wear a coloured hat. Count exactly how many wear a RED 
hat, enter the number in the form and submit. Do NOT read the page source or call the site's HTTP 
endpoints directly. End with the count.
```
