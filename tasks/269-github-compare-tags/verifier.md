# 269-github-compare-tags, verifier

**Method:** LLM-as-judge (Claude).

## Pass criteria

The judge fetches https://api.github.com/repos/pallets/flask/compare/3.1.0...3.1.1 and checks total_commits, files (count) and the last commit's author login/name and short sha against the report; screenshots must show the compare page.

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually navigated to and evidence it captured THIS run.
