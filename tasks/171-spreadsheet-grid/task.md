# 171-spreadsheet-grid

- **kind**: keyboard-driven grid editing (programmatic)
- **site**: localhost widget (widgetapp/gridsheet.py, port 8859)
- **what it tests**: editing cells in a spreadsheet-style grid that is driven by cell focus and keys (arrows, type, Enter) rather than form fields, including entering a formula
- **discrimination hypothesis**: the grid has no input until a cell is activated; agents that type into the wrong cell, leave an edit uncommitted, or write a value instead of a formula fail; three edits plus Save.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: saved A6 is Batteries, C5 is 1.40, D7 is =SUM(D2:D6) and evaluates to the correct total.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8859/ . It is a small spreadsheet web app: click a cell or move with the 
arrow keys, type to edit, Enter commits; formulas like =B2*C2 and =SUM(D2:D6) are supported. Make 
these changes: fix the misspelled item name in A6 to "Batteries"; set the unit price of Adapters (its Unit price cell, C5) to 1.40; put a formula in D7 that sums the line totals D2 to D6. Then click Save. Do NOT 
read the page source or call the site's HTTP endpoints directly. End with the total shown in D7.
```
