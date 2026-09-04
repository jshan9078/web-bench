# 246-wikipedia-sandbox-edit, verifier

**Method:** LLM-as-judge (Claude).

## Pass criteria

The judge queries the sandbox's revisions (action=query&prop=revisions&titles=Wikipedia:Sandbox&rvprop=timestamp|comment|user&rvlimit=50 and rvprop=content for the candidate) and passes the run only if a revision within the run's time window has the summary 'webbench test line' and the content ends with the exact line 'webbench check: harbor 4471', and the run reported that revision's timestamp from the history page. A CAPTCHA/protection report is a pass only if the captured page shows it.

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually navigated to and evidence it captured THIS run.
