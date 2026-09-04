# 319-github-first-release, verifier

**Method:** LLM-as-judge (Claude).

## Pass criteria

The judge determines the earliest tag containing commit 0ec7f713 (e.g. by checking `gh api repos/pallets/flask/compare/<tag>...0ec7f713` for the candidate tags 3.0.0 and neighbours; a tag contains the commit when the status is identical or behind) and its release date from `gh api repos/pallets/flask/releases/tags/<tag>`; both must match the report and the screenshots must show github.com pages.

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually navigated to and evidence it captured THIS run.
