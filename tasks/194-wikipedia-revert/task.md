# 194-wikipedia-revert

- **kind**: real-site history reading (LLM-judge)
- **site**: en.wikipedia.org (signed-out)
- **what it tests**: reading a page history for revert markers (tags, 'Undid revision' summaries), identifying the most recent reverted edit and its reverter
- **discrimination hypothesis**: reverts are marked by tags and summaries that must be read across two rows; picking the reverting edit instead of the reverted one, or an older revert, fails; the judge verifies with the MediaWiki API (revisions with tags and comments).
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: The judge fetches the last 50 revisions with tags and comments via the MediaWiki API (prop=revisions&rvprop=ids|timestamp|user|comment|tags&rvlimit=50) and determines the most recent revision tagged mw-reverted (or whose successor's comment undoes it); the reported reverted timestamp and editor, and reverting timestamp and editor, must match; captured history pages must show them.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open English Wikipedia (https://en.wikipedia.org) and open the page history of the article "Toronto 
Public Library". Among the 50 most recent revisions, find the MOST RECENT edit that was 
subsequently reverted (undone or rolled back by a later edit). Report the reverted edit's timestamp 
(UTC) and its editor, and the timestamp and editor of the edit that reverted it. Use the history 
page (its tags and edit summaries, and diffs if needed); read everything from the pages, do not 
guess. End with those four items.
```
