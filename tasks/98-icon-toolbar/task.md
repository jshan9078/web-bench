# 98-icon-toolbar

- **kind**: icon-only UI interpretation (programmatic)
- **site**: localhost widget (widgetapp/icontoolbar.py, port 8818)
- **what it tests**: acting through unlabeled icon buttons (no text, no aria-label, random class names) by recognising the glyphs in a screenshot or hovering for the JS tooltip; the accessibility snapshot only shows five anonymous buttons per row
- **discrimination hypothesis**: the archive box and the delete bin are neighbouring glyphs, class names carry no meaning and change per run, and a near-duplicate title ('Q3 vendor invoices', 'Vendor contracts 2025') sits nearby. Clicking blind, or trusting position, deletes a document.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the target document is archived and nothing was deleted.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8818/ . It is a shared-documents list; each row has icon-only action buttons. 
Archive the document titled "Q3 vendor contracts". Do not delete, duplicate, or otherwise act on 
any other document, and do not delete this one (delete is immediate). Do NOT read the page source 
or call the site's HTTP endpoints directly. End with a one-line confirmation.
```
