# 109-legend-match

- **kind**: colour legend matching (programmatic)
- **site**: localhost widget (widgetapp/legendmatch.py, port 8829)
- **what it tests**: matching six related line colours to legend swatches where series cross often, then reading one value
- **discrimination hypothesis**: the overall peak belongs to a different region than the September leader, and adjacent shades are easy to swap; picking the wrong series or misreading against the grid fails.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the submitted region is the September leader and the value is within 3.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8829/ . The page shows a six-region monthly sales line chart as an IMAGE with 
a colour legend (read it from screenshots). Which region had the HIGHEST sales in September, and 
what was its value in k units (within a few)? Enter your answer in the form as 'Region, value' and 
submit. Do NOT read the page source or call the site's HTTP endpoints directly. End with the region 
and value.
```
