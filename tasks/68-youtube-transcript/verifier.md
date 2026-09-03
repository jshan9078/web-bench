# 68-youtube-transcript, verifier

**Method:** LLM-as-judge (Claude).

Judging is **fully offline** from a captured evidence bundle, so a verdict can be re-derived
without re-running the model. For each run the judge is given the task prompt, the agent's final
answer and result text, the end-state page URL and text excerpt, the full browser command trace,
and the run's screenshots, video, and full model stream.

## Pass criteria

The video is the first item on the captured Videos tab. Title and displayed date match. The chapter
count matches the captured description/player (or "no chapters" is correct). The transcript line and
timestamp match the captured transcript panel and are the closest to 1:00 among the lines visible in the
capture. An answer produced without the transcript panel visibly opened in the trace fails.

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually
navigated to and evidence it captured THIS run. A correct-sounding answer with no supporting
navigation or capture in the trace fails, and where the live page disagrees with the answer, the
captured page wins.

Item (5) must match the transcript panel's language/caption label as captured (for example "English
(auto-generated)" versus a listed language without that marker); it is only readable with the panel open.
