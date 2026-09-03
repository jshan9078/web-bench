# 163-gmaps-route-options, verifier

**Method:** LLM-as-judge (Claude).

## Pass criteria

Captured evidence must show (1) the two-point route with its distance and time, (2) a three-point route in the order Union Station, Toronto Reference Library, Toronto Zoo with its totals, (3) the same route with both Avoid tolls and Avoid highways enabled and its totals. Reported figures must match the captured panels; a route in the wrong order, missing option, or estimated figure fails.

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually navigated to and evidence it captured THIS run.
