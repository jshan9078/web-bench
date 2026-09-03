# 194-wikipedia-revert, verifier

**Method:** LLM-as-judge (Claude).

## Pass criteria

The judge fetches the last 50 revisions with tags and comments via the MediaWiki API (prop=revisions&rvprop=ids|timestamp|user|comment|tags&rvlimit=50) and determines the most recent revision tagged mw-reverted (or whose successor's comment undoes it); the reported reverted timestamp and editor, and reverting timestamp and editor, must match; captured history pages must show them.

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually navigated to and evidence it captured THIS run.
