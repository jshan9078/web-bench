# 12-wikipedia-current-events

- **kind**: read (LLM-judge)
- **site**: en.wikipedia.org
- **what it tests**: portal navigation for date-specific current events
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: the three items appear under yesterday's date on the portal captured this run.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open the Wikipedia Current events portal (https://en.wikipedia.org/wiki/Portal:Current_events) and
locate YESTERDAY's date section. Pick three distinct items from different categories if possible.
For each, give a one-sentence summary in your own words and name the linked Wikipedia article the
item points to. End with the date you used and the three items.
```
