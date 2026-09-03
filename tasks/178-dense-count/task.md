# 178-dense-count

- **kind**: exact counting at density (programmatic)
- **site**: localhost widget (widgetapp/densecount.py, port 8862)
- **what it tests**: counting 40-60 target-coloured boxes among 110-150 tightly packed, partly overlapping boxes, exactly
- **discrimination hypothesis**: at this density a single skipped or double-counted box fails; a human counts row by row with care; the perception limit, not a trick.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of blue boxes.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8862/ . It is a warehouse camera photo of a tightly packed pallet of boxes in 
three colours (read it from screenshots; some boxes partly overlap). Count the BLUE boxes exactly, 
enter the number in the form below the photo and submit. Do NOT read the page source or call the 
site's HTTP endpoints directly. End with the count.
```
