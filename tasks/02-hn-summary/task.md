# 02-hn-summary

- **kind**: read (LLM-judge)
- **site**: news.ycombinator.com
- **what it tests**: Read the front page and synthesize a themed digest with an agents section.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: summary reflects the real front-page stories and includes the agents section.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open Hacker News (https://news.ycombinator.com) and read the current front page. Write a concise summary of what's on the front page right now, grouping the notable stories by theme. Include a DEDICATED section titled 'Agents / agentic harnesses' listing any front-page stories about AI agents, agentic coding tools/harnesses, or LLM tool-use (give their titles); if there are none, say so explicitly. Base your summary only on the stories actually shown on the page (you may open a story or its comments to clarify). End with the themed summary including that dedicated section.
```
