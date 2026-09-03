# 87-gcal-scheduling, verifier

**Method:** LLM-as-judge (Claude).

## Pass criteria

From the captured week view, the chosen day must be the first Monday-to-Friday day with no event overlapping 14:00-16:00 (all-day events count as conflicts). The captured event editor or details must show 14:30-15:15, a single 30-minute notification, and visibility Private. The grid screenshot must show the event on that day, and a later capture must show it deleted. Creating on a day with a conflict, leaving the default 10-minute notification, or default visibility, fails.

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually navigated to and evidence it captured THIS run.
