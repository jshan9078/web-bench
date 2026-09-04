# 288-tiny-targets

- **kind**: precision clicks on tiny targets under clutter (programmatic)
- **site**: localhost widget (widgetapp/tinytarget.py, port 8936)
- **what it tests**: finding five 5-pixel blue dots among 40 grey dots and clicking each within 4 px
- **discrimination hypothesis**: tiny targets demand exact coordinates; one miss fails; undo allows correction.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: all five blue dots hit with at most one stray click.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8936/ . The page shows an IMAGE at the top-left with many small grey dots and 
exactly five small BLUE dots (read it from screenshots; click with raw coordinates via click --at 
X,Y; screenshot pixels map 1:1). Click each of the five blue dots precisely (within a few pixels; a 
red ring marks each click and Undo removes the last one), then click Confirm. Do NOT read the page 
source or call the site's HTTP endpoints directly. End with a one-line confirmation.
```
