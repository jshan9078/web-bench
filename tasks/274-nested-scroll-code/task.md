# 274-nested-scroll-code

- **kind**: nested in-element scrolling and search (programmatic)
- **site**: localhost widget (widgetapp/scrollnest.py, port 8932)
- **what it tests**: reaching a line inside an inner scroll panel inside an outer scroll panel far down a long page, among 400 decoy lines
- **discrimination hypothesis**: page-level scrolling does not move the inner panel; find or scroll tools must target the right container; near-identical decoys.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted code equals account HB-4471's code.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8932/ . The page has a confirmation ledger further down, inside a scrollable 
panel that itself contains an inner scrollable list of account lines. Find the line for account 
HB-4471 and enter its confirmation code in the form at the top of the page, then submit. Do NOT 
read the page source or call the site's HTTP endpoints directly. End with the code.
```
