# 114-scatter-threshold

- **kind**: counting against a reference line (programmatic)
- **site**: localhost widget (widgetapp/scatter.py, port 8834)
- **what it tests**: counting points above a dashed threshold line among 40-60 points, including two that sit just above it and two just below
- **discrimination hypothesis**: near-line points and dense clusters cause over- or under-counts; the count is exact.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the submitted count equals the number of points above the SLA line.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8834/ . The page shows a latency scatter plot as an IMAGE with a dashed SLA 
line (read it from screenshots). Count exactly how many points lie ABOVE the SLA line, enter the 
number in the form and submit. Do NOT read the page source or call the site's HTTP endpoints 
directly. End with the count.
```
