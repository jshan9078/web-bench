# 195-github-oldest-approved-pr, verifier

**Method:** LLM-as-judge (Claude).

## Pass criteria

The judge determines via the GitHub API the open pull request with the earliest created_at that has at least one review with state APPROVED, and checks the reported number, title, author, creation date and an approving reviewer's username against it; screenshots must show the PR list and the PR's review section.

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually navigated to and evidence it captured THIS run.
