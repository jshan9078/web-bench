# 91-video-slide-read

- **kind**: video navigation + frame reading at a moment (programmatic)
- **site**: localhost widget (widgetapp/videoplayer.py, port 8811, level 2)
- **what it tests**: locating a moment in a video via its transcript, seeking a canvas player to it, and reading WHICH of four figures the presenter's pointer rests on in that frame (the pointer moves to another figure six seconds later; nothing on the slide is in the DOM)
- **discrimination hypothesis**: the transcript names the moment but not the figure; the frame at that moment is the only evidence. Reading the slide at any other time, or the arbitrary frame that is on screen, picks one of three other figures. Autoplay means an unpaused screenshot is of an arbitrary moment; the six-second rest is far above a harness round-trip.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: a submitted figure equals the one the pointer rests on during the target sentence (digits compared).

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8811/ . It is a recording of a presentation playing in a video player (the 
video autoplays; use the player controls, the keyboard shortcuts, or click a transcript line to 
seek). The slides are burned into the video, so read them from screenshots. On the slide with four 
dollar figures the presenter walks through them with a red pointer dot. Find the moment the 
presenter says "This is the number that goes into the board pack" and report the dollar figure the 
pointer dot is resting on at that moment. Enter it in the form under the player and submit. Do NOT 
read the page source or call the site's HTTP endpoints directly. End with the amount.
```
