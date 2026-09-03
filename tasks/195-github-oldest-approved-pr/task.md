# 195-github-oldest-approved-pr

- **kind**: real-site list navigation with per-item checks (LLM-judge)
- **site**: github.com/pallets/flask (signed-out)
- **what it tests**: sorting open pull requests by age and checking review states until the oldest one with an approval is found
- **discrimination hypothesis**: the review filter (review:approved) and oldest-first sort exist but must be discovered; scanning PR pages one by one is slow and error-prone; the judge verifies via the GitHub API (pulls?state=open&sort=created&direction=asc plus each PR's reviews).
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: The judge determines via the GitHub API the open pull request with the earliest created_at that has at least one review with state APPROVED, and checks the reported number, title, author, creation date and an approving reviewer's username against it; screenshots must show the PR list and the PR's review section.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open https://github.com/pallets/flask/pulls (no sign-in needed). Among the OPEN pull requests, find 
the one with the OLDEST creation date that has at least one approving review. Report its number, 
title, author, creation date and the username of an approving reviewer. Use the list's sort and 
filter options and the PR pages' review sections; read everything from the pages, do not guess. If 
a consent or sign-in interstitial appears, dismiss it without signing in. End with those items.
```
