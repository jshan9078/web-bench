# 64-hn-comment-census

- **kind**: read + structure (LLM-judge)
- **site**: news.ycombinator.com
- **what it tests**: understanding comment nesting on a long thread, counting top-level comments, counting DIRECT replies (one level) rather than descendants
- **discrimination hypothesis**: the thread is long and the nesting is expressed by indentation only; agents that count total descendants, or stop at the first screen of comments, get a different answer. Live threads are pretraining-proof.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: the top-level count and the most-replied top-level comment (author, direct-reply count, excerpt) match the captured thread.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open Hacker News (https://news.ycombinator.com) and open the comments page of the story ranked #2 on the
front page. On the thread as shown (the first comments page, following any "more comments" link at the
bottom only if it is the same thread), count the TOP-LEVEL comments (direct replies to the story, not
nested under another comment). Then find the top-level comment with the MOST DIRECT replies (replies
exactly one level below it; do not count deeper descendants). Report the story title, the top-level
comment count, and for that comment: its author, its direct-reply count, and the first 60 characters of
its text. Base everything on the thread as captured this run. End with those items.
```
