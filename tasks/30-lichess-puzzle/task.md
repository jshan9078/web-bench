# 30-lichess-puzzle

- **kind**: action + vision + pixel (LLM-judge)
- **site**: lichess.org
- **what it tests**: reading a live chess position from a screenshot and moving via two pixel clicks
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: the final screenshot or page state shows the puzzle solved (success indicator).

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open the Lichess puzzle trainer (https://lichess.org/training). No login is needed. The board must
be read visually: take a SCREENSHOT, work out the position and whose move it is (shown beside the
board), and play your chosen move by pixel-clicking the piece's square and then the destination
square. If Lichess marks the move wrong, take a fresh screenshot and try again (use Retry if
offered). Continue until the puzzle is fully solved or you have made 8 move attempts. Take a final
screenshot. End by reporting the moves you played and whether the success indicator appeared.
```
