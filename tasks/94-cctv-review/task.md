# 94-cctv-review

- **kind**: video review + frame reading (programmatic)
- **site**: localhost widget (widgetapp/cctv.py, port 8814)
- **what it tests**: reviewing a recording efficiently (motion markers on the timeline, seek, 1 s steps) to find a short event and read the burned-in clock from that frame
- **discrimination hypothesis**: the red truck (same colour) and the blue car (same shape) are decoys; reading the clock while the car is only partly in frame, or computing the time from the seek position instead of reading the random-start clock, gives a wrong time. Scanning blindly at 10 s steps costs many screenshots inside the budget.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: a submitted HH:MM:SS falls inside the fully-visible window of the red car, +-1 s.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8814/ . It is playback of a 4-minute security-camera recording rendered on a 
canvas (read frames from screenshots), with a timeline that marks motion events, a seek bar, step 
buttons and a speed control. A red CAR passes at some point (a red truck and a blue car also pass). 
Find a frame in which the red car is fully in view and report the camera clock burned into that 
frame as HH:MM:SS. Enter it in the form under the player and submit. Do NOT read the page source or 
call the site's HTTP endpoints directly. End with the time.
```
