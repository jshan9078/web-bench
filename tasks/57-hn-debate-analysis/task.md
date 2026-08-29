# 57-hn-debate-analysis

- **kind**: read (LLM-judge)
- **site**: news.ycombinator.com
- **what it tests**: reading a live discussion thread and synthesizing opposing arguments
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: both arguments and usernames are present in the captured thread.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
On Hacker News (https://news.ycombinator.com), open the comments thread of the CURRENT #1 story.
Read the top of the thread (open more comments if needed). Report: the story title and points, the
main SUPPORTING argument made by a commenter (with that commenter's username), and the main
COUNTERARGUMENT or criticism (with that commenter's username), each summarized in one sentence in
your own words. End with the story, the two arguments, and the two usernames.
```
