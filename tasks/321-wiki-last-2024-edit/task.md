# 321-wiki-last-2024-edit

- **kind**: judge
- **site**: en.wikipedia.org
- **what it tests**: navigating a revision history by date and reading an edit's metadata
- **discrimination hypothesis**: the history view needs date navigation and careful reading of timestamps in UTC.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: editor, date and summary match the API.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Using the English Wikipedia website (no API calls), open the page history of the article "Flask 
(web framework)" and find the LAST edit made in 2024 (UTC): report the username or IP of the 
editor, the date, and the edit summary. End with ANSWER: <editor>, <date>, <summary>.
```
