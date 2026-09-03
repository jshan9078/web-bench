# 100-dual-axis-chart

- **kind**: dual-axis chart reading (programmatic)
- **site**: localhost widget (widgetapp/dualaxis.py, port 8820)
- **what it tests**: reading two series against two different axes and reporting a value from one series at the month determined by the other
- **discrimination hypothesis**: the tallest bar is a different month from the margin peak, and reading the line against the left axis gives nonsense; the margin peak is 3 points clear of the runner-up.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: correct month and revenue within 5 k$.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8820/ . The page shows a monthly performance chart as an IMAGE: revenue bars 
against the LEFT axis (k$) and a gross-margin line against the RIGHT axis (%). Read it from 
screenshots. Report the month with the HIGHEST gross margin and the revenue (k$) in that month 
(within a few k$ is fine). Enter both in the form below the chart and submit. Do NOT read the page 
source or call the site's HTTP endpoints directly. End with the month and revenue.
```
