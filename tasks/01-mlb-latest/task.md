# 01-mlb-latest

- **kind**: read (LLM-judge)
- **site**: ESPN / MLB (agent's choice)
- **what it tests**: Latest scores, then drill into the Cubs box score for run-scorers.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: games/scores and the Cubs' run-scorers match the pages.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Find the results of the latest completed MLB game day (yesterday's games). For each game, report the two teams and the final score. THEN, for the Chicago Cubs' most recent game, open its box score and list every Cubs player who scored a run (the Cubs' scorers). On Chrome, just searching mlb shows the scores; open the Cubs game for the box score. Base your answer only on what the pages show. End with (1) the list of games and scores, and (2) the Cubs' scorers.
```
