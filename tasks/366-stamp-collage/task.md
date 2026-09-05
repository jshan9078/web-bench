# 366-stamp-collage

- **kind**: counting motifs under occlusion (programmatic)
- **site**: localhost widget (widgetapp/stampcollage.py, port 8993)
- **what it tests**: counting one motif among 55 overlapping stamps
- **discrimination hypothesis**: partly covered stamps still count when the motif is visible; occlusion counting failed Sonnet twice before.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted value equals the true value.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8993/ . The page shows an IMAGE (read it from screenshots). It shows a 
collage of overlapping postage stamps, each with one motif (triangle, circle, star or square). 
Count exactly how many stamps show a TRIANGLE motif (a stamp counts if its motif is visible, even 
when the stamp is partly covered), enter the number in the form and submit. Do NOT read the page 
source or call the site's HTTP endpoints directly. End with the count.
```
