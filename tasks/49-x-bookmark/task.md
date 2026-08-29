# 49-x-bookmark

- **kind**: signed-in action (LLM-judge)
- **site**: x.com
- **what it tests**: reading a live timeline and using a private bookmark action, then verifying
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: Bookmarks screenshot contains the post, and the post summary matches the captured profile.
- **requires**: signed-in browser profile

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
You are running on a browser profile where the user is already signed in. If a login page appears anyway, show the window and ask the user to sign in, then continue. On X (https://x.com), open the profile @AnthropicAI. Identify its MOST RECENT post
(ignore any pinned post, which is labeled pinned). Report the post's first sentence (or the whole
post if short) and its relative timestamp. BOOKMARK that post (a private action), then open your
Bookmarks page and take a screenshot showing it. Do not like, repost, or reply. End with the post
summary, its timestamp, and bookmark confirmation.
```
