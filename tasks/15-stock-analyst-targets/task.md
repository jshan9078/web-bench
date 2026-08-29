# 15-stock-analyst-targets

- **kind**: read (LLM-judge)
- **site**: finance.yahoo.com
- **what it tests**: quote page reading plus a tab pivot for analyst data
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: all figures match the captured quote and analysis pages from this run.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
On Yahoo Finance (https://finance.yahoo.com), open the quote page for NVDA. Report the current or
last-close price, the day's range, market cap, and the next earnings date shown. Then open the
Analysis tab, or the Analyst Price Targets widget on the summary page, and report the average
analyst price target (either source is fine). End with those five values
exactly as displayed, noting whether the market was open.
```
