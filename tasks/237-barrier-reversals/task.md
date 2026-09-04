# 237-barrier-reversals

- **kind**: outcome tracking at a barrier over video (programmatic)
- **site**: localhost widget (widgetapp/barrierreverse.py, port 8900)
- **what it tests**: distinguishing vehicles admitted through a barrier from those that reversed away
- **discrimination hypothesis**: the outcome shows only in the last seconds of each approach; exact count.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of reversals.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8900/ . It is a 2-minute car park entry camera clip in a player (canvas video 
with play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots). 
Vehicles drive up to the ticket barrier; usually it rises and they drive in, but for some it stays 
down and they reverse back out. Count exactly how many vehicles reversed away without entering, 
enter the number in the form under the player and submit. Do NOT read the page source or call the 
site's HTTP endpoints directly. End with the count.
```
