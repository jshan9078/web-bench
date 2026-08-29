# 31-wordle-daily

- **kind**: action + vision (LLM-judge)
- **site**: nytimes.com/games/wordle
- **what it tests**: playing a daily puzzle: typing guesses, reading color feedback from screenshots, adapting
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: final board screenshot matches the reported guesses and color patterns.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open today's Wordle (https://www.nytimes.com/games/wordle). Close any welcome or how-to-play
dialogs; no login is needed. Play today's puzzle: type a real five-letter word and press Enter,
then take a SCREENSHOT to read the color feedback (green = right letter right spot, yellow =
right letter wrong spot, gray = not in the word). Use the feedback to pick each next guess. Make
at least four guesses, or fewer if you solve it. Take a final screenshot of the board. End by
listing your guesses in order, each row's color pattern as shown, and the solution if you found
it.
```
