# 64-hn-comment-census, verifier

**Method:** LLM-as-judge (Claude).

Judging is **fully offline** from a captured evidence bundle, so a verdict can be re-derived
without re-running the model. For each run the judge is given the task prompt, the agent's final
answer and result text, the end-state page URL and text excerpt, the full browser command trace,
and the run's screenshots, video, and full model stream.

## Pass criteria

The story is the #2 front-page item at capture time. The top-level count and the identified comment's
author and direct-reply count match the captured thread structure (verify nesting from the trace's
snapshot/text: HN indents replies; direct replies are exactly one level deeper). An answer that counts all descendants, reports a comment that is not top-level, or gives a top-level count that differs from the captured thread, fails (no tolerance: the count is a DOM fact at capture time). If the thread has ties for most direct replies, every tied author must be named; naming only one of several tied comments fails.

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually
navigated to and evidence it captured THIS run. A correct-sounding answer with no supporting
navigation or capture in the trace fails, and where the live page disagrees with the answer, the
captured page wins.
