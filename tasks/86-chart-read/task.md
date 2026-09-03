# 86-chart-read

- **kind**: read + chart perception (programmatic)
- **site**: localhost widget (widgetapp/chartread.py, port 8806)
- **what it tests**: estimating values off an unlabeled line chart against gridlines and comparing consecutive differences
- **discrimination hypothesis**: embedded dashboards ship charts like this; agents that eyeball the steepest-looking segment instead of measuring against the grid pick the wrong month when two drops are close.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: correct month and value within 5 k$.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8806/ . The page shows a monthly revenue line chart as an IMAGE with gridlines and
axis ticks but no data labels or tooltips; read it from screenshots. Report the month with the LARGEST
drop from the previous month and that month's value in k$ (use the gridlines; within a few k$ is fine).
Enter both in the form below the chart and submit. Do NOT read the page source or call the site's HTTP
endpoints directly. End with the month and value.
```
