# 56-sunrise-reykjavik

- **kind**: read (LLM-judge)
- **site**: timeanddate.com
- **what it tests**: location lookup and reading precise, date-specific astronomical times
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: the three values match tomorrow's row on the captured sun page.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
On timeanddate.com (https://www.timeanddate.com), open the sun/daylight page for Reykjavik,
Iceland. For TOMORROW's date, report the exact sunrise time, sunset time, and the day length,
exactly as the table shows. End with tomorrow's date and the three values.
```
