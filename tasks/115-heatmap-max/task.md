# 115-heatmap-max

- **kind**: colour intensity comparison (programmatic)
- **site**: localhost widget (widgetapp/heatmap.py, port 8835)
- **what it tests**: finding the darkest cell in a 7x16 heatmap where two runners-up are one step lighter, and reading its row and column labels
- **discrimination hypothesis**: subtle shade differences and label alignment across a wide grid cause wrong picks; the maximum is unambiguous to a careful eye.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the submitted day and hour match the maximum cell.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8835/ . The page shows a weekday-by-hour activity heatmap as an IMAGE with a 
colour scale and no numbers (read it from screenshots). Identify the single cell with the HIGHEST 
activity and enter it as 'Day HH' (for example: Tue 14) in the form and submit. Do NOT read the 
page source or call the site's HTTP endpoints directly. End with the day and hour.
```
