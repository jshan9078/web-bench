# 111-fill-level

- **kind**: proportional estimation (programmatic)
- **site**: localhost widget (widgetapp/filllevel.py, port 8831)
- **what it tests**: estimating a fill ratio against a tank's own height with only 0/50/100 marks, when the five tanks have different heights
- **discrimination hypothesis**: estimating tank C against a neighbour's scale, or reading absolute liquid height, gives errors well beyond 5 points; measuring against C's own marks is within it.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the submitted percentage is within 5 points of tank C's fill.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8831/ . It is a tank-farm overview showing five storage tanks of different 
sizes with their liquid levels as an IMAGE (read it from screenshots; only 0, 50 and 100 marks are 
drawn). What is tank C's fill level as a percentage of ITS OWN capacity (within 5 points)? Enter it 
in the form below the image and submit. Do NOT read the page source or call the site's HTTP 
endpoints directly. End with the percentage.
```
