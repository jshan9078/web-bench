# 40-arxiv-pdf-figure

- **kind**: read + vision (LLM-judge)
- **site**: arxiv.org
- **what it tests**: opening a fresh PDF in the browser and reading it visually via screenshots
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: the reported details match the screenshot of the PDF's first page from this run.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open today's arXiv new submissions for cs.LG (https://arxiv.org/list/cs.LG/new) and open the PDF of
the FIRST paper in the listing, in the browser. The PDF renders as a canvas: take a SCREENSHOT of
page 1. From the screenshot, report the paper title, the number of authors listed, and whether
page 1 contains a figure; if it does, describe the figure in one sentence. End with title, author
count, and the figure note.
```
