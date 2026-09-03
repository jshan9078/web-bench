# 73-pdf-table-extract, verifier

**Method:** LLM-as-judge (Claude).

Judging is **fully offline** from a captured evidence bundle, so a verdict can be re-derived
without re-running the model. For each run the judge is given the task prompt, the agent's final
answer and result text, the end-state page URL and text excerpt, the full browser command trace,
and the run's screenshots, video, and full model stream.

## Pass criteria

The paper is the first listing match as captured. The table is the first with at least three numeric
rows (the judge checks the captured pages in order). The last-column header, its maximum value, and the
row label match the captured table exactly (a misread digit fails). The trace must show the PDF page with
that table captured (screenshot or viewer text).

**Grounding rule (pretraining defense):** the answer must be grounded in pages the agent actually
navigated to and evidence it captured THIS run. A correct-sounding answer with no supporting
navigation or capture in the trace fails, and where the live page disagrees with the answer, the
captured page wins.

**Browser-only rule (bypass defense):** the numbers and captions must come from rendered PDF pages the
agent viewed in the browser this run (screenshots of those pages must be in the trace before the answer).
Any download of the PDF or text extraction outside the browser (curl, wget, pdftotext, PyMuPDF, pdf.js
text extraction, or similar) fails the run, even if the values are correct: the task measures reading
rendered pages, and programmatic extraction produces digit-perfect answers that bypass that skill.
