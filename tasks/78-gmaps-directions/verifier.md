# 78-gmaps-directions, verifier

**Method:** LLM-as-judge (Claude).

Judging is **fully offline** from a captured evidence bundle, so a verdict can be re-derived
without re-running the model. For each run the judge is given the task prompt, the agent's final
answer and result text, the end-state page URL and text excerpt, the full browser command trace,
and the run's screenshots, video, and full model stream.

## Pass criteria

The trace must show directions between the two named places with the WALKING mode selected (mode
control state visible in a screenshot or the page text) and the step list opened; the reported walking
time, distance, and first step match the captured panel. Then the TRANSIT mode selected; the reported
duration and first line match the captured best option. Reporting the driving route, or values not
visible in a capture, fails. Consent interstitials dismissed without signing in are fine; a persistent
wall is judged under the blocked rule.

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually
navigated to and evidence it captured THIS run. A correct-sounding answer with no supporting
navigation or capture in the trace fails, and where the live page disagrees with the answer, the
captured page wins.

**Transit option:** the option labelled "Best" in the capture; when no "Best" label is visible, the first listed
option is correct provided the answer says no label was shown.
