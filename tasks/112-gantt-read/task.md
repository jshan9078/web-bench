# 112-gantt-read

- **kind**: timeline reading (programmatic)
- **site**: localhost widget (widgetapp/gantt.py, port 8832)
- **what it tests**: reading which bars cover a given day on a Gantt chart with a day axis and no dates printed on the bars
- **discrimination hypothesis**: bars that end the day before or start the day after the target look like they overlap; off-by-one against the axis changes the set. The answer is an exact set of names.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the submitted list equals the set of tasks whose bar covers the named day.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8832/ . The page shows a project Gantt chart as an IMAGE (read it from 
screenshots). The question under the chart names a day; list ALL tasks whose bar covers that day, 
comma-separated, in the form and submit. Do NOT read the page source or call the site's HTTP 
endpoints directly. End with the list.
```
