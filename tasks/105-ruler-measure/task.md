# 105-ruler-measure

- **kind**: measurement against a scale (programmatic)
- **site**: localhost widget (widgetapp/ruler.py, port 8825)
- **what it tests**: measuring an object against a ruler with mm ticks when the object does not start at zero, distinguishing it from a distractor part of similar size
- **discrimination hypothesis**: reading the right-end position as the length (ignoring the offset), or measuring part B, gives an error far beyond the 2 mm tolerance; careful tick counting is within it.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: a submitted length within 2 mm of part A.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8825/ . It is a listing photo of two replacement parts next to a ruler (read 
it from screenshots). Report the length of part A in millimetres (within 2 mm), enter it in the 
form below the photo and submit. Do NOT read the page source or call the site's HTTP endpoints 
directly. End with the length.
```
