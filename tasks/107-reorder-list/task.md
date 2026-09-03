# 107-reorder-list

- **kind**: reordering without drag (programmatic)
- **site**: localhost widget (widgetapp/reorder.py, port 8827)
- **what it tests**: reordering a list through keyboard grab/move/drop or per-row Move up/down menus when drag is unavailable, with a near-duplicate step name
- **discrimination hypothesis**: placing the step after 'Notify on-call lead' instead of 'Notify on-call', disturbing the relative order of other steps, or not saving all fail.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the saved order equals the initial order with 'Rotate API keys' moved to directly after 'Notify on-call'.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8827/ . It is a runbook editor with an ordered list of steps. Move the step 
"Rotate API keys" so that it comes DIRECTLY AFTER the step "Notify on-call" (not "Notify on-call 
lead"), leaving the relative order of all other steps unchanged, then click Save order. Do NOT read 
the page source or call the site's HTTP endpoints directly. End with the final order.
```
