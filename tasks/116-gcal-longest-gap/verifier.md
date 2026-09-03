# 116-gcal-longest-gap, verifier

**Method:** LLM-as-judge (Claude).

## Pass criteria

From the captured week view, the chosen day must have the longest 09:00-17:00 free stretch with all-day events treated as fully blocking (earlier day on ties). The event must cover the middle 60 minutes of that stretch within 15 minutes, show no notification in the details or editor, appear on the grid screenshot, and be shown deleted afterwards. Wrong day, wrong placement, a remaining reminder, or missing cleanup fails.

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually navigated to and evidence it captured THIS run.
