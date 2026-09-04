# 305-plate-read

- **kind**: reading brief small text in video (programmatic)
- **site**: localhost widget (widgetapp/plateread.py, port 8945)
- **what it tests**: seeking to the ~1.3 s window when the red car is visible and reading a 7-character plate at 11 px
- **discrimination hypothesis**: the window is short and the text small; five decoy cars.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted plate equals the red car's.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8945/ . It is a 45-second roadside clip in a player (canvas video with 
play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots). Several 
cars pass, each visible for about a second. Read the licence plate (7 characters, format AAA-0000) 
of the RED car, enter it in the form under the player and submit. Do NOT read the page source or 
call the site's HTTP endpoints directly. End with the plate.
```
