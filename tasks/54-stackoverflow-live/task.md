# 54-stackoverflow-live

- **kind**: read (LLM-judge)
- **site**: stackoverflow.com
- **what it tests**: live feed reading: the newest activity in a tag
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: the question is the newest in the tag as captured, with matching metadata.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
On Stack Overflow (https://stackoverflow.com), open the questions list for the tag rust, sorted by
NEWEST. Report the newest question's exact title, how long ago it was asked, the asker's display
name, and its current answer and view counts. Then open the question and give a one-sentence
summary of what is being asked, in your own words. End with those details.
```
