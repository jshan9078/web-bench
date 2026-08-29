# 46-github-account-audit

- **kind**: signed-in read (LLM-judge)
- **site**: github.com
- **what it tests**: reading account-specific notifications and repository recency
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: the reported notification state and repo list match the captured signed-in pages.
- **requires**: signed-in browser profile

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
You are running on a browser profile where the user is already signed in. If a login page appears anyway, show the window and ask the user to sign in, then continue. On GitHub (https://github.com), while signed in: report how many unread
notifications the bell currently shows (or that there are none), then open the notifications page
and report the titles of up to three most recent items. Next open your own repositories list
sorted by recently updated and report the top three repository names with their last-updated
times. End with the notification summary and the three repos.
```
