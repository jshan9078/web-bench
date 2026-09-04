# 275-memory-pairs

- **kind**: state across timed reveals (programmatic)
- **site**: localhost widget (widgetapp/memorypairs.py, port 8929)
- **what it tests**: remembering revealed symbols across a 4-second window and matching eight pairs
- **discrimination hypothesis**: requires tracking sixteen positions over many flips; forgetting positions costs extra flips but only failure to finish fails.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: all sixteen cards matched.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8929/ . It is a memory game: sixteen face-down cards; clicking a card reveals 
its symbol for 4 seconds; two revealed cards with the same symbol lock in place. Match all eight 
pairs (the page shows the count). Do NOT read the page source or call the site's HTTP endpoints 
directly. End with a one-line confirmation.
```
