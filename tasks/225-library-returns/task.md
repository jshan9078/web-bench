# 225-library-returns

- **kind**: outcome and object attribution over video (programmatic)
- **site**: localhost widget (widgetapp/libraryreturns.py, port 8888)
- **what it tests**: counting only patrons who carried a book and returned it via the slot, among desk returns and empty-handed visitors
- **discrimination hypothesis**: three patron types share the frame and the book is a small cue; exact count.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of slot returns.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8888/ . It is a 2-minute library entrance camera clip in a player (canvas 
video with play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots). 
Patrons enter from the bottom; some carry a red book and return it either through the RETURN SLOT 
on the left wall or by handing it in at the DESK on the right; others carry nothing and walk 
through. Count exactly how many books were returned through the RETURN SLOT, enter the number in 
the form under the player and submit. Do NOT read the page source or call the site's HTTP endpoints 
directly. End with the count.
```
