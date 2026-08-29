# 43-gmail-self-draft

- **kind**: signed-in action, cross-site (LLM-judge)
- **site**: mail.google.com + news.ycombinator.com
- **what it tests**: composing and saving (not sending) a draft whose content requires live cross-site research
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: Drafts screenshot shows the unsent draft with today's date and the current HN #1 title.
- **requires**: signed-in browser profile

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
You are running on a browser profile where the user is already signed in. If a login page appears anyway, show the window and ask the user to sign in, then continue. First open Hacker News (https://news.ycombinator.com) and note the CURRENT #1 story
title. Then open Gmail (https://mail.google.com), compose a new message addressed to the account's
own address, subject: webbench draft check. In the body write today's date and the HN #1 title you
found. SAVE IT AS A DRAFT and do NOT send it (close the compose window to autosave). Open the
Drafts folder and take a screenshot showing the draft. End with the subject, the HN title used,
and confirmation it is in Drafts, unsent.
```
