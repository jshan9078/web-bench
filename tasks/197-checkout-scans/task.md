# 197-checkout-scans

- **kind**: state-flash counting over video (programmatic)
- **site**: localhost widget (widgetapp/checkoutscans.py, port 8873)
- **what it tests**: counting accepted (green) scan flashes among 22-30 scans, each flash lasting one second
- **discrimination hypothesis**: flashes are short and colour is the only cue; sampled frames miss or misattribute flashes; exact count.
- **verification**: see [`verifier.md`](verifier.md)
- **verdict**: Objective: the last submitted count equals the number of accepted scans.

## Prompt (`TASK:` text sent to the agent)

See [`prompt.txt`](prompt.txt) (the runtime source). Verbatim:

```
Open http://127.0.0.1:8873/ . It is a 2-minute self-checkout camera clip in a player (canvas video 
with play/pause, seek, 1 s and 10 s steps and playback speed; read frames from screenshots). Each 
time an item is scanned the screen flashes GREEN (accepted) or RED (not recognised). Count exactly 
how many scans were ACCEPTED during the clip, enter the number in the form under the player and 
submit. Do NOT read the page source or call the site's HTTP endpoints directly. End with the count.
```
