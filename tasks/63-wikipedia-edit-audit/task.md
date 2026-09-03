# 63-wikipedia-edit-audit

- **kind**: read + filtering (LLM-judge)
- **site**: en.wikipedia.org
- **what it tests**: reading a revision history with mixed bot, minor, and reverted edits; applying two exclusion filters consistently across five rows; reading tags
- **discrimination hypothesis**: long-horizon bookkeeping over a dense list: a single mis-applied filter (counting a minor edit, or a bot) or a misread byte delta fails. Live history is pretraining-proof.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: the five rows match the captured history page after excluding bots and minor edits, with correct byte deltas and revert status.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
On English Wikipedia, open the article "Artificial intelligence" and go to its View history page. Using
ONLY the history list as displayed, identify the FIVE most recent edits that are NOT by bot accounts
(usernames ending in "bot"/"Bot" or tagged as bot edits) and NOT marked as minor (the small "m" flag).
For each of the five, report: the username or IP, the timestamp as shown, the byte change (for example
+212 or -48), and the first 80 characters of the edit summary. Then state, for each, whether the history
shows it was later reverted or undone (look for Reverted/Undo/Manual revert tags or a later summary that
undoes it). Base everything on the captured history page, not on the article text. End with the five rows
and the revert status of each.
```
