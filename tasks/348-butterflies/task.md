# 348-butterflies

- **kind**: attribute-conditioned event counting over video (programmatic)
- **site**: localhost widget (widgetapp/butterflies.py, port 8981)
- **what it tests**: counting landings of one colour among fluttering decoys
- **discrimination hypothesis**: landings last 2 s; colour must be read on a moving target; ~7 targets.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted value equals the true value.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8981/ . It is a clip in a player (canvas video with play/pause, seek, 1 s and 
10 s steps and playback speed; read frames from screenshots). It shows a flower bed for 2 minutes; 
butterflies of several colours flutter across, and some land on the large flower for a moment. 
Count exactly how many BLUE butterflies landed on the large flower, enter the number in the form 
under the player and submit. Do NOT read the page source or call the site's HTTP endpoints 
directly. End with the count.
```
