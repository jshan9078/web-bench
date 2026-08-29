# 10-arxiv-agents-paper

- **kind**: read (LLM-judge)
- **site**: arxiv.org
- **what it tests**: navigate a daily listing, select by content, read an abstract
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: the paper is on today's cs.CL new-submissions listing and the summary reflects its actual abstract.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open the arXiv new submissions listing for cs.CL (https://arxiv.org/list/cs.CL/new). Find the FIRST
paper in the listing whose title or abstract mentions agents (agent, agents, or agentic). Open its
abstract page and report: the arXiv identifier, the full title, the number of authors, a
two-sentence summary of the abstract in your own words, and the direct PDF link. End with those
five items.
```
