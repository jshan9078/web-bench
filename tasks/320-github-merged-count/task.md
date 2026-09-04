# 320-github-merged-count

- **kind**: judge
- **site**: github.com (pallets/click)
- **what it tests**: using the pull-request search UI with a merged-date range
- **discrimination hypothesis**: search syntax plus reading a count and ordering by merge date.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: count and title match the API.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Using the GitHub website (github.com, no API calls), find how many pull requests in the 
pallets/click repository were MERGED between 2025-01-01 and 2025-03-31 inclusive, and the title of 
the most recently merged one in that period. End with ANSWER: <count>; <title>.
```
