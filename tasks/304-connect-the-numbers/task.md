# 304-connect-the-numbers

- **kind**: ordered precision clicks with search (programmatic)
- **site**: localhost widget (widgetapp/connectdots.py, port 8944)
- **what it tests**: locating fifteen numbered dots among decoys and clicking them in order within 14 px
- **discrimination hypothesis**: each click must be precise and correctly ordered; a mistake resets; fifteen steps.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the confirmed sequence is 1 through 15.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8944/ . The page shows an IMAGE at the top-left with thirty labelled dots: 
the numbers 1 to 15 plus fifteen letters as decoys (read it from screenshots; click with raw 
coordinates via click --at X,Y; screenshot pixels map 1:1). Click the numbered dots in order from 1 
to 15, clicking within a few pixels of each dot (a red line traces your progress; a wrong click 
resets the sequence), then click Confirm. Do NOT read the page source or call the site's HTTP 
endpoints directly. End with a one-line confirmation.
```
