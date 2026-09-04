# 320-github-merged-count, verifier

**Method:** LLM-as-judge (Claude).

## Pass criteria

The judge runs `gh api -X GET search/issues -f q='repo:pallets/click is:pr is:merged merged:2025-01-01..2025-03-31' -f sort=updated` to get total_count, then lists the PRs' merged_at via `gh api repos/pallets/click/pulls/<n>` (or `gh pr list --repo pallets/click --state merged --search 'merged:2025-01-01..2025-03-31' --json number,title,mergedAt`) to find the latest merge; count and title must match the report; screenshots must show github.com pages.

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually navigated to and evidence it captured THIS run.
