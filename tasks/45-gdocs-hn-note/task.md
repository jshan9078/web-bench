# 45-gdocs-hn-note

- **kind**: signed-in action, cross-site (LLM-judge)
- **site**: docs.google.com + news.ycombinator.com
- **what it tests**: document creation and typing content sourced from live cross-site reading
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: the doc screenshot shows the title and a summary consistent with the story captured this run.
- **requires**: signed-in browser profile

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
You are running on a browser profile where the user is already signed in. If a login page appears anyway, show the window and ask the user to sign in, then continue. Reruns must start fresh: if a leftover webbench-notes document exists from a previous run, move it to trash first so you start clean. First open Hacker News (https://news.ycombinator.com), open the CURRENT #1 story's
link or discussion, and understand what it is about. Then open Google Docs
(https://docs.google.com), create a NEW blank document, title it: webbench-notes, and type a
three-line note: line 1 the story title, line 2 a one-sentence summary in your own words, line 3
today's date. The Docs editor can swallow punctuation typed as raw key presses; verify each line
rendered (screenshot) and keep the lines punctuation-light if characters drop. Take a screenshot of the document. Finally, AFTER taking the verification screenshot, undo your change: move the document to trash (File menu) and confirm it is gone, so a rerun starts fresh; note the cleanup in your final answer. End with the story title and the summary line
you wrote.
```
