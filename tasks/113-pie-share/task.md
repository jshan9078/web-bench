# 113-pie-share

- **kind**: angle-to-share estimation (programmatic)
- **site**: localhost widget (widgetapp/pieshare.py, port 8833)
- **what it tests**: estimating one pie segment's share against the quarter marks with no labels
- **discrimination hypothesis**: angle-to-percentage estimation is a documented vision-model weakness; segments near a quarter or half are excluded so the estimate must come from the wedge itself.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the submitted share is within 4 points of the segment's true share.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8833/ . The page shows a pie chart of traffic sources as an IMAGE with a 
legend and no percentage labels (read it from screenshots). The question under the chart names a 
segment; estimate its share as a percentage (within 4 points), enter it in the form and submit. Do 
NOT read the page source or call the site's HTTP endpoints directly. End with the percentage.
```
