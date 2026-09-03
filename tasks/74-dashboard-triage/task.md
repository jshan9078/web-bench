# 74-dashboard-triage

- **kind**: action + navigation (programmatic)
- **site**: localhost test site (widgetapp/dashboard.py, port 8796)
- **what it tests**: multi-constraint filtering in a SaaS-style console: virtualized list (DOM shows only visible rows), server pagination behind Load more, filter chips, a custom sort menu that clears filters, a detail drawer, a note-required confirm flow, a similarly named decoy company and a more recent Pending decoy ticket
- **discrimination hypothesis**: every obstacle is a real-app pattern; agents that trust a snapshot of the visible rows, forget to load the second page, pick the decoy company, take the more recent Pending ticket, or lose their filters after sorting all end on the wrong ticket. The verdict is objective.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: exactly the target ticket resolved, with a note citing the company's other open ticket id.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8796/ , a helpdesk console. Find the ticket that is (a) from the company "Halvorsen
Logistics" exactly (there is a similarly named company; ignore it), (b) priority High, (c) status Open, and
(d) the most recently opened among those. Open it and RESOLVE it with the resolution note
"Duplicate of #<id>", where <id> is the ticket number of the company's OTHER ticket that is still Open (any
priority). Notes: only the first 40 tickets are loaded until you use "Load more"; the list only renders the
rows near your scroll position, so filters and search are the reliable way to narrow it; changing the sort
clears the filters. Do not resolve any other ticket. End with the resolved ticket id and the id you cited.
```
