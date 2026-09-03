# 65-arxiv-pdf-tables, verifier

**Method:** LLM-as-judge (Claude).

Judging is **fully offline** from a captured evidence bundle, so a verdict can be re-derived
without re-running the model. For each run the judge is given the task prompt, the agent's final
answer and result text, the end-state page URL and text excerpt, the full browser command trace,
and the run's screenshots, video, and full model stream.

## Pass criteria

The paper is the first title match on the listing as captured (verify against the trace). Page count
matches the PDF viewer. The main-text table count matches what the captured PDF pages show (the judge
counts "Table N" captions before the first appendix heading in the pages the agent captured; if the
agent did not page through far enough to see the tables it counted, it fails on grounding). The Table 1
caption sentence matches. If the listing has no title match, the correct answer is to say so.

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually
navigated to and evidence it captured THIS run. A correct-sounding answer with no supporting
navigation or capture in the trace fails, and where the live page disagrees with the answer, the
captured page wins.

**Browser-only rule (bypass defense):** the numbers and captions must come from rendered PDF pages the
agent viewed in the browser this run (screenshots of those pages must be in the trace before the answer).
Any download of the PDF or text extraction outside the browser (curl, wget, pdftotext, PyMuPDF, pdf.js
text extraction, or similar) fails the run, even if the values are correct: the task measures reading
rendered pages, and programmatic extraction produces digit-perfect answers that bypass that skill.
