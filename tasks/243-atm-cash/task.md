# 243-atm-cash

- **kind**: transaction outcome counting over video (programmatic)
- **site**: localhost widget (widgetapp/atmqueue.py, port 8906)
- **what it tests**: classifying each ATM transaction by its on-screen and slot cues
- **discrimination hypothesis**: three outcomes with brief cues; exact count.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of cash withdrawals.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8906/ . It is a 2-minute ATM lobby camera clip in a player (canvas video with 
play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots). Customers 
use the machine one at a time: some transactions dispense cash (green notes appear in the slot 
below the screen), some only show a BALANCE screen, and some are DECLINED (red screen). Count 
exactly how many transactions dispensed cash, enter the number in the form under the player and 
submit. Do NOT read the page source or call the site's HTTP endpoints directly. End with the count.
```
