# 49-x-bookmark, verifier

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

The reported post is the newest non-pinned post on the captured profile, and the Bookmarks
screenshot (which the judge must open) plus trace show it bookmarked this run. The bookmark icon
can flash without persisting, so an icon-state screenshot alone is NOT sufficient evidence: the
Bookmarks page (or the Added to your Bookmarks toast) is required. A just-posted
timeline is strictly post-training data.

**Repeatability:** the verification screenshot is taken BEFORE the cleanup and is the pass
evidence; the trace must then show the created state undone (remove the bookmark)
so a rerun starts fresh. Removing residue from an earlier run at the start does not count as
this run's work, and a run that skips the cleanup fails.

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually
navigated to and evidence it captured THIS run. A correct-sounding answer with no supporting
navigation or capture in the trace fails, and where the live page disagrees with the answer, the
captured page wins.
