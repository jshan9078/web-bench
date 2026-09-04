# 252-keyboard-datagrid

- **kind**: filtering plus keyboard multi-select and bulk action (programmatic)
- **site**: localhost widget (widgetapp/datagrid.py, port 8914)
- **what it tests**: narrowing a 120-row grid with column filters, selecting the right rows via keyboard, and applying a bulk status change
- **discrimination hypothesis**: the near-duplicate customer 'Acme Ltd (EU)' matches a naive filter; selecting with Space/Shift+Arrow must cover exactly the Pending rows; extra or missing rows fail.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: exactly the target customer's initially Pending orders are Shipped and nothing else changed.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8914/ . It is an orders grid with column filter boxes, keyboard row selection 
(Space toggles, Shift+ArrowDown extends) and a bulk status action. Mark every order from the 
customer "Acme Ltd" (exactly that name, not "Acme Ltd (EU)") that is currently Pending as Shipped, 
and change no other order. Do NOT read the page source or call the site's HTTP endpoints directly. 
End with the order numbers you updated.
```
