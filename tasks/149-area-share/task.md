# 149-area-share

- **kind**: irregular area estimation (programmatic)
- **site**: localhost widget (widgetapp/areashare.py, port 8848)
- **what it tests**: estimating what fraction of a rectangle an irregular polygon covers, within 5 points
- **discrimination hypothesis**: area-fraction estimation of irregular shapes is systematically biased (over-estimating compact dark regions); the legend and scale are explicit, so the failure is estimation.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the submitted percentage is within 5 points of the flooded fraction.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8848/ . It is a satellite survey tile of a field outlined in yellow with a 
flooded region in dark blue, rendered as an IMAGE (read it from screenshots). Estimate what 
percentage of the outlined field is flooded (within 5 points), enter it in the form below the tile 
and submit. Do NOT read the page source or call the site's HTTP endpoints directly. End with the 
percentage.
```
