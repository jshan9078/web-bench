# 117-gmaps-transit, verifier

**Method:** LLM-as-judge (Claude).

## Pass criteria

Captured evidence must show transit directions between the two places with the arrive-by option set to 9:00 AM next Monday (or an explicit statement that the control was unavailable, with the default route reported instead). The reported departure time, total duration, number of transfers and first line must match the first route shown in the captured panel. Estimated or unsupported values fail.

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually navigated to and evidence it captured THIS run.
