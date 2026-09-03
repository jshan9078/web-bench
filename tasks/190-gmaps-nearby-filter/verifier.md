# 190-gmaps-nearby-filter, verifier

**Method:** LLM-as-judge (Claude).

## Pass criteria

Captured evidence must show the Nearby pharmacy results with Open now and Rating 4.0+ applied, and the reported pharmacy must be the one with the shortest walking time among those results as shown on the page (results list or Directions), with name, address, rating and walking time matching the captured panels.

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually navigated to and evidence it captured THIS run.
