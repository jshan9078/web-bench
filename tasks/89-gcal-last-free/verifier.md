# 89-gcal-last-free, verifier

**Method:** LLM-as-judge (Claude).

## Pass criteria

From the captured week view, the chosen day must be the LAST Monday-to-Friday day with no event overlapping 09:00-11:00 (all-day events, including holidays, count as conflicts). The captured event must show 09:30-10:15 on that day, the description text, and the Tomato colour; the grid screenshot must show it, and a later capture must show it deleted. Creating on a day with a conflict, on an earlier free day than the last one, or with default colour or no description, fails.

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually navigated to and evidence it captured THIS run.
