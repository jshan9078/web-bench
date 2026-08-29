# 42-youtube-watch-later

- **kind**: signed-in action (LLM-judge)
- **site**: youtube.com
- **what it tests**: menu-driven playlist state change on the user's account, then verification
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: Watch Later screenshot shows the video saved this run.
- **requires**: signed-in browser profile

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
You are running on a browser profile where the user is already signed in. If a login page appears anyway, show the window and ask the user to sign in, then continue. On YouTube, search for: lofi girl radio. Take the top non-ad result and add it to
WATCH LATER using the video's save/menu controls (do not just open it). Then navigate to the Watch
Later playlist and take a screenshot showing the video in the list. Do not delete or reorder
anything else. End with the video title you saved and confirmation it appears in Watch Later.
```
