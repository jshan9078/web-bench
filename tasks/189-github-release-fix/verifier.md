# 189-github-release-fix, verifier

**Method:** LLM-as-judge (Claude).

## Pass criteria

The judge checks CHANGES.rst (raw) and the GitHub releases API to confirm the first version whose changelog lists the fix for #4297 (PR #4487), its release date, and the exact line; the run passes only if all three match and screenshots show the release/changelog pages.

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually navigated to and evidence it captured THIS run.
