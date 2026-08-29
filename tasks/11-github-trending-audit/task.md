# 11-github-trending-audit

- **kind**: read (LLM-judge)
- **site**: github.com
- **what it tests**: trending discovery plus repo metadata drill-down across tabs
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: all five figures match the trending page and repo pages captured this run.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open GitHub trending for Python, daily view (https://github.com/trending/python?since=daily). Take
the top repository. Open it and report: its one-line description, the stars gained today (from the
trending page), total stars, the latest release tag and its date (from the Releases page; say so if
there are no releases), and the current number of open issues. End with those five facts.
```
