# 91-video-slide-read

- **kind**: video navigation + frame reading (programmatic)
- **site**: localhost widget (widgetapp/videoplayer.py, port 8811)
- **what it tests**: locating a moment in a video via its transcript, seeking a canvas player to it, and reading the frame that is on screen there (nothing on a slide is in the DOM)
- **discrimination hypothesis**: the obvious guess (the Refund summary slide) and a draft slide carry other totals; an agent that reads whatever frame is on screen, or the slide whose title matches the keyword, submits the wrong figure. Autoplay means an unpaused screenshot is of an arbitrary moment.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: a submitted total equals the final-invoice figure (digits compared).

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8811/ . It is a recording of a presentation playing in a video player (the 
video autoplays; use the player controls, the keyboard shortcuts, or click a transcript line to 
seek). The slides are burned into the video, so read them from screenshots. Find the moment the 
presenter FIRST says the word "refund" and report the Invoice total shown on the slide that is on 
screen at that moment. Enter it in the form under the player and submit. Do NOT read the page 
source or call the site's HTTP endpoints directly. End with the amount.
```
