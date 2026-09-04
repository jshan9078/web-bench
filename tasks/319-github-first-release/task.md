# 319-github-first-release

- **kind**: judge
- **site**: github.com (pallets/flask)
- **what it tests**: navigating from a commit to the releases/tags that contain it
- **discrimination hypothesis**: requires understanding GitHub's commit header tag list or the compare view; the trace task failed Opus before.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: tag and date match the earliest release containing the commit.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Using the GitHub website (github.com, no API calls, no git clone), find the EARLIEST release tag of 
the pallets/flask repository that contains commit 0ec7f713d679ceed2c605e62ac5d38d579f29fa0. Report 
the tag name and the date of that release. End with ANSWER: <tag>, <date>.
```
