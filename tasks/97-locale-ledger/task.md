# 97-locale-ledger

- **kind**: localized data reading (programmatic)
- **site**: localhost widget (widgetapp/localeledger.py, port 8817)
- **what it tests**: reading dd/mm/yyyy dates and French number formatting (space thousands, comma decimals) correctly on a page whose locale is declared, and summing the right rows
- **discrimination hypothesis**: several March dates have a day of 12 or less and three non-March invoices fall on the 3rd, so a US-style reading selects a different set; the wrong total is plausible-looking. Agents that skim formats answer confidently and wrong.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: a submitted total is within 0.01 of the sum of the March 2026 invoices.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8817/ . It is the invoices page of a French accounting system. Report the 
total amount of all invoices dated in March 2026 (any status), enter it in the form at the bottom 
and submit (comma or dot decimals are both accepted). Do NOT read the page source or call the 
site's HTTP endpoints directly. End with the total.
```
