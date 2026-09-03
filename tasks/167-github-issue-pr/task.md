# 167-github-issue-pr

- **kind**: real-site cross-page tracing (LLM-judge)
- **site**: github.com/pallets/flask (signed-out)
- **what it tests**: using issue filters (closed, label bug, sorted by recently updated or closed) and following the linked pull request to read its author and merge date
- **discrimination hypothesis**: the most recently closed bug issue closed by a merged PR requires checking several candidates' timelines; reporting an issue closed by a commit or without a linked PR, or misreading the merge date, fails. The judge verifies against the GitHub API.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: The judge checks via the GitHub API (curl https://api.github.com/repos/pallets/flask/issues?state=closed&labels=bug&sort=updated) that the reported issue is the most recently closed bug-labelled issue that was closed by a merged pull request, and that the PR number, author and merge date match. Captured screenshots must show the issue and PR pages. Any mismatch or an unverifiable claim fails.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open https://github.com/pallets/flask (no sign-in needed). Using the Issues tab and its filters, 
find the MOST RECENTLY CLOSED issue that carries the label "bug" and was closed by a merged pull 
request (the issue's timeline or linked PR shows this). Report the issue number and title, the pull 
request number that closed it, that pull request's author, and the date it was merged. Read 
everything from the pages you navigate to; do not guess. If a consent or sign-in interstitial 
appears, dismiss it without signing in. End with those items.
```
