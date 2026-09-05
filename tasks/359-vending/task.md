# 359-vending

- **kind**: event outcome classification (programmatic)
- **site**: localhost widget (widgetapp/vending.py, port 8989)
- **what it tests**: distinguishing purchases that dispensed an item from failed ones
- **discrimination hypothesis**: the drop lasts 2 s and the item is small; ~18 events.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted value equals the true value.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8989/ . It is a clip in a player (canvas video with play/pause, seek, 1 s and 
10 s steps and playback speed; read frames from screenshots). It shows a vending machine for 2 
minutes; customers walk up, insert a coin and press the button, and sometimes an item drops into 
the tray. Count exactly how many purchases dispensed an item, enter the number in the form under 
the player and submit. Do NOT read the page source or call the site's HTTP endpoints directly. End 
with the count.
```
