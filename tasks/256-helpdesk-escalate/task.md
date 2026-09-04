# 256-helpdesk-escalate

- **kind**: multi-criteria search plus per-ticket edit (programmatic)
- **site**: localhost widget (widgetapp/helpdesk.py, port 8917)
- **what it tests**: combining filters, sorting by created time, and opening tickets to check the conversation before editing one ticket's four properties
- **discrimination hypothesis**: several tickets match the subject and tier; only those without an agent reply qualify, visible only in the detail pane; editing the wrong ticket or missing a property fails.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the target ticket has priority High, assignee Dana, status Escalated and the note; no other ticket changed.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8917/ . It is a helpdesk ticket queue with filters, sortable columns and a 
detail pane. Find the OLDEST ticket (by created time) that is Open, from a Gold-tier customer, 
mentions a refund in its subject, and has NO agent reply yet (open the ticket to check the 
conversation). Update that ticket only: priority High, assignee Dana, internal note "Escalated per 
refund policy", status Escalated. Do NOT read the page source or call the site's HTTP endpoints 
directly. End with the ticket number.
```
