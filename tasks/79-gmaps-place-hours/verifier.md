# 79-gmaps-place-hours, verifier

**Method:** LLM-as-judge (Claude).

Judging is **fully offline** from a captured evidence bundle, so a verdict can be re-derived
without re-running the model. For each run the judge is given the task prompt, the agent's final
answer and result text, the end-state page URL and text excerpt, the full browser command trace,
and the run's screenshots, video, and full model stream.

## Pass criteria

All values must appear in captured page state: the address and rating from the place card, the
next-Sunday hours from the expanded hours list (a screenshot or text showing the weekday rows), the
open/closed badge as displayed at capture time, and the nearby coffee shop's name plus the distance or
walking time Google displays for it relative to the library. Reporting a different weekday's hours, or a
shop without a displayed distance, fails.

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually
navigated to and evidence it captured THIS run. A correct-sounding answer with no supporting
navigation or capture in the trace fails, and where the live page disagrees with the answer, the
captured page wins.
