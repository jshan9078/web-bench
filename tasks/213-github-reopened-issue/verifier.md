# 213-github-reopened-issue, verifier

**Method:** LLM-as-judge (Claude).

## Pass criteria

The judge fetches https://api.github.com/repos/pallets/flask/issues/events?per_page=100 (paging if needed) and finds the most recent event of type reopened; the reported issue number, reopen date and actor must match it, and screenshots must show the issue's timeline.

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually navigated to and evidence it captured THIS run.
