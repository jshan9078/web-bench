# 39-youtube-frame-describe

- **kind**: read + vision (LLM-judge)
- **site**: youtube.com
- **what it tests**: finding a channel's newest upload and visually describing a paused frame
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Judge: video metadata matches the captured page and the description matches the screenshot frame.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
On YouTube (https://www.youtube.com), open the official NASA channel and sort its Videos tab by
recently uploaded. Open the NEWEST video. Report its exact title, upload recency (as shown, e.g.
2 hours ago), and view count. Let it play a few seconds, pause it (press k), and take a SCREENSHOT.
Describe in two sentences what is visually on screen in that frame. End with title, recency, view
count, and the frame description.
```
