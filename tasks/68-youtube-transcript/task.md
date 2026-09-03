# 68-youtube-transcript

- **kind**: action + read (LLM-judge)
- **site**: youtube.com
- **what it tests**: channel navigation, telling regular uploads from Shorts and live streams, discovering the transcript panel through the description, scrolling inside a panel to a timestamp
- **discrimination hypothesis**: the transcript panel is behind two clicks and scrolls independently of the page; agents that never open it, or that report a chapter list without checking, fail. Live uploads are pretraining-proof.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: the video is the channel's latest regular upload, and the title, date, chapter count, and the transcript line nearest 1:00 match the captured panel.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
On YouTube, open https://www.youtube.com/@NASA/videos and open the channel's MOST RECENT regular upload
(from the Videos tab; not a Short and not a live stream). Expand the description and open "Show
transcript". Report: (1) the video title, (2) the upload date as displayed, (3) the number of chapters
listed for the video (if the description or player shows chapters; otherwise say "no chapters"), and
(4) the transcript line whose timestamp is closest to 1:00, with its timestamp, and (5) whether the
transcript panel labels the captions as auto-generated (read the language selector at the bottom of the
panel). Scroll inside the
transcript panel as needed. If YouTube shows a consent or sign-in interstitial, dismiss it without
signing in. End with those five items.
```
