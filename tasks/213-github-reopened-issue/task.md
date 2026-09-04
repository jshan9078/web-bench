# 213-github-reopened-issue

- **kind**: real-site timeline search (LLM-judge)
- **site**: github.com/pallets/flask (signed-out)
- **what it tests**: finding the most recently reopened issue via search qualifiers and reading its timeline for the reopen event and actor
- **discrimination hypothesis**: reopened events are visible only in timelines; the judge checks via the GitHub events API (issues/events?per_page=100, event=reopened) that the reported issue, date and actor are the most recent reopen.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: The judge fetches https://api.github.com/repos/pallets/flask/issues/events?per_page=100 (paging if needed) and finds the most recent event of type reopened; the reported issue number, reopen date and actor must match it, and screenshots must show the issue's timeline.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open https://github.com/pallets/flask/issues (no sign-in needed). Find the MOST RECENTLY REOPENED 
issue in the repository (an issue whose timeline shows it was closed and later reopened; it may be 
open or closed now). Report the issue number and title, the date it was reopened, and who reopened 
it. Use the issue search and filters, and read the issue timelines; do not guess. If a consent or 
sign-in interstitial appears, dismiss it without signing in. End with those items.
```
