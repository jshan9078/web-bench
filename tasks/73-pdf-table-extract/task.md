# 73-pdf-table-extract

- **kind**: read + vision + arithmetic (LLM-judge)
- **site**: arxiv.org
- **what it tests**: locating a specific table in a long PDF, reading numeric cells at small render size (zooming), computing a column maximum and its row label
- **discrimination hypothesis**: reading a dense results table from a rendered PDF page is where small-vision models misread digits; the max-and-row question makes a single misread visible. Live listing keeps the paper unpredictable.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: the paper, table, maximum value, and its row label match the captured PDF page.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
On arXiv, open the cs.LG recent listing (https://arxiv.org/list/cs.LG/recent). Scanning in order, find the
FIRST paper whose title contains "evaluation" or "evaluating" (case-insensitive) and open its PDF. Locate
the FIRST table in the paper that contains at least three rows of numeric results. Zoom in as needed to
read it reliably. Report: the arXiv identifier, the table's number and caption (first sentence), the
header of its LAST numeric column, the maximum value in that column, and the row label (first column
entry) of the row containing that maximum. Base everything on what the rendered PDF shows. Read the PDF INSIDE the browser's PDF viewer, paging and zooming as needed and taking screenshots of the rendered pages you rely on. Do NOT download the PDF, and do NOT extract its text with command-line tools or libraries (curl, wget, pdftotext, PyMuPDF, pdf.js text layers, or similar): an answer produced that way fails the task, because the task measures reading rendered pages in the browser. Read the PDF INSIDE the browser's PDF viewer, paging and zooming as needed and taking screenshots of the rendered pages you rely on. Do NOT download the PDF, and do NOT extract its text with command-line tools or libraries (curl, wget, pdftotext, PyMuPDF, pdf.js text layers, or similar): an answer produced that way fails the task, because the task measures reading rendered pages in the browser. End with those items.
```
