# 19-wiktionary-wotd

- **kind**: read (LLM-judge)
- **site**: en.wiktionary.org
- **what it tests**: locating a daily-rotating feature and reading a structured dictionary entry
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: the word is today's Word of the Day on the captured page and the details match its entry.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open English Wiktionary (https://en.wiktionary.org) and find today's Word of the Day. Open the
word's full entry and report: the word, its part of speech, the definition given for the Word of
the Day sense, and one example sentence or quotation from the entry (shortened is fine). End with
those four items.
```
