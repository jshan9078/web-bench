# 247-rich-text-format

- **kind**: rich-text editing by keyboard selection (programmatic)
- **site**: localhost widget (widgetapp/richtext.py, port 8909)
- **what it tests**: selecting exact phrases and blocks in a contenteditable editor and applying bold, heading and list formatting through a toolbar
- **discrimination hypothesis**: bolding the exact phrase needs a precise selection; the list must be inserted between two specific paragraphs without merging them; the saved HTML is checked structurally.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: saved HTML bolds exactly 'vendor shortlist', has one H2 'Budget review', and a three-item list Flights/Hotels/Meals between the receipts and questions paragraphs with the other text intact.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8909/ . It is a document editor (a contenteditable page with a toolbar; 
select text with the keyboard, for example Shift+End or Shift+ArrowRight, or with the mouse). Make 
exactly these changes: (1) make the words "vendor shortlist" in the first paragraph bold; (2) turn 
the line "Budget review" into a Heading 2; (3) insert a bullet list with three items, Flights, 
Hotels, Meals, in that order, directly after the paragraph about travel receipts (before the 
"Questions" paragraph). Change nothing else, then click Save. Do NOT read the page source or call 
the site's HTTP endpoints directly. End with a one-line confirmation.
```
