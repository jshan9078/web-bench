# 262-github-blame, verifier

**Method:** LLM-as-judge (Claude).

## Pass criteria

The judge determines via gh api (graphql blame on src/flask/app.py at main, or a local git blame of a fresh clone) the commit that last changed the 'def run(' line, and passes only if the reported short hash, author and date match; screenshots must show the blame view.

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually navigated to and evidence it captured THIS run.
