# 164-gcal-recurring, verifier

**Method:** LLM-as-judge (Claude).

## Pass criteria

Captured evidence must show the event created at 09:15-09:30 with recurrence weekly on Tuesday and Thursday ending after 6 occurrences (rule text or six occurrences across three weeks on the month view), colour Sage, and afterwards the series deleted with the month view clear. Wrong days, wrong end condition, wrong colour, or remaining occurrences fail.

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually navigated to and evidence it captured THIS run.
