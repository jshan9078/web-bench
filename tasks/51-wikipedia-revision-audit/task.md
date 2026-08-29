# 51-wikipedia-revision-audit

- **kind**: read (LLM-judge)
- **site**: en.wikipedia.org
- **what it tests**: article history inspection: who edited what, when
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: the newest revision's details match the captured history page.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
On Wikipedia, open the article: Large language model. Open its View history page and report the
MOST RECENT revision: its date and time, the username or IP of the editor, and the edit summary
(or note that the summary is empty). Also report the article's current number of references
(count shown in or derived from the References section). End with those details.
```
