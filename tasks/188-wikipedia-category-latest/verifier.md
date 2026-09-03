# 188-wikipedia-category-latest, verifier

**Method:** LLM-as-judge (Claude).

## Pass criteria

The judge verifies via the MediaWiki API (list=categorymembers for the category, then the latest revision timestamp and user of each member article) that the reported article is the most recently edited member and that the timestamp and username match; captured pages must show the history or Related changes view used.

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually navigated to and evidence it captured THIS run.
