# 293-word-search

- **kind**: visual word search plus click (programmatic)
- **site**: localhost widget (widgetapp/wordsearch.py, port 8939)
- **what it tests**: finding a word in a letter grid in any of eight directions and clicking its first letter's cell
- **discrimination hypothesis**: backwards and diagonal placements are hard to scan; the click must land in the right cell.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the confirmed click is in the first letter's cell.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8939/ . The page shows a 12x12 letter grid as an IMAGE at the top-left (read 
it from screenshots; click with raw coordinates via click --at X,Y; screenshot pixels map 1:1). The 
text under the grid names a hidden word that appears once, horizontally, vertically or diagonally, 
forwards or backwards. Click the cell containing the word's FIRST letter (a red circle marks your 
click; re-click to move it), then click Confirm. Do NOT read the page source or call the site's 
HTTP endpoints directly. End with the cell you chose.
```
