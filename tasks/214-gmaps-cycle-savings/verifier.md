# 214-gmaps-cycle-savings, verifier

**Method:** LLM-as-judge (Claude).

## Pass criteria

Captured evidence must show walking and cycling directions from the library to each destination; the four reported times must match the captured panels and the stated larger saving must follow from them.

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually navigated to and evidence it captured THIS run.
