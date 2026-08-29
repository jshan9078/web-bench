# 46-gmaps-save-place, verifier

**Method:** LLM-as-judge (Claude).

Judging is **fully offline** from a captured evidence bundle, so a verdict can be re-derived
without re-running the model. For each run the judge is given:

- the task prompt (see `prompt.txt`)
- the agent's final answer and result text
- the **end-state** page URL and a text excerpt of the final page
- the full browser command trace (every `navigate`/`click`/`screenshot`/... this run)
- the run's screenshots, video, and full model stream

**Vision evidence:** this task's proof is visual. The judge MUST open the run's
screenshots (and the video if needed) rather than judging from text alone.

## Pass criteria

The Want to go screenshot (which the judge must open) shows the CN Tower saved there, the trace
shows the save action happened this run, and the reported rating and review count (a live,
drifting figure) match the place card captured this run. Account state plus live counts are both
unfakeable from pretraining, and this flow has no CLI or API equivalent for end users.

**Repeatability:** the verification screenshot is taken BEFORE the cleanup and is the pass
evidence; the trace must then show the created state undone (unsave it from Want to go)
so a rerun starts fresh. Removing residue from an earlier run at the start does not count as
this run's work, and a run that skips the cleanup fails.

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually
navigated to and evidence it captured THIS run. A correct-sounding answer with no supporting
navigation or capture in the trace fails, and where the live page disagrees with the answer, the
captured page wins.
