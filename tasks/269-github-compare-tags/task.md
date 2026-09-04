# 269-github-compare-tags

- **kind**: real-site compare view (LLM-judge)
- **site**: github.com/pallets/flask (signed-out)
- **what it tests**: using GitHub's compare view between two tags and reading its summary and commit list
- **discrimination hypothesis**: the compare URL form must be found, the counts read from the summary bar, and the newest commit identified in a list ordered oldest-first; the judge verifies via the GitHub compare API.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: The judge fetches https://api.github.com/repos/pallets/flask/compare/3.1.0...3.1.1 and checks total_commits, files (count) and the last commit's author login/name and short sha against the report; screenshots must show the compare page.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open https://github.com/pallets/flask (no sign-in needed). Use the repository's compare view 
(Compare, or the /compare/<base>...<head> page) to compare the tags 3.1.0 and 3.1.1. Report how 
many commits the comparison lists, the number of files changed, and the author and short hash of 
the MOST RECENT commit in that range. Read everything from the compare page; do not guess. If a 
consent or sign-in interstitial appears, dismiss it without signing in. End with those items.
```
