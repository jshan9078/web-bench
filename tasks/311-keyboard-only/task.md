# 311-keyboard-only

- **kind**: keyboard-driven UI with no clickable controls (programmatic)
- **site**: localhost widget (widgetapp/keyboardlist.py, port 8949)
- **what it tests**: operating a list purely by key presses, applying a two-condition filter
- **discrimination hypothesis**: requires the press command and cursor bookkeeping; clicks do nothing.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the submitted set equals the overdue-above-500 set.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8949/ . The invoice list is operated only with the keyboard: j and k move the 
cursor, x marks or unmarks the current row, Enter submits the marked rows. Mouse clicks are 
ignored. Mark exactly the invoices whose status is Overdue AND whose amount is above $500, then 
submit. Do NOT read the page source or call the site's HTTP endpoints directly. End with the 
invoice numbers you submitted.
```
