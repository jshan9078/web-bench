# 65-arxiv-pdf-tables

- **kind**: read + PDF navigation (LLM-judge)
- **site**: arxiv.org
- **what it tests**: scanning a listing for a title keyword, opening and paging through a PDF, counting numbered tables in the main text, reading a caption
- **discrimination hypothesis**: PDF reading through the browser's viewer requires paging and zooming; counting tables across 10-30 pages while excluding appendix tables is exactly the kind of long-horizon bookkeeping where weaker tiers lose count or stop early.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: the paper is the first matching title on the captured listing, and the table count, Table 1 caption, and page count match the captured PDF.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
On arXiv, open the cs.CL new-submissions listing (https://arxiv.org/list/cs.CL/new). Scanning in listing
order, find the FIRST paper whose TITLE contains the word "benchmark" (case-insensitive; "benchmarks" and
"benchmarking" count). Open that paper's PDF. Report: (1) its arXiv identifier, (2) the total number of
pages of the PDF, (3) how many numbered tables appear in the MAIN TEXT (Table 1 through Table N, stopping
before any appendix or supplementary section), and (4) the first sentence of Table 1's caption. Page
through the PDF as needed and base the counts on what you actually see. Read the PDF INSIDE the browser's PDF viewer, paging and zooming as needed and taking screenshots of the rendered pages you rely on. If the browser cannot display the PDF natively, you may render its pages to images inside the page (for example with pdf.js drawing to a canvas) and screenshot them; that still counts as reading rendered pages. Do NOT download the PDF to disk, and do NOT extract its text with command-line tools or libraries (curl, wget, pdftotext, PyMuPDF, pdf.js getTextContent or text layers, or similar): an answer produced that way fails the task, because the task measures reading rendered pages in the browser. End with those four items.
```
