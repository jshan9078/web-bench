# 287-sequence-recall

- **kind**: observing a timed sequence and reproducing it (programmatic)
- **site**: localhost widget (widgetapp/simon.py, port 8935)
- **what it tests**: capturing a six-step lit sequence at 2-second cadence and clicking it back in order
- **discrimination hypothesis**: requires sampling the board fast enough and retaining the order; replays are allowed; exact order.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the sequence was entered correctly.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8935/ . It is a sequence-recall game: press Play, watch six tiles light up 
one after another (each stays lit 1.5 seconds; take screenshots quickly or watch with repeated 
snapshots), then click the tiles in the same order. A wrong tile clears your input; you may press 
Play again to re-watch. Complete the sequence (the page says Sequence complete). Do NOT read the 
page source or call the site's HTTP endpoints directly. End with a one-line confirmation.
```
