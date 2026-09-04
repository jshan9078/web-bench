# 321-wiki-last-2024-edit, verifier

**Method:** LLM-as-judge (Claude).

## Pass criteria

The judge queries `https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=Flask_(web_framework)&rvlimit=1&rvstart=2024-12-31T23:59:59Z&rvdir=older&rvprop=user|timestamp|comment&format=json` and compares user, date and comment with the report; screenshots must show the Wikipedia history page.

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually navigated to and evidence it captured THIS run.
