# 205-gmaps-transit-compare, verifier

**Method:** LLM-as-judge (Claude).

## Pass criteria

Captured evidence must show transit routes with the arrive-by 8:00 AM next Monday setting; the reported fewest-transfers route and fastest route (departure, arrival, total time, transfers) must match the captured route list and details, including the case where they coincide.

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually navigated to and evidence it captured THIS run.
