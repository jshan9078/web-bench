# 218-vending-dispensed

- **kind**: event outcome counting over video (programmatic)
- **site**: localhost widget (widgetapp/vending.py, port 8882)
- **what it tests**: counting successful dispenses among attempts, using the item drop and the display message
- **discrimination hypothesis**: SOLD OUT attempts look like purchases except for the display and the missing drop; exact count.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of dispensed items.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8882/ . It is a 2-minute break-room camera clip in a player (canvas video 
with play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots) showing 
a vending machine. Each purchase attempt either dispenses an item (it drops down into the tray 
while the display shows VENDING) or fails (the display shows SOLD OUT and nothing drops). Count 
exactly how many items were actually dispensed, enter the number in the form under the player and 
submit. Do NOT read the page source or call the site's HTTP endpoints directly. End with the count.
```
