# 47-reddit-save

- **kind**: signed-in action (LLM-judge)
- **site**: reddit.com
- **what it tests**: feed sorting, a private save action, and verification in the saved list
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: the saved list captured this run contains the reported post.
- **requires**: signed-in browser profile

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
You are running on a browser profile where the user is already signed in. If a login page appears anyway, show the window and ask the user to sign in, then continue. On Reddit (https://www.reddit.com), open r/programming and sort by Top, past week.
Ignore any pinned Community highlights post and any inline ad; the #1 post is the top ORGANIC result. Report that post's title, points, and comment count. SAVE that post (the save action is private
to the account). Then open your saved items and take a screenshot showing the post there. Do not
vote on or comment on anything. End with the post details and save confirmation.
```
