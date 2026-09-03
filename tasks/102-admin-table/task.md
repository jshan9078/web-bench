# 102-admin-table

- **kind**: distrusting a buggy UI (programmatic)
- **site**: localhost widget (widgetapp/admintable.py, port 8822)
- **what it tests**: noticing that the table's balance sort is a string sort (998.10 ranks above 8431.20) and finding the true maximum anyway (show all rows, or verify the sorted order)
- **discrimination hypothesis**: sorting by balance descending shows a 3-digit balance at the top; agents that trust the sort report it. Two customers share the name of the true maximum, so the id matters.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the submitted id is the customer with the numerically largest balance.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8822/ . It is a customers table in an admin tool (paginated, sortable, with a 
rows-per-page selector). Which customer has the HIGHEST outstanding balance? Enter that customer's 
id in the form at the bottom and submit. Do NOT read the page source or call the site's HTTP 
endpoints directly. End with the customer id and name.
```
