# 167-github-issue-pr, verifier

**Method:** LLM-as-judge (Claude).

## Pass criteria

The judge checks via the GitHub API (curl https://api.github.com/repos/pallets/flask/issues?state=closed&labels=bug&sort=updated) that the reported issue is the most recently closed bug-labelled issue that was closed by a merged pull request, and that the PR number, author and merge date match. Captured screenshots must show the issue and PR pages. Any mismatch or an unverifiable claim fails.

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually navigated to and evidence it captured THIS run.
