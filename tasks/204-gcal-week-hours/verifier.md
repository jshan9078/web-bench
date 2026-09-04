# 204-gcal-week-hours, verifier

**Method:** LLM-as-judge (Claude).

## Pass criteria

Captured week view (and any opened events) must show every timed event the agent lists; the listed times must match; the total (to the nearest quarter hour) and the busiest day must follow from them; all-day events must be excluded. A missed or misread event, or arithmetic error, fails.

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually navigated to and evidence it captured THIS run.
